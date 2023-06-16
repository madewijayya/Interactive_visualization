import streamlit as st
import pandas as pd
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.layouts import column
from bokeh.models import Select, Slider
from bokeh.embed import components

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

# Convert min_year and max_year to integers
min_year = int(min_year)
max_year = int(max_year)

# Membuat dropdown untuk memilih area pada plot line
select_area_line = Select(title="Area", value=df['Area'].unique()[0], options=df['Area'].unique().tolist())

# Membuat slider untuk memilih rentang tahun pada plot line
slider_start_year_line = st.slider('Select Start Year', min_value=min_year, max_value=max_year, value=min_year, step=1)
slider_end_year_line = st.slider('Select End Year', min_value=min_year, max_value=max_year, value=max_year, step=1)

# Mengupdate plot line saat nilai dropdown atau slider berubah
def update_plot_line(attr, old, new):
    selected_area = select_area_line.value
    start_year = slider_start_year_line
    end_year = slider_end_year_line

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

# Membuat dropdown untuk memilih negara 1 pada plot korelasi
select_area_corr1 = Select(title="Area 1", value=df['Area'].unique()[0], options=df['Area'].unique().tolist())

# Membuat dropdown untuk memilih negara 2 pada plot korelasi
select_area_corr2 = Select(title="Area 2", value=df['Area'].unique()[1], options=df['Area'].unique().tolist())

# Membuat slider untuk memilih rentang tahun pada plot korelasi
slider_start_year_corr = st.slider('Select Start Year', min_value=min_year, max_value=max_year, value=min_year, step=1)
slider_end_year_corr = st.slider('Select End Year', min_value=min_year, max_value=max_year, value=max_year, step=1)

# Mengupdate plot korelasi saat nilai dropdown atau slider berubah
def update_plot_corr(attr, old, new):
    selected_area1 = select_area_corr1.value
    selected_area2 = select_area_corr2.value
    start_year = slider_start_year_corr
    end_year = slider_end_year_corr

    # Memfilter data sesuai dengan negara 1, negara 2, dan rentang tahun yang dipilih    
    filtered_data = df[((df['Area'] == selected_area1) | (df['Area'] == selected_area2)) & (df['Year'] >= start_year) & (df['Year'] <= end_year)]

    # Memperbarui data pada ColumnDataSource plot korelasi
    source_corr.data = filtered_data

    # Memperbarui label pada sumbu x dan y plot korelasi
    plot_corr.xaxis.axis_label = selected_area1
    plot_corr.yaxis.axis_label = selected_area2

    # Memperbarui judul plot korelasi
    plot_corr.title.text = f"Correlation Plot: {selected_area1} vs {selected_area2} - Year {start_year} to {end_year}"

select_area_corr1.on_change('value', update_plot_corr)
select_area_corr2.on_change('value', update_plot_corr)

# Menyusun layout menggunakan Streamlit
st.title("Data Visualization with Bokeh and Streamlit")

# Menampilkan plot line dan kontrolnya
line_layout = column(select_area_line, slider_start_year_line, slider_end_year_line, plot_line)

# Menampilkan plot korelasi dan kontrolnya
corr_layout = column(select_area_corr1, select_area_corr2, slider_start_year_corr, slider_end_year_corr, plot_corr)

# Mendapatkan komponen HTML dari plot line dan plot korelasi
line_script, line_div = components(line_layout)
corr_script, corr_div = components(corr_layout)

# Menampilkan komponen HTML pada Streamlit
st.components.v1.html(line_div + line_script)
st.components.v1.html(corr_div + corr_script)
