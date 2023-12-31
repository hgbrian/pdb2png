# Create an image of a PDB file

One dependency:
```
mamba install -c conda-forge pymol-open-source
```

## Colab demo

<a target="_blank" href="https://colab.research.google.com/github/hgbrian/biocolabs/blob/master/pdb2png.ipynb">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

## Examples

```
python pdb2png.py 4O75.pdb
```
<img src="examples/4O75_default.png" width="500px" height="500px" />

```
python pdb2png.py 4O75.pdb --render_style default_bw
```
<img src="examples/4O75_default_bw.png" width="500px" height="500px" />

```
python pdb2png.py 4O75.pdb --render_style default_cartoon
```
<img src="examples/4O75_default_cartoon.png" width="500px" height="500px" />

```
python pdb2png.py 4O75.pdb --render_style dark
```
<img src="examples/4O75_dark.png" width="500px" height="500px" />

```
python pdb2png.py 4O75.pdb --hetatm_color red --ligand_id 2RC --ligand_color 1,1,0 --protein_rotate 0,-70,0 --render_style default
```
<img src="examples/4O75_default_ligand.png" width="500px" height="500px" />

```
python pdb2png.py 8G0Z.pdb
```
<img src="examples/8G0Z_default.png" width="500px" height="500px" />

```
python pdb2png.py 8G0Z.pdb --render_style muted
```
<img src="examples/8G0Z_muted.png" width="500px" height="500px" />


### Example PDB files
```
https://files.rcsb.org/download/4O75.pdb
https://files.rcsb.org/download/8G0Z.pdb
```
