import pickle
import numpy as np
import streamlit as st
import pandas as pd
from src.pipeline.predict import PredictPipeline

def add_sidebar():
  st.sidebar.header("Enter patient health info")

  data = pd.read_csv("data/kidney_disease.csv")
  
  input_dict = {}

  data= data.drop(['class'], axis=1)
  with st.sidebar:
    with st.form("my_form"):
      for i in data.columns:
        if data[i].dtype=='float64':
          input_dict[i]=st.text_input(i)
        if data[i].dtype=='object':
          input_dict[i]=st.radio(i,list(data[i].value_counts().keys()))
    
      submitted = st.form_submit_button("Submit")
      if submitted:
        return input_dict

def main():
    st.set_page_config(
    page_title="Chronic Kidney Disease Predictor",
    layout="wide",
    initial_sidebar_state="expanded"
    )
  
    inp=add_sidebar()
  
    with st.container():
        st.title("Chronic Kidney Disease Predictor")

        if inp:
            predict_pipeline=PredictPipeline()
            results=predict_pipeline.predict(pd.DataFrame(inp,index=[0]))
            st.write("Probability of having disease: ", results[0])
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("This app can assist medical professionals in making a diagnosis, but should not be used as a substitute for a professional diagnosis.")

        else:
           st.write("submit the form with all details to get the result")

if __name__ == '__main__':
  main()