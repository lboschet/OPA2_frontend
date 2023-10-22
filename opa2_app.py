import streamlit as st
from collections import OrderedDict
import streamlit.components.v1 as components


# Import general information such as TITLE, TEAM_MEMBERS and PROMOTION values from config.py.
import config

# Create sidebar tabs in the ./tabs folder, and import them here.
from tabs import intro_tab, struct_tab, explo_tab, recup_tab, aff_tab, concl_tab

# Set application title
st.set_page_config(
    page_title=config.TITLE,
    page_icon="https://datascientest.com/wp-content/uploads/2020/03/cropped-favicon-datascientest-1-32x32.png",
)

# Get page css styles
with open("style.css", "r") as f:
    style = f.read()

st.markdown(f"<style>{style}</style>", unsafe_allow_html=True)

# Add tab in this ordered dict by passing the name in the sidebar as key and the imported tab
# as value as follow :
TABS = OrderedDict(
    [
        (intro_tab.sidebar_name, intro_tab),
        (struct_tab.sidebar_name, struct_tab),
        (explo_tab.sidebar_name, explo_tab),
        (recup_tab.sidebar_name, recup_tab),
        (aff_tab.sidebar_name, aff_tab),
        (concl_tab.sidebar_name, concl_tab),
    ]
)

# Start the streamlit application
# Initial sidebar logo was :
# "https://dst-studio-template.s3.eu-west-3.amazonaws.com/logo-datascientest.png",
#
def run():
    st.sidebar.image(
        "assets/crypto-currency-logo.png",
        width=200,
    )
    tab_name = st.sidebar.radio("", list(TABS.keys()), 0)
    
    # Creer une separateur horizontal
    #components.html("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """)
    st.sidebar.markdown("---")

    st.sidebar.markdown(f"## {config.PROMOTION}")

    # Creer une separateur horizontal
    #components.html("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """)
    st.sidebar.markdown("---")

    st.sidebar.markdown("### Team members:")
    for member in config.TEAM_MEMBERS:
        st.sidebar.markdown(member.sidebar_markdown(), unsafe_allow_html=True)

    tab = TABS[tab_name]

    tab.run()


if __name__ == "__main__":
    run()
