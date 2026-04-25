import pathlib
import time
import subprocess
import pytest
import yaqc_bluesky
from yaqd_core import testing

from bluesky import RunEngine
from bluesky.plans import count
from bluesky_tiled_plugins import TiledWriter
from tiled.server import SimpleTiledServer
from tiled.client import from_uri


__here__ = pathlib.Path(__file__).parent


@testing.run_daemon_entry_point(
    "fake-triggered-sensor", config=__here__ / "triggered-sensor-config.toml"
)
def test_simple_count():
    RE = RunEngine()
    sensor = yaqc_bluesky.Device(39425)
    RE(count([sensor], 41))


@testing.run_daemon_entry_point("fake-camera", config=__here__ / "camera-config.toml")
def test_camera_count():
    """test sensor integration with bluesky/tiled"""

    sensor = yaqc_bluesky.Device(39425)

    save_path = __here__
    ts = SimpleTiledServer(readable_storage=[save_path])
    tc = from_uri(ts.uri)
    tw = TiledWriter(tc, batch_size=1)

    RE = RunEngine()
    RE.subscribe(tw)
    (uid,) = RE(count([sensor], 3))
    tc[uid][f"primary/{sensor.name}_image"].read()


if __name__ == "__main__":
    test_simple_count()
    test_camera_count()
