import pandas as pd
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource
import streamlit as st

# Membaca data
df = pd.read_csv('dataset2.csv')

# Membuat plot line awal
plot_line = figure(title='Dataset Visualization', x_axis_label='Year', y_axis_label='Value', plot_height=400, plot_width=600)
hover_tool_line = HoverTool(tooltips=[('Area', '@Area'), ('Year', '@Year'), ('Value', '@Value')])
plot_line.add_tools(hover_tool_line)

# Membuat dropdown untuk memilih area pada plot line
select_area_line = st.selectbox("Area", df['Area'].unique())

# Membuat slider untuk memilih rentang tahun pada plot line
min_year = int(df['Year'].min())
max_year = int(df['Year'].max())
start_year = st.slider("Start Year", min_value=min_year, max_value=max_year, value=min_year)
end_year = st.slider("End Year", min_value=start_year, max_value=max_year, value=max_year)

# Memfilter data sesuai dengan area dan rentang tahun yang dipilih
filtered_data_line = df[(df['Area'] == select_area_line) & (df['Year'] >= start_year) & (df['Year'] <= end_year)]

# Membuat ColumnDataSource untuk plot line
source_line = ColumnDataSource(data=filtered_data_line)

# Memperbarui label pada sumbu x dan y plot line
plot_line.xaxis.axis_label = 'Year'
plot_line.yaxis.axis_label = 'Value'

# Memperbarui judul plot line
plot_line.title.text = f"Data for {select_area_line} - Year {start_year} to {end_year}"

# Menampilkan plot line
plot_line.line(x='Year', y='Value', source=source_line, line_width=2)
st.bokeh_chart(plot_line)

# Membaca dropdown untuk memilih negara 1 pada plot korelasi
select_area_corr1 = st.selectbox("Area 1", df['Area'].unique())

# Membaca dropdown untuk memilih negara 2 pada plot korelasi
select_area_corr2 = st.selectbox("Area 2", df['Area'].unique())

# Membaca slider untuk memilih rentang tahun pada plot korelasi
start_year_corr = st.slider("Start Year (Correlation)", min_value=min_year, max_value=max_year, value=min_year)
end_year_corr = st.slider("End Year (Correlation)", min_value=start_year_corr, max_value=max_year, value=max_year)

# Memfilter data sesuai dengan negara 1, negara 2, dan rentang tahun yang dipilih    
filtered_data_corr = df[((df['Area'] == select_area_corr1) | (df['Area'] == select_area_corr2)) & (df['Year'] >= start_year_corr) & (df['Year'] <= end_year_corr)]

# Membuat ColumnDataSource untuk plot korelasi
source_corr = ColumnDataSource(data=filtered_data_corr)

# Membuat plot korelasi
plot_corr = figure(title='Correlation Plot', x_axis_label=select_area_corr1, y_axis_label=select_area_corr2, plot_height=400, plot_width=600)
hover_tool_corr = HoverTool(tooltips=[('Area', '@Area'), ('Year', '@Year'), ('Value', '@Value')])
plot_corr.add_tools(hover_tool_corr)

# Memperbarui judul plot korelasi
plot_corr.title.text = f"Correlation Plot: {select_area_corr1} vs {select_area_corr2} - Year {start_year_corr} to {end_year_corr}"

# Menampilkan plot korelasi
plot_corr.circle(x='Value', y='Value', source=source_corr, size=8, color='navy', alpha=0.5)
st.bokeh_chart(plot_corr)
