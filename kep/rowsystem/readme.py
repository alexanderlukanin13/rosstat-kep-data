"""
- TODO fiscal rows

- anything else to final testing with test_mwe and second end-to-end test?
  - TODO dfq, dfm 
  - TODO read all labels, get_all_varnames form rowsystem 

- MAYDO clean txt files in tests
- MAYDO ask about df comparison and reshaping
- LATER classes

- DONE large test
- DONE read as csv file

- LATER were to put database?
- LATER splitting of file to modules  

- LATER read and assign dicts by segments
- DONE load_csg, load_spec + change in format
  start line : 
  end line :
  special reader:
- NODO mwe test


rowsystem.py
file_input.py

задания

альтернативные источники:
- brent
- customs
- ПБ
- regional stats
- SNA rosstat


misc:
- get_nondata_rows - fo file inspection 
"""

"""Test-driven development of CSV file reader with user-defined specification for variable names.   

The reader must produce a pandas dataframe from CSV file based on user-defined specification. The reader attempts 
to label data rows in CSV file with variable names (method *label_rowsystem*), read qualified labelled rows to 
database (omitted in this example) and create resulting dataframe (method *get_annual_df_from_rowsystem*).

    Output: 
        GDP_DF - pandas dataframe with reference data
        
    Input:
        DOC - a string mimicing CSV file contents
        header_dict, unit_dict - a tuple of dictionaries used to parse table headers in CSV file 
                                 to obtain variable names for each data row.

    Methods:
        doc_to_rowsystem(doc)    
        label_rowsystem(rs, dicts)
        get_annual_df_from_rowsystem(rs)    

Algorithm assumptions: 
- data rows in CSV file start with year, e.g  '2014'
- data rows are preceeded with text rows containing headers with text description of variables and units of measurement 
- variable text description is linked to variable headname (e.g. 'GDP', 'SOC_WAGE')
- text containing unit of measurement is parsed to variable units (e.g. 'bln_rub', 'yoy', 'rog')
- in CSV file each variable is usually presented with several units of measurement: levels and 
  different kinds of rates of growth

Naming convention:
- variable headname is written in CAPITAL letters (e.g. 'GDP', 'SOC_WAGE')
- variable unit is written in lowercase letters (e.g. 'bln_rub', 'yoy', 'rog')
- time series label is a combination of variable headname and unit (e.g. 'GDP_bln_rub')

The file contains following sections:
# --- hardcoded constrants ---
# --- methods --- 
# --- testing ---

Not todo now:
- extend DICTS to have segment information
- move all code to this file or keep as package?
- may add explicit location of variables in headers
- use one parser function
"""

"""    Working on a rowsystem facilitates parsing data rows and makes parser 
       code more organised.
"""


#-----------------------------
import yaml

segment_info_yaml_string = """
start line : null
end line : null
special reader: null"""

segment_info_dict = {
#  'default specification': True,  
  'start line' : None,
  'end line' : None,
  'special reader': 'read_special'}

assert yaml.load(segment_info_yaml_string) == segment_info_dict
#-----------------------------  
