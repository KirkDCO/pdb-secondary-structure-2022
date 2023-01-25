#!/usr/bin/env python
# coding: utf-8

from Bio.PDB import PDBList
import gzip

pdb_ids = set() 

files = ['cullpdb_pc25.0_res0.0-2.0_len40-10000_R0.25_Xray_d2022_12_17_chains8385.gz',
         'cullpdb_pc25.0_res0.0-2.5_len40-10000_R0.3_Xray_d2022_12_17_chains11040.gz',
         'cullpdb_pc30.0_res0.0-2.5_len40-10000_R0.3_Xray_d2022_12_17_chains15208.gz']

for f in files:
    with gzip.open(f, 'rt') as fin:
        for i, line in enumerate(fin):
            if i == 0:
                continue  # burn the header
    
            pdb_chain = line.split()[0]
            pdb_id = pdb_chain[:4]
    
            pdb_ids.add(pdb_id)

pdbl = PDBList()
pdbl.download_pdb_files(pdb_codes = list(pdb_ids), file_format = 'pdb', pdir = 'pdb')
