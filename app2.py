from wordcloud import WordCloud
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from bs4 import BeautifulSoup
from urllib.request import urlopen
from io import BytesIO
from PIL import Image


def main():
    try:
        tab1, tab2, tab3 = st.tabs(["DataSet", "Text", "Experimental"])
        with tab1:
            st.header("DataSet")
            uploaded_file = st.file_uploader("Upload_Csv", ["csv", "text"])
            if uploaded_file:
                df = pd.read_csv(uploaded_file)
                st.write(df)
                selected_column = st.selectbox("Select Column", df.columns)
                try:
                    text = " ".join(df[selected_column])
                    function(text)
                except:
                    st.write("Please select text Data")
        with tab2:
            st.header("Text")
            text = st.text_area("Enter Text", height=200)
            button = st.button("Generate")
            if button:
                function(text)
        with tab3:
            st.header("Experimental")
            url = st.text_input("Paste or Enter url")
            if url:
                page = urlopen(url)
                html_bytes = page.read()
                html = html_bytes.decode("utf-8")
                soup = BeautifulSoup(html, "html.parser")
                text = " "
                for data in soup.find_all("p"):
                    text = text + data.get_text()
                function(text)
    except:
        print("Some error")


def function(text):
    cloud = WordCloud(width=800, height=400, background_color="white").generate(text)
    plt.imshow(cloud, interpolation="bilinear")
    plt.axis("off")
    st.set_option("deprecation.showPyplotGlobalUse", False)
    plt.show()
    st.pyplot()
    download_cloud(cloud)


def download_cloud(cloud):
    img = Image.fromarray(cloud.to_array())
    img_bytes = BytesIO()
    img.save(img_bytes, format="png")
    st.download_button("Download", img_bytes, "wordcloud.png")


if __name__ == "__main__":
    main()
