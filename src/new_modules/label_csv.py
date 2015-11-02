# -*- coding: utf-8 -*-
"""Read raw CSV file and write a file with labelled rows.

  Inputs:
    raw csv file with data
    +
    specfile - header and unit definitions
    or
    config file - segnment information: start rows, end rows, spec files by segment
"""

#try:
#    from .common import get_raw_csv_filename, get_labelled_csv_filename
#    from .common import yield_csv_rows, dump_iter_to_csv
#    from .spec import load_spec
#except SystemError:

from common import get_raw_csv_filename, get_labelled_csv_filename, get_spec_filename
from common import yield_csv_rows, dump_iter_to_csv
from load_spec import load_spec, _get_safe_yaml

UNKNOWN_LABELS = ["unknown_var", "unknown_unit"]

#------------------------------------------------------------------------------
#  Convenience wrappers to make CSV with labelled rows 
#------------------------------------------------------------------------------

def yield_labelled_rows(p):
    # obtain filenames
    raw_data_file = get_raw_csv_filename(p)
    spec_file = get_spec_filename(p)
    # get labelled rows as iterator
    return get_labelled_rows_by_single_specfile(raw_data_file, spec_file)

def dump_labelled_rows_to_csv(p):
    gen_out = yield_labelled_rows(p)
    # obtain filename    
    f = get_labelled_csv_filename(p)
    # save to file
    dump_iter_to_csv(gen_out, f)

#------------------------------------------------------------------------------
#  label_csv main function
#------------------------------------------------------------------------------

def get_labelled_rows(raw_data_file, spec_file = None, cfg_file = None):
    if spec_file is not None:
        return get_labelled_rows_by_single_specfile(raw_data_file, spec_file)
    elif cfg_file is not None:
        return get_labelled_rows_by_segment_config_file(raw_data_file, cfg_file)
    else:
        raise ValueError("Must define either *spec_file* or *cfg_file*")

#------------------------------------------------------------------------------
#    Labelize based on single spec file
#------------------------------------------------------------------------------

def get_labelled_rows_by_single_specfile(raw_data_file, yaml_spec_file):
    raw_rows_iter = yield_csv_rows(raw_data_file)
    spec_dicts = load_spec(yaml_spec_file)
    labelled_rows_iter = yield_valid_rows_with_labels(raw_rows_iter, spec_dicts)
    return list(labelled_rows_iter)

def yield_valid_rows_with_labels(incoming_rows, spec_dicts):
    """ Return non-empty data rows with assigned labels."""
    for incoming_row, labels, data_row in yield_all_rows_with_labels(incoming_rows, spec_dicts):
        if data_row is not None:
            yield labels + data_row
      
def yield_all_rows_with_labels(incoming_rows, spec_dicts):
    """ Returns (incoming_row, labels, data_row) tuple. """
    labels = UNKNOWN_LABELS[:] 
    for row in incoming_rows:
        if row[0]:
            if not is_year(row[0]):
                # not a data row, change label
                labels = adjust_labels(row[0], labels, spec_dicts)
                yield row, labels, None
            else:
                # data row, assign label and yield                
                yield row, labels, row
        else:
            yield row, None, None
            
#------------------------------------------------------------------------------
#    Labelize based on config file
#------------------------------------------------------------------------------

def get_labelled_rows_by_segment_config_file(raw_data_file, yaml_cfg_file):
    raw_rows = list(yield_csv_rows(raw_data_file))     
    default_dicts = _get_default_dicts(yaml_cfg_file)
    segment_specs = _get_segment_specs(yaml_cfg_file)
    return _label_raw_rows_by_config(raw_rows, default_dicts, segment_specs)

def _get_default_dicts(segment_info_yaml_filename):
    """First document in config yaml is spec filename. """
    yaml = _get_safe_yaml(segment_info_yaml_filename)
    filename = yaml[0]
    return load_spec(filename)

def _get_segment_specs(segment_info_yaml_filename):
    """Other documents in config yaml are start_line, end_line and spec filename"""
    yaml = _get_safe_yaml(segment_info_yaml_filename)
    return [[start_line, end_line, load_spec(specfile)]
            for start_line, end_line, specfile in yaml[1:]]

def _label_raw_rows_by_config(raw_rows, default_dicts, segment_specs):
    """Returns list of labelled rows, based on default specification and segment info."""
    labelled_rows = []
    labels = UNKNOWN_LABELS[:]    
    for row, spec_dicts in emit_row_and_spec(raw_rows, default_dicts, segment_specs):
        if not is_year(row[0]):
            # label-switching row
            labels = adjust_labels(row[0], labels, spec_dicts)
        else:
            # data row
            labelled_rows.append(labels + row)
    return labelled_rows

def emit_row_and_spec(raw_rows, default_dicts, segment_specs):
    """Yields tuples of valid row and corresponding specification dictionaries.
       Works through segment_specs to determine right spec dict for each row."""       

    in_segment = False
    current_spec = default_dicts
    current_end_line = None

    for row in raw_rows:
        if not row[0]:
            # junk row, ignore it, pass 
            continue
        # are we in the default spec?
        if not in_segment:
            # Do we have to switch to a custom spec?
            for start_line, end_line, spec in segment_specs:
                if row[0].startswith(start_line):
                    # Yes!
                    in_segment = True
                    current_spec = spec
                    current_end_line = end_line
                    break
        else:
            # We are in a custom spec. Do we have to switch to the default one?
            if row[0].startswith(current_end_line):
                in_segment = False
                current_spec = default_dicts
                current_end_line = None                
        yield row, current_spec

# -----------------------------------------------------------------------------
#    Adjust lables based on spec dictionaries
# -----------------------------------------------------------------------------

def adjust_labels(line, cur_labels, spec_dicts):
    dict_headline = spec_dicts[0]
    dict_support  = spec_dicts[1]
    return _adjust_labels(line, cur_labels, dict_headline, dict_support)

def _adjust_labels(line, cur_labels, dict_headline, dict_support):
    """Set new primary and secondary label based on *line* contents.
    *line* is first element of csv row.    

    line = 'Производство транспортных средств и оборудования  / Manufacture of  transport equipment												
    causes change in primary label
    
    line = 'отчетный месяц в % к предыдущему месяцу  / reporting month as percent of previous mon
    causes change in secondary label
    
    ASSUMPTIONS:
      - primary label appears only once in csv file
      - primary label followed by secondary label 
      - secondary label always at start of the line 
    """
    
    labels = cur_labels
    # Does anything from 'dict_headline' appear in 'line'?
    two_labels_list = get_label_in_text(line, dict_headline)
    # Does anything from 'dict_support' appear at the start of 'line'?    
    sec_label = get_label_on_start(line, dict_support) 
        
    if two_labels_list is not None:            
       # reset to new var - change both pri and sec label
       # two_labels_list, if not None, contains primary label like "PROD" and secondary lable like "yoy"                
       labels[0] = two_labels_list[0]
       labels[1] = two_labels_list[1]             
    elif sec_label is not None:
       # change sec label    
       # sec_label, if not None, contains secondary lable like "yoy"
       labels[1] = sec_label
    else: 
       # unknown var, reset labels
       labels = UNKNOWN_LABELS[:]
    return labels    
                

def is_year(s):    
    # "20141)"    
    s = s.replace(")", "")
    try:
        int(s)
        return True        
    except ValueError:
        return False

#______________________________________________________________________________
#
#  Adjust labels - extract labels from text 
#______________________________________________________________________________

# wrappers        
def get_label_on_start(text, lab_dict):    
     return get_label(text, lab_dict, sf_start)

def get_label_in_text(text, lab_dict):    
     return get_label(text, lab_dict, sf_anywhere)

# search function for labels
def get_label(text, label_dict, is_label_found_func):
    """Return new label for *text* based on *lab_dict* and *is_label_found_func*
    """    
    for pat in label_dict.keys():
        if is_label_found_func(text, pat): 
            return label_dict[pat]
    return None

# *is_label_found_func* search functions
def sf_start(text, pat):
   return text.strip().startswith(pat)

def sf_anywhere(text, pat):
   return pat in text   

# --------------------------------------------------------------
# Testing functions

def print_rows(list_):
    # print("Printing list by row in compact form:")
    for row in list_:
         print(" ".join(row[0:6]) + ' ... ' + row[-1])

def test_label_csv1():
    from hardcoded import init_raw_csv_file, init_main_yaml, PARSED_RAW_FILE_AS_LIST
    raw_data_file = init_raw_csv_file()        
    SPEC_FILE = init_main_yaml()
    
    labelled_rows_as_list = get_labelled_rows_by_single_specfile(raw_data_file, SPEC_FILE)
    assert labelled_rows_as_list == PARSED_RAW_FILE_AS_LIST

    print("\nImport by spec file ok...")
    print_rows(labelled_rows_as_list)    

def test_default_dicts():
    from hardcoded import REF_HEADER_DICT, REF_UNIT_DICT, init_config_yaml
    CFG_FILE = init_config_yaml()
    default_dicts = _get_default_dicts(CFG_FILE)
    assert REF_HEADER_DICT == default_dicts[0]
    assert REF_UNIT_DICT == default_dicts[1]

def test_segment_specs():
    from hardcoded import REF_SEGMENT_SPEC, init_config_yaml
    CFG_FILE = init_config_yaml()
    segment_specs = _get_segment_specs(CFG_FILE)
    assert segment_specs == REF_SEGMENT_SPEC

def test_label_csv2():
    from hardcoded import PARSED_RAW_FILE_AS_LIST, init_config_yaml, init_raw_csv_file
    RAW_FILE = init_raw_csv_file()        
    CFG_FILE = init_config_yaml()
    labelled_rows = get_labelled_rows(RAW_FILE, cfg_file = CFG_FILE)
    assert PARSED_RAW_FILE_AS_LIST == labelled_rows
    print("\nImport by config file ok...")
    print_rows(labelled_rows)    


if __name__ == "__main__":
    test_label_csv1()
    test_default_dicts()
    test_segment_specs()
    test_label_csv2()