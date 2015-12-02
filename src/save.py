# -*- coding: utf-8 -*-
import pandas as pd
from datetime import date, datetime
from calendar import monthrange
import shutil

try:
   from .database import read_dfs
   from .common import dump_iter_to_csv
   from .var_names import get_var_list_as_dataframe
except (ImportError, SystemError):
   from database import read_dfs 
   from common import dump_iter_to_csv
   from var_names import get_var_list_as_dataframe

XLSX_FILE     = "output//kep.xlsx"
XLS_FILE      = "output//kep.xls"
ANNUAL_CSV    = "output//data_annual.txt"	
QUARTERLY_CSV = "output//data_qtr.txt"
MONTHLY_CSV   = "output//data_monthly.txt"

#--------------------------------------------------------------------------
def get_end_of_monthdate(y, m):
    return datetime(year=y, month=m, day=monthrange(y, m)[1])

def get_end_of_quarterdate(y, q):
    return datetime(year=y, month=q*3, day=monthrange(y, q*3)[1])
    
def duplicate_labels(df):
    r = df[df.duplicated(['label','year']) == True]
    return r['label'].unique()

def check_for_dups(df): 
    dups = duplicate_labels(df)
    if len(dups) > 0:
        raise Exception("Duplicate labels: " + " ".join(dups))

def reshape_all(dfa, dfq, dfm):
    return reshape_a(dfa), reshape_q(dfq), reshape_m(dfm)
    
def reshape_a(dfa):
    if not dfa.empty:     
        return dfa.pivot(columns='label', values='val', index='year')
    else:
        return pd.DataFrame()
    
def reshape_q(dfq):
    if not dfq.empty:     
        dt = [get_end_of_quarterdate(y,q) for y, q in zip(dfq["year"], dfq["qtr"])]
        dfq["time_index"] = pd.DatetimeIndex(dt, freq = "Q")
        dfq = dfq.pivot(columns='label', values='val', index='time_index')
        dfq.insert(0, "year", dfq.index.year)
        dfq.insert(1, "qtr", dfq.index.quarter)
        return dfq
    else:
        return pd.DataFrame()

def reshape_m(dfm):
    if not dfm.empty:     
        dt = [get_end_of_monthdate(y,m) for y, m in zip(dfm["year"], dfm["month"])]
        dfm["time_index"] = pd.DatetimeIndex(dt, freq = "M")
        dfm = dfm.pivot(columns='label', values = 'val', index = 'time_index')
        dfm.insert(0, "year", dfm.index.year)
        dfm.insert(1, "month", dfm.index.month)
        return dfm
    else: 
        return pd.DataFrame()

#-----------------------------------------------------------------------------------

def get_var_list():
    dfa, dfq, dfm = read_dfs()
    dfa = reshape_a(dfa)
    return dfa.columns.values.tolist()  
    
#-----------------------------------------------------------------------------------
# Excel output

def write_to_xl(dfa, dfq, dfm):
   # Not run/not tested. For issue #28
   df_var_names = get_var_list_as_dataframe()
   for file in [XLSX_FILE, XLS_FILE]:
      _write_to_xl(dfa, dfq, dfm, df_var_names, file)

def _write_to_xl(dfa, dfq, dfm, df_var_names, file):
    with pd.ExcelWriter(file) as writer:
        dfa.to_excel(writer, sheet_name='year')
        dfq.to_excel(writer, sheet_name='quarter')
        dfm.to_excel(writer, sheet_name='month')
        df_var_names.to_excel(writer, sheet_name='variables')
    # copy file to root directory     
    shutil.copy(file, "..")

# ---------------------------------------------------------------------------------
# CSV output

def to_csv(df, filename):
   # Previous version: 
   # dump_iter_to_csv(df_csv_iter(df), filename)

   # We simplify it with following:
   df.to_csv(filename)
   # Reference call:
   # DataFrame.to_csv(path_or_buf=None, sep=', ', na_rep='', float_format=None, columns=None, header=True, index=True, index_label=None, mode='w', encoding=None, quoting=None, quotechar='"', line_terminator='\n', chunksize=None, tupleize_cols=False, date_format=None, doublequote=True, escapechar=None, decimal='.', **kwds)

def write_to_csv(dfa, dfq, dfm):
    to_csv(dfa, ANNUAL_CSV)
    to_csv(dfq, QUARTERLY_CSV)
    to_csv(dfm, MONTHLY_CSV)   

def get_reshaped_dfs():
    dfa, dfq, dfm = read_dfs()
    check_for_dups(dfa)
    dfa = reshape_a(dfa)
    dfq = reshape_q(dfq)
    dfm = reshape_m(dfm)
    return dfa, dfq, dfm

def db_dump():
    dfa, dfq, dfm = get_reshaped_dfs()
    write_to_xl(dfa, dfq, dfm)
    write_to_csv(dfa, dfq, dfm)

if __name__ == "__main__":
    dfa, dfq, dfm = read_dfs()
    check_for_dups(dfa)
    dfa, dfq, dfm = reshape_all(dfa, dfq, dfm)
    write_to_xl(dfa, dfq, dfm)

# NOTE: from var_names import get_var_list_as_dataframe may be a circular reference with var_names.py as it uses get_var_list()
