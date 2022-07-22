from math import ceil
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import streamlit as st
import warnings
warnings.filterwarnings("ignore")
import pandas as pd


def compare():
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
    #up = st.number_input('Viscosity of Polymer Solution (in cp) :', value=10.0)
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
       
    # Plotting the relative permeability curves
    
    fig_perm = make_subplots(specs=[[{"secondary_y": True}]])
    fig_perm.add_trace(go.Line(x=np.insert(np.append(Sw,0),0,1.0), y=np.insert(np.append(kro,kro[-1]),0,0.0),name="Relative Permeability of Oil (kro)"),secondary_y=False,)
    fig_perm.add_trace(go.Line(x=np.insert(np.append(Sw,0),0,1.0), y=np.insert(np.append(krw,0.0),0,krw[0]),name="Relative Permeability of Water (krw)"),secondary_y=True,)
    fig_perm.update_yaxes(title_text="<b>Relative Permeability of Oil (kro)</b>", secondary_y=False, range=[0.0,1.0],nticks=20)
    fig_perm.update_yaxes(title_text="<b>Relative Permeability of Water (krw)</b>", secondary_y=True, range=[0.0,1.0],nticks=20)
    fig_perm.update_xaxes(title_text="<b>Water Saturation (Sw)</b>",range=[0.0,1.0],nticks=20)
    fig_perm.update_layout(title={'text':"<b>Relative Permeability Curves<b>",'x':0.48,'y':0.85},legend=dict(x=0.25,y=-0.39))
    st.plotly_chart(fig_perm, use_container_width=True)
    
    st.write("How many viscosities would you like to analyse? ")
    num_up = st.number_input("",value=2)
    up = np.zeros(num_up)
    st.write("Please enter",num_up,"different viscosities for comparative analysis :")
    for i in range(num_up):
        up[i] = st.number_input("Polymer Viscosity (cp) :",key=i,value=5.0)
    
    # Mobility Ratio
    M_polymer = np.zeros((len(Sw),num_up))
    M_water = (krw/uw)/(kro/uo)
    for it in range(num_up):
        M_polymer[:,it] = (krw/up[it])/(kro/uo)


    # Fractional flow of water
    
    fw_water = 1.0/(1.0+(1.0/M_water))
    fw_polymer = np.zeros((len(Sw),num_up))
    for it in range(num_up):
        fw_polymer[:,it] = 1.0/(1.0+(1.0/M_polymer[:,it]))
    
    pos_w = 0
    pos_p = np.zeros(num_up)
    for f in range(len(fw_water)):
        #st.write("fw:",fw[f])
        if fw_water[f]<0.999999:
            #st.write("fw:",fw[f],"f:",f)
            pos_w = f
            break
    for it in range(num_up):
        for f in range(len(fw_water)):
            #st.write("fw:",fw[f])
            if fw_polymer[f,it]<0.999999:
                #st.write("fw:",fw[f],"f:",f)
                pos_p[it] = f
                break
                    
    #st.write(pos)
    
    delfw_delSw_water = (fw_water-0.0)/(Sw+di)
    dfw_dSw_water = np.insert(((np.diff(fw_water,n=1))/np.diff(Sw,n=1)),0,delfw_delSw_water[0],axis=0)            #no need
    dfw_dSw_polymer = np.zeros((len(Sw),num_up))
    delfw_delSw_polymer = np.zeros((len(Sw),num_up))
    for it in range(num_up):
        delfw_delSw_polymer[:,it] = (fw_polymer[:,it]-0.0)/(Sw+di)
        dfw_dSw_polymer[:,it] = np.insert(((np.diff(fw_polymer[:,it],n=1))/np.diff(Sw,n=1)),0,delfw_delSw_polymer[0,it],axis=0)
    
    diff = np.zeros(num_up)
    diff = abs(dfw_dSw_polymer-delfw_delSw_polymer)           
    diff_w = abs(dfw_dSw_water-delfw_delSw_water)            #no need

    Wid = np.zeros((len(Sw),num_up))
    Npd = np.zeros((len(Sw),num_up))
    #Wid_BT_w = 1.0/dfw_dSw_water[min_index_w]
    Wid_BT_p = np.zeros(num_up)
    vel_BT = np.zeros(num_up)
    
    min_index = np.zeros(num_up)
    min_index_w = np.zeros(num_up)
    SwBT = np.zeros(num_up)
    t_BT = np.zeros(num_up)
    for it in range(num_up):
        reff = int(up[it])
        min_index[it] = reff + np.argmin(diff[reff:(len(Sw)-reff),it])
        iii = int(min_index[it])
        Wid_BT_p[it] = 1.0/dfw_dSw_polymer[iii,it]
        vel_BT = 1.0/Wid_BT_p[it]
        min_index_w[it] = min_index[it] + np.argmin(abs(delfw_delSw_water[iii:]-np.array([vel_BT]*(len(Sw)-iii))))
        SwBT[it] = Sw[5 + np.argmin(diff[5:(len(Sw)-5),it])]
        t_BT[it] = (len(Sw)-iii)
    
    fig_fw = make_subplots()
    fig_fw.add_trace(go.Line(x=Sw[pos_w:], y=fw_water[pos_w:],name="Fractional Flow Curve of Water"))
    
    for it in range(num_up):
        pp = int(pos_p[it])
        fig_fw.add_trace(go.Line(x=Sw[pp:], y=fw_polymer[pp:,it],name=str("Fractional Flow Curve of Polymer with Viscosity = "+str(up[it])+" cp")))
        fig_fw.update_yaxes(title_text="<b>Fractional Flow</b>",range=[0.0,1.0],nticks=20)
        
    fig_fw.update_xaxes(title_text="<b>Water Saturation (Sw)</b>",range=[0.0,0.8],nticks=20)
    fig_fw.update_layout(title={'text':"<b>Fractional Flow Curves<b>",'x':0.48,'y':0.85},legend=dict(x=0.23,y=-0.28*num_up))
    
    st.plotly_chart(fig_fw, use_container_width=True)
        
    # Taking input of Time
    
    st.write('\n ### Please enter the time (in days) for which waterflooding has been done.')
    time = st.slider('Time (in days)', min_value=0, max_value=100*ceil((len(Sw)-min(min_index))/100), value=100)
    
    xD = np.zeros((len(Sw),num_up))
    for it in range(num_up):
        xD[:,it] = (qt*time/(phi*area*L))*dfw_dSw_polymer[:,it]
    
    xD_w = (qt*time/(phi*area*L))*dfw_dSw_water             #no need
    #max_ind = 5 + np.argmax(xD[5:(len(Sw)-5)])
    
    # Making Adjustments for Plot
    Sw_plot = np.transpose(np.tile(Sw,(num_up,1)))
    #st.write(np.shape(Sw_plot))
    
    Sw_bank = np.zeros(num_up)
    fw_bank = np.zeros(num_up)
    for it in range(num_up):
        iii = int(min_index[it])
        jjj = int(min_index_w[it])
        #st.write(iii,jjj)
        xD[iii:jjj,it] = (np.linspace((round(100*(xD[iii,it]))),round(100*(xD[jjj,it])),num=abs(jjj-iii)))/100.0
        Sw_plot[iii:jjj,it] = np.repeat(Sw[jjj],abs(jjj-iii))
        xD[jjj:,it] = (np.linspace((round(100*(xD[jjj,it]))),100,num=(len(xD[:,it])-jjj)))/100.0
        Sw_plot[jjj:,it] = np.repeat(Swc,(len(xD[:,it])-jjj))
        
        Sw_bank[it] = sat[iii + np.argmin(abs(delfw_delSw_water[iii:]-np.array([vel_BT]*(len(sat)-iii))))]
        fw_bank[it] = fw_water[iii + np.argmin(abs(delfw_delSw_water[iii:]-np.array([vel_BT]*(len(sat)-iii))))]
    

    
    # Plotting the Saturation profile
    
    fig = make_subplots()
    for it in range(num_up):
        fig.add_trace(go.Line(x=xD[1:,it], y=Sw_plot[1:,it],name=str("Saturation of Polymer with Viscosity = "+str(up[it])+" cp")))
        fig.update_yaxes(title_text="<b>Saturation</b>",range=[0.0,1.0],nticks=20)
    fig.update_xaxes(title_text="<b>Dimensionless Distance (xD)</b>",range=[0.0,1.0],nticks=20)
    fig.update_layout(title={'text':"<b>Saturation Profile<b>",'x':0.48,'y':0.85},legend=dict(x=0.23,y=-0.24*num_up))
    st.plotly_chart(fig, use_container_width=True)
    
    # Recovery Plot
    
    temp = np.zeros((len(Sw),num_up))
    
    #st.write("Sw_bank",Sw_bank)
    #st.write("fw_bank",fw_bank)
    #st.write("Swc",Swc)
    #sat = shift(sat,1)
    for it in range(num_up):
        for i in range(len(Sw)-1,0,-1):
            if sat[i]<=SwBT[it]:
                Wid[i,it] = (len(Sw)-i)*Wid_BT_p[it]/t_BT[it]
                temp[i,it] = ((Sw_bank[it]-Swc) +Wid[i,it]*(1-fw_bank[it]))
            else:
                Wid[i,it] = 1.0/dfw_dSw_polymer[i,it]
        for i in range(len(Sw)-1,0,-1):
            if sat[i]<=SwBT[it]:
                Npd[i,it] = min(Wid[i,it],temp[i,it])
            else:
                Npd[i,it] = ((sat[i]-Swc)+(1-fw_polymer[i,it])*Wid[i,it])

    fig_rec = make_subplots()
    
    for it in range(num_up):
        pp = int(pos_p[it])
        fig_rec.add_trace(go.Line(x=Wid[pp:,it], y=Npd[pp:,it],name=str("Recovery Plot for polymer with viscosity = "+str(up[it]))))
    
    fig_rec.update_yaxes(title_text="<b>Recovered Pore Volume</b>",range=[0.0,0.6],nticks=10)
    fig_rec.update_xaxes(title_text="<b>Injected Pore Volume</b>",range=[0.0,2.0],nticks=20)
    fig_rec.update_layout(title={'text':"<b>Recovery Plot<b>",'x':0.48,'y':0.85},legend=dict(x=0.23,y=-0.24*num_up))
    st.plotly_chart(fig_rec, use_container_width=True)
    
    for it in range(num_up):
        st.write("### Injected Pore Volumes of",up[it]," cp polymer at Breakthrough :",round(Wid_BT_p[it],5))