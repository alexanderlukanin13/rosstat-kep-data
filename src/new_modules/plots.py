# -*- coding: utf-8 -*-

import matplotlib
# Without the following import, setting matplotlib.style crashes with AttributeError.
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

from query import get_var_list
from api2 import get_dataframe

matplotlib.style.use('ggplot')


# The default page_size is an A4 sheet in inches
def save_plots_as_pdf(filename, nrows, ncols, df, vars, page_size=(8.27, 11.7)):
    vars_per_page = nrows * ncols
    with PdfPages(filename) as pdf:
        for start_index in range(0, len(vars), vars_per_page):
            page_vars = vars[start_index:start_index+vars_per_page]

            # The following command uses the built-in Pandas mechanism for placing subplots on a page.
            # It automatically increases spacing between subplots and rotates axis ticks if they
            # take up too much space. However, this mechanism is broken in Pandas < 0.17.
            # See: https://github.com/pydata/pandas/issues/11536
            # It also cannot handle multiple variables per subplot, so if we want that, we'll have to
            # replicate parts of the Pandas implementation or write our own.
            axes = df[page_vars].plot(subplots=True, layout=(nrows, ncols), legend=None, figsize=page_size)

            # Now removing axis labels and adding plot titles.
            for i, axes_row in enumerate(axes):
                for j, ax in enumerate(axes_row):
                    var_idx = i * ncols + j
                    if var_idx >= len(page_vars):
                        # We're at the end of the last page, which is not filled completely.
                        break
                    ax.set_title(page_vars[var_idx], fontsize=12)
                    ax.set_xlabel('')

                    # The following is an example of how to draw vertical labels.
                    # API references:
                    # - http://matplotlib.org/api/axes_api.html#matplotlib.axes.Axes.get_xticklabels
                    # - http://matplotlib.org/api/text_api.html#matplotlib.text.Text.set_rotation
                    labels = ax.get_xticklabels()
                    for l in labels:
                        l.set_rotation('vertical')

            pdf.savefig()

vars_ = get_var_list()
all_monthly_df = get_dataframe(vars_, "m", "1999-01")
save_plots_as_pdf('monthly.pdf', 3, 2, all_monthly_df, vars_)

# todo-plot-7:49 06.11.2015:

# у нас из tab.csv в итоге будет считываться очень много (несколько деястков) переменных

# задача рисунков сейчас - вывести все эти переменные на экран
# комбинации по два рисунка на график будут очень полезны, но не сейчас

# требуется:
# - на одном рисунке один график + название переменной только в заголовке сверху
# - задавать размещение графиков на страницу M*N - 3 на 2 например
# - постранично вывести все граифики из get_var_list() 
# - каждое окно с таким граифом сохранить в графический файл (например .png)
# - объединить эти рисунки в pdf или html файл
# - можно сразу сливать рисунки в один PDF - http://matplotlib.org/api/backend_pdf_api.html#matplotlib.backends.backend_pdf.PdfPages

# цель этой задачи - иметь выдачу, на которой нарисованы все имеющиеся 
# на этот момент в базе данных графики

# - таких выдач должно быть в итоге три - месячная, квартальая, годовая.

# end - todo-plot-7:49 06.11.2015:
