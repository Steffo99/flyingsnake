import click as c
import lihzahrd as li
import json
from PIL import Image, ImageDraw
from .default_colors import DEFAULT_COLORS


@c.command()
@c.argument("input_file", type=c.Path(exists=True))
@c.argument("output_file", type=c.Path(exists=False))
@c.option("-c", "--colors", "colors_file",
          help="The json file to get the tile colors from.", type=c.Path(exists=True))
@c.option("--background/--no-background", "draw_background",
          help="Draw the sky/underground/cavern wall beneath the tiles.", default=True)
@c.option("--blocks/--no-blocks", "draw_blocks",
          help="Draw the blocks present in the world.", default=True)
@c.option("--walls/--no-walls", "draw_walls",
          help="Draw the walls present in the world.", default=True)
@c.option("--liquids/--no-liquids", "draw_liquids",
          help="Draw the liquids present in the world.", default=True)
@c.option("--wires/--no-wires", "draw_wires",
          help="Draw the liquids present in the world.", default=True)
def flyingsnake(input_file: str,
                output_file: str,
                colors_file: str,
                draw_background: bool,
                draw_blocks: bool,
                draw_walls: bool,
                draw_liquids: bool,
                draw_wires: bool):
    if colors_file:
        c.echo("Reading colors...")
        with open(colors_file) as file:
            colors = json.load(file)
    else:
        c.echo("No colors file specified, using default Terraria colors.")
        colors = DEFAULT_COLORS

    to_merge = []

    c.echo("Parsing world...")
    world = li.World.create_from_file(input_file)

    if draw_background:
        c.echo("Drawing the background...")
        background = Image.new("RGBA", (world.size.x, world.size.y))
        draw = ImageDraw.Draw(background)
        draw.rectangle(((0, 0), (world.size.x, world.underground_level)), tuple(colors["Globals"]["Sky"]))
        draw.rectangle(((0, world.underground_level + 1), (world.size.x, world.cavern_level)),
                       tuple(colors["Globals"]["Earth"]))
        draw.rectangle(((0, world.cavern_level + 1), (world.size.x, world.size.y - 192)),
                       tuple(colors["Globals"]["Rock"]))
        draw.rectangle(((0, world.size.y - 191), (world.size.x, world.size.y)), tuple(colors["Globals"]["Hell"]))
        del draw
        to_merge.append(background)

    if draw_walls:
        c.echo("Drawing walls...")
        walls = Image.new("RGBA", (world.size.x, world.size.y))
        draw = ImageDraw.Draw(walls)
        for x in range(world.size.x):
            for y in range(world.size.y):
                tile = world.tiles[x, y]
                if tile.wall:
                    draw.point((x, y), tuple(colors["Walls"][str(tile.wall.type.value)]))
            if not x % 100:
                c.echo(f"{x} / {world.size.x} rows done")
        del draw
        to_merge.append(walls)

    if draw_liquids:
        c.echo("Drawing liquids...")
        liquids = Image.new("RGBA", (world.size.x, world.size.y))
        draw = ImageDraw.Draw(liquids)
        for x in range(world.size.x):
            for y in range(world.size.y):
                tile = world.tiles[x, y]
                if tile.liquid:
                    if tile.liquid.type == li.tiles.LiquidType.WATER:
                        draw.point((x, y), tuple(colors["Globals"]["Water"]))
                    elif tile.liquid.type == li.tiles.LiquidType.LAVA:
                        draw.point((x, y), tuple(colors["Globals"]["Lava"]))
                    elif tile.liquid.type == li.tiles.LiquidType.HONEY:
                        draw.point((x, y), tuple(colors["Globals"]["Honey"]))
            if not x % 100:
                c.echo(f"{x} / {world.size.x} rows done")
        del draw
        to_merge.append(liquids)

    if draw_blocks:
        c.echo("Drawing blocks...")
        blocks = Image.new("RGBA", (world.size.x, world.size.y))
        draw = ImageDraw.Draw(blocks)
        for x in range(world.size.x):
            for y in range(world.size.y):
                tile = world.tiles[x, y]
                if tile.block:
                    draw.point((x, y), tuple(colors["Blocks"][str(tile.block.type.value)]))
            if not x % 100:
                c.echo(f"{x} / {world.size.x} rows done")
        del draw
        to_merge.append(blocks)

    if draw_wires:
        c.echo("Drawing wires...")
        wires = Image.new("RGBA", (world.size.x, world.size.y))
        draw = ImageDraw.Draw(wires)
        for x in range(world.size.x):
            for y in range(world.size.y):
                tile = world.tiles[x, y]
                if tile.wiring:
                    if tile.wiring.red:
                        draw.point((x, y), tuple(colors["Globals"]["Wire"]))
                    if tile.wiring.blue:
                        draw.point((x, y), tuple(colors["Globals"]["Wire1"]))
                    if tile.wiring.green:
                        draw.point((x, y), tuple(colors["Globals"]["Wire2"]))
                    if tile.wiring.yellow:
                        draw.point((x, y), tuple(colors["Globals"]["Wire3"]))
            if not x % 100:
                c.echo(f"{x} / {world.size.x} rows done")
        del draw
        to_merge.append(wires)

    c.echo("Merging images...")
    final = Image.new("RGBA", (world.size.x, world.size.y))
    while to_merge:
        final = Image.alpha_composite(final, to_merge.pop(0))

    c.echo("Saving file...")
    final.save(output_file)

    c.echo("Done!")


if __name__ == "__main__":
    flyingsnake()
