import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Veri çekme fonksiyonu
@st.cache_data
def load_vaccination_data():
    url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv'
    data = pd.read_csv(url)
    data['date'] = pd.to_datetime(data['date'])
    return data

# Verileri yükle
vaccination_data = load_vaccination_data()

def show_vaccinations_page():
    st.title("Covid-19 Vaccination Dashboard")

    # Sol panelde ülke seçimi
    countries = sorted(vaccination_data['location'].unique().tolist())
    countries.insert(0, 'All')
    selected_country = st.sidebar.selectbox("Select a country", countries)

    # Ülkeye göre verileri filtreleme
    if selected_country == 'All':
        filtered_data = vaccination_data
    else:
        filtered_data = vaccination_data[vaccination_data['location'] == selected_country]

    latest_date = filtered_data['date'].max()
    filtered_data_latest = filtered_data[filtered_data['date'] == latest_date]

    total_vaccinations = filtered_data['daily_vaccinations'].sum()
    people_vaccinated = filtered_data_latest['people_vaccinated'].sum()
    people_fully_vaccinated = filtered_data_latest['people_fully_vaccinated'].sum()
    daily_vaccinations_avg = filtered_data['daily_vaccinations'].mean()
    people_vaccinated_per_hundred = filtered_data_latest['people_vaccinated_per_hundred'].mean()
    people_fully_vaccinated_per_hundred = filtered_data_latest['people_fully_vaccinated_per_hundred'].mean()
    daily_vaccinations_per_million_avg = filtered_data['daily_vaccinations_per_million'].mean()
    daily_people_vaccinated_per_hundred_avg = filtered_data['daily_people_vaccinated_per_hundred'].mean()

    # Ortadaki kısım - Genel Bilgiler
    col1, col2, col3 = st.columns(3)
    col1.metric("People Vaccinated", f"{people_vaccinated:,}")
    col2.metric("People Fully Vaccinated", f"{people_fully_vaccinated:,}")
    col3.metric("Total Vaccinations", f"{total_vaccinations:,}")

    col4, col5, col6 = st.columns(3)
    col4.metric("Daily Vaccinations (Avg)", f"{daily_vaccinations_avg:.2f}")
    col5.metric("People Vaccinated Per Hundred", f"{people_vaccinated_per_hundred:.2f}")
    col6.metric("People Fully Vaccinated Per Hundred", f"{people_fully_vaccinated_per_hundred:.2f}")

    col7, col8 = st.columns(2)
    col7.metric("Daily Vaccinations Per Million (Avg)", f"{daily_vaccinations_per_million_avg:.2f}")
    col8.metric("Daily People Vaccinated Per Hundred (Avg)", f"{daily_people_vaccinated_per_hundred_avg:.2f}")

    # Aşılanan Kişi Sayısı (people_vaccinated): Zaman Serisi Grafik
    st.subheader(f"{selected_country} - People Vaccinated Over Time")
    fig1 = px.line(filtered_data, x='date', y='people_vaccinated', title='People Vaccinated Over Time')
    st.plotly_chart(fig1, use_container_width=True)

    # Tamamen Aşılanan Kişi Sayısı (people_fully_vaccinated): Donut Chart
    st.subheader(f"{selected_country} - People Fully Vaccinated")
    fig2 = go.Figure(data=[go.Pie(labels=['Fully Vaccinated', 'Not Fully Vaccinated'],
                                  values=[people_fully_vaccinated, total_vaccinations - people_fully_vaccinated],
                                  hole=.3)])
    st.plotly_chart(fig2, use_container_width=True)

    # Günlük Aşı Sayısı (daily_vaccinations): Line+Bar Chart
    st.subheader(f"{selected_country} - Daily Vaccinations")
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(x=filtered_data['date'], y=filtered_data['daily_vaccinations'], name='Daily Vaccinations', marker_color='blue'))
    fig3.add_trace(go.Scatter(x=filtered_data['date'], y=filtered_data['daily_vaccinations'], name='Trend', line=dict(color='red')))
    fig3.update_layout(title='Daily Vaccinations', xaxis_title='Date', yaxis_title='Daily Vaccinations')
    st.plotly_chart(fig3, use_container_width=True)

    # Nüfusa Oranla Aşılanan Kişi Sayısı (people_vaccinated_per_hundred): Scatter Plot with Trend Line
    st.subheader(f"{selected_country} - People Vaccinated Per Hundred Over Time")
    fig4 = px.scatter(filtered_data, x='date', y='people_vaccinated_per_hundred', trendline="ols",
                      title='People Vaccinated Per Hundred Over Time')
    st.plotly_chart(fig4, use_container_width=True)

    # Nüfusa Oranla Tamamen Aşılanan Kişi Sayısı (people_fully_vaccinated_per_hundred): Gantt Chart
    st.subheader(f"{selected_country} - People Fully Vaccinated Per Hundred Over Time")
    fig5 = px.timeline(filtered_data, x_start='date', x_end='date', y='people_fully_vaccinated_per_hundred',
                       title='People Fully Vaccinated Per Hundred Over Time')
    st.plotly_chart(fig5, use_container_width=True)

    # Günlük Aşı Sayısı (daily_vaccinations_per_million): Sunburst Chart
    st.subheader(f"{selected_country} - Daily Vaccinations Per Million")
    fig6 = px.sunburst(filtered_data, path=['location'], values='daily_vaccinations_per_million',
                       title='Daily Vaccinations Per Million by Continent and Country')
    st.plotly_chart(fig6, use_container_width=True)

    # Milyon Kişi Başına Günlük Aşı Sayısı (daily_vaccinations_per_million): Heatmap
    st.subheader(f"{selected_country} - Daily Vaccinations Per Million Over Time")
    fig7 = px.density_heatmap(filtered_data, x='date', y='location', z='daily_vaccinations_per_million',
                              title='Daily Vaccinations Per Million Over Time')
    st.plotly_chart(fig7, use_container_width=True)

    # Günlük Aşılanan Kişi Sayısı (daily_people_vaccinated): Treemap
    st.subheader(f"{selected_country} - Daily People Vaccinated")
    fig8 = px.treemap(filtered_data, path=['location'], values='daily_people_vaccinated',
                      title='Daily People Vaccinated by Continent and Country')
    st.plotly_chart(fig8, use_container_width=True)

    # İnteraktif Harita (Choropleth Map)
    st.subheader("Global Vaccination Map")
    fig_map = go.Figure(data=go.Choropleth(
        locations=filtered_data['iso_code'],
        z=filtered_data['total_vaccinations'],
        text=filtered_data['location'],
        colorscale='Blues',
        autocolorscale=False,
        reversescale=True,
        marker_line_color='darkgray',
        marker_line_width=0.5,
        colorbar_title='Total Vaccinations',
    ))

    fig_map.update_layout(
        title_text='Total Vaccinations by Country',
        geo=dict(
            showcoastlines=True,
            projection_type='equirectangular'
        ),
    )

    st.plotly_chart(fig_map, use_container_width=True)

# Uygulamayı Çalıştırma
if __name__ == "__main__":
    st.sidebar.title("Navigation")
    menu = st.sidebar.radio("Go to", ["Home", "Vaccinations"])
    if menu == "Vaccinations":
        show_vaccinations_page()
