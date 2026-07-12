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

def switch_tab(label: str):
    st.session_state.selected_tab = label
    st.session_state.show_login = False
    st.session_state.show_register = False
    st.session_state.show_profile = False
    st.session_state.show_settings = False

def render_sidebar():
    # Скрываем только меню и футер Streamlit, header оставляем (нужен для открытия sidebar)
    hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stSidebar"] {
        background-color: #E5E9F0;   /* мягкий серо‑голубой */
    }
    </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    with st.sidebar:
        # Логотип (не кликабельный)
        st.markdown("<h2 style='text-align: center; margin-bottom: 30px;'>🏆 GoalApp</h2>", unsafe_allow_html=True)

        # Навигационные кнопки‑вкладки
        for label in TAB_PERIOD_MAP.keys():
            is_active = (st.session_state.selected_tab == label)
            if st.button(
                label,
                key=f"tab_{label}",
                use_container_width=True,
                type="primary" if is_active else "secondary"
            ):
                switch_tab(label)