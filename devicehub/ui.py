"""Statusseite eines Geräts: Zustand, Messwert, Ein/Aus. Alle Elemente haben ein data-testid.

Die Seite kommt ohne externe Dateien aus (offline-fähig) und fragt den Zustand alle 0,5 s ab.
"""

from string import Template

from devicehub.simulation import DeviceSpec

_PAGE = Template("""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<title>DeviceHub – $device_id</title>
<style>
  body { font-family: system-ui, sans-serif; font-size: 1.25rem;
         max-width: 30rem; margin: 3rem auto; }
  dl { display: grid; grid-template-columns: 8rem 1fr; gap: .5rem; }
  dd { margin: 0; font-weight: bold; }
  button { font-size: 1.1rem; padding: .5rem 1.5rem; }
  [data-testid="message"] { color: #c62828; }
</style>
</head>
<body>
  <h1 data-testid="device-title">$model Variante $variant</h1>
  <dl>
    <dt>Zustand</dt><dd data-testid="device-state">–</dd>
    <dt>Messwert</dt><dd><span data-testid="measured-voltage">–</span> V</dd>
  </dl>
  <button data-testid="power-on">Ein</button>
  <button data-testid="power-off">Aus</button>
  <p data-testid="message"></p>
<script>
  const deviceUrl = "/devices/$device_id";

  function element(testId) {
    return document.querySelector('[data-testid="' + testId + '"]');
  }

  async function refresh() {
    try {
      const response = await fetch(deviceUrl);
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail);
      element("device-state").textContent = data.state;
      element("measured-voltage").textContent =
        data.measured_voltage_v === null ? "–" : data.measured_voltage_v.toFixed(3);
      element("message").textContent = "";
    } catch (error) {
      element("device-state").textContent = "KEINE VERBINDUNG";
      element("message").textContent = error.message;
    }
  }

  async function power(on) {
    await fetch(deviceUrl + "/power", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ on: on }),
    });
    refresh();
  }

  element("power-on").addEventListener("click", () => power(true));
  element("power-off").addEventListener("click", () => power(false));
  refresh();
  setInterval(refresh, 500);
</script>
</body>
</html>
""")


def device_page(spec: DeviceSpec) -> str:
    return _PAGE.substitute(
        device_id=spec.device_id,
        model=spec.model,
        variant=spec.variant,
    )
