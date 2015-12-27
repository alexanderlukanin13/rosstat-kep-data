#------------------------------------------------------------------------------
#  Raw data and readings 
#------------------------------------------------------------------------------

ip_raw_data_doc = """1.2. Индекс промышленного производства1)         / Industrial Production index1)																	
в % к соответствующему периоду предыдущего года  / percent of corresponding period of previous year																	
2014	101,7	101,1	101,8	101,5	102,1	99,8	102,1	101,4	102,4	102,8	100,4	101,5	100,0	102,8	102,9	99,6	103,9
в % к предыдущему периоду  / percent of previous period																	
2014		87,6	103,6	102,7	109,6	81,2	101,6	109,7	97,3	99,6	99,9	102,2	99,8	102,7	105,1	99,8	108,1
период с начала отчетного года  в % к соответствующему периоду предыдущего года  / period from beginning of reporting year  as percent of corresponding period of previous year																	
2014						99,8	100,9	101,1	101,4	101,7	101,5	101,5	101,3	101,5	101,7	101,5	101,7"""

ip_spec_doc = """# Раздел 1. Специальная/дополнительная информация
# Section 1. Auxillary information
RUR_USD : read13

---
# Раздел 2. Единицы измерении
# Section 2. Units of measurement

в % к предыдущему периоду: rog
в % к соответствующему периоду предыдущего года: yoy

---
# Раздел 3. Определения переменных
# Section 3. Variable definitions
#
# Формат:
# Часть названия таблицы :
# - VAR_LABEL # sample label
# - bln_rub # sample units

#1.7. Инвестиции в основной капитал1), млрд. рублей  / Fixed capital investments1), bln rubles

Инвестиции в основной капитал :
 - I
 - bln_rub
"""
ip_spec_dicts = {'headers' = {'Инвестиции в основной капитал': ['I', 'bln_rub']},
                   'units' = {'в % к предыдущему периоду': 'rog',
                              'в % к соответствующему периоду предыдущего года': 'yoy'})
				  
ip = {'raw_data_doc': ip_raw_data_doc, 'spec_doc': ip_spec, 'spec_dicts':ip_spec_dicts)
 
# write ip['spec_doc'] to file 
# from file with ip['spec_doc'] must obtain ip['spec_dicts']




trans = """Производство транспортных средств и оборудования  / Manufacture of  transport equipment												
отчетный месяц в % к предыдущему месяцу  / reporting month as percent of previous month												
2015	31,1	126,3	139,8	83,8	94,6	115,8						
отчетный месяц в % к соответствующему месяцу предыдущего года  / reporting month as percent of corresponding month of previous year												
2015	87,2	77,6	94,8	77,8	82,2	80,1						
	Янв. Jan.	Фев. Feb.	Март Mar.	Апр. Apr.	Май May	Июнь June	Июль July	Август Aug.	Сент. Sept.	Окт. Oct.	Нояб. Nov.	Дек. Dec.
период с начала отчетного года  в % к соответствующему периоду предыдущего года  / period from beginning of reporting year  as percent of corresponding period of previous year												
2015	87,2	82,4	86,5	84,3	83,9	83,3						"""

investment = """1.7. Инвестиции в основной капитал1), млрд. рублей  / Fixed capital investments1), bln rubles																	
2014	13527,7	1863,8	2942,0	3447,6	5274,3	492,2	643,2	728,4	770,4	991,1	1180,5	1075,1	1168,5	1204,0	1468,5	1372,5	2433,3
в % к соответствующему периоду предыдущего года / percent of corresponding period of previous year																	
2014	97,3	94,7	98,1	98,5	97,2	92,7	95,5	95,3	97,4	97,3	99,3	99,1	98,4	98,1	99,2	92,2	98,9
в % к предыдущему периоду  / percent of previous period																	
2014		35,7	158,2	114,9	149,9	21,1	129,6	114,5	106,6	127,0	119,0	90,5	107,1	103,3	121,6	92,7	173,8"""

#note: both cpi_block and food_block contain "непродовольственные товары", when importing 
#      text string cpi_block + food_block must use segment specification and config file
cpi_block = """3.5. Индекс потребительских цен (на конец периода, в % к концу предыдущего периода) / Consumer Price Index (end of period, percent of end of previous period)																	
1999	136,5	116,0	107,3	105,6	103,9	108,4	104,1	102,8	103,0	102,2	101,9	102,8	101,2			
	Год Year	Кварталы / Quarters	Янв. Jan.	Фев. Feb.	Март Mar.	Апр. Apr.	Май May	Июнь June	Июль July	Август Aug.	Сент. Sept.	Окт. Oct.	Нояб. Nov.	Дек. Dec.			
		I	II	III	IV												
непродовольственные товары / non-food products																	
1999	139,2	114,0	108,6	107,2	104,9	106,2	104,0	103,2	104,0	102,7	101,6	101,9	102,4	
"""

food_block = """Из общего объема оборота розничной торговли:																	
пищевые продукты, включая напитки, и табачные изделия1), млрд.рублей / Of total volume of retail trade turnover: food products, including beverages, and tobacco1),																	
bln rubles																	
1999	866,1	186,8	204,3	222,6	252,4	60,3	60,7	65,8	66,2	68,6	69,5	71,6	74,0	77,0	79,1	79,1	94,2
2015		79,1	101,8	103,7		70,4	96,4	107,1	97,2	102,4	99,3	103,0	101,5	97,9	101,4		
	Год Year	Кварталы / Quarters	Янв. Jan.	Фев. Feb.	Март Mar.	Апр. Apr.	Май May	Июнь June	Июль July	Август Aug.	Сент. Sept.	Окт. Oct.	Нояб. Nov.	Дек. Dec.			
		I	II	III	IV												
непродовольственные товары1), млрд.рублей / non-food goods1), bln rubles																	
1999	931,3	192,2	212,2	242,0	284,9	61,5	62,2	68,5	69,2	70,3	72,7	74,2	83,6	84,2	88,0	91,1	105,8
"""

# will use end_string to capture segment that is at the end of file 
end_string = "*** End of raw csv file ***" 

full_raw_doc = ip_raw_data_doc + trans + invetsment + cpi_block + food_block + end_string

# next:
# - check what data is used in specification testing, may also move to different folder
# - how to start stand-alone unittest (?)
# - header and unit dictionaries for each of these blocks 
# - specification text files 
# - cfg file
# - data structure that is obtained when reading cfg

# also:
# - simplify yaml (two docs in it)

