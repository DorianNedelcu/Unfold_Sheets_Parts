import streamlit as st
from PIL import Image

col1, col2 = st.columns([0.2,0.5])
col1.subheader(":email: :green[CONTACT]")
col2.link_button("Author web page", "https://dorian-nedelcu.streamlit.app/")
st.subheader(":e-mail: :red[Emails]") 

col1, col2, col3 = st.columns(3)
col1.write(":large_yellow_square: dorian.nedelcu@ubbcluj.ro")
col2.write(":large_yellow_square: ne_dor@yahoo.com")
col3.write(":large_yellow_square: nedor1957@gmail.com")