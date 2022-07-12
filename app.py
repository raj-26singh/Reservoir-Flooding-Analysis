import pandas as pd
import numpy as np
import streamlit as st
import warnings
warnings.filterwarnings("ignore")

#import home
import water_flooding


st.info(""" Flooding Breakthrough Analysis """)

st.write('### Introdction to the interface')

st.write('''Waterflood is a secondary enhanced oil recovery process used to maintain the reservoir pressure,
thus providing energy to the reservoir and improving its recovery by displacing the previously
bypassed or the residual oil. Reservoir heterogeneities in reservoirs in the form of channels and
fractures leads to decrease in the efficiency of the waterflood and can cause early breakthrough
of water in the production wells.
In this project, the relative permeability curve, fractional flow curve, saturation profile and the
recovery plot were plotted by employing various mathematical tools such as
Multi-phase Conservation Equation, Fractional Flow theory, Buckley-Leverett Analysis.''')
st.write('\n')

if st.checkbox('Flooding Breakthrough Analysis'):
    
    
    st.title('Conduct Flooding Breakthrough Analysis')

    st.sidebar.write("## Please Select the type of flooding ")

    option = st.sidebar.radio('',  ['Water Flooding', 'Polymer Flooding'])

    if option == 'Water Flooding':
        st.info(""" Flooding Breakthrough Analysis """)
        water_flooding.water_flooding()
        