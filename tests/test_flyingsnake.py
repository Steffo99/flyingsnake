import pytest
import flyingsnake
from click.testing import CliRunner


# Main integration test
def test_full_render():
    runner = CliRunner()
    result = runner.invoke(flyingsnake.flyingsnake, ["./tests/Small_Example.wld", "./tests/Small_Example_full.png"])
    assert result.exit_code == 0
    # TODO: compare image with a valid one


def test_partial_render():
    runner = CliRunner()
    result = runner.invoke(flyingsnake.flyingsnake, ["./tests/Small_Example.wld", "./tests/Small_Example_part.png",
                                                     "-x", "500", "-y", "500", "-w", "123", "-h", "321"])
    assert result.exit_code == 0
    # TODO: compare image with a valid one


# TODO: test the various options
