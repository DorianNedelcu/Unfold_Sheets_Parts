import streamlit as st
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
crt_dir_img= str(current_dir).rstrip("pages")+"/Images/"
crt_dir_vid= str(current_dir).rstrip("pages")+"/Video/"

st.subheader(":green[Intersection of three cylinders with the same diameter]")

Place_Images = st.empty()
col1, col2 = Place_Images.columns([0.5,0.5])
col1.image(Image.open(crt_dir_img+"Three_Cylinders.jpg"), width=350, caption='Three Cylinders')
col2.image(Image.open(crt_dir_img+"Cylinder_V1_Demo.jpg"), width=290, caption='Unfolding demo & Restrictions')

Place_Images = st.empty()
col1, col2, col3  = Place_Images.columns([0.2,0.6,0.2])
video_file = open(crt_dir_vid+'Three_Cylinders.mp4', 'rb')
video_bytes = video_file.read()
col2.video(video_bytes, format="mp4", start_time=0)

with st.form('Input_Data'):
    st.subheader(':green[Input Data]')
    col1, col2, col3= st.columns(3) 
    Diameter = col1.number_input('Diameter [mm]', value=80.0)
    H1 = col2.number_input('Height H1 [mm]', value=100.0)
    H2 = col3.number_input('Height H2 [mm]', value=100.0)
    submit_button = st.form_submit_button('Calculate')
if submit_button:
	PI=np.arctan(1)*4
	Alfa1 = 22.5 * PI / 180
	Beta1 = 45 * PI / 180
	Alfa2 = 22.5 * PI / 180
	Beta2 = 22.5 * PI / 180
	
	# Restrictions check
	Umax1 = np.arctan(2 * H1 / Diameter)
	Umax2 = np.arctan(2 * H2 / Diameter)
	if Alfa1 > Umax1 or Beta1 > Umax1 :
		sir = "For element no.  1 or 3 the angles 'Alpha', 'Beta' must be smaller than "
		sir = sir + '%0.2f' % Umax1 +" [deg]"
		st.warning(sir)
	elif Alfa2 > Umax2 or Beta2 > Umax2 :
		sir = "For element no. 2 the angles 'Alpha', 'Beta' must be smaller than "
		sir = sir + '%0.2f' % Umax2 + " [deg]"
		st.warning(sir)
	else:
		NrPct = 8
		Ld = PI * Diameter  # Unfolded length 
		H11 = H1 - Diameter * np.tan(Alfa1) / 2
		H12 = H1 - Diameter * np.tan(Beta1) / 2
		H21 = H2 - Diameter * np.tan(Alfa2) / 2
		H22 = H2 - Diameter * np.tan(Beta2) / 2
		Aria1 = Diameter * (H1 * PI - Diameter * (np.tan(Alfa1) + np.tan(Beta1)) / 2)
		Aria2 = Diameter * (H2 * PI - Diameter * (np.tan(Alfa2) + np.tan(Beta2)) / 2)
		X=[] ; Y1=[] ; Y2=[] ; Teta=[]
		for i in range(1, 4 * NrPct + 2):
			UT = (i - 1) * PI / 2 / NrPct
			Teta.append(UT*180/PI)
			X.append(UT * Diameter / 2)
			if (UT < PI / 2) or (UT > 3 * PI / 2) :
				Y1.append(H1-Diameter/2*np.cos(UT)*np.tan(Alfa1))
				Y2.append(H2-Diameter/2*np.cos(UT)*np.tan(Alfa2))
			else:
				Y1.append(H1+Diameter/2*np.cos(UT)*np.tan(Beta1))
				Y2.append(H2+Diameter/2*np.cos(UT)*np.tan(Beta2))
		
        # Chart drawing cylinder 1
		Place_Chart = st.empty()
		fig=plt.figure()
		plt.title("Unfolded cylinder 1", fontsize=14, fontweight='bold',color='Black')
		plt.grid(True)
		for i in range(1, 4 * NrPct+1):
			plt.plot([X[i],X[i]], [0,Y1[i]], color='Red', linewidth=1)
		for i in range(1, 4 * NrPct+1):
			plt.plot(X, Y1, color='Blue', linewidth=3)
		plt.plot([0,0],[0,H11], color='Blue', linewidth=3)
		plt.plot([0,Ld],[0,0], color='Blue', linewidth=3)
		plt.plot([Ld,Ld],[0,H11], color='Blue', linewidth=3)	
		Place_Chart.write(fig)	
				
		# Chart drawing cylinder 2
		Place_Chart = st.empty()
		fig=plt.figure()
		plt.title("Unfolded cylinder 2", fontsize=14, fontweight='bold',color='Black')
		plt.grid(True)
		for i in range(1, 4 * NrPct+1):
			plt.plot([X[i],X[i]], [0,Y2[i]], color='Red', linewidth=1)
		for i in range(1, 4 * NrPct+1):
			plt.plot(X, Y2, color='Blue', linewidth=3)
		plt.plot([0,0],[0,H22], color='Blue', linewidth=3)
		plt.plot([0,Ld],[0,0], color='Blue', linewidth=3)
		plt.plot([Ld,Ld],[0,H22], color='Blue', linewidth=3)	
		Place_Chart.write(fig)

        # Chart dimensions & coordinates
		st.divider()
		col1, col2 = st.columns([0.4,0.6])
		col1.subheader(":green[Main dimensions]")
		col1.write("Height H11="+'%0.2f' % H11+" [mm]")
		col1.write("Height H12="+'%0.2f' % H12+" [mm]")
		col1.write("Height H21="+'%0.2f' % H21+" [mm]")
		col1.write("Height H22="+'%0.2f' % H22+" [mm]")
		col1.write("Lenght="+'%0.2f' % Ld+" [mm]")
		col1.write("Area 1="+'%0.2f' % Aria1+" [mm2]")
		col1.write("Area 2="+'%0.2f' % Aria2+" [mm2]")
		df= pd.DataFrame(
            {'Angle [deg]': Teta,
            'X [mm]': X,
            'Y1 [mm]': Y1,
            'Y2 [mm]': Y2,
            })
		col2.subheader(":green[Unfolded Coordinates]")
		col2.dataframe(df)
		st.divider()		    
