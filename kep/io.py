# -*- coding: utf-8 -*-
"""CSV input/output."""

import csv
import os


def get_filenames(data_folder):
    csv  = os.path.join(data_folder, "tab.csv")
    spec = os.path.join(data_folder, "tab_spec.txt")
    cfg =  os.path.join(data_folder, "tab_cfg.txt")
    return csv, spec, cfg
 
#def infolder(folder, file):
#   path = os.path.join(folder, file)
#   if os.path.isfile(path):
#       return path 
#   else:
#       raise FileNotFoundError(path)

#------------------------------------------------------------------------------
#  Root io functions with encoding 
#------------------------------------------------------------------------------
ENCODING = 'utf8' #'cp1251'
       
def w_open(file):
    return open(file, 'w', encoding = ENCODING)

def r_open(file):
    return open(file, 'r', encoding = ENCODING)
    
#------------------------------------------------------------------------------
# CSV IO 
#------------------------------------------------------------------------------

# todo later: recyle  delimiter='\t', lineterminator='\n'

def dump_iter_to_csv(iterable, csv_filename):
    """Copy generator *iterable* into file *csv_filename*. """    
    with w_open(csv_filename) as csvfile:
        spamwriter = csv.writer(csvfile,  delimiter='\t', lineterminator='\n')
        for row in iterable:        
             spamwriter.writerow(row)
    return csv_filename

def yield_csv_rows(csv_filename):
    """Open csv file named *c* and return an iterable."""
    with r_open(csv_filename) as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\t', lineterminator='\n')
        for row in spamreader:
            yield row

            
#------------------------------------------------------------------------------
# Dump of test files in subfolder
#------------------------------------------------------------------------------

# WARNING: always assume we are in parent direcory of 'kep'
SUBFOLDER = "kep//test//temp"

def docstring_to_file(docstring, filename):
    if os.path.exists(SUBFOLDER):
        path = os.path.join(SUBFOLDER, filename)
    else:
        path = filename
    with w_open(path) as f:
        f.write(docstring)
    return path

#------------------------------------------------------------------------------
# YAML import 
#------------------------------------------------------------------------------

import yaml

def test_yaml():
    print(85)
    
def load_spec(filename):
    """Returns specification  dictionaries. 
    
       YAML file structure (3 sections):    
        # readers (very little lines)
        -----
        # units (a bit more lines)
        -----
        # headlines (many lines)"""
    spec = _get_safe_yaml(filename)     
    # depreciated_reader_dict = spec[0]    
    unit_dict = spec[1]
    headline_dict = spec[2]
    return headline_dict, unit_dict

def _get_yaml(filename):
    with r_open(filename) as file:
        return list(yaml.load_all(file))   

def _get_safe_yaml(filename):        
    try:
        return _get_yaml(filename)
    except FileNotFoundError:
        raise FileNotFoundError ("YAML file not found: " + filename)
    except:
        raise Exception ("Error parsing YAML file: " + filename)


