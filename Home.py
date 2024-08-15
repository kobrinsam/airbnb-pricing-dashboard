import streamlit as st

st.set_page_config(
    page_title="MADS Capstone Project",
    page_icon="🏠",
)


# Display the image with the custom class
st.image("images/photo_1.png", use_column_width=True)

st.markdown("""
    <div style="text-align: center;">
        Unlock your Airbnb's potential with a listing price strategy. <br> Our new app offers a solution for Airbnb hosts to predict prices based on your property’s characteristics.
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div style="text-align: center;">
        <hr style="width: 100%; border-top: 2px solid #ccc;">
    </div>
""", unsafe_allow_html=True)

st.subheader("Motivation")
st.write("As platforms like Airbnb and VRBO have grown in popularity, hosting has become a common way to make additional income. However, setting the right price for a property can be difficult. Each listing is unique, affected by factors like location, amenities, and the number of bedrooms and bathrooms. Additionally, demand fluctuates with the day of the week, peak seasons, weather conditions, and holidays. Although tools such as AirDNA can help with pricing, they often involve sharing personal information, which can be a privacy concern. We aimed to develop an open-source tool that allows Airbnb hosts to estimate listing prices based on their property's attributes while ensuring privacy is preserved.")

st.subheader("Markets")
st.write("Albany, NY; New York City, NY; Chicago, IL; Los Angeles, CA; San Francisco, CA; Seattle, WA; Washington, D.C.")

st.subheader("Features")
st.markdown("- Interactive dashboard with user inputs for listing details.")
st.markdown("- Price prediction using a trained machine learning model.")
st.markdown("- Map visualization to select the potential Airbnb listing price.")

st.subheader("How to use")
st.markdown("- Go to **Price Prediction** page.  Enter the details of your Airbnb listing.")
st.markdown("- The dashboard will display the predicted list price for your Airbnb listing.")
st.markdown("- Leverage the insights provided to strategically set your listing price.")

st.subheader("Additional Resources")
st.markdown(
    """
    A [full report](https://docs.google.com/document/d/1MaAcnBMZyobaA8xIv-hmPaDRzPohxaQikKjxP2Gtrk8/edit?usp=sharing)and [GitHub repo](https://github.com/kobrinsam/airbnb-pricing-dashboard) are available alongside this app.
    """
)



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