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
          help="Draw the sky/underground/cavern wall beneath the tiles.", default=None)
@c.option("--blocks/--no-blocks", "draw_blocks",
          help="Draw the blocks present in the world.", default=None)
@c.option("--walls/--no-walls", "draw_walls",
          help="Draw the walls present in the world.", default=None)
@c.option("--liquids/--no-liquids", "draw_liquids",
          help="Draw the liquids present in the world.", default=None)
@c.option("--wires/--no-wires", "draw_wires",
          help="Draw the liquids present in the world.", default=None)
@c.option("--paint/--no-paint", "draw_paint",
          help="Draw painted blocks with the paint color overlayed on them.", default=True)
def flyingsnake(input_file: str,
                output_file: str,
                colors_file: str,
                draw_background: bool,
                draw_blocks: bool,
                draw_walls: bool,
                draw_liquids: bool,
                draw_wires: bool,
                draw_paint: bool):
    # If at least a draw flag is set to True, default everything else to False
    if draw_background is True \
       or draw_blocks is True \
       or draw_walls is True \
       or draw_liquids is True \
       or draw_wires is True:
        draw_background = False if (draw_background is None or draw_background is False) else True
        draw_blocks = False if (draw_blocks is None or draw_blocks is False) else True
        draw_walls = False if (draw_walls is None or draw_walls is False) else True
        draw_liquids = False if (draw_liquids is None or draw_liquids is False) else True
        draw_wires = False if (draw_wires is None or draw_wires is False) else True

    # If at least a draw flag is set to False, default everything else to True
    if draw_background is False \
       or draw_blocks is False \
       or draw_walls is False \
       or draw_liquids is False \
       or draw_wires is False:
        draw_background = True if (draw_background is None or draw_background is True) else False
        draw_blocks = True if (draw_blocks is None or draw_blocks is True) else False
        draw_walls = True if (draw_walls is None or draw_walls is True) else False
        draw_liquids = True if (draw_liquids is None or draw_liquids is True) else False
        draw_wires = True if (draw_wires is None or draw_wires is True) else False

    # If no flags are set, draw everything
    if draw_background is None \
       and draw_blocks is None \
       and draw_walls is None \
       and draw_liquids is None \
       and draw_wires is None:
        draw_background = True
        draw_blocks = True
        draw_walls = True
        draw_liquids = True
        draw_wires = True

    # If all layers are disabled, raise an Error
    if draw_background is False \
       and draw_blocks is False \
       and draw_walls is False \
       and draw_liquids is False \
       and draw_wires is False:
        raise c.ClickException("All layers are disabled, nothing to render")

    c.echo(f"Draw background layer: {draw_background}")
    c.echo(f"Draw blocks layer: {draw_blocks}")
    c.echo(f"Draw walls layer: {draw_walls}")
    c.echo(f"Draw liquids layer: {draw_liquids}")
    c.echo(f"Draw wires layer: {draw_wires}")
    c.echo(f"Draw paints: {draw_paint}")
    if colors_file:
        c.echo(f"Colors: from {colors_file}")
    else:
        c.echo("Colors: TEdit defaults")
    c.echo("")

    if colors_file:
        c.echo("Reading colors...")
        with open(colors_file) as file:
            colors = json.load(file)
    else:
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
        with click.progressbar(world.tiles, length = world.size) as bar:
            for tile in bar:
                if tile.wall:
                    if draw_paint and tile.wall.paint:
                        color = tuple(colors["Paints"][str(tile.wall.paint)])
                    else:
                        color = tuple(colors["Walls"][str(tile.wall.type.value)])
                    draw.point((x, y), color)
                
        del draw
        to_merge.append(walls)

    if draw_liquids:
        c.echo("Drawing liquids...")
        liquids = Image.new("RGBA", (world.size.x, world.size.y))
        draw = ImageDraw.Draw(liquids)
        with click.progressbar(world.tiles, length = world.size) as bar:
            for tile in bar:
                if tile.liquid:
                    if tile.liquid.type == li.tiles.LiquidType.WATER:
                        draw.point((x, y), tuple(colors["Globals"]["Water"]))
                    elif tile.liquid.type == li.tiles.LiquidType.LAVA:
                        draw.point((x, y), tuple(colors["Globals"]["Lava"]))
                    elif tile.liquid.type == li.tiles.LiquidType.HONEY:
                        draw.point((x, y), tuple(colors["Globals"]["Honey"]))

        del draw
        to_merge.append(liquids)

    if draw_blocks:
        c.echo("Drawing blocks...")
        blocks = Image.new("RGBA", (world.size.x, world.size.y))
        draw = ImageDraw.Draw(blocks)
        with click.progressbar(world.tiles, length = world.size) as bar:
            for tile in bar:
                if tile.block:
                    if draw_paint and tile.block.paint:
                        color = tuple(colors["Paints"][str(tile.block.paint)])
                    else:
                        color = tuple(colors["Blocks"][str(tile.block.type.value)])
                    draw.point((x, y), color)
                    

        del draw
        to_merge.append(blocks)

    if draw_wires:
        c.echo("Drawing wires...")
        wires = Image.new("RGBA", (world.size.x, world.size.y))
        draw = ImageDraw.Draw(wires)
        with c.progressbar(world.tiles, length = world.size) as bar:
            for tile in bar:
                if tile.wiring:
                    if tile.wiring.red:
                        draw.point((x, y), tuple(colors["Globals"]["Wire"]))
                    if tile.wiring.blue:
                        draw.point((x, y), tuple(colors["Globals"]["Wire1"]))
                    if tile.wiring.green:
                        draw.point((x, y), tuple(colors["Globals"]["Wire2"]))
                    if tile.wiring.yellow:
                        draw.point((x, y), tuple(colors["Globals"]["Wire3"]))

        del draw
        to_merge.append(wires)

    c.echo("Merging layers...")
    final = Image.new("RGBA", (world.size.x, world.size.y))
    while to_merge:
        final = Image.alpha_composite(final, to_merge.pop(0))

    c.echo("Saving image...")
    final.save(output_file)

    c.echo("Done!")


if __name__ == "__main__":
    flyingsnake()
