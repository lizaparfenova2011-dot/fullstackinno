import streamlit as st
from api_client import api_request

def render_badges_tab():
    st.subheader("Награды")

    # ---------- Счётчики ----------
    if st.session_state.get("token"):
        counters = api_request("GET", "/badges/me/counters")
        if counters:
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("День", counters.get("day_count", 0))
            col2.metric("Неделя", counters.get("week_count", 0))
            col3.metric("Месяц", counters.get("month_count", 0))
            col4.metric("Год", counters.get("year_count", 0))
        else:
            st.info("Войдите, чтобы увидеть счётчики")
    else:
        st.info("Войдите, чтобы увидеть счётчики")

    st.write("---")

    # ---------- Список наград ----------
    all_badges = api_request("GET", "/badges/") or []
    earned_badges = []
    if st.session_state.get("token"):
        earned_badges = api_request("GET", "/badges/me/earned") or []
    earned_ids = [b["badge_id"] for b in earned_badges]

    if not all_badges:
        st.info("Награды пока не загружены. Перезапустите бэкенд для их создания.")
        return

    cols = st.columns(3)
    for i, badge in enumerate(all_badges):
        col = cols[i % 3]
        with col:
            earned = badge["id"] in earned_ids
            opacity = "1.0" if earned else "0.3"
            text_class = "earned-badge" if earned else ""
            st.markdown(
                f"<div style='opacity:{opacity}; text-align:center;'>",
                unsafe_allow_html=True,
            )

            # Пытаемся показать картинку, если image_url задан и не является blob-ссылкой
            img = badge.get("image_url")
            if img and not img.startswith("blob:"):
                st.image(f"images/{img}", width=80)
            st.markdown(
                f"<p class='{text_class}' style='font-weight:bold; margin:0;'>{badge['name']}</p>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"<p class='{text_class}' style='font-size:0.9em; margin:0;'>{badge['description']}</p>",
                unsafe_allow_html=True,
            )

            st.markdown("</div>", unsafe_allow_html=True)