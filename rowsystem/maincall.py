from rowsystem.path_config import CURRENT_MONTH_DATA_FOLDER

from rowsystem.rowsystem import RowSystem 
from rowsystem.db_interface import KEP


def get_dfa():
        
    folder = CURRENT_MONTH_DATA_FOLDER
    rs = RowSystem(folder)
    rs.save()    
    return KEP().annual_df()
    #kep = KEP()
    #dfa = kep.annual_df()
    #dfq = kep.quarter_df()
    #dfm = kep.monthly_df()

dfa = get_dfa()

