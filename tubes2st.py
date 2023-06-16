import pandas as pd
import streamlit as st
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.models.widgets import Select, Slider
from bokeh.io import curdoc

# Membaca data
df = pd.read_csv('dataset2.csv')

# Membuat ColumnDataSource awal untuk plot line
source_line = ColumnDataSource(data=df)

# Membuat plot line awal
plot_line = figure(title='Dataset Visualization', x_axis_label='Year', y_axis_label='Value', plot_height=400, plot_width=600)
line = plot_line.line(x='Year', y='Value', source=source_line, line_width=2)
hover_tool_line = HoverTool(tooltips=[('Area', '@Area'), ('Year', '@Year'), ('Value', '@Value')])
plot_line.add_tools(hover_tool_line)

# Membuat ColumnDataSource awal untuk plot korelasi
source_corr = ColumnDataSource(data=df)

# Membuat plot korelasi awal
plot_corr = figure(title='Correlation Plot', x_axis_label='Area 1', y_axis_label='Area 2', plot_height=400, plot_width=600)
circle = plot_corr.circle(x='Value', y='Value', source=source_corr, size=8, color='navy', alpha=0.5)
hover_tool_corr = HoverTool(tooltips=[('Area', '@Area'), ('Year', '@Year'), ('Value', '@Value')])
plot_corr.add_tools(hover_tool_corr)

# Membaca tahun minimal dan maksimal dari dataset
min_year = df['Year'].min()
max_year = df['Year'].max()

# Membuat dropdown untuk memilih area pada plot line
select_area_line = Select(title="Area", value=df['Area'].unique()[0], options=df['Area'].unique().tolist())

# Membuat slider untuk memilih rentang tahun pada plot line
slider_start_year_line = Slider(title="Start Year", start=min_year, end=max_year, value=min_year, step=1)
slider_end_year_line = Slider(title="End Year", start=min_year, end=max_year, value=max_year, step=1)

# Mengupdate plot line saat nilai dropdown atau slider berubah
def update_plot_line(attr, old, new):
    selected_area = select_area_line.value
    start_year = slider_start_year_line.value
    end_year = slider_end_year_line.value

    # Memfilter data sesuai dengan area dan rentang tahun yang dipilih
    filtered_data = df[(df['Area'] == selected_area) & (df['Year'] >= start_year) & (df['Year'] <= end_year)]

    # Memperbarui data pada ColumnDataSource plot line
    source_line.data = filtered_data

    # Memperbarui label pada sumbu x dan y plot line
    plot_line.xaxis.axis_label = 'Year'
    plot_line.yaxis.axis_label = 'Value'

    # Memperbarui judul plot line
    plot_line.title.text = f"Data for {selected_area} - Year {start_year} to {end_year}"

    # Memperbarui plot korelasi
    update_plot_corr(None, None, None)

select_area_line.on_change('value', update_plot_line)
slider_start_year_line.on_change('value', update_plot_line)
slider_end_year_line.on_change('value', update_plot_line)

# Membuat dropdown untuk memilih negara 1 pada plot korelasi
select_area_corr1 = Select(title="Area 1", value=df['Area'].unique()[0], options=df['Area'].unique().tolist())

# Membuat dropdown untuk memilih negara 2 pada plot korelasi
select_area_corr2 = Select(title="Area 2", value=df['Area'].unique()[1], options=df['Area'].unique().tolist())

# Membuat slider untuk memilih rentang tahun pada plot korelasi
slider_start_year_corr = Slider(title="Start Year", start=min_year, end=max_year, value=min_year, step=1)
slider_end_year_corr = Slider(title="End Year", start=min_year, end=max_year, value=max_year, step=1)

# Mengupdate plot korelasi saat nilai dropdown atau slider berubah
def update_plot_corr(attr, old, new):
    selected_area1 = select_area_corr1.value
    selected_area2 = select_area_corr2.value
    start_year = slider_start_year_corr.value
    end_year = slider_end_year_corr.value

    # Memfilter data sesuai dengan negara 1, negara 2, dan rentang tahun yang dipilih
    filtered_data = df[((df['Area'] == selected_area1) | (df['Area'] == selected_area2)) &(df['Year'] >= start_year) &(df['Year'] <= end_year)]

    # Memperbarui data pada ColumnDataSource plot korelasi
    source_corr.data = filtered_data

    # Memperbarui label pada sumbu x dan y plot korelasi
    plot_corr.xaxis.axis_label = selected_area1
    plot_corr.yaxis.axis_label = selected_area2

    # Memperbarui judul plot korelasi
    plot_corr.title.text = f"Correlation Plot: {selected_area1} vs {selected_area2} - Year {start_year} to {end_year}"

select_area_corr1.on_change('value', update_plot_corr)
select_area_corr2.on_change('value', update_plot_corr)
slider_start_year_corr.on_change('value', update_plot_corr)
slider_end_year_corr.on_change('value', update_plot_corr)

# Menyusun layout
layout = column(select_area_line, slider_start_year_line, slider_end_year_line, plot_line,select_area_corr1, select_area_corr2, slider_start_year_corr, slider_end_year_corr, plot_corr,)

# Menambahkan layout ke current document
doc = curdoc()
doc.add_root(layout)

# Menampilkan plot menggunakan streamlit
st.bokeh_chart(layout)
