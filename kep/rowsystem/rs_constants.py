SPEC1 = ({'Gross domestic product': ['GDP', 'bln_rub']}, {'percent change from previous year': 'yoy', 'billion ruble': 'bln_rub'}, {'special reader': None, 'start line': None, 'end line': None})

LABELLED_RS = [
       {'string':"1. Gross domestic product at current prices",
          'list':["1. Gross domestic product at current prices"],
          'head_label':'GDP',
          'unit_label':'bln_rub',
          'spec': SPEC1},
        
        {'string':"billion ruble",
          'list':["billion ruble"],
          'head_label':'GDP',
          'unit_label':'bln_rub',
          'spec': SPEC1},          
        
        {'string':"\tYEAR\tVALUE",
          'list':["", "YEAR", "VALUE"],
          'head_label':'GDP',
          'unit_label':'bln_rub',
          'spec': None},
          
        {'string':"2013\t61500",
          'list':["2013", "61500"],
          'head_label':'GDP',
          'unit_label':'bln_rub',
          'spec': SPEC1},
                    
        {'string':"2014\t64000",
          'list':["2014", "64000"],
          'head_label':'GDP',
          'unit_label':'bln_rub',
          'spec': SPEC1},
          
         {'string': "percent change from previous year - annual basis",
          'list': ["percent change from previous year - annual basis"],
          'head_label': 'GDP',
          'unit_label': 'yoy',
          'spec': SPEC1},
          
        {'string':"2013\t1.013",
          'list':["2013", "1.013"],
          'head_label':'GDP',
          'unit_label':'yoy',
          'spec': SPEC1},

        {'string':"2014\t1.028",
          'list':["2014", "1.028"],
          'head_label':'GDP',
          'unit_label':'yoy',
          'spec': SPEC1}         
]

LABELLED_WITH_SEGMENTS = [{'head_label': 'GDP',
  'list': ['1. Gross domestic product at current prices'],
  'spec': ({'Gross domestic product': ['GDP', 'bln_rub']},
           {'billion ruble': 'bln_rub',
            'percent change from previous year': 'yoy'},
           {'end line': None, 'special reader': None, 'start line': None}),
  'string': '1. Gross domestic product at current prices',
  'unit_label': 'bln_rub'},
 {'head_label': 'GDP',
  'list': ['billion ruble'],
  'spec': ({'Gross domestic product': ['GDP', 'bln_rub']},
           {'billion ruble': 'bln_rub',
            'percent change from previous year': 'yoy'},
           {'end line': None, 'special reader': None, 'start line': None}),
  'string': 'billion ruble',
  'unit_label': 'bln_rub'},
 {'head_label': 'GDP',
  'list': ['', 'YEAR', 'VALUE'],
  'spec': None,
  'string': '\tYEAR\tVALUE',
  'unit_label': 'bln_rub'},
 {'head_label': 'GDP',
  'list': ['2013', '61500'],
  'spec': ({'Gross domestic product': ['GDP', 'bln_rub']},
           {'billion ruble': 'bln_rub',
            'percent change from previous year': 'yoy'},
           {'end line': None, 'special reader': None, 'start line': None}),
  'string': '2013\t61500',
  'unit_label': 'bln_rub'},
 {'head_label': 'GDP',
  'list': ['2014', '64000'],
  'spec': ({'Gross domestic product': ['GDP', 'bln_rub']},
           {'billion ruble': 'bln_rub',
            'percent change from previous year': 'yoy'},
           {'end line': None, 'special reader': None, 'start line': None}),
  'string': '2014\t64000',
  'unit_label': 'bln_rub'},
 {'head_label': 'GDP',
  'list': ['percent change from previous year - annual basis'],
  'spec': ({'Gross domestic product': ['GDP', 'bln_rub']},
           {'billion ruble': 'bln_rub',
            'percent change from previous year': 'yoy'},
           {'end line': None,
            'special reader': 'read_special',
            'start line': 'percent change'}),
  'string': 'percent change from previous year - annual basis',
  'unit_label': 'yoy'},
 {'head_label': 'GDP',
  'list': ['2013', '1.013'],
  'spec': ({'Gross domestic product': ['GDP', 'bln_rub']},
           {'billion ruble': 'bln_rub',
            'percent change from previous year': 'yoy'},
           {'end line': None,
            'special reader': 'read_special',
            'start line': 'percent change'}),
  'string': '2013\t1.013',
  'unit_label': 'yoy'},
 {'head_label': 'GDP',
  'list': ['2014', '1.028'],
  'spec': ({'Gross domestic product': ['GDP', 'bln_rub']},
           {'billion ruble': 'bln_rub',
            'percent change from previous year': 'yoy'},
           {'end line': None,
            'special reader': 'read_special',
            'start line': 'percent change'}),
  'string': '2014\t1.028',
  'unit_label': 'yoy'}]
