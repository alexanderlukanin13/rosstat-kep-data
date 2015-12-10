##Краткосрочные экономические показатели Российской Федерации  

Исходная публикация на сайте Росстата: [www.gks.ru][gks-stei] 

Ряды данных: 
- в формате Excel: [kep.xlsx][kep-at-git-xlsx], [kep.xls][kep-at-git-xls]
- в формате csv: 
  - [годовые](https://raw.githubusercontent.com/epogrebnyak/rosstat-kep-data/master/src/output/data_annual.txt) 
  - [квартальные](https://raw.githubusercontent.com/epogrebnyak/rosstat-kep-data/master/src/output/data_qtr.txt)
  - [месячные](https://raw.githubusercontent.com/epogrebnyak/rosstat-kep-data/master/src/output/data_monthly.txt) 

- [список переменных](https://raw.githubusercontent.com/epogrebnyak/rosstat-kep-data/master/src/output/varnames.md)

Графики:
- [PDF](https://github.com/epogrebnyak/rosstat-kep-data/blob/master/src/output/monthly.pdf)
- [*.png](https://github.com/epogrebnyak/rosstat-kep-data/blob/master/src/output/images.md)

[kep-at-git-xlsx]: https://github.com/epogrebnyak/rosstat-kep-data/blob/master/src/output/kep.xlsx?raw=true
[kep-at-git-xls]: https://github.com/epogrebnyak/rosstat-kep-data/blob/master/src/output/kep.xls?raw=true
[gks-stei]: http://www.gks.ru/wps/wcm/connect/rosstat_main/rosstat/ru/statistics/publications/catalog/doc_1140080765391


## Основные показатели

![](src/output/png/CPI_rog.png)![](src/output/png/IND_PROD_yoy.png)![](src/output/png/I_yoy.png)![](src/output/png/RUR_USD_eop.png)
![](src/output/png/SOC_UNEMPLOYMENT_percent.png)![](src/output/png/SOC_WAGE_rub.png)

## Примеры работы с программой 

### Получение данных (для конечного пользователя)

Note: save this as as example_end_user.py 
```python
import kep

# query by variable name(s) 
annual_wage_rub = kep.get_ts('SOC_WAGE_rub','a')
df1 =  kep.get_df(['SOC_WAGE_rub', 'CPI_rog'], 'm', '2012-01', '2015-06')

# NOTE: maybe check real wage growth can be computed inside here

# complete database:
annual_varnames = kep.get_varnames("a")
qtr_varnames    = kep.get_varnames("q")
month_varnames  = kep.get_varnames("m")
all_varnames    = kep.get_varnames(all = True)

dfa = kep.get_df(annual_varnames)
dfq = kep.get_df(qtr_varnames)
dfm = kep.get_df(month_varnames)

# shorter alternative for complete database:
dfa, dfq, dfm = kep.get_all_dfs()

# check different query methods return same result
assert dfa.SOC_WAGE_rub == kep.get_ts('SOC_WAGE_rub','a')
```

### Импорт в базу данных (для администратора БД)

Note: this is main.py, save this as as example_db_administrator.py 
```python
import kep 

data_folder = "data/2015/ind10"

# must stop if (1) no Word installed, (2) CSV file already exists - message about flag  "use (..., force_overwrite = True) to overwrite CSV". Intent - do not invoke here if there is no Word or file already exists.
kep.make_csv()

# import CSV file to database
kep.import_csv()

# save data and variable list to Excel and CSV files + write plots to PDF and *.png 
kep.dump_db()
```

## Структура программы (program flow)
```
1. Converter
doc - > raw csv
(word.py)

2. Parser
raw csv + specification -> labelled csv -> flat stream -> database
         (load_spec.py)   (label_csv.py)  (stream.py)    (database.py)

3. Selector
database -> dfm, dfq, dfa -> get_ts(), get_df()
                      ... -> get_varnames()   
(query.py)

4. Plotting
(plot.py)
```

##Comments
---------
13:04 07.12.2015

- import longer history
- datasets to be used in R and Excel for further analysis/modelling
- at git:
  (G0) maintainable/readable code + data structure
  (G1) enhance graphs 
  (G2) make full coverage of KEP publication + brush dataset, 
  (G3) make friendly API and 
  (G4) clean data export  
  (G5) data transformation (seasonality/detrending wth HP, index time series)
- propose key features for online interactive shell for KEP, similar to FRED

(G0) maintainable/readable code + data structure
- decide on packages (convert,parse,store + read/select + plot) or flat structure 

(G1) enhance graphs 
- no rigged upper end on png plots
- extend x axis to end of current year 
- add text name to graph title

(G2) make full coverage of KEP publication + brush dataset
- import October 2015 data

(G3) make friendly API 

this is used above:
```
# + also tests as samples
 
get_var_list(freq=None)
"""Returns a list of (a)nnual, (q)tr and (m)onthly variables in database."""
{"a": [...], "q": [...], "m": [...], "all": [...]}

get_df(var_list, freq):
"""Returns dataframe with *var_list* variables"""

get_ts(var_name, freq):
"""Returns time series base on *var_name*"""

a_list = get_var_list(freq="a")
q_list = get_var_list(freq="q")
m_list = get_var_list(freq="m")

# dfa, dfq and dfm are complete contents of the database
dfa = get_df(a_list)
dfq = get_df(q_list)
dfm = get_df(m_list)
```

(G4) clean data export  
- add NA to CSV/Excel export
- indicate which variables are a, q or m in 'variables sheet'

(G5) data transformation (seasonality/detrending wth HP, index time series)
- add seasonal component for selected variables (output monthly_nsa, monthly_sa, monthly_trend)
- add trend component for selected variables (output monthly_nsa, monthly_sa, monthly_trend)
- dating resession: data structure and background picture

##Todo

Самое важное сейчас:
- [ ] наладить работу как пакета 

Экспорт данных
- [ ] issue  #1 - экспорт данных: улучшение форматирования xls(x) файлов / apearance of xlsx file

Парсинг и импорт 
- [ ] issue #34: make varlist, including segments
- [ ] make varlist in order of appearance in markupfile + include segments

Тестирование

Текущие ошибки парсинга 
- [ ] #14: https://github.com/epogrebnyak/rosstat-kep-data/issues/14 'CORP_DEBT_rog' is invalid data (ind06)
- [ ] #35: не читается переменная 'PROFIT'

Рисунки:
- [ ] issue #33: Plotting: all single .png plots in plots.py lack proper dates on x axis

Докуменатция:
- [ ] issue #25: улучшить скрипт построения документации
- [ ] issue #32: написать примеры использвоания API - write API examples for README.md

##Done

Тестирование и стурктура пакета
- [x] issue #31: Testing: make test_1.py executable with py.test  
  -- from project root directory invoke tests (or individual files) as:  
```
py.test kep/test/test_yaml_import.py
python -m kep.test.test_yaml_import
```
- [x] issue #31 - запустить py.test внутри пакета (вместе c __init__.py) - Testing: run test_1.py executable with py.test 


Парсинг и импорт 
- [x] issue #30 - прочитать данные из csv c иcпользованием нескольких файлов разметки - read raw csv using config file and two spec files 

Экспорт данных
- [x] issue #24 - экспорт данных: xls файл
- [x] issue #26 - упрощение формата csv, use native pandas export for csv files

Рисунки:
- [x] issue #29: Save all monthly plots as .png files 
- [x] issue #27: make full list of .png files as markdown file 

##Not todo

Новые функции
- [ ] таблицы с нестандартным количеством столбцов, импорт данных по ВВП
- [ ] разбивка png-md или pdf файла на разделы
- [ ] новый шаблон pdf файла
- [ ] sql dump of database

Некритические
- [ ] transfer useful functions from old_src at src branch
- [ ] генерировать tab_headers.txt - использовать make_headers(p) в label_csv из ветки old_src
- [ ] issue #20: integrity check of database
- [ ] may remove first 'readers functions' part in spec file
- [ ] issue #6: orderly sequence of variables in xlsx file - in columns
- [ ] groups/sections of variables in pdf/md-png
- [ ] rename common to io + move load_spec to common + make test_load_spec.py
- [ ] check if header (eg "Объем платных услуг населению") has multiple appearances in raw csv file 
- [ ] issue #36: substitute 'tabulate' module with simple pure python function to write table
- [ ] maybe move 'output' folder to root  


##Итоговое использование
1. Ряды со снятием сезонности
2. Переменная состояния среды (фильтр Калмана по 3-5 переменным)
3. Индекс промышленного производства через натуральные показатели
4. Индекс инвестиций через инвестицонные товары 
5. Описание недостающих переменных и блоков (экспортные цены на нефть, например)
6. Простая структурная модель с одновременными уравнениями (ВВП по компонентам, нефть, простой платежный баланс)
