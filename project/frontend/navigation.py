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
        st.markdown(
    """
    <div style='text-align: center; margin-bottom: 30px;'>
        <img src='https://mail.google.com/mail/u/0?ui=2&ik=09d30294bd&attid=0.1&permmsgid=msg-a:r-8940339758702768248&th=19f5a98df1fa50fd&view=fimg&fur=ip&permmsgid=msg-a:r-8940339758702768248&sz=s0-l75-ft&attbid=ANGjdJ_K1eWs0RpQSf0cQ0-C_cUJROXUAtvTb-nnsx8o00Hq1rzbdujp377TzMSqW3N7yuErJcSsqwxCURoiL5MfxPfkz--Uq5-YlBXEM1zMsF-FthuRl-nPOHoWN9c&disp=emb&realattid=ii_19f5a98cd5aac42c2ba1&zw'
             style='height: 160px; vertical-align: middle; margin-right: 8px;'>
        <span style='font-size: 48px; font-weight: bold; vertical-align: middle;'>GoalApp</span>
    </div>
    """,
    unsafe_allow_html=True
)

        for label in TAB_PERIOD_MAP.keys():
            is_active = (st.session_state.selected_tab == label)
            if st.button(
                label,
                key=f"tab_{label}",
                use_container_width=True,
                type="primary" if is_active else "secondary"
            ):
                switch_tab(label)