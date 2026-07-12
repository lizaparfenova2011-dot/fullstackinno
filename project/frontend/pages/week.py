import streamlit as st
from api_client import api_request

def render_week_tab():
    st.subheader("Цели на неделю")
    goals = api_request("GET", "/goals/period/week") or []

    # Закреплённые — выше
    goals.sort(key=lambda g: not g.get("is_pinned", False))

    filter_option = st.radio("Показать:", ["Все", "Активные", "Завершённые"], horizontal=True, key="week_filter")
    filtered_goals = goals
    if filter_option == "Активные":
        filtered_goals = [g for g in goals if not g.get("is_completed")]
    elif filter_option == "Завершённые":
        filtered_goals = [g for g in goals if g.get("is_completed")]

    for goal in filtered_goals:
        pinned = goal.get("is_pinned", False)
        card_style = "background-color: #f0f0f0; border-radius: 8px; padding: 0.5rem; margin-bottom: 0.5rem;" if pinned else ""
        with st.container():
            if pinned:
                st.markdown(f"<div style='{card_style}'>", unsafe_allow_html=True)
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            with col1:
                status = "✅" if goal.get("is_completed") else "⬜"
                st.write(f"{status} **{goal['name']}**")
            with col2:
                if st.button("🔁", key=f"toggle_{goal['id']}_week"):
                    api_request("PATCH", f"/goals/{goal['id']}/toggle-completed")
                    st.rerun()
            with col3:
                if st.button("📌", key=f"pin_{goal['id']}_week"):
                    api_request("PATCH", f"/goals/{goal['id']}/toggle-pinned")
                    st.rerun()
            with col4:
                if st.button("🗑️", key=f"del_{goal['id']}_week"):
                    api_request("DELETE", f"/goals/{goal['id']}")
                    st.rerun()
            if pinned:
                st.markdown("</div>", unsafe_allow_html=True)

    completed = [g for g in goals if g.get("is_completed")]
    if completed:
        if st.button("🗑️ Удалить все выполненные", key="clear_completed_week"):
            for g in completed:
                api_request("DELETE", f"/goals/{g['id']}")
            st.rerun()

    with st.form("add_week_goal"):
        name = st.text_input("Название")
        submitted = st.form_submit_button("Добавить цель")
        if submitted:
            if not name.strip():
                st.error("Название цели не может быть пустым")
            else:
                response = api_request("POST", "/goals/", json={"name": name.strip(), "period": "week"})
                if response is None:
                    st.error("Не удалось создать цель. Проверьте подключение к серверу и авторизацию.")
                else:
                    st.rerun()