# -*- coding: utf-8 -*-
import os

# data source 
CURRENT_MONTH_DATA_FOLDER = os.path.join('data', '2015', 'ind10')

# database file
DB_FILE = os.path.join('kep', 'database', 'kep.sqlite')

# output
OUTPUT_DIR = 'output'
PDF_FILE      = os.path.join(OUTPUT_DIR, 'monthly.pdf')
MD_PATH       = os.path.join(OUTPUT_DIR, 'images.md')
PNG_FOLDER    = os.path.join(OUTPUT_DIR, 'png')

XLSX_FILE     = os.path.join(OUTPUT_DIR, 'kep.xlsx')
XLS_FILE      = os.path.join(OUTPUT_DIR, 'kep.xls')
ANNUAL_CSV    = os.path.join(OUTPUT_DIR, 'data_annual.txt')
QUARTERLY_CSV = os.path.join(OUTPUT_DIR, 'data_qtr.txt')
MONTHLY_CSV   = os.path.join(OUTPUT_DIR, 'data_monthly.txt')

VARNAMES_FILE = os.path.join(OUTPUT_DIR, 'varnames.md')

# temp folder for testing
SUBFOLDER = os.path.join('kep', 'test', 'temp')

# inspection files (not used now)
INSPECTION_FOLDER = os.path.join('kep', 'inspection')
