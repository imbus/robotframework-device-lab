"""DeviceHub: REST-API und Statusseite für das simulierte Messmodul MM-100.

Start mit `just sim`, API-Doku unter http://127.0.0.1:8080/docs (auch offline).
Einstellungen über Umgebungsvariablen: SIM_TIME_SCALE (Standard 0.1), SIM_SEED (Standard 42).
"""

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi_offline import FastAPIOffline
from pydantic import BaseModel, Field

from devicehub.simulation import Fault, Simulation, SimulationError
from devicehub.ui import device_page

sim = Simulation.from_env()

app = FastAPIOffline(
    title="DeviceHub",
    version="1.0.0",
    description="Simuliertes Messmodul MM-100 (Varianten A, B und C) für die Robot-Framework-Demos.",
)


@app.exception_handler(SimulationError)
async def simulation_error(request: Request, error: SimulationError) -> JSONResponse:
    return JSONResponse(status_code=error.status_code, content={"detail": str(error)})


class PowerRequest(BaseModel):
    on: bool = Field(description="true = ein, false = aus")


class RegisterValue(BaseModel):
    value: float = Field(ge=0)


class MeasurementRequest(BaseModel):
    repetitions: int = Field(default=1, ge=1, le=20)


class FaultRequest(BaseModel):
    fault: Fault = Field(
        description="hang: bleibt in SETTLING · drift: Messwert läuft weg · disconnect: 503"
    )


def device_reachable() -> None:
    """Fehler "disconnect": Das Gerät antwortet nicht mehr."""
    if sim.has_fault("disconnect"):
        raise SimulationError("Gerät antwortet nicht (Verbindung unterbrochen)", 503)


devices = APIRouter(prefix="/devices", tags=["Geräte"], dependencies=[Depends(device_reachable)])


@devices.get("", summary="Alle Geräte")
async def list_devices() -> list[dict]:
    return [device.info() for device in sim.devices.values()]


@devices.get("/{device_id}", summary="Gerätedaten mit aktuellem Messwert")
async def get_device(device_id: str) -> dict:
    return sim.device(device_id).info()


@devices.post("/{device_id}/power", summary="Ein- oder ausschalten")
async def power(device_id: str, request: PowerRequest) -> dict:
    device = sim.device(device_id)
    device.power(request.on)
    return {"id": device_id, "state": device.state}


@devices.get("/{device_id}/state", summary="Aktueller Zustand")
async def get_state(device_id: str) -> dict:
    return {"id": device_id, "state": sim.device(device_id).state}


@devices.get("/{device_id}/registers/{address}", summary="Register lesen")
async def read_register(device_id: str, address: int) -> dict:
    return {"address": address, "value": sim.device(device_id).read_register(address)}


@devices.put(
    "/{device_id}/registers/{address}", summary="Register schreiben (nur Eingangsspannung)"
)
async def write_register(device_id: str, address: int, request: RegisterValue) -> dict:
    device = sim.device(device_id)
    device.write_register(address, request.value)
    return {"address": address, "value": request.value, "state": device.state}


@devices.post("/{device_id}/measurements", status_code=202, summary="Messung starten")
async def start_measurement(device_id: str, request: MeasurementRequest) -> dict:
    device = sim.device(device_id)
    device.start_measurement(request.repetitions)
    return {"state": device.state}


@devices.get("/{device_id}/measurements", summary="Ergebnis der letzten Messung abholen")
async def get_measurement(device_id: str) -> dict:
    return sim.device(device_id).measurement_result()


@devices.post("/{device_id}/reset", summary="Sicherer Zustand: aus, Eingangsspannung 0 V")
async def reset(device_id: str) -> dict:
    device = sim.device(device_id)
    device.reset()
    return {"id": device_id, "state": device.state}


app.include_router(devices)


@app.get("/health", tags=["Simulation"], summary="Läuft der Mock? Welche Fehler sind aktiv?")
async def health() -> dict:
    return {
        "status": "ok",
        "time_scale": sim.time_scale,
        "seed": sim.seed,
        "faults": sorted(sim.faults),
    }


@app.post("/sim/faults", tags=["Simulation"], summary="Fehler einschalten")
async def add_fault(request: FaultRequest) -> dict:
    sim.faults.add(request.fault)
    return {"faults": sorted(sim.faults)}


@app.delete("/sim/faults", tags=["Simulation"], summary="Alle Fehler löschen")
async def clear_faults() -> dict:
    sim.faults.clear()
    return {"faults": []}


@app.post("/sim/reset", tags=["Simulation"], summary="Alle Fehler löschen, alle Geräte aus")
async def reset_simulation() -> dict:
    sim.reset()
    return {"faults": [], "devices": "OFF"}


@app.get("/ui/devices/{device_id}", response_class=HTMLResponse, include_in_schema=False)
async def device_ui(device_id: str) -> str:
    return device_page(sim.device(device_id).spec)
