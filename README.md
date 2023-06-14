# Create an image of a PDB file

## Example PDB file:
```
curl -O https://files.rcsb.org/download/4O75.pdb
```

## Example pngs
```
python pdb2png.py 4O75.pdb --hetatm_color red --ligand_id 2RC --ligand_color 1,1,0 --protein_rotate 0,-70,0 --render_style default
```
<img src="4O75.png" />