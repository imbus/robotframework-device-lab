"""Schlanker REST-Client für DeviceHub mit verständlichen Fehlermeldungen."""

from typing import Any

import httpx


class DeviceHubError(Exception):
    """DeviceHub ist nicht erreichbar oder lehnt eine Anfrage ab."""

    ROBOT_SUPPRESS_NAME = True


class DeviceHubClient:
    """Schickt Anfragen an DeviceHub und übersetzt Fehler in verständliche Meldungen."""

    def __init__(self, base_url: str, timeout_s: float = 5.0) -> None:
        self.base_url = base_url.rstrip("/")
        self._http = httpx.Client(base_url=self.base_url, timeout=timeout_s)

    def request(self, method: str, path: str, body: dict | None = None) -> Any:
        """Schickt eine Anfrage und liefert die JSON-Antwort."""
        try:
            response = self._http.request(method, path, json=body)
        except httpx.TransportError as error:
            reason = str(error) or type(error).__name__
            raise DeviceHubError(
                f"DeviceHub unter {self.base_url} nicht erreichbar ({reason}). "
                "Läuft der Mock (just sim)?"
            ) from None
        if response.is_error:
            raise DeviceHubError(
                f"DeviceHub lehnt {method} {path} ab ({response.status_code}): {_detail(response)}"
            )
        return response.json()


def _detail(response: httpx.Response) -> str:
    """Fehlertext aus der Antwort; DeviceHub schickt ihn als {"detail": ...}."""
    try:
        return str(response.json()["detail"])
    except ValueError, KeyError, TypeError:
        return response.text[:200]
