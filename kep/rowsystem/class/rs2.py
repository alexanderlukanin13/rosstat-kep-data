# -*- coding: utf-8 -*-

import re
import os
from pprint import pprint
import itertools

import pandas as pd
from pandas.util.testing import assert_frame_equal

from datetime import date, datetime
from calendar import monthrange

from definitions import InputDefinition

UNKNOWN_LABELS = ["unknown_var", "unknown_unit"]
SAFE_NONE = -1


class RowSystem():
    
    def read_definition(self, *arg):
    	folder = arg[0] 
	self.in_def = InputDefinition(folder)
	self.rs = doc_to_rowsystem(in_def)    
	
    def label(self):
    	self.rs = label_rowsystem(self.rs, sekf.in_def)
    
    def __init__(*arg):
        # read definition
        self.read_definition(*arg)
        # label rows
        self.label()
        # allow call like rs.data.dfa()
        self.data = DataframeEmitter(self.dicts_as_iter())

    def dicts_as_iter(self):
        return test_iter()

    def dicts_as_list(self):
        return list(test_iter())
    
    def save(self):
        DefaultDatabase().save_stream(gen = self.dicts_as_iter())
    
       
# =============================================================================
# READING ROWSYSTEM

def is_year(s):    
    # case for "20141)"    
    s = s.replace(")", "")
    try:
       int(s)
       return True        
    except ValueError:
       return False

def is_textinfo_row(row):
    head = row['list'][0]
    if is_year(head):
       return False
    elif head == '':
       return False
    else:
       return True

def is_data_row(row):
    if is_year(row['list'][0]):
       return True
    else:
       return False

def doc_to_rowsystem(input_definition):
    """Import CSV file contents from *input_definition* and return corresponding rowsystem,
       where each line(row) from *input_definition,rows* is presented as a dictionary containing 
       raw data and supplementary information."""
       
    rowsystem = []
    for row in input_definition.rows:
       rs_item = {   'string': row,  # raw string
                       'list': row.split('\t'),  # string separated coverted to list  
                 'head_label': None, # 
                 'unit_label': None, # 
                      'label': None, # placeholder for parsing result
                       'spec': None} # placeholder parsing specification
       rowsystem.append(rs_item)
    return rowsystem

# END READING ROWSYSTEM
# =============================================================================


# =============================================================================
# LABELLING

# -----------------------------------------------------------------------------
# Label rowsystem

def label_rowsystem(rs, id):
    """Label data rows in rowsystems *rs* using markup information from id*.
       Returns *rs* with labels added in 'head_label' and 'unit_label' keys. 
    """

    rs = assign_parsing_specification_by_row(rs, id)
    
    # run label adjuster     
    cur_labels = UNKNOWN_LABELS[:]    
    for i, row in enumerate(rs):
       if is_textinfo_row(row):            
              new_labels = adjust_labels(line=row['string'], 
                                         cur_labels=cur_labels, 
                                         spec_dicts= (row['spec'].header_dict, row['spec'].unit_dict, row['spec'].reader) 
                                         )
              # set labels in current row of rowssystem
              rs[i]['head_label'] = new_labels[0]
              rs[i]['unit_label'] = new_labels[1]
              cur_labels = new_labels[:]
       else:
              # set labels in current row of rowssystem
              rs[i]['head_label'] = cur_labels[0]
              rs[i]['unit_label'] = cur_labels[1]
              
    return rs
    
    
# -----------------------------------------------------------------------------
# assign_parsing_specification_by_row    

def emit_rowheads(rs):
    for i, row in enumerate(rs):
       try:
           head = row['list'][0]
           if head:
              yield i, head              
       except:
           pass   
   
def is_matched(head, line):
    if line:
        return head.startswith(line)
    else:
        return False  
  
def assign_parsing_specification_by_row(rs, id):
    
    in_segment = False
    current_end_line = None
    current_spec = id.default_spec
    default_spec = id.default_spec
    
    for i, head in emit_rowheads(rs):
    
        # are we in the default spec?
        if not in_segment:
        
            # --------- repeated code -------------    
            # is segment info provided? 
            if id.segments:
              # do we have to switch to a custom spec?
              for segment_spec in id.segments:
                  if is_matched(head, segment_spec.start_line):
                      # Yes!
                      in_segment = True
                      current_spec = segment_spec
                      current_end_line = segment_spec.end_line
                      break
                      # --------- end repeated code -------------         
                
        else:
            # we are in custom spec. do we have to switch to the default spec? 
            if is_matched(head,current_end_line):
                in_segment = False
                current_spec = default_spec
                current_end_line = None                
            
            # --------- repeated code -------------             
            # is segment info provided? 
            if id.segments:
              # do we have to switch to a custom spec?
              for segment_spec in id.segments:
                  if is_matched(head, segment_spec.start_line):
                      # Yes!
                      in_segment = True
                      current_spec = segment_spec
                      current_end_line = segment_spec.end_line
                      break
                      # --------- end repeated code -------------         
                
        #finished adjusting specification for i-th row 
        rs[i]['spec'] = current_spec
    return rs

# -----------------------------------------------------------------------------
#  Adjust lables based on spec dictionaries

def adjust_labels(line, cur_labels, spec_dicts):
       
    # TODO: adjust varnames and description use head_label, header_dict, unit_lable, unit_dict     
    dict_headline = spec_dicts[0]
    dict_support  = spec_dicts[1]

    """Set new primary and secondary label based on *line* contents. *line* is first element of csv row.    

    line = 'Производство транспортных средств и оборудования  / Manufacture of  transport equipment                                                
    causes change in primary label
    
    line = 'отчетный месяц в % к предыдущему месяцу  / reporting month as percent of previous mon
    causes change in secondary label
    
    ASSUMPTIONS:
      - primary label appears only once in csv file (may not be true, need to use segments then)
      - primary label followed by secondary label 
      - secondary label always at start of the line 
    """
    
    labels = cur_labels
    
    # Does anything from 'dict_headline' appear in 'line'?
    pri_and_sec_labels = get_label_in_text(line, dict_headline)
    
    # Does anything from 'dict_support' appear at the start of 'line'?    
    sec_label = get_label_on_start(line, dict_support) 
        
    if pri_and_sec_labels is not None:            
       # new variable detected! - must change both pri and sec label
       # pri_and_sec_labels, if not None, contains primary label like "PROD" and secondary lable like "yoy"                
       labels[0] = pri_and_sec_labels[0]
       labels[1] = pri_and_sec_labels[1]             
    elif sec_label is not None:
       # change sec label
       # sec_label, if not None, contains secondary lable like "yoy"
       labels[1] = sec_label
    else: 
       # this unknown variable, we reset labels
       labels = UNKNOWN_LABELS[:]
       
    return labels    

# -----------------------------------------------------------------------------
#  Extract labels from text

def get_label_on_start(text, lab_dict):         
     def _search_func_at_start(text, pat):
         return text.strip().startswith(pat)
       
     return get_label(text, lab_dict, _search_func_at_start)

def get_label_in_text(text, lab_dict):    
     def _search_func_anywhere(text, pat):
          return pat in text
       
     return get_label(text, lab_dict, _search_func_anywhere)

def get_label(text, label_dict, is_label_found_func):
    """Search function for labels. Returns new label for *text*  based on *lab_dict* and *is_label_found_func*"""    
    for pat in label_dict.keys():
        if is_label_found_func(text, pat): 
            return label_dict[pat]
    return None

# END LABELLING
# =============================================================================


# =============================================================================
# QUERY ROWSYSTEM

# ------------------------------------------------------------------------------
# Read rows by annual, qtr, month section 
# split* functions return (year, annual value, quarterly values list, monthly values list) 

def split_row_by_periods(row):           
    """Year A Q Q Q Q M*12"""
    return int(row[0]), row[1], row[2:2+4], row[2+4:2+4+12]

def split_row_by_months(row):         
    """Year M*12"""
    return int(row[0]), None, None, row[1:12+1]
    
def split_row_by_months_and_annual(row):         
    """Year A M*12"""
    return int(row[0]), row[1], None, row[2:12+2]

def split_row_by_accum_qtrs(row):         
    """Year Annual AccumQ1 AccumH1 Accum9mo"""
    # Год Year	I квартал Q 1	I полугодие 1st half-year	Январь-сентябрь January-September
    # WARNING: may interfere with other qtr readers  
    return int(row[0]), row[1], row[2:2+3] + [row[1]], None    

def split_row_by_year_and_qtr(row):         
    """Year A Q Q Q Q"""
    return int(row[0]), row[1], row[2:2+4], None    

'''
	Год Year	Янв. Jan.	Янв-фев. Jan-Feb	I квартал Q1	Янв-апр. Jan-Apr	Янв-май Jan-May	I полугод. 1st half year	Янв-июль Jan-Jul	Янв-авг. Jan-Aug	Янв-cент. Jan-Sent	Янв-окт. Jan-Oct	Янв-нояб. Jan-Nov
Консолидированные бюджеты субъектов Российской Федерации, млрд.рублей / Consolidated budgets of constituent entities of the Russian Federation, bln rubles												
1999	653,8	22,7	49,2	91,5	138,7	185,0	240,0	288,5	345,5	400,6	454,0	528,0
   0	    1	   2       3 	   4	    5	    6	    7	    8	    9	   10	   11	   12
'''

def split_row_fiscal(row):         
    return int(row[0]), [row[x] for x in [3,6,9,1]], row[2:2+11] + row[1]

def special_case_testing(row):         
    return int(row[0]), row[1], None, None

#test_row = "1999	653,8	22,7	49,2	91,5	138,7	185,0	240,0	288,5	345,5	400,6	454,0	528,0"
#print(split_row_fiscal(test_row))
#TODO: ERROR - cannot read fiscal indicators because their length is same monthly, but order of columns is different.
#DONE: addressed in get_reader_func_by_row_length_and_special_dict()
    
ROW_LENGTH_TO_FUNC = { 1+1+4+12: split_row_by_periods, 
                           1+12: split_row_by_months,
                         1+1+12: split_row_by_months_and_annual,
                            1+4: split_row_by_accum_qtrs,
                          1+1+4: split_row_by_year_and_qtr,
                            1+1: special_case_testing
}

SPECIAL_FUNC_NAMES_TO_FUNC = {'fiscal': split_row_fiscal}

def get_reader_func_by_row_length(row):
    return ROW_LENGTH_TO_FUNC[len(row)]       

def special_reader_func(row):
   special_reader_func_name = row['spec'].reader # [2][2]
   return special_reader_func_name
   
def get_reader_func_by_row_length_and_special_dict(row):
    rdr = special_reader_func(row)
    if rdr is None:
       return ROW_LENGTH_TO_FUNC[len(row)]
    elif rdr in SPECIAL_FUNC_NAMES_TO_FUNC.keys():
       return SPECIAL_FUNC_NAMES_TO_FUNC[rdr]
    else:
       raise ValueError("Special reader function not recognised: " + rdr + ". Try checking spec file.")    
       
   
# ------------------------------------------------------------------------------
# Filter data on db import

# Allows to catch a value with with comment) or even double comment
_COMMENT_CATCHER = re.compile("([\d.]*)\s*(?=\d\))")

def kill_comment(text):    
    return _COMMENT_CATCHER.match(text).groups()[0]

def process_text_with_bracket(text):     
     # if there is mess like '6512.3 6762.31)' in  cell, return first value
     if " " in text:
        return filter_value(text.split(" ")[0])          
     # otherwise just through away comment   
     else:
        return kill_comment(text)          
    
def filter_value(text):  
   """Converts *text* to float number assuming it may contain 'comment)'  or other unexpected contents"""
   text = text.replace(",",".")
   if ')' in text:
       text = process_text_with_bracket(text)
   if text == "" or text == "…":       
       return None   
   else:       
       try: 
          return float(text)
       # WARNING: bad error handling, needs testing.  	  
       except ValueError:
          return "### This value encountered error on import - refer to stream.filter_value() for code ###"
       
# ---------------------------------------------------
# Get dataframes 

def is_labelled(rs):
    labs = [row['head_label'] for row in get_raw_data_rows(rs) if row['head_label'] is not None]
    return len(labs) > 0
 
# yeild all data rows from rowsystem
def get_raw_data_rows(rs):
   for row in rs:
      if is_data_row(row):
          yield row

def special_reader_func(row):
   special_reader_func_name = row['spec'][2][2]
   return special_reader_func_name
   
          
def get_labelled_rows_by_component(rs):
   for row in get_raw_data_rows(rs):
         if row['head_label'] == UNKNOWN_LABELS[0]:
             pass
         else:
             var_name = row['head_label'] + "_" + row['unit_label']
             filtered_list = [filter_value(x) for x in row['list']]
             reader = get_reader_func_by_row_length(filtered_list)            
             year, annual_value, qtr_values, monthly_values = reader(filtered_list)
             yield var_name, year, annual_value, qtr_values, monthly_values

def yield_flat_tuples(row_tuple):
       """Generate flat tuples (freq, year, qtr, month, label, val) from row components."""
       vn, y, a, qs, ms = row_tuple
           
       if a is not None:
                  yield ("a", vn, y, SAFE_NONE, SAFE_NONE, a)
   
       if qs is not None:         
           for i, val in enumerate(qs):
               if val is not None:
                  yield ("q", vn, y, i+1, SAFE_NONE, val)
   
       if ms is not None:         
           for j, val in enumerate(ms):
               if val is not None:
                  yield ("m", vn, y, SAFE_NONE, j+1, val)
 
def db_tuple_to_dict(db_tuple):
    return {'freq'    :db_tuple[0],
            'varname' :db_tuple[1],
            'year'    :db_tuple[2],
            'qtr'     :db_tuple[3],
            'month'   :db_tuple[4],
            'value'   :db_tuple[5]}

def stream_flat_data(rs):
     """Emit varname-labeled rows as flat database-ready rows."""
     for row_tuple in get_labelled_rows_by_component(rs):
         for db_row in yield_flat_tuples(row_tuple):
             yield db_row 
             
# NOTE: may use database and db_tuple_to_dict(db_row) here + stream_flat_data(rs) to database
# to_database(sqlite_filename)
# here we can write a stream of dicts


# here we can obtain a stream of dicts
# RowEmitter(sqlite_filename)


def data_stream(rs, freq, keys):
   # MAY DO: raise excetion if not labelled
   for db_row in stream_flat_data(rs):
          d = db_tuple_to_dict(db_row)
          if d['freq'] == freq:
              yield {k: d[k] for k in keys}

def annual_data_stream(rs):
     return data_stream(rs, 'a', ['varname', 'year', 'value'])

def qtr_data_stream(rs):
     return data_stream(rs, 'q', ['varname', 'year', 'qtr', 'value'])

def monthly_data_stream(rs):
     return data_stream(rs, 'm', ['varname', 'year', 'month', 'value'])
   
def get_annual_df(rs):
    """Returns pandas dataframe with annual data from labelled rowsystem *rs*."""
    
    def duplicate_labels(df):
           r = df[df.duplicated(['varname','year']) == True]
           return r['varname'].unique()
       
    def check_for_dups(df): 
           dups = duplicate_labels(df)
           if len(dups) > 0:
               raise Exception("Duplicate labels: " + " ".join(dups))

    dfa = pd.DataFrame(annual_data_stream(rs))
    dfa = dfa.pivot(columns='varname', values='value', index='year')
    #TODO: 
    #check_for_dups(dfa)
    return dfa

def get_end_of_monthdate(y, m):
    return datetime(year=y, month=m, day=monthrange(y, m)[1])

def get_end_of_quarterdate(y, q):
    return datetime(year=y, month=q*3, day=monthrange(y, q*3)[1])
    
def get_qtr_df(rs):
    """Returns pandas dataframe with QUARTERLY data from labelled rowsystem *rs*."""
    
    # get datastream     
    dfq = pd.DataFrame(qtr_data_stream(rs))
    
    # add time index
    dt = [get_end_of_quarterdate(y,q) for y, q in zip(dfq["year"], dfq["qtr"])]
    dfq["time_index"] = pd.DatetimeIndex(dt, freq = "Q")

    # reshape
    dfq = dfq.pivot(columns='varname', values='value', index='time_index')
    
    # add extra columns
    dfq.insert(0, "year", dfq.index.year)    
    dfq.insert(1, "qtr", dfq.index.quarter)
    return dfq

def get_monthly_df(rs):
    """Returns pandas dataframe with MONTHLY data from labelled rowsystem *rs*."""
    # get datastream     
    dfm = pd.DataFrame(monthly_data_stream(rs))
    
    # add time index
    dt = [get_end_of_monthdate(y,m) for y, m in zip(dfm["year"], dfm["month"])]
    dfm["time_index"] = pd.DatetimeIndex(dt, freq = "M")

    # reshape
    dfm = dfm.pivot(columns='varname', values='value', index='time_index')
    
    # add extra columns
    dfm.insert(0, "year", dfm.index.year)
    dfm.insert(1, "month", dfm.index.month)
    return dfm
    
def dfs(rs):
    dfa = get_annual_df(rs)
    dfq = get_qtr_df(rs)
    dfm = get_monthly_df(rs)
    return dfa, dfq, dfm

# END QUERY ROWSYSTEM
# =============================================================================    
    
# =============================================================================    
# QUERY LABELS

#------------------------------------------------------------------------------
#  Variable label manipulation
#------------------------------------------------------------------------------
def get_var_abbr(name):
    words = name.split('_')
    return '_'.join(itertools.takewhile(lambda word: word.isupper(), words))
assert get_var_abbr('PROD_E_TWh') == 'PROD_E' 

def get_unit_abbr(name):
    words = name.split('_')
    return '_'.join(itertools.dropwhile(lambda word: word.isupper(), words))
assert get_unit_abbr('PROD_E_TWh') == 'TWh'

     
def unique(x):
    return sorted(list(set(x)))

# labels in rowsystem data    
def rowsystem_full_labels(rs):
    assert is_labelled(rs)
    varnames = unique(db_tuple_to_dict(t)['varname'] for t in stream_flat_data(rs))
    return sorted(varnames)    
    
def rowsystem_head_labels(rs):
    return unique([get_var_abbr(name) for name in rowsystem_full_labels(rs)])


folder = os.path.dirname(os.path.realpath(__file__))
rs = init_rowsystem_from_folder(folder)
print(rowsystem_head_labels(rs))    

    
    
# labels in definition files    
def definition_full_labels(folder):
     pass
     
def definition_full_labels(folder):
     pass

def get_user_defined_full_labels(data_folder):
    hdr, seg = get_spec_and_cfg_varnames(data_folder)
    return unique(hdr+seg)

def get_user_defined_varnames(data_folder):
    hdr, seg = get_spec_and_cfg_varnames(data_folder)
    return unique(hdr+seg)

def get_spec_and_cfg_varnames(data_folder):
    csv, default_spec, segments = get_folder_definitions(folder)
    header_dict = default_spec[0]
    hdr = unpack_header_dict(header_dict)
    seg = unpack_segments(segments)
    return hdr, seg
    
def unpack_header_dict(header_dict):
   """Get varnames from header_dict"""
   return list(x[0] for x in header_dict.values())

def unpack_segments(segments):
   """Get varnames from segments"""
   var_list = []
   for seg in segments:
       seg_var_list =  unpack_header_dict(seg[2][0])       
       var_list.extend(seg_var_list)
   return var_list    

    
# =============================================================================    
