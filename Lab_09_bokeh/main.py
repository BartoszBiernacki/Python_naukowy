# bokeh serve --show main.py

from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.layouts import row, column
from bokeh.models import Slider

from SIR import SIR


def update(attr, old, new):
    t, S, I, R = SIR(beta=beta_slider.value, gamma=gamma_slider.value)

    line_S.data_source.data = {'x': t, 'y': S}
    line_I.data_source.data = {'x': t, 'y': I}
    line_R.data_source.data = {'x': t, 'y': R}


fig = figure(width=400, aspect_ratio=1)
fig.grid.visible = False

beta_slider = Slider(
    start=0, end=1, value=0.20, step=0.01,
    title=r'$$\beta$$', width=200
)

gamma_slider = Slider(
    start=0, end=1, value=0.05, step=0.01,
    title=r'$$\gamma$$', width=200
)

beta_slider.on_change('value_throttled', update)
gamma_slider.on_change('value_throttled', update)

t, S, I, R = SIR(beta=beta_slider.value, gamma=gamma_slider.value)
line_S = fig.line(x=t, y=S, line_color='blue', legend_label='S')
line_I = fig.line(x=t, y=I, line_color='red', legend_label='I')
line_R = fig.line(x=t, y=R, line_color='green', legend_label='R')

curdoc().add_root(row(
    column(beta_slider, gamma_slider),
    fig))
