import streamlit as st

st.set_page_config(
    page_title="MADS Capstone Project",
    page_icon="🏠",
)


# Display the image with the custom class
st.image("photo_1.png", use_column_width='auto')

st.markdown("""
    <div style="text-align: center;">
        <h1>Airbnb Price Prediction</h1>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div style="text-align: center;">
        Unlock your Airbnb potential with pricing strategy. <br> Our new app offers a solution for Airbnb hosts to predict prices based on your property’s characteristics.
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div style="text-align: center;">
        <hr style="width: 100%; border-top: 2px solid #ccc;">
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div style="text-align: center;">
        SIADS 699 | Team 14: Big House <br> Sam Kobrin, Sachiko Uchikoshi, Alex Chan <br> - 2024 August -
    </div>
""", unsafe_allow_html=True)



st.sidebar.success("Select a page above.")