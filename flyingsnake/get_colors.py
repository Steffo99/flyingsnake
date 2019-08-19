import typing
from xml.etree import ElementTree
from PIL import ImageColor
import json


def get_block_colors_from_tedit_settings(filename: str) -> typing.Dict[int, typing.Tuple[int, int, int, int]]:
    tree = ElementTree.parse(filename)
    root = tree.findall(".//Tile")

    colors = {}

    for block in root:
        id_ = block.attrib["Id"]
        color = block.attrib["Color"]
        alpha, red, green, blue = ImageColor.getrgb(color)
        colors[id_] = red, green, blue, alpha

    return colors


def get_wall_colors_from_tedit_settings(filename: str) -> typing.Dict[int, typing.Tuple[int, int, int, int]]:
    tree = ElementTree.parse(filename)
    root = tree.findall(".//Wall")

    colors = {}

    for wall in root:
        id_ = wall.attrib["Id"]
        color = wall.attrib["Color"]
        alpha, red, green, blue = ImageColor.getrgb(color)
        colors[id_] = red, green, blue, alpha

    return colors


def get_global_colors_from_tedit_settings(filename: str) -> typing.Dict[int, typing.Tuple[int, int, int, int]]:
    tree = ElementTree.parse(filename)
    root = tree.findall(".//GlobalColor")

    colors = {}

    for wall in root:
        name = wall.attrib["Name"]
        color = wall.attrib["Color"]
        alpha, red, green, blue = ImageColor.getrgb(color)
        colors[name] = red, green, blue, alpha

    return colors


def get_colors_from_tedit_settings(filename: str) -> typing.Dict:
    return {
        "Blocks": get_block_colors_from_tedit_settings(filename),
        "Walls": get_wall_colors_from_tedit_settings(filename),
        "Globals": get_global_colors_from_tedit_settings(filename)
    }


if __name__ == "__main__":
    with open("colors.json", "w") as file:
        json.dump(get_colors_from_tedit_settings("settings.xml"), file)
