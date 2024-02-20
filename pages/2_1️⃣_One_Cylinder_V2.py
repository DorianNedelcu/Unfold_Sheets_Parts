import streamlit as st
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
crt_dir_img= str(current_dir).rstrip("pages")+"/Images/"
crt_dir_vid= str(current_dir).rstrip("pages")+"/Video/"

st.subheader(":green[One cylinder intersected with 2 planes - Version 2]")

Place_Images = st.empty()
col1, col2 = Place_Images.columns([0.3,0.7])
col1.image(Image.open(crt_dir_img+"Cylinder_V2.jpg"), width=180, caption='Cylinder - Version 2')
col2.image(Image.open(crt_dir_img+"Cylinder_V2_Demo.jpg"), width=490, caption='Unfolding demo')

Place_Images = st.empty()
col1, col2, col3  = Place_Images.columns([0.2,0.6,0.2])
video_file = open(crt_dir_vid+'Cylinder V2.mp4', 'rb')
video_bytes = video_file.read()
col2.video(video_bytes, format="mp4", start_time=0)

with st.form('Input_Data'):
    st.subheader(':green[Input Data]')
    col1, col2, col3, col4 = st.columns(4) 
    Diameter = col1.number_input('Diameter [mm]', value=60.0)
    Height = col2.number_input('Height [mm]', value=110.0)
    Alfa = col3.number_input('Alpha angle [deg]', value=15.0)
    Beta = col4.number_input('Beta angle [deg]', value=25.0)
    submit_button = st.form_submit_button('Calculate')
if submit_button:
    PI=np.arctan(1)*4  ; ALFAR=Alfa * PI / 180 ; BETAR=Beta * PI / 180
    H1 = Height - Diameter * (np.tan(ALFAR) + np.tan(Beta * PI / 180)) 
    if H1 < 0 :
        sir = "The H1 = " +'%0.2f' % H1+ " height cannot be negative !" 
        sir = sir + "Try increasing the height of the cylinder !"
        st.warning(sir)
    else:
        Lungime = PI * Diameter # Unfolded length
        HAlfa = Diameter * np.tan(ALFAR)
        HBeta = Diameter * np.tan(BETAR)
        Aria = PI * Diameter * (Height - Diameter * (np.tan(ALFAR) + np.tan(BETAR)) / 2)
        NrPct = 8 
        XP=[] ; YP1=[] ; YP2=[] ; Teta=[]
        for i in range(1, 4 * NrPct + 2):
            UT = (i - 1) * PI / 2 / NrPct
            Teta.append(UT*180/PI)
            XP.append(UT * Diameter / 2)
            YP1.append(H1+Diameter * (1 - np.cos(UT)) * np.tan(ALFAR) / 2)
            YP2.append(-Diameter * (1 - np.cos(UT)) * np.tan(BETAR) / 2)
	    
        # Chart drawing
        Place_Chart = st.empty()
        Xmax=XP[4 * NrPct] 
        fig=plt.figure()
        plt.title("Unfolded cylinder - Variant 2", fontsize=14, fontweight='bold',color='Black')
        plt.grid(True)
        for i in range(1, 4 * NrPct):
            plt.plot([XP[i], XP[i]],[YP1[i], YP2[i]], color='Red', linewidth=1)
        plt.plot(XP,YP1, color='Blue', linewidth=3)
        plt.plot(XP,YP2, color='Blue', linewidth=3)
        plt.plot([0,0],[0,H1], color='Blue', linewidth=3)
        plt.plot([Xmax,Xmax],[0,H1], color='Blue', linewidth=3)
        Place_Chart.write(fig)	

        # Chart dimensions & coordinates
        st.divider()
        col1, col2 = st.columns([0.4,0.6])
        col1.subheader(":green[Main dimensions]") 
        col1.write("H1="+'%0.2f' % H1+" [mm]")
        col1.write("HAlfa="+'%0.2f' % HAlfa+" [mm]")
        col1.write("HBeta="+'%0.2f' % HBeta+" [mm]")
        col1.write("Lenght="+'%0.2f' % Lungime+" [mm]")
        col1.write("Area="+'%0.2f' % Aria+" [mm2]")
        df= pd.DataFrame(
            {'Teta [deg]': Teta,
            'X [mm]': XP,
            'Y1 [mm]': YP1,
            'Y2 [mm]': YP2,
            })
        col2.subheader(":green[Unfolded Coordinates]")
        col2.dataframe(df)
        st.divider()
