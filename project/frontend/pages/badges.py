import streamlit as st
from api_client import api_request

def render_badges_tab():
    st.subheader("Награды")

    if st.session_state.token:
        counters = api_request("GET", "/badges/me/counters")
        if counters:
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("День", counters.get("day_count", 0))
            col2.metric("Неделя", counters.get("week_count", 0))
            col3.metric("Месяц", counters.get("month_count", 0))
            col4.metric("Год", counters.get("year_count", 0))
        else:
            st.info("Войдите, чтобы увидеть счётчики")

    all_badges = api_request("GET", "/badges/") or []
    earned_badges = []
    if st.session_state.token:
        earned_badges = api_request("GET", "/badges/me/earned") or []
    earned_ids = [b["badge_id"] for b in earned_badges]

    st.write("---")
    cols = st.columns(3)
    for i, badge in enumerate(all_badges):
        col = cols[i % 3]
        with col:
            opacity = "1.0" if badge["id"] in earned_ids else "0.3"
            st.markdown(
                f"<div style='opacity:{opacity}; text-align:center;'>",
                unsafe_allow_html=True,
            )
            if badge.get("image_url"):
                st.image(badge["image_url"], width=80)
            else:
                st.image("https://via.placeholder.com/80?text=🏅", width=80)
            st.caption(f"**{badge['name']}**")
            st.caption(badge["description"])
            if badge["id"] in earned_ids:
                st.success("Получена!")
            st.markdown("</div>", unsafe_allow_html=True)