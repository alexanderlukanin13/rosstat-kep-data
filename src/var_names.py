# -*- coding: utf-8 -*-
""" Generate variable list. Entry point: 
    dump_var_list_explained() writes output/varnames.md
"""
import itertools
import pandas as pd
import tabulate  # Uncommented for test_pure_tabulate

from common import docstring_to_file

# NOTE: this function is a direct query to all unique labels
from database import get_unique_labels

FILLER = "<...>"


# ----------------------------------------------------------------------------

from common import get_filenames
data_folder = "../data/ind09/"
csv, spec, cfg = get_filenames(data_folder)

from load_spec import load_spec
default_dicts = load_spec(spec)

# ----------------------------------------------------------------------------

def get_var_abbr(name):
    words = name.split('_')
    return '_'.join(itertools.takewhile(lambda word: word.isupper(), words))
assert get_var_abbr('PROD_E_TWh') == 'PROD_E' 

def get_unit_abbr(name):
    words = name.split('_')
    return '_'.join(itertools.dropwhile(lambda word: word.isupper(), words))
assert get_unit_abbr('PROD_E_TWh') == 'TWh'

# ----------------------------------------------------------------------------

def get_title(name, ddict = default_dicts):
    title_abbr = get_var_abbr(name)
    headline_dict = ddict[0]
    for title, two_labels_list in headline_dict.items():
        if title_abbr == two_labels_list[0]:
            return title
    return FILLER       
assert get_title('CONSTR_yoy') == 'Объем работ по виду деятельности "Строительство"'
assert get_title('I_bln_rub') == 'Инвестиции в основной капитал'

# ----------------------------------------------------------------------------
    
inspection = dict((v[1], k.split(",")[-1]) for k,v in default_dicts[0].items())

UNITS_ABBR = {
# --- part from default_dicts [0]
    'rog':'в % к предыдущему периоду',
    'rub':'рублей',
    'yoy':'в % к аналог. периоду предыдущего года' ,
# --- part from default_dicts [1],
     #'bln t-km': 'млрд. т-км',
    'bln_t_km': 'млрд. т-км',
    'percent': '%',
    'bln_rub': 'млрд. руб.',
     #'bln rub': 'млрд. руб.',
    'bln_rub_fix': 'млрд. руб. (в фикс. ценах)',
    'mln': 'млн. человек',
    'mln_t': 'млн. т',
    'TWh': 'млрд. кВт·ч',
    'eop': 'на конец периода',
    'bln': 'млрд.',
    'units': 'штук',
    'th': 'тыс.',
}

def get_unit(name):
    unit_abbr = get_unit_abbr(name)
    if unit_abbr in UNITS_ABBR.keys():
        return UNITS_ABBR[unit_abbr]
    else:
        return FILLER 
assert get_unit('CONSTR_yoy') == 'в % к аналог. периоду предыдущего года'
assert get_title('I_yoy') == 'Инвестиции в основной капитал'

# ----------------------------------------------------------------------------

TABLE_HEADER = ["Код", "Описание", "Ед.изм."]

def get_var_list_components():
    """Returns a list of tuples each containing variable name, text description and unit of measurement."""
    var_names = get_unique_labels()
    return [[vn, get_title(vn), get_unit(vn)] for vn in var_names]

def get_max_widths(table):
    """Returns a list of maximum lenghts of variable names, text descriptions and unit of measurements."""
    xx = [[len(value) for value in row] for row in table]
    max_widths = [max(xx, key = lambda x: x[i])[i] for i in range(len(xx[0]))]
    return max_widths
def get_var_table_as_dataframe():
    """Not tested. This is for issue #36"""
    # TODO
    list_ = get_var_list_components()
    return pd.DataFrame(list_, columns = TABLE_HEADER)

def pure_tabulate(table, header = TABLE_HEADER):
    """For issue #28:
    This function must return same result as tabulate.tabulate with tablefmt="pipe"
    It should pass test_pure_tabulate().  
    Currently it is a valid markdown, but without proper spacing."""
    width = get_max_widths(table)
    width_dict = {'width{}'.format(i):width[i] for i in range(len(width))}
    str_ = ("| " + '{:<{width0}}' + " | " + '{:<{width1}}' + " | " + '{:<{width2}}' + " |\n").format('Код','Описание','Ед.изм.',**width_dict) + \
    ("|:-" + '{:-<{width0}}' + "|:-" + '{:-<{width1}}' + "|:-" + '{:-<{width2}}' + "|\n").format('','','', **width_dict) + \
    "\n".join([("| " + '{:<{width0}}' + " | " + '{:<{width1}}' + " | " + '{:<{width2}}' + " |").format(vn,desc,unit,**width_dict) for vn, desc, unit in table])
    return str_

def test_pure_tabulate():
    table = get_var_list_components() 
    assert pure_tabulate(table, TABLE_HEADER) == tabulate.tabulate(table, TABLE_HEADER, tablefmt="pipe")

def get_table():
    table = get_var_list_components()
    return pure_tabulate(table)
    #return tabulate.tabulate(table, header, tablefmt="pipe") 

def dump_var_list_explained():
    """Writes table of variables (label, desciption, unit) to src/output/varnames.md"""    
    tab_table = get_table()
    docstring_to_file(tab_table, "varnames.md", "output")

if __name__ == "__main__":
    print(default_dicts)
    print()
    print(get_table())
    dump_var_list_explained()

# NOTE 1: not using additional dictionaries yet
# from label_csv import _get_segment_specs_no_header_doc
# segment_specs = _get_segment_specs_no_header_doc(cfg)
# print(segment_specs)

# NOTE 2: presence of variable in this table in does not guarantee 
# it is filled with data at all or at particular frequency (e.g. monthly).
