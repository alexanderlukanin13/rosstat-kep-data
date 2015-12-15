# -*- coding: utf-8 -*-
# 
# Scope of work:
# - read all variable names from spec/cfg files. DONE
# - read all variable names in database DONE. (all non-empty / at specific frequency) WONT FIX
# - make and count headers (non-data rows) NOT TODO.
#

from kep.file_io.common import get_filenames, get_var_abbr
from kep.file_io.specification import load_cfg, load_spec
from kep.database.db import get_unique_labels

VERBOSE_FLAG = True

# -------------------------------------------------

def count_entries(z, list_):
    count = 0
    for x in list_:
       if z == x:
           count += 1
    return count 

assert count_entries("a", ["a","a","b"]) == 2
assert count_entries("b", ["a","a","b"]) == 1

def get_duplicates(full_list):
    ix = [count_entries(x,full_list) > 1 for x in full_list]
    return [full_list[i] for i, flag in enumerate(ix) if flag]

assert get_duplicates(["a","a","b"]) == ["a","a"]

# -------------------------------------------------

def unique(lst):
    return sorted(list(set(lst)))
assert unique([0,0]) == [0]

# -------------------------------------------------

def which_only_in_left(a,b):
    return [x for x in a if x not in b] 
def which_only_in_right(a,b):
    return which_only_in_left(b,a)
def which_in_both(a,b):
    return [x for x in a if x in b and x in a]

a = [1,2,3,4]
b = [3,4,10,100]
assert which_only_in_left(a,b) == [1,2]
assert which_only_in_right(a,b) == [10,100]
assert which_in_both(a,b) == [3,4]
assert get_duplicates(a + b) == [3,4,3,4]

# -------------------------------------------------

def get_complete_dicts(data_folder):
    csv, spec, cfg = get_filenames(data_folder)
    segments = load_cfg(cfg)
    header_dict, unit_dict = load_spec(spec)
    for seg in segments:
        seg_header_dict = seg[2][0]
        seg_unit_dict   = seg[2][1]
        header_dict.update(seg_header_dict)
        unit_dict.update(seg_unit_dict)
    return header_dict, unit_dict
    
def unpack_header_dict(header_dict):
   return list(x[0] for x in header_dict.values())

def unpack_segments(segments):
   var_list = []
   for seg in segments:
       seg_var_list =  unpack_header_dict(seg[2][0])       
       var_list.extend(seg_var_list)
   return var_list 

def get_spec_and_cfg_varnames(data_folder):
    csv, spec, cfg = get_filenames(data_folder)
    segments = load_cfg(cfg)
    header_dict, unit_dict = load_spec(spec)
    hdr = unpack_header_dict(header_dict)
    seg = unpack_segments(segments)
    return hdr, seg
    
def get_spec_varnames(data_folder):
    hdr, seg = get_spec_and_cfg_varnames(data_folder)
    return hdr    

def get_cfg_varnames(data_folder):
    hdr, seg = get_spec_and_cfg_varnames(data_folder)
    return seg
    
def get_user_defined_varnames(data_folder):
    hdr, seg = get_spec_and_cfg_varnames(data_folder)
    return hdr+seg

def get_overlapping_varnames_from_spec_and_cfg(data_folder):
    hdr, seg = get_spec_and_cfg_varnames(data_folder)
    return which_in_both(s, h)

def get_tuple_of_user_defined_varnames_and_derivatives(data_folder):
    from_spec, from_cfg = get_spec_and_cfg_varnames(data_folder)
    return from_spec, from_cfg, from_spec+from_cfg, which_in_both(from_spec, from_cfg)

def msg(text, total_list, verbose = VERBOSE_FLAG):
    unique_list = unique(total_list)
    count_msg = " ({0} total, {1} unique)".format(len(total_list), len(unique_list))
    if verbose:
        print("\n" + text + count_msg + ":\n", unique_list)
    else:
        print(text + count_msg)
    
def inspect_user_varnames(data_folder):
    from_spec, from_cfg, all_user_varnames, overlap = get_tuple_of_user_defined_varnames_and_derivatives(data_folder)
    def _msg_block(verbose_flag):
        msg("1. Varnames in spec and cfg/segments", all_user_varnames, verbose_flag)
        msg("2. Varnames in spec", from_spec, verbose_flag)
        msg("3. Varnames in cfg/segments", from_cfg, verbose_flag)
        msg("4. Overlapping varnames in spec and cfg/segments", overlap, verbose_flag)
    _msg_block(True)
    print("\nSummary:")
    _msg_block(False)
    
def get_db_varnames():
    return [get_var_abbr(x) for x in get_unique_labels()]

def get_varnames_not_in_db(data_folder):
    db_vars = get_db_varnames()
    udf_vars = unique(get_user_defined_varnames(data_folder)) 
    return which_only_in_left(udf_vars,db_vars)
    
def inspect_db(data_folder):
    udf_vars = unique(get_user_defined_varnames(data_folder)) 
    # msg("User-defined variables", udf_vars)
    db_vars = get_db_varnames()
    msg("1. Variables in database", db_vars)
    not_in_db = which_only_in_left(udf_vars,db_vars)
    msg("2. Not imported to database", not_in_db)

if __name__ == "__main__":
    data_folder = "data/2015/ind10"
    from kep.importer.parser.csv2db import import_csv
    # import_csv(data_folder)
    inspect_user_varnames(data_folder)
    inspect_db(data_folder)
    
	# assert len(get_varnames_not_in_db()) == 0
    # TODO: add config file to import 'PROFIT' 
    assert get_varnames_not_in_db(data_folder) == ["PROFIT"]