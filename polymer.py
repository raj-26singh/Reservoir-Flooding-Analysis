from math import ceil
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import streamlit as st
import warnings
warnings.filterwarnings("ignore")
import pandas as pd


def polymer():
    st.header("Polymer Flooding")
    st.write("Please enter the values of the following parameters :")
    
    # Input Variables

    Swc = st.number_input('Swc :', min_value=0.0, max_value=1.0, value=0.1, step=0.01)
    Sorw = st.number_input('Sorw :', min_value=0.0, max_value=1.0, value=0.2, step=0.01)
    Krwiro = st.number_input('Krwiro :', min_value=0.0, max_value=1.0, value=0.6, step=0.01)
    Krocw = st.number_input('Krocw :', min_value=0.0, max_value=1.0, value=0.92, step=0.01)
    Nw = st.number_input('Nw :', value=2.5)
    No = st.number_input('Nw :', value=6.0)
    uw = st.number_input('Viscosity of Water (in cp) :', value=0.5)
    uo = st.number_input('Viscosity of Oil (in cp) :', value=17.0)
    up = st.number_input('Viscosity of Polymer Solution (in cp) :', value=10.0)
    di = st.number_input('Retardation Factor (Di) :', value=1.02)
    area = st.number_input('Area (in sq. feets) :', value=1.0*(10**6))
    L = st.number_input('L (in feet) :', value=100.0)
    phi = st.number_input('Porosity :', value=0.2)
    qt = st.number_input('Constant injection rate (SCFD) :', value=20000.0)
    
    # Assumed Parameters
    
    Sw = (np.linspace(100,850,num=751))/1000.0
    Sw = np.flipud(Sw)
    sat = np.copy(Sw)
    
    # Calculations

    # Relative Permeabilities
    
    kro = Krocw*(((1.0-Sw-Sorw)/(1.0-Swc-Sorw))**No)
    krw = Krwiro*(((Sw-Swc)/(1.0-Swc-Sorw))**Nw)

# Potha
    st.write("## Relative Permeability")
    st.write("For each saturation, relative permeability to water and oil were calculated by using Corey’s Model. The formulae forthe Corey’s Model is as follows:")
    col1, col2, col3 = st.beta_columns([1,2,1])
    with col1:
        st.write("")
    with col2:
        st.image("images/coreys formula.jpg")  
    with col3:
        st.write("")  
    st.write("Relative permeability is the ratio of effective permeability of a particular fluid at a particular saturation to absolute permeability of that fluid at total saturation. If a single fluid is present in a rock, its relative permeability is 1.0. Calculation of relative permeability is of vital significance as it allows comparison of the different abilities of fluids to flow in the presence of each other, since the presence of more than one fluid generally inhibits flow. Accurate predictions of three-phase oil relative permeabilities are required for a variety of petroleum processes and ground water pollution problems. Simultaneous flow of water-gas-oil mixtures are encountered in petroleum reservoirs producing under primary, secondary, and tertiary processes. Enhanced oil recovery methods such as thermal recovery, carbon dioxide immiscible displacement, or any gas injection process generates simultaneous flow of three phases.")
    
    # Plotting the relative permeability curves
    
    fig_perm = make_subplots(specs=[[{"secondary_y": True}]])
    fig_perm.add_trace(go.Line(x=np.insert(np.append(Sw,0),0,1.0), y=np.insert(np.append(kro,kro[-1]),0,0.0),name="Relative Permeability of Oil (kro)"),secondary_y=False,)
    fig_perm.add_trace(go.Line(x=np.insert(np.append(Sw,0),0,1.0), y=np.insert(np.append(krw,0.0),0,krw[0]),name="Relative Permeability of Water (krw)"),secondary_y=True,)
    fig_perm.update_yaxes(title_text="<b>Relative Permeability of Oil (kro)</b>", secondary_y=False, range=[0.0,1.0],nticks=20)
    fig_perm.update_yaxes(title_text="<b>Relative Permeability of Water (krw)</b>", secondary_y=True, range=[0.0,1.0],nticks=20)
    fig_perm.update_xaxes(title_text="<b>Water Saturation (Sw)</b>",range=[0.0,1.0],nticks=20)
    fig_perm.update_layout(title={'text':"<b>Relative Permeability Curves<b>",'x':0.48,'y':0.85},legend=dict(x=0.25,y=-0.39))
    st.plotly_chart(fig_perm, use_container_width=True)
    
    # Mobility Ratio
    
    M_water = (krw/uw)/(kro/uo)
    M_polymer = (krw/up)/(kro/uo)


    # Fractional flow of water
    
    fw_water = 1.0/(1.0+(1.0/M_water))
    fw_polymer = 1.0/(1.0+(1.0/M_polymer))
    
    pos_w = 0
    pos_p = 0
    for f in range(len(fw_water)):
        #st.write("fw:",fw[f])
        if fw_water[f]<0.999999:
            #st.write("fw:",fw[f],"f:",f)
            pos_w = f
            break
    for f in range(len(fw_polymer)):
        #st.write("fw:",fw[f])
        if fw_polymer[f]<0.999999:
            #st.write("fw:",fw[f],"f:",f)
            pos_p = f
            break
                
    #st.write(pos)
    
    delfw_delSw_water = (fw_water-0.0)/(Sw+di)
    delfw_delSw_polymer = (fw_polymer-0.0)/(Sw+di)

    dfw_dSw_water = np.insert(((np.diff(fw_water,n=1))/np.diff(Sw,n=1)),0,delfw_delSw_water[0],axis=0)            #no need
    dfw_dSw_polymer = np.insert(((np.diff(fw_polymer,n=1))/np.diff(Sw,n=1)),0,delfw_delSw_polymer[0],axis=0)
    
    diff = abs(dfw_dSw_polymer-delfw_delSw_polymer)           
    diff_w = abs(dfw_dSw_water-delfw_delSw_water)            #no need

    min_index = 5 + np.argmin(diff[5:(len(Sw)-5)])
    min_index_w = 5 + np.argmin(diff_w[5:(len(Sw)-5)])          #no need
    SwBT = Sw[min_index]
    
    st.write("")
    st.write("## Fractional Flow")
    st.write("Fractional flow theory has been a very important tool with wide applications in understanding and validation of various reservoir simulation and numerical models. It still has been applied in understanding the mechanisms of various Chemical-Enhanced Oil Recovery (CEOR) process and for the purposes of interpreting the transport behaviour of various chemicals in porous and permeable media.")
    st.write("For a 1D incompressible , two phase flow, the fractional flow equation is stated as follows:") 
    col1, col2, col3 = st.beta_columns([1,6,1])
    with col1:
        st.write("")
    with col2:
        st.image("images/fractional_3.jpg")    
    with col3:
        st.write("")   
    st.write("First term is the advection term which basically symbolizes the flow rate that is going with the flow. The second term is the flow rate of water due to capillary pressure effects and third one is due to gravity or buoyancy effects.") 
    st.write("In case of waterflooding, the advection term dominated here while the gravity and capillary terms are neglected. So,")  
    col1, col2, col3 = st.beta_columns([1,1,1])
    with col1:
        st.write("")
    with col2:
        st.image("images/fractional.jpg")    
    with col3:
        st.write("")  
    st.write("Now, fractional flow of water is defined as the ratio of flow rate of water with respect to the total flow rate. Therefore,")
    col1, col2, col3 = st.beta_columns([1,3,1])
    with col1:
        st.write("")
    with col2:
        st.image("images/fractional_2.jpg")    
    with col3:
        st.write("") 
         
    '''x_val = np.copy(sat)
    y_val = (x_val-np.repeat(Swc,len(Sw)))*dfw_dSw[min_index]
    x_plot_val = [u for u,v in zip(x_val,y_val) if (v>=0 and u<=1 and v<=1)]
    y_plot_val = [v for u,v in zip(x_val,y_val) if (v>=0 and u<=1 and v<=1)]'''
    
    #st.write(pd.DataFrame({"x":x_plot_val,"y":y_plot_val}))
    # Plotting the fractional flow curve
    
    fig_fw = make_subplots(specs=[[{"secondary_y": True}]])
    fig_fw.add_trace(go.Line(x=Sw[pos_w:], y=fw_water[pos_w:],name="Fractional Flow Curve of Water"),secondary_y=False,)
    fig_fw.add_trace(go.Line(x=Sw[pos_p:], y=fw_polymer[pos_p:],name="Fractional Flow Curve of Polymer"),secondary_y=True,)
    fig_fw.update_yaxes(title_text="<b>Fractional Flow of water (fw)</b>",range=[0.0,1.0],nticks=20,secondary_y=False,)
    fig_fw.update_yaxes(title_text="<b>Fractional Flow of polymer (fp)</b>",range=[0.0,1.0],nticks=20,secondary_y=True,)
    fig_fw.update_xaxes(title_text="<b>Water Saturation (Sw)</b>",range=[0.0,1.0],nticks=20)
    fig_fw.update_layout(title={'text':"<b>Fractional Flow Curves<b>",'x':0.48,'y':0.85},legend=dict(x=0.25,y=-0.39))
    st.plotly_chart(fig_fw, use_container_width=True)
    
    st.write("## Buckley-Leverett Theory")
    st.write("Buckley- Leverett Theory is widely used for the evaluating the movement of a fluid displacing front for an immiscible displacement process in a porous media. The theory is based on the fractional flow theory and made use of the following assumptions to estimate the rate of injected fluid bank movement :-")
    st.write("• Linear and horizontal 1D flow")
    st.write("• Water is used as the injected fluid in the oil reservoir")
    st.write("• Both oil and water are incompressible in nature")
    st.write("• Both oil and water are immiscible with one another")
    st.write("• Capillary and gravity pressure effects are neglected")
    st.write("Mathematically, using Buckley Leverett theory, we calculate the velocity of the constant saturation front by applying the multiphase conservation and fractional flow theory.")
    st.image("images/buckley.png")
    t_BT = (len(Sw)-min_index)
    t_BT_w = (len(Sw)-min_index_w)          #no need
    st.write('### Breakthrough Time :',t_BT,"days")
    st.write('### Breakthrough Saturation :',SwBT)
    
    # Taking input of Time
    
    st.write('\n ### Please enter the time (in days) for which waterflooding has been done.')
    time = st.slider('Time (in days)', min_value=0, max_value=100*ceil((len(Sw)-min_index)/100), value=100)
    
    xD = (qt*time/(phi*area*L))*dfw_dSw_polymer
    xD_w = (qt*time/(phi*area*L))*dfw_dSw_water             #no need
    #max_ind = 5 + np.argmax(xD[5:(len(Sw)-5)])
    
    # Making Adjustments for Plot
    Sw_plot = Sw
    xD[min_index:min_index_w] = (np.linspace((round(100*(xD[min_index]-0.0025))),round(100*(xD[min_index_w]-0.0025)),num=abs(min_index_w-min_index)))/100.0
    Sw_plot[min_index:min_index_w] = np.repeat(Sw[min_index_w],abs(min_index_w-min_index))
    xD[min_index_w:] = (np.linspace((round(100*(xD[min_index_w]-0.0025))),100,num=(len(xD)-min_index_w)))/100.0
    Sw_plot[min_index_w:] = np.repeat(Swc,(len(xD)-min_index_w))

    
    # Plotting the Saturation profile
    
    fig = make_subplots()
    fig.add_trace(go.Line(x=xD[1:], y=Sw_plot[1:],name="Saturation"))
    fig.update_yaxes(title_text="<b>Saturation</b>",range=[0.0,1.0],nticks=20)
    fig.update_xaxes(title_text="<b>Dimensionless Distance (xD)</b>",range=[0.0,1.0],nticks=20)
    fig.update_layout(title={'text':"<b>Saturation Profile<b>",'x':0.48,'y':0.85})
    st.plotly_chart(fig, use_container_width=True)
    
    # Recovery Plot
    
    st.write("## Recovery Analysis")
    st.write("One of the major applications of the Buckley-Leverett theory is to estimate the recovery of a reservoir before and after a CEOR process. Using the Buckley-Leverett theory, the pore volumes of oil produced with respect to the pore volume of water (or any other fluid) can be calculated and plotted before and after the breakthrough of the flood-front.")
    st.write("Npd = Pore volumes of oil produced")
    st.write("Wid = Pore volumes of water injected")
    st.write("### Case I: Before Breakthrough")
    st.write("In this case, since the flood-front hasn’t reached the production well yet, therefore, only oil is getting produced. Therefore, the amount of pore volume of oil produced is equal to the amount of pore volume of water injected. Now we define,")
    col1, col2, col3 = st.beta_columns([1,1,1])
    with col1:
        st.write("")
    with col2:
        st.image("images/case1.jpg")    
    with col3:
        st.write("")
    st.write("### Case II: After Breakthrough")
    st.write("After the breakthrough, the water saturation and fractional flow of water in the production well will slowly increase. But the total reservoir length remains same. Therefore, we take the average of the total water saturation present before the producing well (𝑆¯𝑤). Now, the pore volume of oil produced equals,")
    st.image("images/case2_0.jpg")
    st.write("Where,")
    st.image("images/case2_1.jpg") 
    #st.image("case2_2.jpg") 
    st.write("Substituting this value of average water saturation to get the final number of pore volumes of oil produced.")
    col1, col2, col3 = st.beta_columns([1,3,1])
    with col1:
        st.write("")
    with col2:
        st.image("images/case2_2.jpg")    
    with col3:
        st.write("")
    
    Wid = np.zeros(len(Sw))
    Npd = np.zeros(len(Sw))
    Wid_BT_w = 1.0/dfw_dSw_water[min_index_w]
    Wid_BT_p = 1.0/dfw_dSw_polymer[min_index]
    
    #st.write(Wid_BT)
    st.write("Water Breakthrough Sat :",sat[min_index_w])
    st.write("polymer Breakthrough Sat :",sat[min_index])
    
   ''' 
    vel_BT = 1.0/Wid_BT_p
    temp = np.zeros(len(Sw))
    Sw_bank = 
    fw_bank = 
    for i in range(len(Sw)):
        if sat[i]<=SwBT:
            Wid[i] = (len(Sw)-i)*Wid_BT_p/t_BT
            temp = ((Sw_bank-Swc) +Wid[i]*(1-fw_bank))
        else:
            Wid[i] = 1.0/dfw_dSw_polymer[i]
    for i in range(len(Sw)):
        if sat[i]<=SwBT:
            Npd[i] = min(Wid[i],temp)
        else:
            Npd[i] = ((sat[i]-Swc)+(1-fw_polymer[i])*Wid[i])
            
   '''
    
    
    for i in range(len(Sw)):
        if sat[i]<=SwBT:
            Wid[i] = (len(Sw)-i)*Wid_BT_p/t_BT
            temp = ((SwBT-Swc) + Wid[i]*(1-fw_water[min_index_w]))
            Npd[i] = min(Wid[i],temp)
        else:
            Wid[i] = 1.0/dfw_dSw_polymer[i]
            Npd[i] = ((sat[i]-Swc)+(1-fw_polymer[i])*Wid[i])
    
    #st.write(pos_p,pos_w)     
    st.write(pd.DataFrame({"Sw":np.flipud(sat[pos_p:]),"Npd":np.flipud(Npd[pos_p:]),"Wid":np.flipud(Wid[pos_p:])}))
    fig_rec = make_subplots()
    fig_rec.add_trace(go.Line(x=Wid[pos_p:], y=Npd[pos_p:],name="Recovery Plot"))
    fig_rec.update_yaxes(title_text="<b>Recovered Pore Volume</b>",range=[0.0,0.6],nticks=10)
    fig_rec.update_xaxes(title_text="<b>Injected Pore Volume</b>",range=[0.0,2.0],nticks=20)
    fig_rec.update_layout(title={'text':"<b>Recovery Plot<b>",'x':0.48,'y':0.85})
    st.plotly_chart(fig_rec, use_container_width=True)
    
    st.write("### Injected Pore Volumes at Breakthrough :",Wid_BT_p)
    
    
    
