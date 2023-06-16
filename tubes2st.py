import streamlit as st
import pandas as pd
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.layouts import column, row
from bokeh.models import Select, Slider

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
select_area_line = st.selectbox("Area", df['Area'].unique())

# Membuat slider untuk memilih rentang tahun pada plot line
start_year = st.slider("Start Year", min_value=min_year, max_value=max_year, value=min_year, step=1)
end_year = st.slider("End Year", min_value=min_year, max_value=max_year, value=max_year, step=1)

# Mengupdate plot line saat nilai dropdown atau slider berubah
def update_plot_line():
    selected_area = select_area_line
    filtered_data = df[(df['Area'] == selected_area) & (df['Year'] >= start_year) & (df['Year'] <= end_year)]
    source_line.data = filtered_data
    plot_line.title.text = f"Data for {selected_area} - Year {start_year} to {end_year}"
    st.bokeh_chart(plot_line)

update_plot_line()

# Membuat dropdown untuk memilih negara 1 pada plot korelasi
select_area_corr1 = st.selectbox("Area 1", df['Area'].unique())

# Membuat dropdown untuk memilih negara 2 pada plot korelasi
select_area_corr2 = st.selectbox("Area 2", df['Area'].unique())

# Mengupdate plot korelasi saat nilai dropdown atau slider berubah
def update_plot_corr():
    selected_area1 = select_area_corr1
    selected_area2 = select_area_corr2
    filtered_data = df[((df['Area'] == selected_area1) | (df['Area'] == selected_area2)) &
                       (df['Year'] >= start_year) &
                       (df['Year'] <= end_year)]
    source_corr.data = filtered_data
    plot_corr.xaxis.axis_label = selected_area1
    plot_corr.yaxis.axis_label = selected_area2
    plot_corr.title.text = f"Correlation Plot: {selected_area1} vs {selected_area2} - Year {start_year} to {end_year}"
    st.bokeh_chart(plot_corr)

update_plot_corr()
