import streamlit as st
from PIL import Image
from pathlib import Path

st.set_page_config(
	page_title="Unfold Sheets Parts",
	page_icon="🧊",  # layout="wide",
	initial_sidebar_state="expanded" )

dark = '''
	<style>
		.stApp {  
		primaryColor="Red"
		backgroundColor="Black"
		secondaryBackgroundColor="Black"
		textColor="Gray"
		font="sans serif"
		}
	</style>
'''
st.markdown(dark, unsafe_allow_html=True)

current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
crt_dir_img = str(current_dir)+"/Images/"

st.header(":large_blue_square: Unfold Sheets Parts :arrow_down:")
st.write(":green[This application has been developed in Streamlit & Python & Matplotlib to unfold the sheet metal parts.]")
st.write(":red[The application is accesible through Internet, does not contain any viruses and not store data to any external server.]")
st.link_button(":green[The same application created in B4A (Basic4Application) is available as downloading for smartphones ('Unfold Sheets Parts.apk' file) at the author page, section 'Programming'.]", "https://dorian-nedelcu.streamlit.app/")

st.divider()
Place_Images = st.empty()
col1, col2 = col1, col2 = Place_Images.columns(2)
col1.image(Image.open(crt_dir_img+"Cylinder_V1.jpg"), width=250, caption='One Cylinder - Version 1')
col2.image(Image.open(crt_dir_img+"Cylinder_V2.jpg"), width=200, caption='One Cylinder - Version 2')
col1.image(Image.open(crt_dir_img+"Two_Cylinders.jpg"), width=250, caption='Two Cylinders')
col2.image(Image.open(crt_dir_img+"Elbow.jpg"), width=225, caption='Cylindrical Elbow')

Place_Images = st.empty()
col1, col2, col3 = Place_Images.columns([0.01,0.8,0.1])
col2.image(Image.open(crt_dir_img+"Three_Cylinders.jpg"), width=550, caption='Three Cylinders')

st.divider()



	
	

		 



