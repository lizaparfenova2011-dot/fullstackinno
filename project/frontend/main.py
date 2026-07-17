import streamlit as st
from datetime import datetime
from navigation import init_session_state, render_sidebar
from api_client import api_request

init_session_state()

# ==================== ТЕМЫ ОФОРМЛЕНИЯ ====================
def apply_theme():
    st.markdown("""
    <style>
    p.earned-badge {
        color: #32CD32 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    theme = "system"
    if st.session_state.user and "theme" in st.session_state.user:
        theme = st.session_state.user["theme"]

    # ---------- LIGHT (светло-лимонная) ----------
    if theme == "light":
        st.markdown("""
        <style>
        /* Основной фон */
        .stApp {
            background-color: #FFFDE7;
        }

        /* Поле ввода светлее основного фона */
        input, textarea, .stTextInput > div > div > input {
            background-color: #FFFFFF !important;
            border: 1px solid #FFB300 !important;
            border-radius: 8px !important;
            color: #000000 !important;
        }

        /* Боковая панель: жёлтая, темнее фона, светлее кнопок */
        [data-testid="stSidebar"] {
            background-color: #FFF9C4;
        }

        /* Кнопки */
        .stButton > button {
            background-color: #FFD54F !important;
            color: #000000 !important;
            border-radius: 12px !important;
            font-family: 'Comic Sans MS', 'Chalkboard SE', sans-serif !important;
            font-style: italic !important;
            font-weight: bold !important;
            text-transform: uppercase !important;
            border: none !important;
            transition: all 0.15s ease;
        }
        .stButton > button:hover {
            background-color: #FFB300 !important;
        }
        .stButton > button:active,
        .stButton > button[kind="primary"] {
            background-color: #FFC107 !important;
            box-shadow: inset 0 2px 4px rgba(0,0,0,0.2);
        }

        /* Текст */
        body, .stMarkdown, .stText {
            font-family: 'Comic Sans MS', 'Chalkboard SE', sans-serif !important;
            font-style: italic !important;
            text-transform: uppercase !important;
            color: #000000 !important;
        }
        </style>
        """, unsafe_allow_html=True)
    elif theme == "dark":
        st.markdown("""
        <style>
        /* Основной фон – чёрный */
        .stApp {
            background-color: #330066 !important;
        }

        /* Поле ввода */
        input, textarea, .stTextInput > div > div > input {
            background-color: #4B0082 !important;
            border: 1px solid #8A5CF5 !important;
            border-radius: 8px !important;
            color: #FFFFFF !important;
        }

        /* Боковая панель */
        [data-testid="stSidebar"] {
            background-color: #4B0082 !important;
        }

        /* Обычные кнопки и кнопки отправки формы */
        .stButton > button,
        button[kind="formSubmit"] {
            background-color: #8A5CF5 !important;
            color: #FFFFFF !important;
            border-radius: 12px !important;
            font-family: 'Comic Sans MS', 'Chalkboard SE', sans-serif !important;
            font-style: italic !important;
            font-weight: bold !important;
            text-transform: uppercase !important;
            border: none !important;
            transition: all 0.15s ease;
        }
        .stButton > button:hover,
        .stButton > button:active,
        .stButton > button:focus,
        button[kind="formSubmit"]:hover,
        button[kind="formSubmit"]:active,
        button[kind="formSubmit"]:focus {
            background-color: #E6E6FA !important;
            color: #000000 !important;
            box-shadow: 0 0 8px #E6E6FA !important;
        }

        /* ----- АКТИВНАЯ (primary) КНОПКА – ЯРКАЯ ЛАВАНДОВАЯ ----- */
        .stButton > button[kind="primary"] {
            background-color: #AF69EF !important;   /* яркий лавандовый фон */
            color: #000000 !important;             /* чёрный текст */
            border: 2px solid #FFFFFF !important;  /* белая обводка для выделения */
            box-shadow: 0 0 12px #E6E6FA !important;
        }

        /* Галочки и кружочки – лавандовые */
        input[type="checkbox"],
        input[type="radio"] {
            accent-color: #8A5CF5 !important;
        }
        .stRadio label, .stCheckbox label {
            color: #FFFFFF !important;
        }

        /* Меню popover (профиль/настройки) */
        [data-testid="stPopover"] {
            background-color: #8A5CF5 !important;
        }
        [data-testid="stPopover"] button {
            background-color: #8A5CF5 !important;
            color: #000000 !important;
        }

        /* Весь текст – белый */
        body, .stMarkdown, .stText, .stRadio label, .stCheckbox label,
        .stSelectbox label, h1, h2, h3, h4, h5, h6, p, span, div,
        .stCaption, .stMetric, .stExpander, .stAlert,
        .st-bb, .st-at, .st-c9, .st-c8, .st-c7, .st-c6, .st-c5,
        .st-c4, .st-c3, .st-c2, .st-c1 {
            color: #E6E6FA !important;
        }

        /* Шрифт */
        body, .stMarkdown, .stText {
            font-family: 'Comic Sans MS', 'Chalkboard SE', sans-serif !important;
            font-style: italic !important;
            text-transform: uppercase !important;
        }

        /* Жёсткий сброс для любых кнопок при нажатии */
        button:active,
        button:focus,
        button:hover {
            background-color: #E6E6FA !important;
            color: #000000 !important;
        }
        </style>
        """, unsafe_allow_html=True)
    elif theme == "forest":
        st.markdown("""
            <style>
            /* Основной фон – светло-зелёный, но не мятный (темнее) */
            .stApp {
            background-color: #899D31 !important;
        }

        /* Поле ввода – мятное */
        input, textarea, .stTextInput > div > div > input {
            background-color: #B9C24B !important;
            border: 1px solid #4A7C59 !important;
            border-radius: 8px !important;
            color: #000000 !important;
        }

        /* Боковая панель – коричневая (дерево) */
        [data-testid="stSidebar"] {
            background-color: #8B5A2B !important;
        }

        /* Кнопки (обычные, form submit) – зелёные, не тёмные */
        .stButton > button,
        button[kind="formSubmit"] {
            background-color: #6B8E23 !important;   /* оливковый */
            color: #000000 !important;
            border-radius: 12px !important;
            font-family: 'Comic Sans MS', 'Chalkboard SE', sans-serif !important;
            font-style: italic !important;
            font-weight: bold !important;
            text-transform: uppercase !important;
            border: none !important;
            transition: all 0.15s ease;
        }

        /* При наведении – тёмно-зелёные */
        .stButton > button:hover,
        .stButton > button:active,
        .stButton > button:focus,
        button[kind="formSubmit"]:hover,
        button[kind="formSubmit"]:active,
        button[kind="formSubmit"]:focus {
            background-color: #2E5E2E !important;   /* тёмно-зелёный */
            color: #FFFFFF !important;
            box-shadow: 0 0 8px #2E5E2E;
        }

        /* Активная (нажатая) вкладка – изумрудная */
        .stButton > button[kind="primary"] {
            background-color: #899D31 !important;   /* изумрудный */
            color: #000000 !important;
            box-shadow: 0 0 6px #50C878;
            border: 1px solid #FFFFFF !important;
        }

        /* Кнопка «Добавить цель» (form submit) – БЕЛАЯ, но только в обычном состоянии */
        button[kind="formSubmit"] {
            background-color: #FFFFFF !important;
            color: #000000 !important;
        }
        /* При наведении на «Добавить цель» – тёмно-зелёная, как и все */
        button[kind="formSubmit"]:hover {
            background-color: #2E5E2E !important;
            color: #FFFFFF !important;
        }

        /* Галочки и кружочки – зелёные */
        input[type="checkbox"],
        input[type="radio"] {
            accent-color: #4A7C59 !important;
        }
        .stRadio label, .stCheckbox label {
            color: #000000 !important;
        }

        /* Меню popover (шестерёнка) – тёмно-зелёное */
        [data-testid="stPopover"] {
            background-color: #5B7917 !important;
        }
        [data-testid="stPopover"] button {
            background-color: #5B7917 !important;
            color: #FFFFFF !important;
        }

        /* Весь текст – чёрный */
        body, .stMarkdown, .stText, .stRadio label, .stCheckbox label,
            .stSelectbox label, h1, h2, h3, h4, h5, h6, p, span, div,
        .stCaption, .stMetric, .stExpander, .stAlert,
        .st-bb, .st-at, .st-c9, .st-c8, .st-c7, .st-c6, .st-c5,
        .st-c4, .st-c3, .st-c2, .st-c1 {
            color: #000000 !important;
        }

        /* Шрифт */
        body, .stMarkdown, .stText {
            font-family: 'Comic Sans MS', 'Chalkboard SE', sans-serif !important;
            font-style: italic !important;
            text-transform: uppercase !important;
        }

        /* Жёсткий сброс для любых кнопок при нажатии */
        button:active,
        button:focus,
        button:hover {
            background-color: #2E5E2E !important;
            color: #FFFFFF !important;
        }
        </style>
        """, unsafe_allow_html=True)
    elif theme == "ocean":
        st.markdown("""
            <style>
            /* Основной фон – light cyan */
            .stApp {
                background-color: #E0FFFF !important;
            }

            /* Поле ввода – белое */
            input, textarea, .stTextInput > div > div > input {
                background-color: #FFFFFF !important;
                border: 1px solid #1E90FF !important;
                border-radius: 8px !important;
                color: #000000 !important;
            }

            /* Боковая панель – dodger blue */
            [data-testid="stSidebar"] {
                background-color: #00BFFF !important;
            }

            /* Кнопки (обычные, form submit) – аквамарин */
            .stButton > button,
            button[kind="formSubmit"] {
                background-color: #7FFFD4 !important;
                color: #000000 !important;
                border-radius: 12px !important;
                font-family: 'Comic Sans MS', 'Chalkboard SE', sans-serif !important;
                font-style: italic !important;
                font-weight: bold !important;
                text-transform: uppercase !important;
                border: none !important;
                transition: all 0.15s ease;
            }

            /* При наведении – pale turquoise */
            .stButton > button:hover,
            .stButton > button:active,
            .stButton > button:focus,
            button[kind="formSubmit"]:hover,
            button[kind="formSubmit"]:active,
            button[kind="formSubmit"]:focus {
                background-color: #AFEEEE !important;
                color: #000000 !important;
                box-shadow: 0 0 8px #AFEEEE;
            }

            /* Активная (нажатая) вкладка – light cyan */
            .stButton > button[kind="primary"] {
                background-color: #E0FFFF !important;
                color: #000000 !important;
                box-shadow: 0 0 6px #E0FFFF;
                border: 1px solid #FFFFFF !important;
            }

            /* Галочки и кружочки – голубые */
            input[type="checkbox"],
            input[type="radio"] {
                accent-color: #1E90FF !important;
            }
            .stRadio label, .stCheckbox label {
                color: #000000 !important;
            }

            /* Меню popover (шестерёнка) – аквамарин */
            [data-testid="stPopover"] {
                background-color: #7FFFD4 !important;
            }
            [data-testid="stPopover"] button {
                background-color: #AFEEEE !important;
                color: #000000 !important;
            }

            /* Весь текст – чёрный */
            body, .stMarkdown, .stText, .stRadio label, .stCheckbox label,
            .stSelectbox label, h1, h2, h3, h4, h5, h6, p, span, div,
            .stCaption, .stMetric, .stExpander, .stAlert,
            .st-bb, .st-at, .st-c9, .st-c8, .st-c7, .st-c6, .st-c5,
            .st-c4, .st-c3, .st-c2, .st-c1 {
                color: #000000 !important;
            }

            /* Шрифт */
            body, .stMarkdown, .stText {
                font-family: 'Comic Sans MS', 'Chalkboard SE', sans-serif !important;
                font-style: italic !important;
                text-transform: uppercase !important;
            }

            /* Жёсткий сброс для любых кнопок при нажатии */
            button:active,
            button:focus,
            button:hover {
                background-color: #AFEEEE !important;
                color: #000000 !important;
            }
            </style>
        """, unsafe_allow_html=True)
    elif theme == "sunset":
        st.markdown("""
            <style>
            /* Основной фон – F4C430 */
            .stApp {
            background-color: #FF9900 !important;
            }

            /* Поле ввода – FFFFCC */
            input, textarea, .stTextInput > div > div > input {
                background-color: #FFCC00 !important;
                border: 1px solid #FF9900 !important;
                border-radius: 8px !important;
                color: #000000 !important;
            }

            /* Боковая панель – FF9900 */
            [data-testid="stSidebar"] {
                background-color: #FF33CC !important;
            }

            /* Кнопки (обычные, form submit) – CC33FF */
            .stButton > button,
            button[kind="formSubmit"] {
                background-color: #CC33FF !important;
                color: #FFFFFF !important;
                border-radius: 12px !important;
                font-family: 'Comic Sans MS', 'Chalkboard SE', sans-serif !important;
                font-style: italic !important;
                font-weight: bold !important;
                text-transform: uppercase !important;
                border: none !important;
                transition: all 0.15s ease;
            }

            /* Кнопка «Добавить цель» – FFFF33 */
            button[kind="formSubmit"] {
                background-color: #FFFF33 !important;
                color: #000000 !important;
            }

            /* При наведении – CC33CC */
            .stButton > button:hover,
            .stButton > button:active,
            .stButton > button:focus,
            button[kind="formSubmit"]:hover,
            button[kind="formSubmit"]:active,
            button[kind="formSubmit"]:focus {
                background-color: #CC33CC !important;
                color: #FFFFFF !important;
                box-shadow: 0 0 8px #CC33CC;
            }

            /* Активная (нажатая) вкладка – 9933FF */
            .stButton > button[kind="primary"] {
                background-color: #9933FF !important;
                color: #FFFFFF !important;
                box-shadow: 0 0 6px #9933FF;
                border: 1px solid #FFFFFF !important;
            }

            /* Остальные кнопки (удалить, закрепить, настройки и т.д.) – FF0066 */
            .stButton > button:not([kind="formSubmit"]):not([kind="primary"]) {
                background-color: #FF0066 !important;
                color: #FFFFFF !important;
            }

            /* Галочки и кружочки – оранжевые */
            input[type="checkbox"],
            input[type="radio"] {
                accent-color: #FF9900 !important;
            }
            .stRadio label, .stCheckbox label {
                color: #000000 !important;
            }

            /* Меню popover (шестерёнка) – FF9900 */
            [data-testid="stPopover"] {
                background-color: #FF9900 !important;
            }
            [data-testid="stPopover"] button {
                background-color: #CC33FF !important;
                color: #FFFFFF !important;
            }

            /* Весь текст – чёрный */
            body, .stMarkdown, .stText, .stRadio label, .stCheckbox label,
            .stSelectbox label, h1, h2, h3, h4, h5, h6, p, span, div,
            .stCaption, .stMetric, .stExpander, .stAlert,
            .st-bb, .st-at, .st-c9, .st-c8, .st-c7, .st-c6, .st-c5,
            .st-c4, .st-c3, .st-c2, .st-c1 {
                color: #000000 !important;
            }

            /* Шрифт */
            body, .stMarkdown, .stText {
                font-family: 'Comic Sans MS', 'Chalkboard SE', sans-serif !important;
                font-style: italic !important;
                text-transform: uppercase !important;
            }

            /* Жёсткий сброс для любых кнопок при нажатии */
            button:active,
            button:focus,
            button:hover {
                background-color: #CC33CC !important;
                color: #FFFFFF !important;
            }
            </style>
        """, unsafe_allow_html=True)
apply_theme()

# ========== НЕАВТОРИЗОВАННЫЙ ПОЛЬЗОВАТЕЛЬ ==========
if not st.session_state.token:
    st.title("🏆 Goalaxy")
    st.markdown("### Добро пожаловать! Войдите или зарегистрируйтесь.")

    tab1, tab2 = st.tabs(["Вход", "Регистрация"])

    with tab1:
        with st.form("login_form"):
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Пароль", type="password", key="login_password")
            if st.form_submit_button("Войти"):
                if not email or not password:
                    st.error("Заполните email и пароль")
                else:
                    response = api_request("POST", "/auth/login", json={
                        "email": email,
                        "password": password
                    }, ignore_401=True)
                    if response and "access_token" in response:
                        st.session_state.token = response["access_token"]
                        user_data = api_request("GET", "/profile/")
                        if user_data and not user_data.get("error"):
                            st.session_state.user = user_data
                            st.rerun()
                        else:
                            st.error("Не удалось загрузить профиль. Попробуйте снова.")
                            st.session_state.token = None
                    else:
                        st.error("Неверный email или пароль")

    with tab2:
        with st.form("register_form"):
            email = st.text_input("Email", key="reg_email")
            password = st.text_input("Пароль", type="password", key="reg_password")
            password_confirm = st.text_input("Повторите пароль", type="password", key="reg_password_confirm")
            if st.form_submit_button("Зарегистрироваться"):
                if not email or not password or not password_confirm:
                    st.error("Заполните все поля")
                elif password != password_confirm:
                    st.error("Пароли не совпадают")
                else:
                    response = api_request("POST", "/auth/register", json={
                        "email": email,
                        "password": password
                    })
                    if response and not response.get("error"):
                        st.success("Регистрация успешна! Теперь войдите.")
                    else:
                        st.error("Ошибка регистрации. Возможно, email уже используется.")
    st.stop()
# ========== АВТОРИЗОВАННЫЙ ПОЛЬЗОВАТЕЛЬ ==========
def render_top_bar():
    user = st.session_state.user
    if user:
        col1, col2, col3 = st.columns([7, 2, 1])
        with col2:
            st.write(f"**{user.get('name', user.get('email'))}**")
        with col3:
            avatar_url = user.get("avatar_url", "")
            print("\n" * 50)
            print(avatar_url)
            print("\n" * 50)
            st.image(avatar_url, width=40)
            with st.popover("⚙️"):
                if st.button("Профиль"):
                    st.session_state.show_profile = True
                if st.button("Настройки"):
                    st.session_state.show_settings = True

def show_profile_dialog():
    with st.expander("Профиль", expanded=True):
        user = st.session_state.user
        if not user:
            st.warning("Пользователь не найден")
            if st.button("Закрыть", key="close_profile"):
                st.session_state.show_profile = False
            return
        st.write(f"**Email:** {user['email']}")
        created_at = user.get("created_at")
        if created_at:
            try:
                dt = datetime.fromisoformat(str(created_at))
                formatted_date = dt.strftime("%d.%m.%Y, %H:%M")
                st.write(f"**Дата регистрации:** {formatted_date}")
            except Exception:
                st.write(f"**Дата регистрации:** {created_at}")
        else:
            st.write("**Дата регистрации:** неизвестно")
        name = st.text_input("Имя", value=user.get("name", ""))
        avatar_url = st.text_input("URL аватарки", value=user.get("avatar_url", ""))
        if st.button("Сохранить профиль"):
            update_data = {}
            if name != user.get("name"):
                update_data["name"] = name
            if avatar_url != user.get("avatar_url"):
                update_data["avatar_url"] = avatar_url
            if update_data:
                # Отправляем изменения на сервер
                print("\n" * 30)
                print(update_data)
                resp = api_request("PATCH", "/profile/", json=update_data)
                if resp and not resp.get("error"):
    # ← ДОБАВЛЕНО: получаем свежий профиль с сервера
                    fresh = api_request("GET", "/profile/")
                    if fresh and not fresh.get("error"):
                        st.session_state.user = fresh   # ← теперь используем ответ от GET
                        st.toast("✅ Профиль обновлён", icon="✅")
                        st.rerun()
                    else:
                        st.error("Не удалось загрузить обновлённый профиль")
                else:
                    st.error("Не удалось сохранить изменения")
        st.write("---")
        st.write("**Сменить пароль**")
        old_pw = st.text_input("Старый пароль", type="password", key="old_pw")
        new_pw = st.text_input("Новый пароль", type="password", key="new_pw")
        confirm_new_pw = st.text_input("Повторите новый пароль", type="password", key="confirm_new_pw")
        if st.button("Сменить пароль"):
            if not old_pw or not new_pw or not confirm_new_pw:
                st.error("Заполните все поля")
            elif new_pw != confirm_new_pw:
                st.error("Новые пароли не совпадают")
            else:
                pw_resp = api_request("PATCH", "/profile/password", json={
                    "old_password": old_pw,
                    "new_password": new_pw
                })
                if pw_resp and not pw_resp.get("error"):
                    st.toast("🔒 Пароль изменён", icon="🔒")
                else:
                    st.error("Не удалось сменить пароль")
        if st.button("Закрыть", key="close_profile"):
            st.session_state.show_profile = False

def show_settings_dialog():
    with st.expander("Настройки", expanded=True):
        user = st.session_state.user
        if not user:
            st.warning("Пользователь не найден")
            if st.button("Закрыть", key="close_settings"):
                st.session_state.show_settings = False
            return
        current_theme = user.get("theme", "system")
        themes = ["system", "light", "dark", "forest", "ocean", "sunset"]
        if current_theme not in themes:
            current_theme = "system"
        theme = st.selectbox("Тема оформления", themes, index=themes.index(current_theme))
        if st.button("Сохранить тему"):
            resp = api_request("PATCH", "/profile/", json={"theme": theme})
            if resp and not resp.get("error"):
                st.session_state.user = resp
                st.toast("🎨 Тема изменена", icon="🎨")
                st.rerun()
            else:
                st.error("Не удалось сменить тему")
        if st.button("Закрыть", key="close_settings"):
            st.session_state.show_settings = False

# --- Отрисовка ---
render_sidebar()
render_top_bar()

if st.session_state.get("show_profile"):
    show_profile_dialog()
if st.session_state.get("show_settings"):
    show_settings_dialog()

tab = st.session_state.selected_tab
if tab == "На день":
    from pages.day import render_day_tab
    render_day_tab()
elif tab == "На неделю":
    from pages.week import render_week_tab
    render_week_tab()
elif tab == "На месяц":
    from pages.month import render_month_tab
    render_month_tab()
elif tab == "На год":
    from pages.year import render_year_tab
    render_year_tab()
elif tab == "Награды":
    from pages.badges import render_badges_tab
    render_badges_tab()