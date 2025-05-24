import streamlit as st
from dotenv import load_dotenv

from snowflake.session_manager import get_snowpark_session
from snowflake.object_initializer import init_snowflake_object
from mode.single import single_image
from mode.multiple import multiple_images

load_dotenv()

def init_page():
    st.set_page_config(
        page_title="Cortex COMPLETE Multimodal Demo", 
        page_icon="❄️"
    )
    st.header("Cortex COMPLETE Multimodal Demo ❄️")
    st.markdown("""
        SnowflakeのCortex COMPLETE Multimodal機能を使用して、画像処理タスクを実行します。
        https://docs.snowflake.com/en/user-guide/snowflake-cortex/complete-multimodal
    """)

def main():

    init_page()
    
    if "session" not in st.session_state:
        session = get_snowpark_session()
        init_snowflake_object(session)
        st.session_state["session"] = session

    tabs = st.tabs(["SINGLE", "MULTIPLE"])    

    with tabs[0]:
        single_image()
    with tabs[1]:
        multiple_images()
        pass

if __name__ == "__main__":
    main()