import pandas as pd
import streamlit as st
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.layouts import row
from bokeh.models.widgets import Select, Slider

# Membaca data
df = pd.read_csv('dataset2.csv')

# Membuat ColumnDataSource awal
source = ColumnDataSource(data=df)

# Membuat plot awal
plot = figure(title='Dataset Visualization',x_axis_label='Year', y_axis_label='Value',plot_height=400, plot_width=600)

# Membuat glyph Line
line = plot.line(x='Year', y='Value', source=source, line_width=2)

# Membuat tooltips untuk HoverTool
hover_tool = HoverTool(tooltips=[('Area', '@Area'), ('Year', '@Year'), ('Value', '@Value')])

# Menambahkan tooltips ke plot
plot.add_tools(hover_tool)

# Membuat dropdown untuk memilih area
select_area = Select(title="Area", value=df['Area'].unique()[0], options=df['Area'].unique().tolist())

# Membuat slider untuk memilih tahun
slider_year = Slider(title="Year", start=df['Year'].min(),end=df['Year'].max(), value=df['Year'].min(), step=1)

# Mengupdate ColumnDataSource dan plot saat nilai dropdown atau slider berubah
def update_data(attr, old, new):
    selected_area = select_area.value
    selected_year = slider_year.value

    # Memfilter data sesuai dengan area dan tahun yang dipilih
    filtered_data = df[(df['Area'] == selected_area) & (df['Year'] == selected_year)]

    # Memperbarui data pada ColumnDataSource
    source.data = ColumnDataSource(filtered_data).data

    # Memperbarui label pada sumbu x dan y
    plot.xaxis.axis_label = 'Year'
    plot.yaxis.axis_label = 'Value'

    # Memperbarui judul plot
    plot.title.text = f"Data for {selected_area} - Year {selected_year}"

# Membuat daftar negara yang tersedia untuk dropdown
available_areas = df['Area'].unique().tolist()

# Membuat dictionary untuk menyimpan plot berdasarkan negara
plots = {}

# Membuat plot untuk setiap negara
for area in available_areas:
    filtered_data = df[df['Area'] == area]
    plots[area] = figure(title=f"Data for {area}",x_axis_label='Year', y_axis_label='Value',plot_height=400, plot_width=600)
    plots[area].line(x='Year', y='Value', source=ColumnDataSource(filtered_data), line_width=2)
    plots[area].add_tools(hover_tool)

# Mengupdate plot yang ditampilkan saat nilai dropdown berubah
def update_plot(attr, old, new):
    selected_area = select_area.value

    # Memperbarui plot yang ditampilkan
    plot_layout.children[1] = plots[selected_area]

select_area.on_change('value', update_plot)
slider_year.on_change('value', update_data)

# Menyusun layout
plot_layout = row(select_area, slider_year, plot)

# Menampilkan plot pertama kali saat halaman dibuka
update_data(None, None, None)

# Menampilkan plot dan widget pada halaman Streamlit
st.bokeh_chart(plot_layout)
