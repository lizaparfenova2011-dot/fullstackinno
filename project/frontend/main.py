import streamlit as st
from navigation import init_session_state, render_sidebar
from api_client import api_request   # пока заглушка

# ---------- Инициализация ----------
init_session_state()

# ---------- Верхняя строка с авторизацией (правая часть) ----------
def render_top_bar():
    if st.session_state.token and st.session_state.user:
        user = st.session_state.user
        col1, col2, col3 = st.columns([7, 2, 1])
        with col2:
            st.write(f"**{user.get('name', user.get('email'))}**")
        with col3:
            avatar_url = user.get("avatar_url", "")
            if avatar_url:
                st.image(avatar_url, width=40)
            else:
                st.markdown(
                    "<div style='width:40px;height:40px;border-radius:50%;background-color:gray;'></div>",
                    unsafe_allow_html=True,
                )
            # Всплывающее меню при клике на аватарку
            with st.popover("⚙️"):
                if st.button("Профиль"):
                    st.session_state.show_profile = True
                if st.button("Настройки"):
                    st.session_state.show_settings = True
    else:
        # Кнопки «Войти» и «Регистрация» – всегда на одной строке
        col_empty, col_login, col_register = st.columns([7, 1, 1])
        with col_login:
            if st.button("Войти", key="btn_login"):
                st.session_state.show_login = True
        with col_register:
            if st.button("Регистрация", key="btn_register"):
                st.session_state.show_register = True

# ---------- Модальные окна (показываются при нажатии на кнопки) ----------
def show_login_dialog():
    with st.expander("Вход", expanded=True):
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Пароль", type="password", key="login_password")
        if st.button("Войти", key="login_submit"):
            payload = {"email": email, "password": password}
            response = api_request("POST", "/auth/login", json=payload)
            if response and "access_token" in response:
                st.session_state.token = response["access_token"]
                # После входа сразу получаем профиль
                user_data = api_request("GET", "/profile/")
                if user_data:
                    st.session_state.user = user_data
                st.success("Успешный вход!")
                st.rerun()
            else:
                st.error("Неверный email или пароль")
        if st.button("Отмена", key="cancel_login"):
            st.session_state.show_login = False

def show_register_dialog():
    with st.expander("Регистрация", expanded=True):
        email = st.text_input("Email", key="reg_email")
        password = st.text_input("Пароль", type="password", key="reg_password")
        if st.button("Зарегистрироваться", key="reg_submit"):
            payload = {"email": email, "password": password}
            response = api_request("POST", "/auth/register", json=payload)
            if response:
                st.success("Регистрация успешна! Теперь войдите.")
                st.session_state.show_register = False
                st.session_state.show_login = True
                st.rerun()
        if st.button("Отмена", key="cancel_register"):
            st.session_state.show_register = False

def show_profile_dialog():
    with st.expander("Профиль", expanded=True):
        user = st.session_state.user
        if not user:
            st.warning("Пользователь не найден. Войдите заново.")
            if st.button("Закрыть"):
                st.session_state.show_profile = False
            return
        st.write(f"**Email:** {user['email']}")
        st.write(f"**Дата регистрации:** {user.get('created_at', 'неизвестно')}")
        name = st.text_input("Имя", value=user.get("name", ""))
        avatar_url = st.text_input("URL аватарки", value=user.get("avatar_url", ""))
        if st.button("Сохранить профиль"):
            update_data = {}
            if name != user.get("name"):
                update_data["name"] = name
            if avatar_url != user.get("avatar_url"):
                update_data["avatar_url"] = avatar_url
            if update_data:
                resp = api_request("PATCH", "/profile/", json=update_data)
                if resp:
                    st.session_state.user = resp
                    st.success("Профиль обновлён")
                    st.rerun()
        st.write("---")
        st.write("**Сменить пароль**")
        old_pw = st.text_input("Старый пароль", type="password", key="old_pw")
        new_pw = st.text_input("Новый пароль", type="password", key="new_pw")
        if st.button("Сменить пароль"):
            pw_resp = api_request("PATCH", "/profile/password", json={
                "old_password": old_pw,
                "new_password": new_pw
            })
            if pw_resp:
                st.success("Пароль изменён")
        if st.button("Закрыть", key="close_profile"):
            st.session_state.show_profile = False

def show_settings_dialog():
    with st.expander("Настройки", expanded=True):
        user = st.session_state.user
        if not user:
            st.warning("Пользователь не найден. Войдите заново.")
            if st.button("Закрыть"):
                st.session_state.show_settings = False
            return
        current_theme = user.get("theme", "system")
        theme = st.selectbox(
            "Тема оформления",
            ["light", "dark", "system"],
            index=["light", "dark", "system"].index(current_theme)
        )
        if st.button("Сохранить тему"):
            resp = api_request("PATCH", "/profile/", json={"theme": theme})
            if resp:
                st.session_state.user = resp
                st.success("Тема изменена")
                st.rerun()
        if st.button("Закрыть", key="close_settings"):
            st.session_state.show_settings = False

# ---------- Основной рендер ----------
render_sidebar()          # левая панель с навигацией и логотипом
render_top_bar()          # правый верхний угол с кнопками/профилем

# Модальные окна
if st.session_state.show_login:
    show_login_dialog()
if st.session_state.show_register:
    show_register_dialog()
if st.session_state.show_profile:
    show_profile_dialog()
if st.session_state.show_settings:
    show_settings_dialog()

# Контент выбранной вкладки
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