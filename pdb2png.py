"""
Visualize a pdb file as a png.

Requires pymol, which can be installed as follows:
!mamba install -c conda-forge pymol-open-source
"""

import argparse
import json
from pymol import cmd

RENDER_OPTIONS = {
    "default": {
        "bg_color": "white",
        "ray_opaque_background": "off",
        "antialias": 2,
        "orthoscopic": "on",
        "depth_cue": "0",
        "ray_trace_mode": "1",
    },
    "default_bw": {
        "bg_color": "white",
        "ray_opaque_background": "off",
        "antialias": 2,
        "orthoscopic": "on",
        "depth_cue": "0",
        "ray_trace_mode": "2",
    },
    "default_cartoon": {
        "bg_color": "white",
        "ray_opaque_background": "off",
        "antialias": 2,
        "orthoscopic": "on",
        "depth_cue": "0",
        "ray_trace_mode": "3",
    },
    "dark": {
        "bg_color": "black",
        "ray_opaque_background": "off",
        "antialias": 2,
        "orthoscopic": "on",
        "light_count": "2",
        "specular": "1",
        "depth_cue": "0",
        "ray_trace_mode": "1",
    },
    "muted": {
        "bg_color": "white",
        "valence": 0,
        "bg_rgb": "white",
        "reflect": "0",
        "spec_direct": "0",
        "light_count": "1",
        "spec_count": "0",
        "shininess": "0",
        "power": "1",
        "specular": "0",
        "ambient_occlusion_mode": "1",
        "ambient_occlusion_scale": "15",
        "ambient_occlusion_smooth": "15",
        "ray_trace_gain": "0.1",
        "ambient": "0.9",
        "direct": "0.2",
        "ray_trace_mode": "0",
    },
}

# in groups of three
DEFAULT_PROTEIN_COLORS = (0.8, 0.8, 0.6, 0.8, 0.6, 0.8, 0.6, 0.8, 0.8)
DEFAULT_HETATM_COLORS = (0.15, 0.7, 0.9, 0.9, 0.75, 0.15, 0.9, 0.15, 0.75)


def apply_render_style(render_style:str) -> None:
    """Apply render styles from a dict. 
    Everything is global, because pymol.
    
    I cannot just use hasattr to sell what is cmd.set vs an attribute, 
    because some attributes are both cmd attributes and cmd.set attributes
    e.g., valence is both an attribute of cmd and can be 
    set with cmd.set and seems to have different meanings
    """

    if render_style in RENDER_OPTIONS:
        render_style_dict = RENDER_OPTIONS[render_style]
    else:
        render_style_dict = json.loads(render_style)

    for k, v in render_style_dict.items():
        if k == "bg_color":
            cmd.bg_color(v)
        else:
            cmd.set(k, v)


def pdb2png(pdb_file:str, 
            protein_rotate:tuple[float, float, float]|None=None,
            protein_color:tuple[float, float, float]|str|None=None,
            protein_zoom:float|None=None,
            hetatm_color:tuple[float, float, float]|str|None=None,
            ligand_id:str|None=None,
            ligand_chain:str|None=None,
            ligand_zoom:float=1.0, 
            ligand_color:tuple[float, float, float]|str|None="red",
            show_water:bool=False,
            render_style:str="default",
            width:int=1600,
            height:int=1600) -> str:
    """
    Input is a pdb file.
    Output is a png file.
    """
    cmd.reinitialize()

    cmd.load(pdb_file)
    cmd.orient() # needed??

    if protein_rotate is not None:
        cmd.rotate("x", protein_rotate[0])
        cmd.rotate("y", protein_rotate[1])
        cmd.rotate("z", protein_rotate[2])

    if protein_color is not None:
        if isinstance(protein_color, tuple):
            n = 0
            for chain in cmd.get_chains():
                cmd.set_color("protein_color", protein_color[n:n+3])
                cmd.color("protein_color", f"chain {chain} and not hetatm")
                n = (n + 3) % len(protein_color)
        else:
            cmd.color(protein_color, f"not hetatm")

    # Color proteins and hetatms
    for hp_id, hp_color, hp_sel in [("protein", protein_color, "not hetatm"), 
                                    ("hetatm", hetatm_color, "hetatm")]:
        if hp_color is not None:
            if isinstance(hp_color, tuple):
                n = 0
                for chain in cmd.get_chains():
                    cmd.select(f"sel_{hp_id}_{chain}", f"chain {chain} and {hp_sel}")
                    if cmd.count_atoms(f"sel_{hp_id}_{chain}") > 0:
                        cmd.set_color(f"{hp_id}_color_{chain}", hp_color[n:n+3])
                        cmd.color(f"{hp_id}_color_{chain}", f"sel_{hp_id}_{chain}")
                        n = (n + 3) % len(hp_color)
            else:
                cmd.color(hp_color, hp_sel)

    if protein_zoom is not None:
        cmd.zoom("all", protein_zoom)

    if ligand_id is not None:
        and_chain = f" and chain {ligand_chain}" if ligand_chain else ""
        cmd.select("ligand", f"resn {ligand_id}{and_chain}")
        cmd.zoom("ligand", ligand_zoom)

        if ligand_color is not None:
            if isinstance(ligand_color, tuple):
                cmd.set_color("ligand_color", ligand_color)
                cmd.color("ligand_color", "ligand")
            else:
                cmd.color(ligand_color, "ligand")

    if not show_water:
        cmd.select("HOH", "resn HOH")
        cmd.hide("everything", "HOH")

    apply_render_style(render_style)

    cmd.ray(width, height)    
    cmd.save(pdb_file.replace(".pdb", ".png"), pdb_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Visualize a PDB file.')
    parser.add_argument('pdb_file', type=str, help='Path to the PDB file to visualize.')
    parser.add_argument('--protein_rotate', type=str, default=None, help='protein rotation in degrees, comma-delimited')
    parser.add_argument('--protein_color', type=str, default=DEFAULT_PROTEIN_COLORS, help='protein color (e.g., red or 250,50,50,50,50,200)')
    parser.add_argument('--protein_zoom', type=float, default=None, help='protein zoom (e.g., -40 (zoomed in) to 100 (zoomed out)')
    parser.add_argument('--hetatm_color', type=str, default=DEFAULT_HETATM_COLORS, help='hetatm color (e.g., red or 250,50,50')
    parser.add_argument('--ligand_id', type=str, default=None, help='ligand_id to focus on (may also require a ligand_chain if >1 ligand)')
    parser.add_argument('--ligand_chain', type=str, default=None, help='ligand chain (needed if >1 ligand)')
    parser.add_argument('--ligand_zoom', type=float, default=10, help='zoom for ligand, (e.g., 10 is zoomed out a bit)')
    parser.add_argument('--ligand_color', type=str, default=None, help='ligand color (e.g., red or 250,50,50)')
    parser.add_argument('--show_water', action='store_true', help='show water molecules')
    parser.add_argument('--render_style', type=str, default="default", help=f'render style: ({",".join(RENDER_OPTIONS.keys())}) or custom \'{"ray_trace_mode":3}\'')
    parser.add_argument('--width', type=str, default=1600, help='resolution width')
    parser.add_argument('--height', type=str, default=1600, help='resolution height')

    try:
        args = parser.parse_args()
    except BaseException as e:
        parser.print_help()
        raise SystemExit(1)

    def _color_to_tuple(color):
        if isinstance(color, tuple):
            return color
        elif isinstance(color, str) and ',' in color:
            return tuple(float(val) for val in color.split(','))
        elif isinstance(color, str):
            return color
        else:
            return None

    pdb2png(args.pdb_file,
            protein_rotate = args.protein_rotate.split(',') if args.protein_rotate else None,
            protein_color = _color_to_tuple(args.protein_color),
            protein_zoom = args.protein_zoom,
            hetatm_color = _color_to_tuple(args.hetatm_color),
            ligand_id = args.ligand_id,
            ligand_chain = args.ligand_chain,
            ligand_zoom = args.ligand_zoom,
            ligand_color = _color_to_tuple(args.ligand_color),
            show_water = args.show_water,
            render_style = args.render_style,
            width = args.width,
            height = args.height)