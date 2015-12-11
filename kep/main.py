# -*- coding: utf-8 -*-
import os

# Converting tables from Word files to one CSV file
from kep.converter.word import make_csv

# Parsing CSV file and uploading to database
from kep.parser.csv2db import import_csv

# Save data from database to CSV and Excel xls(x)
from kep.selector.save import db_dump


if __name__ == "__main__":
    data_folder = "data/2015/ind09/"
    
    # Create CSV file
    # TODO: uncomment after issue #50 is done
    # make_csv(data_folder)
    
    # Parse and upload CSV file to database
    # import_csv(data_folder)
    
    # Save data from database to CSV and Excel xls(x)
    db_dump()
    
    # must restore     
    # dump_var_list_explained()