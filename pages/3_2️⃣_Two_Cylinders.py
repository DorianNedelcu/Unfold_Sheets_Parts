import streamlit as st
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
crt_dir_img= str(current_dir).rstrip("pages")+"/Images/"
crt_dir_vid= str(current_dir).rstrip("pages")+"/Video/"

st.subheader(":green[Intersection of two cylinders with the same diameter]")

Place_Images = st.empty()
col1, col2 = Place_Images.columns([0.3,0.7])
col1.image(Image.open(crt_dir_img+"Two_Cylinders.jpg"), width=180, caption='Two_Cylinders')
col1.image(Image.open(crt_dir_img+"Two_Cylinders_Unfolded.jpg"), width=180, caption='Two_Cylinders Unfolded') 
col2.image(Image.open(crt_dir_img+"Two_Cylinders_Demo.jpg"), width=440, caption='Unfolding demo & Restrictions')

Place_Images = st.empty()
col1, col2, col3  = Place_Images.columns([0.2,0.6,0.2])
video_file = open(crt_dir_vid+'Two_Cylinders.mp4', 'rb')
video_bytes = video_file.read()
col2.video(video_bytes, format="mp4", start_time=0)


with st.form('Input_Data'):
    st.subheader(':green[Input Data]')
    col1, col2, col3, col4, col5 = st.columns(5) 
    Diameter = col1.number_input('Diameter [mm]', value=80.0)
    Height = col2.number_input('Height [mm]', value=100.0)
    Gama = col3.number_input('Gama angle [deg]', value=60.0)
    L1 = col4.number_input('L1 [mm]', value=50.0)
    L = col4.number_input('L [mm]', value=150.0)
    submit_button = st.form_submit_button('Calculate')
if submit_button:
    PI=np.arctan(1)*4
    Alfa = Gama / 2
    Beta = 90 - Gama / 2 
    Ld = PI * Diameter
    Umax= np.arctan(2 * Height / Diameter) * 180 / PI
    if (Alfa > Umax or Beta > Umax ):
        sir = "The angles 'Alpha' , 'Beta' must be smaller than "+ '%0.2f' % Umax  
        sir = sir +" [deg]"+"Try increasing the height of the cylinder !"
        st.warning(sir)
    elif np.tan(Gama / 2 * PI / 180) < Diameter / 2 / (L - L1) :
        sir = "The following condition: tg(Gama/2) >= D/[2*(L-l1)]"
        sir=sir +"is not respected !"
        st.warning(sir)
    else:
        NrPct = 8 ; Grad = Gama * PI / 180   ; ALFAR=Alfa * PI / 180 ; BETAR=Beta * PI / 180
        H1 = Height - Diameter * np.tan(ALFAR) / 2  ;  H2 = Height - Diameter * np.tan(BETAR) / 2
        Aria1 = PI * Diameter * L - Diameter * Diameter / 2 * (1 + np.tan(Grad/2) * np.tan(Grad/2) ) / (np.tan(Grad/2))
        Aria2 = Diameter * (Height * PI - Diameter * (np.tan(ALFAR) + np.tan(BETAR)) / 2)
        XP=[] ; YP=[] ; YP1=[]  ; YP2=[] ; Teta=[] 
        for i in range(1, 4 * NrPct + 2):
            UT = (i - 1) * PI / 2 / NrPct 
            Teta.append(UT*180/PI)
            XP.append(UT * Diameter / 2)
            if (UT < PI / 2) or (UT > 3 * PI / 2) :
                YP.append(Height - Diameter / 2 * np.cos(UT) * np.tan(ALFAR))
            else:
                YP.append(Height + Diameter / 2 * np.cos(UT) * np.tan(BETAR))
            if (UT >= PI / 2) and (UT <= 3 * PI / 2) :
                YP1.append(L1 - np.sin(UT - PI / 2) * (Diameter / 2 * np.tan(Grad / 2 )))
                YP2.append(L1 + np.sin(UT - PI / 2) * (Diameter / 2 /(np.tan(Grad / 2 ))))
            else:
                YP1.append(L1) ; YP2.append(L1)
        # Chart drawing 1
        Place_Chart = st.empty()
        fig=plt.figure()
        plt.title("Unfolded cylinder 1", fontsize=14, fontweight='bold',color='Black')
        plt.grid(True)
        # Unrolled bending lines 1
        for i in range(1, 4 * NrPct + 1):
            if (Teta[i] > 90) and (Teta[i] < 270 ):
                plt.plot([XP[i],XP[i]],[0,YP1[i]], color='Red', linewidth=1)     
                plt.plot([XP[i],XP[i]],[YP2[i],L], color='Red', linewidth=1) 
            else:
                plt.plot([XP[i],XP[i]],[0,L], color='Red', linewidth=1)  
        # Draw the rectangle
        plt.plot([0,Ld],[0,0], color='Blue', linewidth=3)
        plt.plot([Ld,Ld],[0,L], color='Blue', linewidth=3)
        plt.plot([Ld,0],[L,L], color='Blue', linewidth=3)
        plt.plot([0,0],[L,0], color='Blue', linewidth=3)
        XD=[] ; YA=[]  ; YB=[]
        for i in range(1, 4 * NrPct + 1):
            if (Teta[i] >= 90) and (Teta[i] <= 270 ):
                XD.append(XP[i])  ;  YA.append(YP1[i])  ;  YB.append(YP2[i])
        plt.plot(XD,YA, color='Blue', linewidth=3)
        plt.plot(XD,YB, color='Blue', linewidth=3)
        Place_Chart.write(fig)

        # Chart drawing 2
        Place_Chart = st.empty()
        fig=plt.figure()
        plt.title("Unfolded cylinder 2", fontsize=14, fontweight='bold',color='Black')
        plt.grid(True)
        # Unrolled bending lines 2
        for i in range(1, 4 * NrPct + 1):
            plt.plot([XP[i],XP[i]],[0,YP[i]], color='Red', linewidth=1)  
        # Upper contour drawing
        XD=[] ; YA=[]  ; YB=[]
        for i in range(1, 4 * NrPct + 1):
            plt.plot(XP,YP, color='Blue', linewidth=3)
        # Drawing straight contour lines
        plt.plot([XP[0],XP[0]],[0,YP[0]], color='Blue', linewidth=3) 
        plt.plot([XP[0],Ld],[0,0], color='Blue', linewidth=3) 
        plt.plot([Ld,Ld],[0,YP[0]], color='Blue', linewidth=3) 
        Place_Chart.write(fig)

        # Chart dimensions & coordinates
        st.divider()
        col1, col2 = st.columns([0.4,0.6])
        col1.subheader(":green[Main dimensions]") 
        col1.write("Alfa angle="+'%0.2f' % Alfa+" [deg]")
        col1.write("Beta angle="+'%0.2f' % Beta+" [deg]")
        col1.write("Height H1="+'%0.2f' % H1+" [mm]")
        col1.write("Height H2="+'%0.2f' % H2+" [mm]")
        col1.write("Height Hmax="+'%0.2f' % Height +" [mm]")
        col1.write("Lenght="+'%0.2f' % Ld+" [mm]")
        col1.write("Area 1="+'%0.2f' % Aria1+" [mm2]")
        col1.write("Area 2="+'%0.2f' % Aria2+" [mm2]")
        df= pd.DataFrame(
            {'Angle [deg]': Teta,
            'X [mm]': XP,
            'Y [mm]': YP,
            'Y1 [mm]': YP1,
            'Y2 [mm]': YP2,
            })
        col2.subheader(":green[Unfolded Coordinates]")
        col2.dataframe(df)
        st.divider()
        
