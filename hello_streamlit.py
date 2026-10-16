import pandas as pd
import streamlit as st
from ga import inject_ga

inject_ga()

data = st.file_uploader("upload file", type={"csv", "txt"})
if data is not None:
  df = pd.read_csv(data)
  df = df[::-1]
  df['time'] = df.index
  st.write(df)
  st.line_chart(df, x="time", y="Close")
