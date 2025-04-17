import streamlit as st

pages = {
    st.Page("main.py", title="Create your account"),
    st.Page("shutdown.py", title="Create your account")
}

pg = st.navigation(pages)
pg.run()