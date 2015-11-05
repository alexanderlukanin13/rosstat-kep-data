# -*- coding: utf-8 -*-

import database, query

dfa, dfq, dfm = database.read_dfs()

def get_rows_by_date_range(freq, start_date, end_date=None):
    if freq == 'a':
        df = dfa
        if isinstance(start_date, str):
            start_date = int(start_date)
        indexer = df.year >= start_date
        if end_date is not None:
            if isinstance(end_date, str):
                end_date = int(end_date)
            indexer &= df.year <= end_date
    elif freq == 'q':
        df = dfq
        start_year, start_qtr = map(int, start_date.split('-'))
        indexer = (df.year > start_year) | ((df.year == start_year) & (df.qtr >= start_qtr))
        if end_date is not None:
            end_year, end_qtr = map(int, end_date.split('-'))
            indexer &= (df.year < end_year) | ((df.year == end_year) & (df.qtr <= end_qtr))
    elif freq == 'm':
        df = dfm
        start_year, start_month = map(int, start_date.split('-'))
        indexer = (df.year > start_year) | ((df.year == start_year) & (df.month >= start_month))
        if end_date is not None:
            end_year, end_month = map(int, end_date.split('-'))
            indexer &= (df.year < end_year) | ((df.year == end_year) & (df.month <= end_month))
    else:
        raise ValueError("Unrecognized frequency: %s" % freq)
    return df[indexer]

def get_time_series(label, freq, start_date, end_date=None):
    df = get_rows_by_date_range(freq, start_date, end_date)
    return df[df.label == label]['val']

def get_dataframe(labels, freq, start_date, end_date=None):
    df = get_rows_by_date_range(freq, start_date, end_date)
    filtered = df[df.label.isin(labels)]
    if freq == 'a':
        return query.reshape_a(filtered)
    elif freq == 'q':
        return query.reshape_q(filtered)
    else:
        return query.reshape_m(filtered)

print(get_time_series("I_yoy", "a", 2000))
print(get_time_series("I_yoy", "q", "2000-1", "2015-2"))
print(get_time_series("I_yoy", "m", "2000-07", "2015-01"))
print(get_dataframe(["I_yoy", ], "m", "2000-07", "2015-01"))

#------------- todo api-2 - отрисовывать all_monthly_df

from query import get_var_list

vars = get_var_list()
all_monthly_df = get_dataframe(vars, "m", "1999-01")
print(all_monthly_df)

# нужно подумать над способом рисовать многочисленную группу графиков all_monthly_df 
# например по 2*3 = 6 штук на страницу в окно, а потом нескоько страниц скливать в pdf или html
# идея в том, чтобы примерно видеть наполнение базы данных + затем группировать показатели по разделам
# мжно сначала что-то корявое типа all_monthly_df.plot() но там из-за большлго количества графиков не будет видно подписей 
 

