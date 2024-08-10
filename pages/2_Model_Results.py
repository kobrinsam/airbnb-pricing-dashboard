import streamlit as st
import sys
import os
st.set_option('deprecation.showPyplotGlobalUse', False)

# Add the parent directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", 'Plots')))

# Import functions from model_result_plots.py
from model_result_plots import plot_model_performance, plot_feature_importance

st.title('Model Performance')

fig1 = plot_model_performance()
st.pyplot(fig1)

st.title('Feature Performance')

fig2 = plot_feature_importance()
st.pyplot(fig2)