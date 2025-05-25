import os
import tempfile
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

def single_image():

    st.subheader("単一画像処理")
    session = st.session_state["session"]
    st.session_state.upload_success = False

    # 画像ファイルのアップロード
    uploaded_file = st.file_uploader(
        label='Upload your Image here',
        type=['jpg', 'jpeg', 'png', 'webp', 'gif'],
        accept_multiple_files=False
    )

    # アップロードされたファイルが存在場合
    if uploaded_file is not None:
        
        file_name = uploaded_file.name
        ext = os.path.splitext(file_name)[1]
        
        # 一時ファイルに保存
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_file_path = tmp_file.name
        
        # Snowflakeの STAGE へ PUT（ファイルアップロード）
        put_sql = f"""
            PUT 'file://{tmp_file_path}'
            @{os.environ["SNOWFLAKE_DATABASE"]}.{os.environ["SNOWFLAKE_SCHEMA"]}.{os.environ["SNOWFLAKE_STAGE"]}
            AUTO_COMPRESS=FALSE
            OVERWRITE=TRUE
        """
        try:
            with st.spinner("処理中..."):
                result = session.sql(put_sql).collect()
                st.success(f"{file_name} を Stage にアップロードしました。")
                st.session_state.upload_success = True
        except Exception as e:
            st.error(f"アップロードに失敗しました: {e}")
            st.session_state.upload_success = False
        finally:
            os.remove(tmp_file_path)  # 一時ファイル削除
        
    if st.session_state.upload_success:
        user_prompt = st.text_area("プロンプトを入力してください", "100文字程度でキャプションを生成してください。")
        if st.button("実行", key="single_image"):
            try:
                with st.spinner("処理中..."):
                    result = session.sql(f"""
                        SELECT SNOWFLAKE.CORTEX.COMPLETE('claude-3-5-sonnet',
                        '{user_prompt}',
                        TO_FILE('@{os.environ["SNOWFLAKE_STAGE"]}', '{os.path.basename(tmp_file_path)}'));
                    """
                    ).collect()
                    st.subheader("結果")
                    st.write(result[0][0])
            except Exception as e:
                st.error(f"処理中にエラーが発生しました: {e}")