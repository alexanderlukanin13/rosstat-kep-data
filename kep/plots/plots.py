# -*- coding: utf-8 -*-

import os
import matplotlib
# Without the following import, setting matplotlib.style crashes with AttributeError.
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

from kep.selector.save import get_dfm   

matplotlib.style.use('ggplot')

# The default figsize is the of an A4 sheet in inches
A4_SIZE_PORTRAIT = [8.27, 11.7]
TITLE_FONT_SIZE = 12

PDF_FILE   = 'output/monthly.pdf'
MD_PATH    = 'output/images.md'
PNG_FOLDER = 'output/png'

#####################################################################################################
# Entry points

def write_plots():
    """Write monthly graphs as *.png plots with markdown showcase file and as a PDF file."""       
    print("Reading stored data...")
    df = get_dfm()
    
    # png images    
    print("Writing .png images...")
    write_png_pictures(df)   
    
    # md file
    print("Writing markdown (.md) showcase file with images...")
    generate_md(df)
    
    # PDF output
    print("Writing PDF file...")
    write_monthly_pdf()
    
    print("Done.")

def write_monthly_pdf():
    df = get_dfm()
    save_plots_as_pdf(df, PDF_FILE)  

def write_monthly_png(): 
    df = get_dfm()    
    write_png_pictures(df)       
    generate_md(df)

#-----------------------------------------------------
# PDF


def save_plots_as_pdf(df, filename=PDF_FILE, nrows=3, ncols=2, figsize=A4_SIZE_PORTRAIT, title_font_size=TITLE_FONT_SIZE):
    vars_ = df.columns
    nvars = len(vars_)
    vars_per_page = nrows * ncols
    with PdfPages(filename) as pdf:
        for start_index in range(0, nvars, vars_per_page):
            page_vars = vars_[start_index:start_index+vars_per_page]
            axes = many_plots_per_page(df[page_vars], nrows, ncols, figsize, title_font_size)
            pdf.savefig()
            # plt.close()

def many_plots_per_page(df, nrows, ncols, figsize=A4_SIZE_PORTRAIT, title_font_size=TITLE_FONT_SIZE):
    
    page_vars = df.columns
    
    # The following command uses the built-in Pandas mechanism for placing subplots on a page.
    # It automatically increases spacing between subplots and rotates axis ticks if they
    # take up too much space. However, this mechanism is broken in Pandas < 0.17.
    # See: https://github.com/pydata/pandas/issues/11536
    # It also cannot handle multiple variables per subplot, so if we want that, we'll have to
    # replicate parts of the Pandas implementation or write our own.
    axes = df.plot(subplots=True, layout=(nrows, ncols), legend=None, figsize=figsize)
    
    # Now removing axis labels and adding plot titles.
    for i, axes_row in enumerate(axes):
        for j, ax in enumerate(axes_row):
            var_idx = i * ncols + j
            if var_idx >= len(page_vars):
                # We're at the end of the last page, which is not filled completely.
                break
            ax.set_title(page_vars[var_idx], fontsize=title_font_size)
            format_ax(ax)
    return axes

#-----------------------------------------------------
# additional formatting for plot - in PDF and png
    
def format_ax(ax):
    ax.set_xlabel('')
    # NOTE - API references:
    # - http://matplotlib.org/api/axes_api.html#matplotlib.axes.Axes.get_xticklabels
    # - http://matplotlib.org/api/text_api.html#matplotlib.text.Text.set_rotation
    labels = ax.get_xticklabels()
    for l in labels:
        l.set_rotation('vertical')
    ax.xaxis.tick_bottom()
    #return ax

#-----------------------------------------------------
# PNG

def one_plot(df, nrows = 3, ncols = 2,  figsize=A4_SIZE_PORTRAIT, title_font_size=TITLE_FONT_SIZE):   
    # set single plot size propotional to paper and number of plot rows/columns per page
    # WARNING: updating figsize in-place means that A4_SIZE_PORTRAIT gets modified.
    # This leads to unexpected problems.
    ax = df.plot(legend=None, figsize=(figsize[0] / ncols, figsize[1] / nrows))
    ax.set_title(df.name, fontsize=title_font_size)
    # additional formatting for plot
    format_ax(ax)
    return ax

def make_png_filename(vn, dirpath = PNG_FOLDER):
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
    return os.path.join(dirpath, "%s.png" % vn)
    
def write_png_pictures(df):   
    for vn in df.columns:
        # Indexing df as df[[vn]] produces a DataFrame, not a Series. Therefore,
        # it does not have a .name attribute, but it has .columns instead.
        ts = df[vn]
        
        # one_plot returns Axes and sets matplotlib's current figure to the plot it draws
        try:        
            ax = one_plot(ts)
            filepath = make_png_filename(vn)
            plt.subplots_adjust(bottom=0.15)
            plt.savefig(filepath)        
            plt.close() 
        except:
            raise Exception("Error plotting variable: " + str(vn)) 

def generate_md(df):
    var_names = df.columns
    # сгенерировать markdown файл, в котором по 3 на строку
    # выведены все картинки var_names + ".png"
    IMAGES_PER_LINE = 3

    # Any sense in using a specialized package for this?
    with open(MD_PATH, 'w') as f:
        for row_start in range(0, len(var_names), IMAGES_PER_LINE):
            line_vars = var_names[row_start:row_start+IMAGES_PER_LINE]
            f.write(' '.join('![](png/%s.png)' % var_name for var_name in line_vars) + '\n')
	
    
def sample_plot():
    # sample plot
	#from end_user import get_ts
    #ts = get_ts('IND_PROD_yoy', "m", "1999-01")    
    #one_plot(ts)  
    #plt.close()
	pass
    
if __name__ == "__main__":    
    write_plots()
    #write_monthly_pdf()
    
# NOTE: с меньшим количеством лет ориентация подписей по оси х некрасивая +  на англ. яз.