#!/usr/bin/env python
# coding: utf-8

from Bio.PDB import PDBParser
from Bio.PDB.DSSP import DSSP

import gzip
from sys import argv

import warnings
warnings.filterwarnings("ignore")

# extract command line arguments
start = int(argv[1])
stop = int(argv[2])

# sst8 to sst3 converter

STATE_DD_8T3 = {
    'G': 'H',
    'H': 'H',
    'I': 'H',
    
    'B': 'E',
    'E': 'E',
    
    'T': 'C',
    'S': 'C',
    'C': 'C',
}

def convert_8to3_state(sst):
    out = sst
    for i, j in STATE_DD_8T3.items():
        out = out.replace(i, j)
    return out

# define input and output filenames and headers 
culled_filenames = ['cullpdb_pc25.0_res0.0-2.0_len40-10000_R0.25_Xray_d2022_12_17_chains8385.gz',
                    'cullpdb_pc25.0_res0.0-2.5_len40-10000_R0.3_Xray_d2022_12_17_chains11040.gz',
                    'cullpdb_pc30.0_res0.0-2.5_len40-10000_R0.3_Xray_d2022_12_17_chains15208.gz']

output_filenames = ['2022-12-17-pdb-intersect-pisces_pc25_r2.0.csv',
                    '2022-12-17-pdb-intersect-pisces_pc25_r2.5.csv',
                    '2022-12-17-pdb-intersect-pisces_pc30_r2.5.csv']

output_header = ['pdb_id', 'chain_code', 'seq', 'sst8', 'sst3', 'len_x', 'has_nonstd_aa', 'len_y',
                 'method', 'resol', 'rfac', 'freerfac']

# storage and parser for later use
completed_structs = {}
p = PDBParser()

# loop over cull files
for culled_fn, output_fn in zip(culled_filenames, output_filenames):
    output_fn = ''.join([ str(start), '_', str(stop-1), '_', output_fn])

    with gzip.open(culled_fn, 'rt') as fin, open(output_fn, 'w') as fout:
        
        burn_header = fin.readline()

        # if on the first file in the set, start at line 0
        # write out a header.  Later files won't have a header
        # and can be concatenated easily 
        if start == 0:
            fout.write(','.join(output_header) + '\n')
        
        # get lines and step over target lines
        lines = fin.readlines()

        for i in range(start, stop):
            
            if i + 1 >= len(lines):
                break

            tokens = lines[i].strip().split()
            
            pdb_id = tokens[0][:4].upper()
            chain_code = tokens[0][4].upper()

            if (pdb_id, chain_code) in completed_structs:
                out_line = completed_structs[(pdb_id, chain_code)]
                fout.write(out_line)
                continue

            line_content = {'pdb_id': tokens[0][:4].upper(),
                            'chain_code': tokens[0][4].upper(),
                            'seq': None,
                            'sst8': None, 
                            'sst3': None,
                            'len_x': None,
                            'has_nonstd_aa': 'False',
                            'len_y': None,
                            'method': tokens[2],
                            'resol': tokens[3],
                            'rfac': tokens[4],
                            'freerfac': tokens[5]}
            
            expected_length = int(tokens[1])
            
            # load the pdb and generate secondary structure data
            try:
                pdb_fn = ''.join(['pdb/pdb', line_content['pdb_id'].lower(), '.ent'])
                struct = p.get_structure(id = line_content['pdb_id'],
                                         file = pdb_fn, )
                dssp = DSSP(model = struct[0], 
                            in_file = pdb_fn)
            except:
                # some PDBs were not found when downloading
                # or have issues with DSSP
                missing_fn =  ''.join([ str(start), '_', str(stop-1), '_missing_pdbs.txt'])
                with open(missing_fn, 'a') as missing:
                    missing.write('\t'.join([line_content['pdb_id'], 'blah', pdb_fn, '\n']))
                continue
                
            # build the output line
            keys = [key[1] for key in dssp.keys() if key[0] == line_content['chain_code']]
            
            line_content['seq'] = ''.join([dssp[(line_content['chain_code'], key)][1] for key in keys])
            line_content['sst8'] = ''.join([dssp[(line_content['chain_code'], key)][2] for key in keys]).replace('-','C')
            line_content['sst3'] = convert_8to3_state(line_content['sst8'])
            
            if len(line_content['seq']) != expected_length:
                with open('flagged_lengths.txt', 'a') as flags:
                    flags.write('\t'.join([line_content['pdb_id'], str(len(line_content['seq'])), 
                                           str(expected_length), '\n']))
            
            line_content['len_x'] = len(line_content['seq'])
            line_content['len_y'] = len(line_content['sst8'])
            
            out_line = ','.join([str(v) for k,v in line_content.items()]) + '\n'
            fout.write(out_line)
            
            completed_structs[(line_content['pdb_id'], line_content['chain_code'])] = out_line
            
            if i % 100 == 0:
                print('Processed: ', i)
                



