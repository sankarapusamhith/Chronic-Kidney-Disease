import streamlit as st
import pandas as pd
from src.pipeline.predict import PredictPipeline
from selenium import webdriver
import time


def add_sidebar():
  st.sidebar.header("Enter patient health info")

  data = pd.read_csv("data/kidney_disease.csv")
  
  input_dict = {}

  data= data.drop(['class'], axis=1)
  with st.sidebar:
    with st.form("my_form",clear_on_submit=True):
      for i in data.columns:
        if data[i].dtype=='float64':
          input_dict[i]=st.number_input(i,value=None)
        if data[i].dtype=='object':
          input_dict[i]=st.radio(i,list(data[i].value_counts().keys()),index=None)
      submitted = st.form_submit_button("Submit")
      if submitted:
        if "" in list(input_dict.values()) or None in list(input_dict.values()):
           st.error("Enter all details in order to submit form")
        else:
          return input_dict

def main():
    st.set_page_config(
    page_title="Chronic Kidney Disease Predictor",
    layout="wide",
    initial_sidebar_state="expanded"
    )
  
    features=add_sidebar()
  
    with st.container():
        st.title("Chronic Kidney Disease Predictor")

        if features:
            predict_pipeline=PredictPipeline()
            results=predict_pipeline.predict(pd.DataFrame(features,index=[0]))
            if results[0]>0.5:
               st.error("Person may have chronic Kidney disease")
            else :
               st.success("Person is most likely clear of chronic Kidney disease")
               
            st.write("")
            st.write("")
            
            if 'clicked' not in st.session_state:
              st.session_state.clicked = False

            def click_button():
              st.session_state.clicked = True

            st.write("Want to submit another response ?")
            st.button('Click', on_click=click_button)

            if st.session_state.clicked:
              driver = webdriver.Chrome()
              driver.get(driver.getCurrentUrl());

            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("This app can assist medical professionals in making a diagnosis, but should not be used as a substitute for a professional diagnosis.")

        else:
           st.warning("To obtain the result, fill out the form completely.")

if __name__ == '__main__':
  main()