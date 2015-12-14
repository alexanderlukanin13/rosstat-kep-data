# -*- coding: utf-8 -*-

import yaml
from kep.io.common import docstring_to_file, delete_file
from kep.io.specification import load_spec, get_yaml

MUST_CLEANUP = True

DOC_SPEC = """# Configuration file
# 1. Names of special reader functions for some variables. Used for uncoventional tables. TO BE DEPRECIATED.
CPI : read12
---
# 2. Unit headers <-> unit names
в % к предыдущему периоду : rog
---
# 3. Main headers <-> variable names + default unit names
Инвестиции в основной капитал :
  - I
  - bln_rub"""

def test_spec():
    p = docstring_to_file(DOC_SPEC, "test_spec.txt")
    header_dict, unit_dict = load_spec(p)
    assert header_dict == {"Инвестиции в основной капитал" : ["I", "bln_rub"]}
    assert unit_dict == {"в % к предыдущему периоду" : "rog"}
    if MUST_CLEANUP:
        delete_file(p)
    
CFG_SPEC = """- 3.5. Индекс потребительских цен
- 4. Социальная сфера 
- spec_cpi.txt
----
- Производство транспортных средств и оборудования
- 1.7. Инвестиции в основной капитал
- _spec_1.txt"""

def test_cfg():
    p = docstring_to_file(DOC_SPEC, "test_cfg.txt")
    cfgs = load_cfg(p)
    assert cfgs[0][0] == "3.5. Индекс потребительских цен"
    assert cfgs[1][2] == "_spec_1.txt"
    if MUST_CLEANUP:
        delete_file(p)
  
  
def test_cfg():
    p = docstring_to_file(DOC_SPEC, "test_spec.txt")
    header_dict, unit_dict = load_spec(p)
    assert header_dict == {"Инвестиции в основной капитал" : ["I", "bln_rub"]}
    assert unit_dict == {"в % к предыдущему периоду" : "rog"}
    delete_file(p)
	
	
	