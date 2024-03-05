import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file,get_table_data
import streamlit as st
from langchain_community.callbacks import get_openai_callback
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain
from src.mcqgenerator.logger import logging

#loading json file

with open ("D:\Project\LLM-Projects\MCQ Generator\Response.json",'r') as file:
    RESPONSE_JSON=json.load(file)

#creating title    
st.title("MCQ Generator from PDF or Txt file")

#creating a form
with st.form("user_inputs"):
    #file upload
    uploaded_file=st.file_uploader("Upload as PDF or txt file")

    #Input fields
    mcq_count=st.number_input("Number of MCQs", min_value=3, max_value=50)

    #Subject
    subject=st.text_input("Insert subject", max_chars=20)

    #quiz_tone
    tone=st.text_input("Complexity Level of Questions",max_chars=20, placeholder="Simple")

    #Add Button
    button=st.form_submit_button("Create MCQs")

    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("loading.."):
            try:
                text=read_file(uploaded_file)

                with get_openai_callback() as cb:
                    response=generate_evaluate_chain(
                          {
                          "text": text,
                          "number": mcq_count,
                          "subject":subject,
                          "tone": tone,
                          "response_json": json.dumps(RESPONSE_JSON)
                              }
                        )
            except Exception as e:
                traceback.print_exception(type(e),e,e.__traceback__)
                st.error("Error")
            else:
                if isinstance(response,dict):
                    quiz=response.get("quiz", None)
                    if quiz is not None:
                        table_data=get_table_data(quiz)
                        if table_data is not None:
                            df=pd.DataFrame(table_data)
                            df.index=df.index+1
                            st.table(df)

                            st.text_area("Review", value=response['review'])
                        else:
                            st.error("Error in the table data")
                    
                    else:
                        st.write(response)

                        



