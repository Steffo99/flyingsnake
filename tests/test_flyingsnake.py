import pytest
import flyingsnake
from click.testing import CliRunner
from PIL import Image
import hashlib


# Main integration test
def test_full_render():
    runner = CliRunner()
    result = runner.invoke(flyingsnake.flyingsnake, ["./tests/Small_Example.wld", "./tests/Small_Example_full.png"])
    assert result.exit_code == 0

    with open("Small_Example_full_prerendered.png") as prerendered:
        prerendered_hash = hashlib.sha1(prerendered)
    with open("Small_Example_full.png") as created:
        created_hash = hashlib.sha1(created)
    assert prerendered_hash.hexdigest() == created_hash.hexdigest()


def test_partial_render():
    runner = CliRunner()
    result = runner.invoke(flyingsnake.flyingsnake,
                           ["./tests/Small_Example.wld", "./tests/Small_Example_partial.png",
                            "-x", "100",
                            "-y", "600",
                            "-w", "321",
                            "-h", "123"])
    assert result.exit_code == 0

    with open("Small_Example_partial_prerendered.png") as prerendered:
        prerendered_hash = hashlib.sha1(prerendered)
    with open("Small_Example_partial.png") as created:
        created_hash = hashlib.sha1(created)
    assert prerendered_hash.hexdigest() == created_hash.hexdigest()
