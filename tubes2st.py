import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.layouts import column, row
from bokeh.models.widgets import Select, Slider
import streamlit as st

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
select_area_line = st.selectbox("Area", df['Area'].unique().tolist())

# Membuat slider untuk memilih rentang tahun pada plot line
start_year_line = st.slider("Start Year", min_value=min_year, max_value=max_year, value=min_year, step=1)
end_year_line = st.slider("End Year", min_value=min_year, max_value=max_year, value=max_year, step=1)

# Mengupdate plot line saat nilai dropdown atau slider berubah
def update_plot_line():
    selected_area = select_area_line
    start_year = start_year_line
    end_year = end_year_line

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
    update_plot_corr()

# Membuat dropdown untuk memilih negara 1 pada plot korelasi
select_area_corr1 = st.selectbox("Area 1", df['Area'].unique().tolist())

# Membuat dropdown untuk memilih negara 2 pada plot korelasi
select_area_corr2 = st.selectbox("Area 2", df['Area'].unique().tolist())

# Membuat slider untuk memilih rentang tahun pada plot korelasi
start_year_corr = st.slider("Start Year", min_value=min_year, max_value=max_year, value=min_year, step=1)
end_year_corr = st.slider("End Year", min_value=min_year, max_value=max_year, value=max_year, step=1)

# Mengupdate plot korelasi saat nilai dropdown atau slider berubah
def update_plot_corr():
    selected_area1 = select_area_corr1
    selected_area2 = select_area_corr2
    start_year = start_year_corr
    end_year = end_year_corr

    # Memfilter data sesuai dengan negara 1, negara 2, dan rentang tahun yang dipilih
    filtered_data = df[((df['Area'] == selected_area1) | (df['Area'] == selected_area2)) &
                       (df['Year'] >= start_year) &
                       (df['Year'] <= end_year)]

    # Memperbarui data pada ColumnDataSource plot korelasi
    source_corr.data = filtered_data

    # Memperbarui label pada sumbu x dan y plot korelasi
    plot_corr.xaxis.axis_label = selected_area1
    plot_corr.yaxis.axis_label = selected_area2

    # Memperbarui judul plot korelasi
    plot_corr.title.text = f"Correlation Plot: {selected_area1} vs {selected_area2} - Year {start_year} to {end_year}"

# Memperbarui plot line saat nilai dropdown atau slider berubah
update_plot_line()

# Memperbarui plot korelasi saat nilai dropdown atau slider berubah
update_plot_corr()

# Menyusun layout
layout = column(
    row(select_area_line, start_year_line, end_year_line),
    row(plot_line),
    row(select_area_corr1, select_area_corr2, start_year_corr, end_year_corr),
    row(plot_corr)
)

# Menampilkan layout di Streamlit
st.bokeh_chart(layout, use_container_width=True)
