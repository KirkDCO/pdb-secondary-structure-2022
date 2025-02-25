## PDB Secondary Structure Dataset - 2022 Update

This repository contains a collection of protein sequences and their annotated secondary structures, all derived from the [RCSB-PDB](https://www.rcsb.org/).  The repository is a fork of the original [pdb-secondary-strucutre repository](https://github.com/zyxue/pdb-secondary-structure) by [zyxue](https://github.com/zyxue).  Thanks to zyxue for the code to gather and annotate protein sequences with their secondary structure.

The intention of this repository is to update the original dataset which was created in 2018.  Additionally, the dataset is expanded to have more sequences by relaxing some constraints on structure resolution and the degree of similarity between proteins.

Following is the orignal README text with updates noted.

----

*Update 23.02.04*

The data associated with the 6M12 structure was found to lack protein sequence, SST-3, and SST-8.  This only appears to affect the 2022-12-17-pdb-intersect-pisces_pc30_r2.5.csv file.  This is likely due to an error with DSSP's calculation of secondary structures and there is not verification in the current code to catch this error.  To reproduce the entire dataset minus this one protein would require downloading all PDB structures and rerunning the code.  Instead, the single line with the error was removed using `grep -v 6M12 2022-12-17-pdb-intersect-pisces_pc30_r2.5.csv > temp.csv`.  The `temp.csv` file was checked and copied over the original file.

*Update 23.01.22*

After finding that the ss.txt file I had downloaded in August 2022 actually dated to July 2020, and not being able to find a substitute for the ss.txt file, I wrote new code to derive the sequence and secondary structure files myself.

* download_culled_pdb.py - creates a list of PDB accession numbers that are found in the culled PDB lists and then downloads them all.  For this update, ~15,500 files were downloaded and processed.

* CreateCleanedSS.py - creates the sequence - secondary structure .csv files.  Prevoius versions started with the ss.txt, merged it with the cullpdb* files, and then converted them to the target .csv files.

* create_runner.bash - simple bash script to parallelize the structure file creation process.  Each cullpdb* file is processed, PDB files accessed from a specified directory, and partial files written.  Final files need to be concatenated.

* deprecated/ - old code is moved here.

**Original README from 22.08.06**

#### Download secondary structure data

```
DATE_STAMP=$(date  +'%Y-%m-%d')
wget https://cdn.rcsb.org/etl/kabschSander/ss.txt.gz -O ${DATE_STAMP}-ss.txt.gz
```

#### Transform to csv format
```
python transform_ss_txt_to_csv.py -i ${DATE_STAMP}-ss.txt.gz
```
---
*Update 22.08.06*

Both the original ss.txt.gz and the transformed ss.txt.gz files are in the `raw-data` folder along with the 2018 files from the original repository.

---

#### Download PISCES data, removed peptides with high similarity

https://academic.oup.com/bioinformatics/article/19/12/1589/258419

```
wget http://dunbrack.fccc.edu/Guoli/culledpdb_hh/cullpdb_pc25_res2.0_R0.25_d180531_chains9099.gz
```

If the above URL doesn't work, update it according to http://dunbrack.fccc.edu/Guoli/culledpdb_hh/.

---
*Update 22.08.06*

The PISCES data files have changed formats and naming slightly since the original work was done.  The notebooks in this repository have been updated with the current file names, but the code operates in the same way.

One particular update is that the PISCES data files do not contain any sequences shorter that 40 amino acids.  This was a likely source of problems previously with the same sequence appearing multiple times but with different secondary structure annotations.  Additoinally, these shorter sequences were likely less informative for model dvelopment.

Additional updates included relaxing the percentage identity cutoff from 25% to 30% as well as relaxing the resolution cutoff from 2.0 angstroms to 2.5 angstroms.  Neither of these relaxed constraints should overtly affect the quality of the data, but do increase the number of example sequences substantially from ~9000 sequences (ranging in length from 20 to 1632 amino acids) to ~13,400 sequences (ranging in length from 40 to 2128 amino acids).

Changes in filename interpretation are noted below.  All files are found in `raw_data/` along with the 2018 files from the original repository.

---

Interpretation of the filename based on http://dunbrack.fccc.edu/Guoli/pisces_download.php: 

* `pc25`:  the percentage identity cutoff is 25%  (or `pc30` for 30% identity cutoff)
* `res2.0`: the resolution cutoff is 2.0 angstroms
   *  The resolution cutoff now consists of a range, e.g., `res0.0-2.5` and `res0.0-3.0` were used here for 2.5 and 3.0 angstrom resolution cutoffs.
* `R0.25`: the R-factor cutoff is 0.25
* `d180531`: datestamp (updated to `d2022_07_23`, which was the latest available at the time of the update)
* `chains9099`: the number of sequences in the file (updated to `chains8275`, `chains10904`, or `chains15023` depending on the specific combination of identity and resolution cutoffs)
* `len40-10000`: a new filename inclusion at the time of the update signifying the minimum and maximum sequence lengths. 

In addition:

* `inclNOTXRAY`: include sequences from non-xray-derived structures (mostly NMR but also including electron diffraction, FTIR, fiber diffraction, etc.). 
* `inclCA`: include sequences of structures that contain only backbone CA coordinates.

---

*Update 22.08.06*

The `inclNOTXRAY` and `inclCA` filename portions did not appear to exist any longer.  Rather, there were:

* `Xray`: X-ray crystal structures only. (This was used for the datasets here.)
* `Xray+EM`: X-ray crystal structures and cryo-electron microscopy.
* `Xray+Nmr+EM`: X-ray crystal structures, cryo-electron microscopy, and NMR.
* `noBrks`: Files marked with `noBrks` consisted of no chain breaks.

After files were transformed, the notebooks were run:
* Clean-pdb-ss-csv.ipynb
* Intersect-PDB-and_PISCES.ipynb

For the update, 3 different files were generated by changing the code to refer to the appropriate `cullpdb*` file and naming the output files appropriately.  Note that some of the column names in downloaded files have changed, requiring changes in the notebook code - changes are noted with comments.

The final files were then gzipped in order to conserve space and can be found in `raw_data/`.

---

#### Original Kaggle page:

https://www.kaggle.com/alfrandom/protein-secondary-structure

#### Updated Kaggle page:

https://www.kaggle.com/datasets/kirkdco/protein-secondary-structure-2022
