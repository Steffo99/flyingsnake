import pytest
import flyingsnake
from click.testing import CliRunner
from PIL import Image


# Main integration test
def test_full_render():
    runner = CliRunner()
    result = runner.invoke(flyingsnake.flyingsnake, ["./Small_Example.wld", "./Small_Example_full.png"])
    assert Image.open("./Small_Example_full.png") == Image.open("./Small_Example_full_prerendered.png")
