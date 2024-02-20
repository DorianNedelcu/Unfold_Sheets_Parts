import streamlit as st
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
crt_dir_img= str(current_dir).rstrip("pages")+"/Images/"
crt_dir_vid= str(current_dir).rstrip("pages")+"/Video/"

st.subheader(":green[One cylinder intersected with 2 planes - Version 1]")

Place_Images = st.empty()
col1, col2 = Place_Images.columns([0.4,0.6])
col1.image(Image.open(crt_dir_img+"Cylinder_V1.jpg"), width=240, caption='Cylinder - Version 1')
col2.image(Image.open(crt_dir_img+"Cylinder_V1_Demo.jpg"), width=390, caption='Unfolding demo & Restrictions')

Place_Images = st.empty()
col1, col2, col3  = Place_Images.columns([0.2,0.6,0.2])
video_file = open(crt_dir_vid+'Cylinder V1.mp4', 'rb')
video_bytes = video_file.read()
col2.video(video_bytes, format="mp4", start_time=0)

with st.form('Input_Data'):
    st.subheader(':green[Input Data]')
    col1, col2, col3, col4 = st.columns(4) 
    Diameter = col1.number_input('Diameter [mm]', value=80.0)
    Height = col2.number_input('Height [mm]', value=140.0)
    Alfa = col3.number_input('Alpha angle [deg]', value=60.0)
    Beta = col4.number_input('Beta angle [deg]', value=30.0)
    submit_button = st.form_submit_button('Calculate')
if submit_button:
    PI=np.arctan(1)*4 
    Umax= np.arctan(2 * Height / Diameter) * 180 / PI
    if Diameter=="" or Height==""  or Alfa==""  or Beta==""  :
        st.warning("Please fill all fields with numerical data !")
    elif (Alfa > Umax or Beta > Umax):
        st.warning("Alpha and Beta angles cannot be greater than "+str(Umax)+" grade")  
    else:   # st.success("Success !")
        NrPct = 8 ; ALFAR=Alfa * PI / 180 ; BETAR=Beta * PI / 180
        H1 = Height - Diameter * np.tan(ALFAR) / 2
        H2 = Height - Diameter * np.tan(BETAR) / 2
        Lungime = PI * Diameter # Lungime desfasurata
        Aria = Diameter * (Height * PI - Diameter * (np.tan(ALFAR) + np.tan(BETAR)) / 2)
        XP=[] ; YP=[] ; Teta=[]
        for i in range(1, 4 * NrPct + 2):
            UT=(i - 1) * PI / 2 / NrPct
            Teta.append(UT*180/PI)
            XP.append(UT * Diameter / 2)
            if ((UT < PI / 2) or (UT > 3 * PI / 2)):
            	YP.append(Height - Diameter / 2 * np.cos(UT) * np.tan(ALFAR))
            else:
                YP.append(Height + Diameter / 2 * np.cos(UT) * np.tan(BETAR))
        
        # Chart drawing
        Place_Chart = st.empty()
        Xmax=XP[4 * NrPct] ; H1=YP[0]
        fig=plt.figure()
        plt.title("Unfolded cylinder - Variant 1", fontsize=14, fontweight='bold',color='Black')
        plt.grid(True)
        for i in range(1, 4 * NrPct):
            plt.plot([XP[i], XP[i]],[0, YP[i]], color='Red', linewidth=1)
        plt.plot(XP,YP, color='Blue', linewidth=3)
        plt.plot([0,0],[0,H1], color='Blue', linewidth=3)
        plt.plot([0,Xmax],[0,0], color='Blue', linewidth=3)
        plt.plot([Xmax,Xmax],[0,H1], color='Blue', linewidth=3)
        Place_Chart.write(fig)
        
        # Chart dimensions & coordinates
        st.divider()
        col1, col2 = st.columns([0.4,0.6])
        col1.subheader(":green[Main dimensions]") 
        col1.write("H1="+'%0.2f' % H1+" [mm]")
        col1.write("H2="+'%0.2f' % H2+" [mm]")
        col1.write("Hmax="+'%0.2f' % Height+" [mm]")
        col1.write("Lenght="+'%0.2f' % Lungime+" [mm]")
        col1.write("Area="+'%0.2f' % Aria+" [mm2]")
        df= pd.DataFrame(
            {'Teta [deg]': Teta,
            'X [mm]': XP,
            'Y [mm]': YP
            })
        col2.subheader(":green[Unfolded Coordinates]")
        col2.dataframe(df)
        st.divider()
        
