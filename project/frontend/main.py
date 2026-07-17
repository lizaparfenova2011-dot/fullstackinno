import streamlit as st
from navigation import init_session_state, render_sidebar
from api_client import api_request

init_session_state()

# ========== НЕАВТОРИЗОВАННЫЙ ПОЛЬЗОВАТЕЛЬ ==========
if not st.session_state.token:
    st.title("🏆 GoalApp")
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
                    })
                    if response and "access_token" in response:
                        st.session_state.token = response["access_token"]
                        # получаем профиль
                        user_data = api_request("GET", "/profile/")
                        if user_data:
                            st.session_state.user = user_data
                        st.rerun()
                    else:
                        st.error("Неверный email или пароль")

    with tab2:
        with st.form("register_form"):
            email = st.text_input("Email", key="reg_email")
            password = st.text_input("Пароль", type="password", key="reg_password")
            password_confirm = st.text_input("Повторите пароль", type="password", key="reg_password_confirm")
            if st.form_submit_button("Зарегистрироваться"):
                if not email or not password:
                    st.error("Заполните email и пароль")
                elif password != password_confirm:
                    st.error("Пароли не совпадают")
                else:
                    response = api_request("POST", "/auth/register", json={
                        "email": email,
                        "password": password
                    })
                    if response:
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
            if avatar_url:
                st.image(avatar_url, width=40)
            else:
                st.markdown(
                    "<div style='width:40px;height:40px;border-radius:50%;background-color:gray;'></div>",
                    unsafe_allow_html=True,
                )
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
                if pw_resp:
                    st.success("Пароль изменён")

        if st.button("Закрыть", key="close_profile"):
            st.session_state.show_profile = False

def show_settings_dialog():
    with st.expander("Настройки", expanded=True):
        user = st.session_state.user
        if not user:
            st.warning("Пользователь не найден")
            if st.button("Закрыть"):
                st.session_state.show_settings = False
            return
        current_theme = user.get("theme", "system")
        theme = st.selectbox(
            "Тема оформления",
            ["light", "dark", "system", "forest", "ocean", "sunset"],
            index=(["light", "dark", "system", "forest", "ocean", "sunset"].index(current_theme)
                if current_theme in ["light", "dark", "system", "forest", "ocean", "sunset"]
                else 0)
        )
        if st.button("Сохранить тему"):
            resp = api_request("PATCH", "/profile/", json={"theme": theme})
            if resp:
                st.session_state.user = resp
                st.success("Тема изменена")
                st.rerun()
        if st.button("Закрыть", key="close_settings"):
            st.session_state.show_settings = False

# --- Отрисовка для авторизованного ---
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