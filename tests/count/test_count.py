import pathlib
import time
import subprocess
import pytest
import yaqc_bluesky
from yaqd_core import testing
from bluesky import RunEngine
from bluesky.plans import count
import sys


__here__ = pathlib.Path(__file__).parent


@testing.run_daemon_entry_point(
    "fake-triggered-sensor", config=__here__ / "triggered-sensor-config.toml"
)
def test_simple_count():
    RE = RunEngine()
    sensor = yaqc_bluesky.Device(39425)
    RE(count([sensor], 41))


@pytest.mark.skipif(sys.version_info>=(3,12), reason="requires distutils")
@testing.run_daemon_entry_point("fake-camera", config=__here__ / "camera-config.toml")
def test_camera_count():
    import databroker.v2
    cat = databroker.v2.temp()
    RE = RunEngine()
    RE.subscribe(cat.v1.insert)
    sensor = yaqc_bluesky.Device(39425)
    RE(count([sensor], 4))
    cat[-1].primary.read()


if __name__ == "__main__":
    test_simple_count()
