import streamlit as st

# Başlık
st.title("Welcome To Covid-19 Dashboard!")

# Alt Başlık
st.header("Covid-19: A Turning Point and a Scientific Journey")

# Yan Panel - Menü
st.sidebar.title("Navigation")
menu = st.sidebar.selectbox("Menu", ["Home", "Cases", "Vaccinations", "Testing", "Hospitalization", "Excess Mortality", "Mortality Risk", "Pandemic Foresight", "Summary"])

# Sayfa Dosyalarını İçe Aktarma ve Menüye Göre Yönlendirme
if menu == "Cases":
    import Cases
    Cases.show_cases_page()
elif menu == "Vaccinations":
    import Vaccinations
    Vaccinations.show_vaccinations_page()
elif menu == "Testing":
    import testing
    testing.show_testing_page()
elif menu == "Hospitalization":
    import hospitalization
    hospitalization.show_hospitalization_page()
elif menu == "Excess Mortality":
    import excess_mortality
    excess_mortality.show_excess_mortality_page()
elif menu == "Mortality Risk":
    import mortality_risk
    mortality_risk.show_mortality_risk_page()
elif menu == "Pandemic Foresight":
    import pandemic_foresight
    pandemic_foresight.show_pandemic_foresight_page()
elif menu == "Summary":
    import summary
    summary.show_summary_page()
else:
    st.write("""
    Covid-19: A Turning Point and a Scientific Journey
    At the beginning of 2020, the world changed unexpectedly. A virus that emerged in Wuhan, China, and spread rapidly, upended the lives of all humanity. This disease, named Covid-19, quickly spread to all corners of the globe, crossing borders and confining everyone to their homes, emptying streets, and fundamentally altering our habits. People stayed away from their loved ones, schools closed, and workplaces fell silent. This period was a challenging, uncertain, and emotionally exhausting experience for all of us.

    However, humanity's darkest moments often bring forth the brightest sparks of hope. The pandemic was not just a health crisis but also a story of solidarity and the triumph of science. While healthcare workers fought tirelessly on the front lines, scientists worked day and night to understand and control the virus. The World Health Organization (WHO) and other international health organizations provided a continuous flow of information, keeping us informed during this challenging time.

    The Covid-19 pandemic has once again highlighted the vital importance of modern medicine, data analysis, and scientific research. During this period, the accurate and effective analysis of data played a critical role in the measures and strategies to be taken. The official data from the World Health Organization became one of the most reliable sources for tracking and understanding the course of the pandemic.

    This study aims to visualize Covid-19 data to understand the global impacts of the pandemic. This data visualization platform, prepared with official data from the World Health Organization, aims to present detailed information on the pandemic's progression, including case numbers, recoveries, fatalities, and vaccination rates. The goal is to evaluate the past and provide a scientifically-based resource to help us be better prepared for similar crises in the future.

    Data visualization is a powerful tool that makes complex information easier to understand. In this context, this platform aims to provide a valuable resource for the public, academics, and policymakers by presenting the dynamics and impacts of Covid-19 in a clear and accessible manner. We hope that this study will contribute to a better understanding of the challenges brought by the pandemic and help build a stronger and more resilient society for the future.

    This study was conducted as a graduation project in the data visualization category by Çağrı Bektaşoğlu, in the Department of Computer Engineering at Çukurova University, using Python and Streamlit.
    """)
