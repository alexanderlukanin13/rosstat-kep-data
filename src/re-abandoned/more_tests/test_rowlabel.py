# -*- coding: utf-8 -*-
from ..label_csv import get_label_in_text, get_label_on_start, yield_row_with_labels
from ..spec import load_spec
import os
    
headline_dict = {
    "Производство транспортных средств и оборудования":  ['PROD_TRANS', None]
     }
     
support_dict =  {
     "отчетный месяц в % к предыдущему месяцу" : 'rog',
     "отчетный месяц в % к соответствующему месяцу предыдущего года": 'yoy',
     "период с начала отчетного года" : 'ytd'
     }     

txt = """<added text> Производство транспортных средств и оборудования  / Manufacture of  transport equipment												
отчетный месяц в % к предыдущему месяцу  / reporting month as percent of previous month												
2002	81,4	101,1	102,6	107,5	94,2	105,2	102,5	102,5	105,8	95,6	89,1	103,3
отчетный месяц в % к соответствующему месяцу предыдущего года  / reporting month as percent of corresponding month of previous year												
2002	101,4	102,2	89,2	106,9	102,0	106,8	96,8	110,0	105,4	99,4	85,1	87,9
	Янв. Jan.	Фев. Feb.	Март Mar.	Апр. Apr.	Май May	Июнь June	Июль July	Август Aug.	Сент. Sept.	Окт. Oct.	Нояб. Nov.	Дек. Dec.
период с начала отчетного года  в % к соответствующему периоду предыдущего года  / period from beginning of reporting year  as percent of corresponding period of previous year												
2015	87,2	82,4	86,5	84,3	83,9	83,3						"""

def stub_rows():
    for row in [x.split("\t") for x in txt.split("\n")]:
        yield row
    
ROWS_GEN = stub_rows()
     
def test_dict_test():    
    a = "Производство транспортных средств и оборудования  / Manufacture of  transport equipment												"
    key = "Производство транспортных средств и оборудования"
    assert a.startswith(key) == True
    a1 = """<added text> Производство транспортных средств и оборудования  / Manufacture of  transport equipment												"""
    assert (key in a1) == True
    
    b = "период с начала отчетного года  в % к соответствующему периоду предыдущего года  / period from beginning of reporting year  as percent of corresponding period of previous year"
    
    assert get_label_in_text(a, headline_dict) ==  ['PROD_TRANS', None]
    assert get_label_in_text(a1, headline_dict) ==  ['PROD_TRANS', None]
    assert get_label_on_start(a, support_dict) == False 
    assert get_label_on_start(b, support_dict) == "ytd"

def test_row_label():    
    gen = yield_row_with_labels(ROWS_GEN, headline_dict, support_dict)
        
    assert next(gen)[0:2] == ['PROD_TRANS', 'rog']
    assert next(gen)[0:2] == ['PROD_TRANS', 'yoy']
    assert next(gen)[0:2] == ['PROD_TRANS', 'ytd']
    

doc_small = """1.10. Внешнеторговый оборот – всего1),  млрд.долларов США / Foreign trade turnover – total1),  bln US dollars																	
1999	115,1	24,4	27,2	28,4	35,1	7,2	7,9	9,3	9,8	8,0	9,3	9,5	9,3	9,6	10,4	11,1	13,7"""

def iter_doc(doc = doc_small):
    for row in [x.split("\t") for x in doc.split("\n")]:
        yield row
        
def test_has_unknowns():
    p = os.path.abspath("../data/minitab/minitab.csv")
    # open csv
    gen_in = iter_doc()
    # produce new rows
    headline_dict, support_dict = load_spec(p)    
    g = yield_row_with_labels(iter_doc(), headline_dict, support_dict)
    print(next(g))
    #assert next(g)[0] == 'unknown_var'
    
if __name__ == "__main__":
    test_has_unknowns()