# -*- coding: utf-8 -*-
import os

# Converting tables from Word files to one CSV file (if CSV file does not exist, need MS Word installation)
from kep.importer.converter.word import make_csv

# Parsing CSV file and uploading to database
from kep.importer.csv2db import import_csv

# Save data from database to CSV and Excel xls(x)
from kep.query.save import db_dump

# Draw graphs and save them as one PDF file and many .png files 
from kep.query.plots import write_plots

# Dump variable names to markdown file 
from kep.query.var_names import dump_var_list_explained

# Inspection procedure
from kep.inspection.var_check import notify_on_import_result 

def update(data_folder):
    # Create CSV file
    make_csv(data_folder)
    
    # Parse and upload CSV file to database
    import_csv(data_folder)
    
    # Run some inspection of import results - are all variables imported?
    notify_on_import_result(data_folder)    
    
    # Export times series from database to CSV files and Excel xls(x)
    db_dump()
    
    # Create and save PDF and *.png graphs
    write_plots()
    
    # Write list of variables to markdown file 
    # Note: may also want to see frequencies of data
    dump_var_list_explained()

def update_current_month():
    from kep.paths import CURRENT_MONTH_DATA_FOLDER # "data/2015/ind10/"
    update(CURRENT_MONTH_DATA_FOLDER)
    print("Finished updating based on folder:", CURRENT_MONTH_DATA_FOLDER)
    
if __name__ == "__main__":
    update_current_month()
