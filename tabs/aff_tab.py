import streamlit as st
import pandas as pd
import numpy as np

title = ":blue[AFFICHAGE DES DONNEES]"
sidebar_name = ":blue[Affichage des données]"

# 1) Données historique
# 2) Données de streaming (websocket)

def run():

    st.title(title)

    st.markdown(
        """
        This is the third sample tab.
        """
    )

    st.write(pd.DataFrame(np.random.randn(100, 4), columns=list("ABCD")))
