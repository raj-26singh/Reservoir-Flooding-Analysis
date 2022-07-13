
from numpy.core.defchararray import count
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import streamlit as st
import warnings
warnings.filterwarnings("ignore")
import pandas as pd

def water_flooding():
    
    st.header("Water Flooding")
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
        st.image("coreys formula.jpg")  
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
    
    M = (krw/uw)/(kro/uo)


    # Fractional flow of water
    
    fw = 1.0/(1.0+(1.0/M))
    
    # Plotting the fractional flow curve
    #st.write(max(fw))
    #st.write(fw[0])
    #st.write(fw)
    pos = 0
    for f in range(len(fw)):
        #st.write("fw:",fw[f])
        if fw[f]<0.999999:
            #st.write("fw:",fw[f],"f:",f)
            pos = f
            break
            
    #st.write(pos)
    

    
    st.write("")
    st.write("## Fractional Flow")
    st.write("Fractional flow theory has been a very important tool with wide applications in understanding and validation of various reservoir simulation and numerical models. It still has been applied in understanding the mechanisms of various Chemical-Enhanced Oil Recovery (CEOR) process and for the purposes of interpreting the transport behaviour of various chemicals in porous and permeable media.")
    st.write("For a 1D incompressible , two phase flow, the fractional flow equation is stated as follows:") 
    col1, col2, col3 = st.beta_columns([1,6,1])
    with col1:
        st.write("")
    with col2:
        st.image("fractional_3.jpg")    
    with col3:
        st.write("")   
    st.write("First term is the advection term which basically symbolizes the flow rate that is going with the flow. The second term is the flow rate of water due to capillary pressure effects and third one is due to gravity or buoyancy effects.") 
    st.write("In case of waterflooding, the advection term dominated here while the gravity and capillary terms are neglected. So,")  
    col1, col2, col3 = st.beta_columns([1,1,1])
    with col1:
        st.write("")
    with col2:
        st.image("fractional.jpg")    
    with col3:
        st.write("")  
    st.write("Now, fractional flow of water is defined as the ratio of flow rate of water with respect to the total flow rate. Therefore,")
    col1, col2, col3 = st.beta_columns([1,3,1])
    with col1:
        st.write("")
    with col2:
        st.image("fractional_2.jpg")    
    with col3:
        st.write("")  
    fig_fw = make_subplots()
    fig_fw.add_trace(go.Line(x=Sw[pos:], y=fw[pos:],name="Fractional Flow Curve"))
    fig_fw.update_yaxes(title_text="<b>Fractional Flow of water (fw)</b>",range=[0.0,1.0],nticks=20)
    fig_fw.update_xaxes(title_text="<b>Water Saturation (Sw)</b>",range=[0.0,1.0],nticks=20)
    fig_fw.update_layout(title={'text':"<b>Fractional Flow Curve<b>",'x':0.48,'y':0.85})
    st.plotly_chart(fig_fw, use_container_width=True)
    
    
    delfw_delSw = (fw-0.0)/(Sw-Swc)

    dfw_dSw = np.insert(((np.diff(fw,n=1))/np.diff(Sw,n=1)),0,delfw_delSw[0],axis=0)

    diff = abs(dfw_dSw-delfw_delSw)

    min_index = 5 + np.argmin(diff[5:(len(Sw)-101)])
    
    SwBT = Sw[min_index]
    
    st.write("## Buckley-Leverett Theory")
    st.write("Buckley- Leverett Theory is widely used for the evaluating the movement of a fluid displacing front for an immiscible displacement process in a porous media. The theory is based on the fractional flow theory and made use of the following assumptions to estimate the rate of injected fluid bank movement :-")
    st.write("• Linear and horizontal 1D flow")
    st.write("• Water is used as the injected fluid in the oil reservoir")
    st.write("• Both oil and water are incompressible in nature")
    st.write("• Both oil and water are immiscible with one another")
    st.write("• Capillary and gravity pressure effects are neglected")
    st.write("Mathematically, using Buckley Leverett theory, we calculate the velocity of the constant saturation front by applying the multiphase conservation and fractional flow theory.")
    st.image("buckley.png")
    t_BT = (len(Sw)-min_index)
    st.write('### Breakthrough Time :',t_BT,"days")
    st.write('### Breakthrough Saturation :',SwBT)
    
    
    # Taking input of Time
    
    st.write('\n ### Please enter the time (in days) for which waterflooding has been done.')
    time = st.slider('Time (in days)', min_value=0, max_value=100*round((len(Sw)-min_index)/100), value=100)
    
    xD = (qt*time/(phi*area*L))*dfw_dSw
    max_ind = 5 + np.argmax(xD[5:(len(Sw)-101)])
    
    #st.write("Max ind:",max_ind,"Sw[max_ind]:",Sw[max_ind],"xD[max_ind]",xD[max_ind])
    
    # Making Adjustments for Plot
    Sw_plot = Sw
    xD[min_index:] = (np.linspace((round(100*(xD[min_index]-0.0025))),100,num=(len(xD)-min_index)))/100.0
    Sw_plot[min_index:] = np.repeat(Swc,(len(xD)-min_index))
    
    #st.write(pd.DataFrame({"xD:": xD,"Sw:":Sw}))
    
    #st.write(sat)
    
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
        st.image("case1.jpg")    
    with col3:
        st.write("")
    st.write("### Case II: After Breakthrough")
    st.write("After the breakthrough, the water saturation and fractional flow of water in the production well will slowly increase. But the total reservoir length remains same. Therefore, we take the average of the total water saturation present before the producing well (𝑆¯𝑤). Now, the pore volume of oil produced equals,")
    st.image("case2_0.jpg")
    st.write("Where,")
    st.image("case2_1.jpg") 
    #st.image("case2_2.jpg") 
    st.write("Substituting this value of average water saturation to get the final number of pore volumes of oil produced.")
    col1, col2, col3 = st.beta_columns([1,3,1])
    with col1:
        st.write("")
    with col2:
        st.image("case2_2.jpg")    
    with col3:
        st.write("")
    
    Wid = np.zeros(len(Sw))
    Npd = np.zeros(len(Sw))
    Wid_BT = 1.0/dfw_dSw[min_index]
    st.write("### Injected Pore Volumes at Breakthrough :",Wid_BT)
    #st.write(Wid_BT)
    for i in range(len(Sw)):
        if sat[i]<=SwBT:
            Wid[i] = (len(Sw)-i)*Wid_BT/t_BT
            Npd[i] = Wid[i] 
        else:
            Wid[i] = 1.0/dfw_dSw[i]
            Npd[i] = ((Sw[i]-Swc)+(1-fw[i])*Wid[i])
            
    #st.write(pd.DataFrame({"Sw":sat[pos:],"Npd":Npd[pos:],"Wid":Wid[pos:]}))
    fig_rec = make_subplots()
    fig_rec.add_trace(go.Line(x=Wid[pos:], y=Npd[pos:],name="Recovery Plot"))
    fig_rec.update_yaxes(title_text="<b>Recovered Pore Volume</b>",range=[0.0,0.6],nticks=10)
    fig_rec.update_xaxes(title_text="<b>Injected Pore Volume</b>",range=[0.0,2.0],nticks=20)
    fig_rec.update_layout(title={'text':"<b>Recovery Plot<b>",'x':0.48,'y':0.85})
    st.plotly_chart(fig_rec, use_container_width=True)
    
    '''
    fig = plt.figure(figsize=(8,8))
    ax = fig.add_subplot(111)
    fig.subplots_adjust(bottom = 0.2, top = 0.75)

    ax_time = fig.add_axes([0.3,0.85,0.4,0.05])
    ax_time.spines['top'].set_visible(True)
    ax_time.spines['right'].set_visible(True)

    slider_time = Slider(ax = ax_time, label = 'Time (days)', valmin = 0, valmax = 1000, valfmt = '%f days', facecolor = '#0000cc')

    # Input Variables

    Swc = 0.1
    Sorw = 0.2
    Krwiro = 0.6
    Krocw = 0.92
    Nw = 2.5    
    No = 6
    uw = 0.5        # cp
    uo = 17.0       # cp
    area = 10**6    # sq. feet
    L = 100         # feet
    phi = 0.2      # Porosity
    qt = 20000      # cubic feet per day (SCFD)
    t = 100      # days

    # Assumed Parameters
    Sw = (np.linspace(100,850,num=751))/1000.0
    #Sw = np.flipud(Sw)

    # Calculations

    # Relative Permeabilities
    kro = Krocw*(((1.0-Sw-Sorw)/(1.0-Swc-Sorw))**No)
    krw = Krwiro*(((Sw-Swc)/(1.0-Swc-Sorw))**Nw)

    # Mobility Ratio
    M = (krw/uw)/(kro/uo)

    # Fractional flow of water
    fw = 1.0/(1.0+(1.0/M))

    delfw_delSw = (fw-0.0)/(Sw-Swc)

    dfw_dSw = np.insert(((np.diff(fw,n=1))/np.diff(Sw,n=1)),0,delfw_delSw[0],axis=0)

    diff = abs(dfw_dSw-delfw_delSw)

    min_index = 101 + np.argmin(diff[101:])

    print("Index :",min_index," Value :",Sw[min_index],"Difference :",diff[min_index])
    SwBT = Sw[min_index]
    max_ind = 0

    def get_values(time):
        xD = (qt*time/(phi*area*L))*dfw_dSw
        #x_bt = (qt*time/(phi*area*L))*(dfw_dSw[min_index])
        max_index = 101 + np.argmax(xD[101:])
        xdm = 100*round(xD[max_index])
        xD = np.append(xD, (np.linspace(xdm,100,num=100))/100.0)
        return xD, max_index

    xD, max_ind = get_values(t)

    # SwBT ka jugaad
    jugaad_Sw = np.zeros(len(Sw))
    for i in range(len(Sw)):
        if Sw[i]>=Sw[max_ind]:
            jugaad_Sw[i] = Sw[i]
        else:
            jugaad_Sw[i] = Swc

    a = 100*round(Swc)
    b = 100*round(Sw[max_ind])
    jugaad_Sw = np.append(jugaad_Sw,(np.linspace(a,b,num=100)/100))

    print("Max Index:",max_ind,"Sat :", Sw[max_ind],"xD :",xD[max_ind])

    graph, = ax.plot(xD,jugaad_Sw, linewidth=2.5)
    ax.set_xlim([0,1])
    ax.set_ylim([0,1])

    def updates(val):
        val = slider_time.val
        x, ind = get_values(val)
        graph.set_data(x,jugaad_Sw)
        fig.canvas.draw_idle()
        plt.show()
        
    slider_time.on_changed(updates)
    plt.show()
    '''


'''
xD = np.linspace(0,100,num = 20)
xD = xD/100.0
Sw = xD*time/1000.0
'''
'''
def get_Sw(xD, time):
    Sw = xD*time/1000.0
    return Sw

Sw = get_Sw(xD, 100)
graph, = ax.plot(xD, Sw, linewidth=2.5)
ax.set_xlim([0,1])
ax.set_ylim([0,1])

def updates(val):
    val = slider_time.val
    graph.set_data(xD, get_Sw(xD, val))
    fig.canvas.draw_idle()
    plt.show()
    
slider_time.on_changed(updates)
plt.show()
'''