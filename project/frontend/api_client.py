import streamlit as st
import httpx

API_BASE_URL = "http://127.0.0.1:8000"

def api_request(method, endpoint, ignore_401=False, **kwargs):
    """
    ignore_401=True нужен для запроса входа, чтобы не сбрасывать сессию
    и показать сообщение об ошибке.
    """
    headers = kwargs.pop("headers", {})
    if "token" in st.session_state and st.session_state.token:
        headers["Authorization"] = f"Bearer {st.session_state.token}"
    try:
        if method == "GET":
            r = httpx.get(f"{API_BASE_URL}{endpoint}", headers=headers, **kwargs)
        elif method == "POST":
            r = httpx.post(f"{API_BASE_URL}{endpoint}", headers=headers, **kwargs)
        elif method == "PATCH":
            r = httpx.patch(f"{API_BASE_URL}{endpoint}", headers=headers, **kwargs)
        elif method == "DELETE":
            r = httpx.delete(f"{API_BASE_URL}{endpoint}", headers=headers, **kwargs)
        else:
            return None

        if r.status_code == 401 and not ignore_401:
            st.session_state.token = None
            st.session_state.user = None
            st.rerun()

        if not r.is_success:
            detail = None
            try:
                detail = r.json().get("detail", r.text)
            except Exception:
                detail = r.text
            return {"error": True, "status_code": r.status_code, "detail": detail}

        return r.json() if r.content else {}
    except httpx.ConnectError:
        st.error("🚫 Не удалось подключиться к серверу. Убедитесь, что бэкенд запущен на http://127.0.0.1:8000")
        return None
    except Exception as e:
        st.error(f"Ошибка: {e}")
        return None