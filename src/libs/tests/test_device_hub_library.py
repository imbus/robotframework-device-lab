"""Unit-Tests für die DeviceHubLibrary: Profil laden und Toleranzprüfung (ohne laufenden Mock)."""

import json
from pathlib import Path

import pytest
from DeviceHubLibrary.checks import Check
from DeviceHubLibrary.model import Expectation, Reading
from DeviceHubLibrary.profile import ProfileError, load_profile

TESTDATA = Path(__file__).parents[3] / "data" / "devices"


def test_load_profile_reads_all_sections():
    profile = load_profile(TESTDATA / "variante_b.json")

    assert (profile.model, profile.variant) == ("MM-100", "B")
    assert profile.registers["setpoint_voltage"] == 41001
    assert profile.repetitions == 3
    assert [p.name for p in profile.measurement_points] == ["MP1", "MP2", "MP3"]
    assert profile.point("MP2").expected == Expectation(
        voltage_v=48.0, tolerance_v=0.48, max_temperature_c=70.0
    )


def test_load_profile_names_wrong_field(tmp_path):
    data = json.loads((TESTDATA / "variante_a.json").read_text(encoding="utf-8"))
    data["measurement_points"][1]["expected"]["tolerance_v"] = "0,1"
    broken = tmp_path / "kaputt.json"
    broken.write_text(json.dumps(data), encoding="utf-8")

    with pytest.raises(ProfileError) as error:
        load_profile(broken)

    assert (
        "Feld 'measurement_points[1].expected.tolerance_v' ist \"0,1\" – erwartet: Zahl ≥ 0"
        in str(error.value)
    )


@pytest.mark.parametrize(
    ("measured_v", "passed"),
    [(5.0, True), (5.05, True), (4.95, True), (5.051, False), (4.9, False)],
)
def test_tolerance_limit_is_inclusive(measured_v, passed):
    expected = Expectation(voltage_v=5.0, tolerance_v=0.05, max_temperature_c=60)

    check = Check(Reading("MP1", 1, measured_v, temperature_c=40.0), expected)

    assert check.passed is passed
