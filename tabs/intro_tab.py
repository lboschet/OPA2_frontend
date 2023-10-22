import streamlit as st
from pathlib import Path
import streamlit.components.v1 as components

title = ":blue[INTRODUCTION PROJET OPA2]"
sidebar_name = ":blue[Introduction]"

def read_markdown_file(markdown_file):
   return Path(markdown_file).read_text()

def run():

    # Define a presentation image
    # Some sample available at : https://www.freepik.com/free-photos-vectors/crypto-graph
    
    # st.image("https://dst-studio-template.s3.eu-west-3.amazonaws.com/1.gif")
    # st.image("https://dst-studio-template.s3.eu-west-3.amazonaws.com/2.gif")
    # st.image("https://dst-studio-template.s3.eu-west-3.amazonaws.com/3.gif")
    
    st.image("assets/crypto-currency-background.jpg")
    
    # Display title and center
    #st.write(f'<h1 style="text-align: center;">{title}</h1>', unsafe_allow_html=True)
    st.title(title)

    # Créer une separateur horizontal de couleur 
    components.html("""<hr style="height:10px;border:none;color:#333;background-color:#514f51;" /> """)

    # Recuperer le descriptif du projet au formay-t Markdown dans le repertoire /docs
    intro_markdown = read_markdown_file("../docs/opa2_step1_extract_datas.md")

    # Afficher le decriptif du projet (markdown)
    st.markdown(intro_markdown, unsafe_allow_html=True)

#    st.markdown(
#        """
#        Here is a bootsrap template for your DataScientest project, built with [Streamlit](https://streamlit.io).
#
#        You can browse streamlit documentation and demos to get some inspiration:
#        - Check out [streamlit.io](https://streamlit.io)
#        - Jump into streamlit [documentation](https://docs.streamlit.io)
#        - Use a neural net to [analyze the Udacity Self-driving Car Image
#          Dataset] (https://github.com/streamlit/demo-self-driving)
#        - Explore a [New York City rideshare dataset]
#          (https://github.com/streamlit/demo-uber-nyc-pickups)
#        """
#    )