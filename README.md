## PDB Secondard Structure Dataset 2022 Update

This repository contains a collection of protein sequences and their annotated secondary structures, all derived from the [RCSB-PDB](https://www.rcsb.org/).  The repository is a fork of the original [pdb-secondary-strucutre repository](https://github.com/zyxue/pdb-secondary-structure) by [zyxue](https://github.com/zyxue).  Thanks to zyxue for the code to gather and annotate protein sequences with their secondary structure.

The intend of this repository is to update the original dataset which was created in 2018.  Additionally, the dataset is expanded to have more sequences by relaxing some constraints on structure resolution and the degree of similarity between proteins.

Following is the orignal README text with updates noted.

----

This repo records details of how the protein secondary structure data is curated.


#### Download secondary structure data

```
DATE_STAMP=$(date  +'%Y-%m-%d')
wget https://cdn.rcsb.org/etl/kabschSander/ss.txt.gz -O ${DATE_STAMP}-ss.txt.gz
```

#### Transform to csv format
```
python transform_ss_txt_to_csv.py -i ${DATE_STAMP}-ss.txt.gz
```

#### Download PISCES data, removed peptides with high similarity

https://academic.oup.com/bioinformatics/article/19/12/1589/258419

```
wget http://dunbrack.fccc.edu/Guoli/culledpdb_hh/cullpdb_pc25_res2.0_R0.25_d180531_chains9099.gz
```

If the above URL doesn't work, update it according to http://dunbrack.fccc.edu/Guoli/culledpdb_hh/.

---
*UPDATE 2022:*

The PISCES data files have changed formats and naming slightly since the original work was done.  The notebooks in this repository have been updated with the current file names, but the code operates in the same way.

One paritcular update is that the PISCES data files do not contain any sequences shorter that 40 amino acids.  This was a likely source of problems previously with the same sequence appearing multiple times but with different secondary structure annotations.  Additoinally, these shorter sequences were likely less informative for model dvelopment.

Additional updates included relaxing the percentage identity cutoff from 25% to 30% as well as relaxing the resolution cutoff from 2.0 angstroms to 2.5 angstroms.  Neither of these relaxed constraints should overtly affect the quality of the data, but do increase the number of example sequences substantially from ~9000 sequences (ranging in length from 20 to 1632 amino acids) to ~13,400 sequences (ranging in length from 40 to 2128 amino acids).

Changes in filename interpretation are noted below.

---

Interpretation of the filename based on http://dunbrack.fccc.edu/Guoli/pisces_download.php: 

* `pc25`:  the percentage identity cutoff is 25%  (or `pc30` for 30% identity cutoff)
* `res2.0`: he resolution cutoff is 2.0 angstroms (or `res2.5` for 2.5 angstrom cutoff)
* `R0.25`: the R-factor cutoff is 0.25
* `d180531`: datestamp (updated to `d2022_07_23`, which was the latest available)
* `chains9099`: the number of sequences in the file (updated to `chains8275`, `chains10904`, or `chains15023` depending on the specific combination of identity and resolution cutoffs)
* `len40-10000`: a new filename inclusion signifying the minimum and maximum sequence lengths. 

In addition:

* `inclNOTXRAY`: include sequences from non-xray-derived structures (mostly NMR but also including electron diffraction, FTIR, fiber diffraction, etc.). 
* `inclCA`: include sequences of structures that contain only backbone CA coordinates.

---

*UPDATE 2022:*

The `inclNOTXRAY` and `inclCA` filename portions did not appear to exist any longer.  Rather, there were:

* `Xray`: X-ray crystal structures only. (This was used for the datasets here.)
* `Xray+EM`: X-ray crystal structures and cryo-electron microscopy.
* 'Xray+Nmr+EM`: X-ray crystal structures, cryo-electron micronscopy, and NMR.
* `noBrks`: Files marked with `noBrks` consisted of no chain breaks.

---

#### Original Kaggle page:

https://www.kaggle.com/alfrandom/protein-secondary-structure

#### Updated Kaggle page:
