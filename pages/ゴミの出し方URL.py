import streamlit as st

# タイトルを表示
st.title("ゴミの出し方URL")

# URLを表示
url = "https://www.city.nagoya.jp/kankyo/cmsfiles/contents/0000066/66330/06zennpe-ji.pdf"
st.markdown(f"[こちらをクリックして名古屋市のゴミ減量・資源化ガイドにアクセス]( {url} )")