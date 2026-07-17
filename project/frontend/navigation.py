import streamlit as st

TAB_PERIOD_MAP = {
    "На день": "day",
    "На неделю": "week",
    "На месяц": "month",
    "На год": "year",
    "Награды": None
}

def init_session_state():
    defaults = {
        "token": None,
        "user": None,
        "selected_tab": "На день",
        "show_login": False,
        "show_register": False,
        "show_profile": False,
        "show_settings": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def render_sidebar():
    hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    with st.sidebar:
        # Логотип
        st.markdown("<h2 style='text-align: center; margin-bottom: 30px;'>🏆 Goalaxy</h2>", unsafe_allow_html=True)

        for label in TAB_PERIOD_MAP.keys():
            if st.button(
                label,
                key=f"tab_{label}",
                use_container_width=True,
                type="primary" if st.session_state.selected_tab == label else "secondary"
            ):
                st.session_state.selected_tab = label
                st.rerun()