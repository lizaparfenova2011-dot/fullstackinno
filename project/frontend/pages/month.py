import streamlit as st
from api_client import api_request

def render_month_tab():
    st.subheader("Цели на месяц")
    # Живой таймер на 28 дней
    st.components.v1.html(
        """
        <div id="month-timer" style="font-size:16px; margin-bottom:12px;"></div>
        <script>
        const monthEnd = new Date().getTime() + 28*24*60*60*1000;
        function updateMonthTimer() {
            const now = new Date().getTime();
            const diff = monthEnd - now;
            if (diff <= 0) {
                document.getElementById("month-timer").innerHTML = "Время истекло!";
                return;
            }
            const days = Math.floor(diff / (1000*60*60*24));
            const hours = Math.floor((diff % (1000*60*60*24)) / (1000*60*60));
            const minutes = Math.floor((diff % (1000*60*60)) / (1000*60));
            const seconds = Math.floor((diff % (1000*60)) / 1000);
            document.getElementById("month-timer").innerHTML =
                "Осталось до конца месяца: <b>" + days + " дн. " +
                String(hours).padStart(2,'0') + ":" +
                String(minutes).padStart(2,'0') + ":" +
                String(seconds).padStart(2,'0') + "</b>";
        }
        updateMonthTimer();
        setInterval(updateMonthTimer, 1000);
        </script>
        """,
        height=35,
    )

    goals = api_request("GET", "/goals/period/month") or []
    goals.sort(key=lambda g: not g.get("is_pinned", False))

    filter_option = st.radio("Показать:", ["Все", "Активные", "Завершённые"], horizontal=True, key="month_filter")
    filtered_goals = goals
    if filter_option == "Активные":
        filtered_goals = [g for g in goals if not g.get("is_completed")]
    elif filter_option == "Завершённые":
        filtered_goals = [g for g in goals if g.get("is_completed")]

    for goal in filtered_goals:
        pinned = goal.get("is_pinned", False)
        with st.container():
            col1, col2, col3 = st.columns([0.5, 4.5, 2])
            with col1:
                completed = goal.get("is_completed", False)
                new_completed = st.checkbox("", value=completed, key=f"completed_{goal['id']}_month", label_visibility="collapsed")
                if new_completed != completed:
                    api_request("PATCH", f"/goals/{goal['id']}/toggle-completed")
                    st.rerun()
            with col2:
                if pinned:
                    st.markdown(
                        f"<span style='background-color: #e0e0e0; padding: 2px 8px; border-radius: 4px;'><b>{goal['name']}</b></span>",
                        unsafe_allow_html=True
                    )
                else:
                    st.write(f"**{goal['name']}**")
            with col3:
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("📌", key=f"pin_{goal['id']}_month"):
                        api_request("PATCH", f"/goals/{goal['id']}/toggle-pinned")
                        st.rerun()
                with c2:
                    if st.button("🗑️", key=f"del_{goal['id']}_month"):
                        api_request("DELETE", f"/goals/{goal['id']}")
                        st.rerun()

    completed = [g for g in goals if g.get("is_completed")]
    if completed:
        if st.button("🗑️ Удалить все выполненные", key="clear_completed_month"):
            for g in completed:
                api_request("DELETE", f"/goals/{g['id']}")
            st.rerun()

    with st.form("add_month_goal"):
        name = st.text_input("Название")
        submitted = st.form_submit_button("Добавить цель")
        if submitted:
            if not name.strip():
                st.error("Название цели не может быть пустым")
            else:
                response = api_request("POST", "/goals/", json={"name": name.strip(), "period": "month"})
                if response is None:
                    st.error("Не удалось создать цель. Проверьте подключение к серверу и авторизацию.")
                else:
                    st.rerun()