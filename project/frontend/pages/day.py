import streamlit as st
from api_client import api_request

def render_day_tab():
    st.subheader("Цели на день")
    theme = st.session_state.user.get("theme", "system") if st.session_state.user else "system"
    timer_color = "#FFFFFF" if theme == "dark" else "#000000"
    st.components.v1.html(
        f"""
        <div id="day-timer" style="font-size:16px; margin-bottom:12px; color: {timer_color};"></div>
        <script>
        function updateDayTimer() {{
            const now = new Date();
            const midnight = new Date(now);
            midnight.setHours(24, 0, 0, 0);
            const diff = midnight - now;
            if (diff <= 0) {{
                document.getElementById("day-timer").innerHTML = "Время истекло!";
                return;
            }}
            const hours = Math.floor(diff / 3600000);
            const minutes = Math.floor((diff % 3600000) / 60000);
            const seconds = Math.floor((diff % 60000) / 1000);
            document.getElementById("day-timer").innerHTML =
                "Осталось до конца дня: <b>" +
                String(hours).padStart(2,'0') + ":" +
                String(minutes).padStart(2,'0') + ":" +
                String(seconds).padStart(2,'0') + "</b>";
        }}
        updateDayTimer();
        setInterval(updateDayTimer, 1000);
        </script>
        """,
        height=35,
    )

    goals = api_request("GET", "/goals/period/day") or []

    goals.sort(key=lambda g: not g.get("is_pinned", False))

    filter_option = st.radio("Показать:", ["Все", "Активные", "Завершённые"], horizontal=True, key="day_filter")
    filtered_goals = goals
    if filter_option == "Активные":
        filtered_goals = [g for g in goals if not g.get("is_completed")]
    elif filter_option == "Завершённые":
        filtered_goals = [g for g in goals if g.get("is_completed")]

    for goal in filtered_goals:
        pinned = goal.get("is_pinned", False)
    # --- начало нового блока ---
        theme = st.session_state.user.get("theme", "system") if st.session_state.user else "system"
        if pinned:
            if theme == "dark":
                pin_bg = "#660099"
                pin_color = "#FFFFFF"
            elif theme == "forest":
                pin_bg = "#4A7C59"
                pin_color = "#FFFFFF"
            elif theme == "ocean":
                pin_bg = "#ADD8E6"   # light blue – хорошо виден на light cyan
                pin_color = "#000000"
            elif theme == "sunset":
                pin_bg = "#FF00FF"   # оранжевый, гармонирует с панелью
                pin_color = "#000000"
            else:
                pin_bg = "#FFB300"
                pin_color = "#000000"
        with st.container():
            col1, col2, col3 = st.columns([0.5, 4.5, 2])
            with col1:
                completed = goal.get("is_completed", False)
                new_completed = st.checkbox("", value=completed, key=f"completed_{goal['id']}_day", label_visibility="collapsed")
                if new_completed != completed:
                    api_request("PATCH", f"/goals/{goal['id']}/toggle-completed")
                    st.rerun()
            with col2:
                if pinned:
                    st.markdown(
                        f"<span style='background-color: {pin_bg}; color: {pin_color}; padding: 0px 4px; border-radius: 3px;'><b>{goal['name']}</b></span>",
                        unsafe_allow_html=True
                    )
                else:
                    st.write(f"**{goal['name']}**")
            with col3:
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("📌", key=f"pin_{goal['id']}_day"):
                        api_request("PATCH", f"/goals/{goal['id']}/toggle-pinned")
                        st.rerun()
                with c2:
                    if st.button("🗑️", key=f"del_{goal['id']}_day"):
                        api_request("DELETE", f"/goals/{goal['id']}")
                        st.rerun()

    completed = [g for g in goals if g.get("is_completed")]
    if completed:
        if st.button("🗑️ Удалить все выполненные", key="clear_completed_day"):
            for g in completed:
                api_request("DELETE", f"/goals/{g['id']}")
            st.rerun()

    with st.form("add_day_goal"):
        name = st.text_input("Название")
        submitted = st.form_submit_button("Добавить цель")
        if submitted:
            if not name.strip():
                st.error("Название цели не может быть пустым")
            else:
                response = api_request("POST", "/goals/", json={"name": name.strip(), "period": "day"})
                if response is None:
                    st.error("Не удалось создать цель. Проверьте подключение к серверу и авторизацию.")
                else:
                    st.rerun()