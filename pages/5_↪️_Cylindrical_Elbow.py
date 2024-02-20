import streamlit as st
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
crt_dir_img= str(current_dir).rstrip("pages")+"/Images/"
crt_dir_vid= str(current_dir).rstrip("pages")+"/Video/"

st.subheader(":green[The unfold components of an elbow]")

Gama_Angles = ["24","25","28","30","32","33","35","36","40","42","44","45","48","49","50","54","55",
            "56","60","63","64","65","66","67.5","70","72","75","77","78","80","84","85","88","90"]

Place_Images = st.empty()
col1, col2 = Place_Images.columns([0.3,0.7])
col1.image(Image.open(crt_dir_img+"Elbow.jpg"), width=200, caption='Cylindrical elbow')
col2.image(Image.open(crt_dir_img+"Elbow_unfolded.jpg"), width=440, caption='Unfolding demo')

Place_Images = st.empty()
col1, col2, col3 = Place_Images.columns([0.1,0.8,0.1])
video_file = open(crt_dir_vid+'Elbow.mp4', 'rb')
video_bytes = video_file.read()
col2.video(video_bytes, format="mp4", start_time=0)

Gama_Angles.reverse()
Gama_Angles.insert(0, "Select angle")

st.divider()
st.subheader(':green[Input Data]')
col1, col2, col3 = st.columns(3) 
Diameter = col1.number_input('Diameter [mm]', value=80.0)
Raza = col2.number_input('Elbow Radius R [mm]', value=150.0)
Gama_Sel=col3.selectbox("Gama angle [deg]",options=Gama_Angles)
if Gama_Sel != "Select angle":
    Alfa_Angles=["2.5","3","3.5","4","5","5.5","6","7.5","8","10","11.25"]
    Ualfa=["Select angle"]
    for alf in Alfa_Angles:
        n = (float(Gama_Sel)/float(alf)+2) / 2
        r = np.floor(n)
        if n == r and n>2 and n<=19:
            Ualfa.append(alf)
    col1, col2, col3 = st.columns(3) 
    Alfa_Sel=col1.selectbox("Alfa angle [deg]",options=Ualfa)
    if Alfa_Sel != "Select angle":
        n1 = (float(Gama_Sel)/float(Alfa_Sel)+2) / 2
        r1 = np.floor(n1)
        if n1 == r1:
            No = col2.text_input('No. of elbow elements [-]', int(np.floor(n1)), disabled=True)
            col3.write("")
            s_btn = col3.button("Calculate",use_container_width=True)
            st.divider()
            if s_btn:
                # Calculate elbow elements
                PI=np.arctan(1)*4
                NrPct = 8
                GamaR=float(Gama_Sel)*PI/180
                AlfaR=float(Alfa_Sel)*PI/180
                K = Raza * np.tan(GamaR / 2)
                t = Raza * np.tan(AlfaR)
                H1 = t - Diameter * np.tan(AlfaR) / 2
                H2 = t + Diameter * np.tan(AlfaR) / 2
                Ld = PI * Diameter   # Unfolded length
                Aria1 = PI * Diameter * (H2 - Diameter * (np.tan(AlfaR) + np.tan(0)) / 2)
                Aria2 = PI * Diameter * (2 * H2 - Diameter * (np.tan(AlfaR) + np.tan(0)) / 2)
                XP=[] ; Y1=[] ; Teta=[]
                for i in range(1, 4 * NrPct + 2):
                    UT = (i - 1) * PI / 2 / NrPct
                    Teta.append(UT)
                    XP.append(UT * Diameter/ 2)
                    Y1.append(Diameter / 2 * (1 - np.cos(UT)) * np.tan(AlfaR))

                # Elbow drawing 
                Place_Chart = st.empty()
                fig=plt.figure()
                plt.title("Elbow geometry with "+'%2d' %  float(No)+" elements", fontsize=14, fontweight='bold',color='Black')
                plt.grid(True)
                plt.axis('equal')
                X11=[] ; Y11=[] ; X22=[] ; Y22=[]
                cnt=0 ; RpD2 = Raza + Diameter/2 ;  RmD2 = Raza - Diameter/2 
                for i in range(1, 2 * int(float(No)) ):
                    unghi = AlfaR * (i - 1)
                    plt.plot([0,RpD2 * np.sin(unghi)],[RpD2,RpD2-RpD2 * np.cos(unghi)], color='Red', linewidth=1)
                    if i==1 or (i % 2) == 0 or i == (2 * int(float(No)) - 2) + 1 :
                        x1=RpD2*np.sin(unghi) ; x2=RmD2*np.sin(unghi)
                        y1=RpD2-RpD2*np.cos(unghi) ; y2=RpD2-RmD2*np.cos(unghi)
                        plt.plot([x1,x2],[y1, y2], color='Blue', linewidth=3)
                        cnt+=1
                        X11.append(x1) ; Y11.append(y1) ; X22.append(x2) ; Y22.append(y2)
                for i in range(0, cnt):
                    if i==0:
                        Xant1=X11[i] ; Yant1=Y11[i] 
                        Xant2=X22[i]  ; Yant2=Y22[i] 
                    else:
                        plt.plot([Xant1,X11[i]],[Yant1, Y11[i] ], color='Blue', linewidth=3)
                        plt.plot([Xant2,X22[i]],[Yant2, Y22[i] ], color='Blue', linewidth=3)
                        Xant1=X11[i] ; Yant1=Y11[i] 
                        Xant2=X22[i]  ; Yant2=Y22[i]
                Place_Chart.write(fig) 

                # Chart drawing element 1
                Place_Chart = st.empty()
                fig=plt.figure()
                plt.title("Unfolded element 1", fontsize=14, fontweight='bold',color='Black')
                plt.grid(True)
                YH1=[]
                for i in range(0, 4 * NrPct+ 1):
                    YH1.append(H1+Y1[i])
                    plt.plot([XP[i], XP[i]],[0, YH1[i]], color='Red', linewidth=1)
                plt.plot(XP,YH1, color='Blue', linewidth=3)
                plt.plot([0,0],[0,H1], color='Blue', linewidth=3)
                plt.plot([0,Ld],[0,0], color='Blue', linewidth=3)
                plt.plot([Ld,Ld],[0,H1], color='Blue', linewidth=3)
                Place_Chart.write(fig) 

                # Chart drawing element 2
                Place_Chart = st.empty()
                fig=plt.figure()
                plt.title("Unfolded element 2", fontsize=14, fontweight='bold',color='Black')
                plt.grid(True)
                YH2a=[] ; YH2b=[] 
                for i in range(0, 4 * NrPct+ 1):
                    YH2a.append(H2-H1-Y1[i])
                    YH2b.append(H2+H1+Y1[i])
                    plt.plot([XP[i], XP[i]],[YH2a[i], YH2b[i]], color='Red', linewidth=1)
                plt.plot(XP,YH2a, color='Blue', linewidth=3)
                plt.plot(XP,YH2b, color='Blue', linewidth=3)
                plt.plot([0, 0],[H2-H1, H2+H1], color='Blue', linewidth=3)
                plt.plot([Ld,Ld],[H2-H1, H2+H1], color='Blue', linewidth=3)
                Place_Chart.write(fig)    

                # Chart dimensions & coordinates
                st.divider()
                col1, col2 = st.columns([0.35,0.65])
                col1.subheader(":green[Main dimensions]")
                col1.write("Diameter="+'%0.2f' % Diameter+" [mm]")
                col1.write("Elbow Radius="+'%0.2f' % Raza+" [mm]") 
                col1.write("Gama angle="+'%0.2f' % float(Gama_Sel)+" [deg]")
                col1.write("Alfa angle="+'%0.2f' % float(Alfa_Sel)+" [deg]")  
                col1.write("Elbow Elements No.="+'%2d' %  float(No)+" [-]") 
                col1.write("K1 length="+'%0.2f' % K+" [mm]")
                col1.write("t length="+'%0.2f' % t+" [mm]")
                col1.write("H1="+'%0.2f' % H1+" [mm]")
                col1.write("H2="+'%0.2f' % H2+" [mm]")
                col1.write("Unfolded length Ld ="+'%0.2f' % Ld +" [mm]")
                col1.write("Area 1="+'%0.2f' % Aria1 +" [mm2]")
                col1.write("Area 2="+'%0.2f' % Aria2 +" [mm2]")
                df= pd.DataFrame(
                    {'Teta [deg]': Teta,
                    'X [mm]': XP,
                    'Y1 [mm]': YH1,
                    'Y2a [mm]': YH2a,
                    'Y2b [mm]': YH2b,
                    })
                col2.subheader(":green[Unfolded Coordinates]")
                col2.dataframe(df)
                st.divider()

