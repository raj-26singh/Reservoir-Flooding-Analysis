
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import streamlit as st
import warnings
warnings.filterwarnings("ignore")

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
    
    SwBT = Sw[min_index]
    

    t_BT = (phi*area*L)/(qt*dfw_dSw[min_index])
    
    st.write('\nEnter the time (in days) for which waterflooding has been done.')
    time = st.slider('Time (in days)', min_value=0, max_value=round(t_BT)+1, value=100)
    
    #def get_values(time):
    xD = (qt*time/(phi*area*L))*dfw_dSw
    #x_bt = (qt*time/(phi*area*L))*(dfw_dSw[min_index])
    max_ind = 101 + np.argmax(xD[101:])
    #xdm = 100*round(xD[max_ind])
    #xD = np.append(xD, (np.repeat(xdm,100))/100.0)
    #return xD, max_index

    for i in range(len(Sw)):
        if Sw[i]<Sw[max_ind]:
            Sw[i] = Swc
            xD[i] = 1 - xD[i]
            if xD[i]<xD[max_ind]:
                xD[i] = xD[max_ind]
            
               
    
    #xD, max_ind = get_values(time)
    
    # SwBT ka jugaad
    '''
    jugaad_Sw = np.zeros(len(Sw))
    count = 0
    key = 0
    for i in range(len(Sw)):
        if Sw[i]>=Sw[max_ind]:
            jugaad_Sw[i] = Sw[i]
        else:
            jugaad_Sw[i] = Swc
            if key==0:
                pos = i
                key = 1
            count = count + 1
        
    
    #xdm = 100*round(xD[max_ind])
    x_swc = (np.linspace(xdm,100,num=count))/100.0
    for i in range(count):
        xD[pos+i] = x_swc[i]
    
    #xD[pos:] = x_swc

    a = 100*round(Swc)
    b = 100*round(Sw[max_ind])
    #jugaad_Sw = np.append(jugaad_Sw,(np.linspace(a,b,num=100)/100))
    '''
    
    
    
    # Plotting
    
    fig = make_subplots()
    fig.add_trace(go.Line(x=xD, y=Sw,name="Saturation"))
    fig.update_yaxes(title_text="<b>Saturation</b>",range=[0.0,1.0],nticks=20)
    fig.update_xaxes(title_text="<b>Dimensionless Distance (xD)</b>",range=[0.0,1.0],nticks=20)
    st.plotly_chart(fig, use_container_width=True)
    
    
    
    
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