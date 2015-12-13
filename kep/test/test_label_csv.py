import os

from kep.io.common import delete_file
from kep.io.specification import load_spec, load_cfg
from kep.parser.label_csv import get_labelled_rows

from kep.test.hardcoded import pass_csv_and_data, pass_spec_and_data, pass_cfg_and_data
raw_data_file, data_as_list = pass_csv_and_data() 
spec_file, ref_header_dict, ref_unit_dict = pass_spec_and_data()
cfg_file, ref_cfg_list = pass_cfg_and_data()

def get_test_labelled_rows():
    return get_labelled_rows(raw_data_file, spec_file, cfg_file)

def test_import():
    assert os.path.exists(raw_data_file)
    assert os.path.exists(spec_file)
    assert os.path.exists(cfg_file)

# testing with spec only   ------------------------- 
def test_specs():
    header_dict, unit_dict = load_spec(spec_file)
    assert header_dict == ref_header_dict
    assert unit_dict == ref_unit_dict

def test_label_csv1():
    assert data_as_list == get_labelled_rows(raw_data_file, spec_file)

# testing with spec and cfg -----------------------     
def test_segment_specs():
    assert ref_cfg_list == load_cfg(cfg_file)

def test_label_csv2():
    assert data_as_list == get_labelled_rows(raw_data_file, spec_file, cfg_file)
    
# TODO: this should be a last call, but not a test, using test_*() function is a stub. 
#       If left plainly in code it is executed before fucntions are called and files are deleted before tests are run.
def test_cleanup():
    for f in (raw_data_file, spec_file, cfg_file):
       delete_file(f)
    assert True