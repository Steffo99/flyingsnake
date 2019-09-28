import pytest
import flyingsnake
from click.testing import CliRunner
from PIL import Image


# Main integration test
def test_full_render():
    runner = CliRunner()
    result = runner.invoke(flyingsnake.flyingsnake, ["./tests/Small_Example.wld", "./tests/Small_Example_full.png"])
    assert Image.open("./tests/Small_Example_full.png") == Image.open("./tests/Small_Example_full_prerendered.png")
