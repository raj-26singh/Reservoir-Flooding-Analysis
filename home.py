import streamlit as st
import warnings
warnings.filterwarnings("ignore")

import water_flooding

def home():
     
    
    
    

    #st.write('\n')
    st.header('Sections')
    st.subheader('Individual Well Analysis')
    st.write('**Home:** A brief description of the web app.')
    st.write('**Visualizer:** For data visualization')
    st.write('**Correlate:** For data correlation')
    st.write('**Data Entry:** For creating a new data entry into the well ABH dataset')
    st.subheader('Field Analysis')
    st.write('**Home:** A brief description of the web app.')
    st.write('**Well Pad Analysis:** Analysis of each well, well-pad wise.')
    st.write('**Overall Field Analysis:** Overall Analysis of the field by selection of multiple wells')
    st.write('**GOR-Based Field Analysis:** GOR-Based Analysis of the field by High, Moderate, Low and Very Low GOR Wells')
    st.write('**Workover/RRU Analysis:** Analysis of Workovers/RRUs of the wells of the ABH field')
    st.write('**Well Wise Visualisation:** Visualise each well of the field')
    st.subheader('           - Created by: Raj Kumar Singh and Shubham Dobliyal')

    
    '''st.write('\n')
    st.header('Well Parameters')
    st.write("1. Porosity = 24 %")
    st.write("2. Permeability = 1 mD")
    st.write("3. Initial Reservoir Pressure = 1510 psi")
    st.write("4. Initial Reservoir Temperature = 64 deg")
    st.write('\n')
    st.header('Fluid Parameters')
    st.write("1. Oil API = 30 deg API")
    st.write("2. Viscosity = 3 cp")
    st.write("3. Bubble Point = 1450 psi")    
    st.write('\n')'''
    