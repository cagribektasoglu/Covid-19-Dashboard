import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import folium
from streamlit_folium import folium_static
from datetime import datetime

def show_cases_page():
    # Veriyi yükle
    data = pd.read_csv('/workspaces/Covid-19-Dashboard/WHO-COVID-19-global-data.csv')
    coord_data = pd.read_csv('/workspaces/Covid-19-Dashboard/countries.csv')

    # Veriyi işleme
    data['Date_reported'] = pd.to_datetime(data['Date_reported'])
    latest_date = data['Date_reported'].max()
    last_month = latest_date - pd.DateOffset(days=30)
    prev_month = last_month - pd.DateOffset(days=30)

    # Ülkeleri listeleme
    countries = list(data['Country'].unique())
    countries.insert(0, 'All')  # 'All' seçeneğini ekle

    # Sol Panel - Ülkeler ve Filtreleme
    st.sidebar.header(f"Last Working Time: {latest_date.strftime('%d.%m.%Y %H:%M')}")
    selected_country = st.sidebar.selectbox("Select a country", countries)

    # Veriyi filtreleme
    if selected_country == 'All':
        filtered_data = data
        total_cases = data['Cumulative_cases'].max()
        total_deaths = data['Cumulative_deaths'].max()
        last_month_cases = data[data['Date_reported'] > last_month]['New_cases'].sum()
        last_month_deaths = data[data['Date_reported'] > last_month]['New_deaths'].sum()
        prev_month_cases = data[(data['Date_reported'] > prev_month) & (data['Date_reported'] <= last_month)]['New_cases'].sum()
        prev_month_deaths = data[(data['Date_reported'] > prev_month) & (data['Date_reported'] <= last_month)]['New_deaths'].sum()
    else:
        filtered_data = data[data['Country'] == selected_country]
        total_cases = filtered_data['Cumulative_cases'].max()
        total_deaths = filtered_data['Cumulative_deaths'].max()
        last_month_cases = filtered_data[filtered_data['Date_reported'] > last_month]['New_cases'].sum()
        last_month_deaths = filtered_data[filtered_data['Date_reported'] > last_month]['New_deaths'].sum()
        prev_month_cases = filtered_data[(filtered_data['Date_reported'] > prev_month) & (filtered_data['Date_reported'] <= last_month)]['New_cases'].sum()
        prev_month_deaths = filtered_data[(filtered_data['Date_reported'] > prev_month) & (filtered_data['Date_reported'] <= last_month)]['New_deaths'].sum()

    # Son ayın bir önceki ayla karşılaştırılması
    case_comparison = last_month_cases - prev_month_cases
    death_comparison = last_month_deaths - prev_month_deaths
    case_indicator = "🔼" if case_comparison > 0 else "🔽"
    death_indicator = "🔼" if death_comparison > 0 else "🔽"

    # Ortadaki kısım - Genel Bilgiler
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Cases", f"{total_cases:,}")
    col2.metric("Total Deaths", f"{total_deaths:,}")
    

    col4, col5, col6 = st.columns(3)
    col4.metric("Last Month Cases", f"{last_month_cases:,}", f"{case_comparison:,} {case_indicator}")
    col5.metric("Last Month Deaths", f"{last_month_deaths:,}", f"{death_comparison:,} {death_indicator}")


    # Sağdaki kısım - Grafikler
    st.subheader(f"{selected_country} Daily Statistics")
    daily_tab, monthly_tab = st.tabs(["Daily", "Monthly"])

    with daily_tab:
        daily_data = filtered_data.groupby('Date_reported').sum().reset_index()

        fig = go.Figure()

        fig.add_trace(go.Scatter(x=daily_data['Date_reported'], y=daily_data['New_cases'],
                        mode='lines',
                        name='New Cases',
                        line=dict(color='firebrick', width=2)))

        fig.add_trace(go.Scatter(x=daily_data['Date_reported'], y=daily_data['New_deaths'],
                        mode='lines',
                        name='New Deaths',
                        line=dict(color='royalblue', width=2)))

        fig.update_layout(title='Daily New Cases and Deaths',
                        xaxis_title='Date',
                        yaxis_title='Count')

        st.plotly_chart(fig, use_container_width=True)

    with monthly_tab:
        monthly_data = filtered_data.resample('M', on='Date_reported').sum().reset_index()

        fig = go.Figure()

        fig.add_trace(go.Scatter(x=monthly_data['Date_reported'], y=monthly_data['New_cases'],
                        mode='lines',
                        name='New Cases',
                        line=dict(color='firebrick', width=2)))

        fig.add_trace(go.Scatter(x=monthly_data['Date_reported'], y=monthly_data['New_deaths'],
                        mode='lines',
                        name='New Deaths',
                        line=dict(color='royalblue', width=2)))

        fig.update_layout(title='Monthly New Cases and Deaths',
                        xaxis_title='Date',
                        yaxis_title='Count')

        st.plotly_chart(fig, use_container_width=True)

    # Harita
    st.subheader("Global Covid-19 Map")

    # Harita için veri hazırlama
    map_data = data.groupby('Country').agg({
        'New_cases': 'sum',
        'New_deaths': 'sum',
        'Cumulative_cases': 'max',
        'Cumulative_deaths': 'max'
    }).reset_index()

    # Ülkelerin koordinatlarını birleştir
    map_data = map_data.merge(coord_data[['country', 'latitude', 'longitude', 'name']], left_on='Country', right_on='name', how='left')

    # Initialize the map centered around the geographical center of the world
    m = folium.Map(location=[0, 0], zoom_start=2, tiles='OpenStreetMap')

    # Add points to the map
    for _, row in map_data.iterrows():
        if pd.notna(row['latitude']) and pd.notna(row['longitude']):
            folium.CircleMarker(
                location=(row['latitude'], row['longitude']),
                radius=max(row['Cumulative_cases'] / 10000000, 2),  # Adjust radius based on cases
                color='crimson',
                fill=True,
                fill_color='crimson',
                fill_opacity=0.6,
                tooltip=(
                    f"Country: {row['Country']}<br>"
                    f"Total Cases: {row['Cumulative_cases']:,}<br>"
                    f"Last Month Cases: {data[(data['Country'] == row['Country']) & (data['Date_reported'] > last_month)]['New_cases'].sum():,}<br>"
                    f"Total Deaths: {row['Cumulative_deaths']:,}<br>"
                    f"Last Month Deaths: {data[(data['Country'] == row['Country']) & (data['Date_reported'] > last_month)]['New_deaths'].sum():,}"
                )
            ).add_to(m)

    # Display the map
    folium_static(m)

# streamlit_app.py içeriği
if __name__ == "__main__":
    show_cases_page()
