import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import date

from opa2_dataclass import *

_SYMBOLS_ = ["BTCUSDT", "ETHUSDT", "XRPUSDT", "DOTUSDT", "SHIBUSDT", "AVAXUSDT", "LINKUSDT", "ATOMUSDT", "UNIUSDT", "XMRUSDT", "TRXUSDT", "LTCUSDT"]
_MODE_ = ["HISTORIQUE", "LIVE"]
_DATE_START_DEFAULT_ = "2022-10-31"

title = ":blue[CHARGEMENT DES DONNEES]"
sidebar_name = ":blue[Chargement des données]"

# Récuperation du choix "clean" ou "not clean" des données locales
def get_clean(col):

    # Cases à cocher pour nettoyage données ?
    col.subheader("Nettoyer données ?")

    # Par défaut, le premier bouton est sélectionné
    #selected_clean = col.button('Clean', key='clean_button', type="primary", help='Choisissez ce mode pour effacer les données historique')

    # Si le premier bouton est sélectionné, le deuxième bouton n'est pas sélectionné
    #selected_clean = not col.button('No Clean', key='no_clean__button', help='Choisissez ce mode pour ne pas effacer les données déjà récuperées')

    # Tests avec une selectbox
    #selected_clean = col.selectbox("Nettoyage ?", ["OUI", "NON"])

    selected_option = None

    # Tests affichage horizontal (experimental)
    #col.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: center;} </style>', unsafe_allow_html=True)
    #col.write('<style>div.st-bf{flex-direction:column;} div.st-ag{font-weight:bold;padding-left:2px;}</style>', unsafe_allow_html=True)
    selected_option = col.radio("Nettoyage ?", ["OUI", "NON"], index=0)

    # Affichez l'option sélectionnée
    #st.write(f"Option sélectionnée : {selected_option}")

    return selected_option

    if selected_clean:
        return "clean"
    else:
        return "no_clean"
    
    # Affichez l'option sélectionnée
    #st.write('Option sélectionnée :', selected_clean)   

    return selected_clean

# Récuperation de la frequence de chargement des données avec plusieurs valeurs possibles (checkboxes)
def get_freq_mutli():

    # Cases à cocher pour le choix de la fréquence de récupération (multi)
    col.subheader("Fréquences de chargement ?")
    # Tableau contenant les valeurs de l'énumération des intervalles
    options = list(ChartInterval)

    # Calcul du nombre d'options par colonne
    options_per_column = len(options) // 4

    # Créez une colonne pour chaque colonne d'options
    col1, col2, col3, col4 = st.columns(4)

    # Liste pour stocker les options sélectionnées
    selected_options = []

    # Organisez les options dans chaque colonne
    for i, option in enumerate(options):
        if i < options_per_column:
            if col1.checkbox(option):
                selected_options.append(option)
        elif i < 2 * options_per_column:
            if col2.checkbox(option):
                selected_options.append(option)
        elif i < 3 * options_per_column:
            if col3.checkbox(option):
                selected_options.append(option)
        else:
            if col4.checkbox(option):
                selected_options.append(option)

    # Affichez les options sélectionnées
    #st.write('Options sélectionnées :', selected_options)   

    return selected_options

# Fréquence de chargement des données avec 1 seule valeur possible (radiobutton)
def get_freq(col):

    # Cases à cocher pour le choix de la frequence de récupération
    col.subheader("Fréquence de chargement ?")

    # Ajoutez un titre
    #st.subheader("Fréquence de chargement :")

    selected_option = None

    # Tests affichage horizontal (experimental)
    #col.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: center;} </style>', unsafe_allow_html=True)
    #col.write('<style>div.st-bf{flex-direction:column;} div.st-ag{font-weight:bold;padding-left:2px;}</style>', unsafe_allow_html=True)
    selected_option = col.radio("Fréquences disponibles", [interval.value for interval in ChartInterval], index=12)

    # Affichez l'option sélectionnée
    #st.write(f"Option sélectionnée : {selected_option}")

    return selected_option

# Récuperation de la liste des cryptos monnaies disponibles
def get_cryptos(col):

    # Liste deroulante avec les cryptos disponibles
    col.subheader("Cryptos à charger ? ")

    # Default crypto is selected_symbols
    selected_symbols = ["BTCUSDT"]

    # Sélection des symboles
    selected_symbols = col.multiselect("Sélectionnez des symboles", _SYMBOLS_, default=["BTCUSDT"])

    # Affichez les symboles sélectionnés
    #st.write("Symboles sélectionnés :", selected_symbols)

    return selected_symbols

def get_mode(col):

    # Cases à cocher pour le mode de récupération
    col.subheader("Mode de chargement ?")

### TESTS BUTTONS
    # Default = history
    #selected_mode = True 

    # Par défaut, le premier bouton est sélectionné
    #selected_mode = col.button('Mode History', key='history_button', type="primary", help='Choisissez ce mode pour récupération historique')

    # Si le premier bouton est sélectionné, le deuxième bouton n'est pas sélectionné
    #selected_mode = not st.button('Mode Live', key='kline_button', help='Choisissez ce mode pour la récupération en live (kline)')

    #if selected_mode:
    #    return "history"
    #else:
    #    return "kline"

    selected_option = None

    # Tests affichage horizontal (experimental)
    #col.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: center;} </style>', unsafe_allow_html=True)
    #col.write('<style>div.st-bf{flex-direction:column;} div.st-ag{font-weight:bold;padding-left:2px;}</style>', unsafe_allow_html=True)
    selected_option = col.radio("Mode de chargement ?", _MODE_, index=0)

    # Affichez l'option sélectionnée
    #st.write(f"Option sélectionnée : {selected_option}")

    return selected_option
    
def get_date_interval(col):

    # Récuperer les dates de début et fin de récupératiion des données
    col.subheader("Date début de chargement ? ")

    # Récuperer la date du jour au format tuple
    d = datetime.now()
    date_du_jour = datetime(d.year, d.month, d.day)

    # Date de fin par defaut (_DATE_START_DEFAULT_) au format tuple
    #d = _DATE_START_DEFAULT_.split('-')
    d = date.fromisoformat(_DATE_START_DEFAULT_)
    date_debut_defaut = datetime(d.year, d.month, d.day)

    print("date_du_jour", date_du_jour)
    #print("date_debut_defaut", date_debut_defaut)

    # Récuperer la date de début
    selected_start_date = col.date_input("Date de début", min_value=None, max_value=date_du_jour, value=date_debut_defaut)

    # Récuperer la date de fin
    selected_end_date = col.date_input("Date de fin", min_value=None, max_value=date_du_jour, value=date_du_jour)

    #return selected_start_date, selected_end_date
    return selected_start_date, selected_end_date

def get_start():

    # Récuperer les dates de début et fin de récupératiion des données
    st.subheader(" ")
    st.subheader("Cliquer pour lancer le chargement ? ")

    selected_start = st.button('DEMARRER', key='start_button', type="primary", help='Cliquez pour demarrer le chargement des données', use_container_width=True, on_click=do_retrieval)

    return

def do_retrieval(freq, cryptos, load_mode, clean_mode, debut, fin):

    # Si mode "clean" alors vidage du repertoire de travail
    #if clean_mode == "clean":
    #    st.write("Nettoyage des données locales")
    #    if os.path.exists("./binance_datas"):
    #        shutil.rmtree("./binance_datas")

    d = datetime.now()
    date_du_jour = datetime(d.year, d.month, d.day)

    print()
    print("*** CALLBACK DO_RETRIEVAL ***")
    print("\tChargement des données lancé à:", date_du_jour)
    print("\tFrequence de récupération:", freq)
    print("\tCryptos selectionnées:", cryptos)
    print("\tMode de récupération:", load_mode)
    print("\tNettoyage des données precedentes:", clean_mode)
    print("\tDates de debut:", debut)
    print("\tDates de debut:", fin)
    print()

    st.write(()
    st.write(("*** CALLBACK DO_RETRIEVAL ***")
    st.write(("\tChargement des données lancé à:", date_du_jour)
    st.write(("\tFrequence de récupération:", freq)
    st.write(("\tCryptos selectionnées:", cryptos)
    st.write(("\tMode de récupération:", load_mode)
    st.write(("\tNettoyage des données precedentes:", clean_mode)
    st.write(("\tDates de debut:", debut)
    st.write(("\tDates de debut:", fin)
    st.write(()

    return

def run():

    st.title(title)

    #st.markdown(
    #    """
    #    RECUPERATION DES DONNEES HISTORIQUES & EN STREAMING
    #    """
    #)

    # Créer plusieurs colonnes pour l'affichage
    col1, col2  = st.columns(2)

    print()

    # Selection de la fréquence de chargement des données (unique)
    sel_freq = get_freq(col1)
    print("Frequence de récupération: ", sel_freq)

    # Selection des cryptos à récupérer parmi la liste _SYMBOL_ (multiple)
    sel_cryptos = get_cryptos(col2)
    print("Cryptos selectionnées: ", sel_cryptos)

    # Selection deu mode de récupération (unique) : LIVE (streaming) ou HISTORIQUE
    sel_mode = get_mode(col2)
    print("Mode de récupération: ", sel_mode)

    # Nettoyage des données precedentes ?
    sel_clean = get_clean(col2)
    print("Nettoyage des données precedentes: ", sel_clean)

    # Intervalle de temps pour le chargement (date_début, date_fin)
    t_debut , t_fin = get_date_interval(col2)
    print("Dates de debut: ", t_debut)
    print("Dates de debut: ", t_fin)
    
    # Creation du bouton de lancement de récupération
    st.subheader(" ")
    st.subheader("Cliquer pour lancer le chargement ? ")

    #selected_start = st.button('DEMARRER', key='start_button', type="primary", help='Cliquez pour demarrer le chargement des données', \
    #                            use_container_width=True, on_click=do_retrieval(sel_freq, sel_cryptos, sel_mode, sel_clean, t_debut, t_fin))

    selected_start = st.button('DEMARRER', key='start_button', type="primary", help='Cliquez pour demarrer le chargement des données', use_container_width=True)
    
    # Declencher la récupération sur click du bouton "DEMARRER" (ne pas utiliser la callback onclick ici)
    if selected_start:
            do_retrieval(sel_freq, sel_cryptos, sel_mode, sel_clean, t_debut, t_fin)


