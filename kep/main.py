# -*- coding: utf-8 -*-

import os
# Converting tables from Word files to one CSV file
from kep.converter.word import make_csv
# Parsing CSV file and uploading to database
from kep.parser.csv2db import import_csv
    
  
 
if __name__ == "__main__":
    data_folder = "data/2015/ind09/"
    # Create CSV file. Must have Word installed 
    # NOTE: may add no_overwrite if CSV file already exists, overwrite_csv()
    # make_csv(data_folder)
    # Parse and upload CSV file to database
    import_csv(data_folder)
    # db_dump()
    # must restore     
    # dump_var_list_explained()   
    
    
    # make_csv(data_folder)



