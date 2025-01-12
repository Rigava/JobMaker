import streamlit as st
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain_core.output_parsers import JsonOutputParser
import json
import pandas as pd
# Define the expected JSON structure
parser = JsonOutputParser(pydantic_object={
    "type": "object",
    "properties": {
        "Task": {"type": "string"},
        "Hazard": {"type": "string"},
        "Severity": {"type": "number"},
        "Likelihood": {"type": "number"}
    }
})
key =st.secrets.API_KEY

llm = ChatGroq(temperature=0,groq_api_key = key,model_name = 'llama-3.1-70b-versatile')

template1 = """
I have a risk assessment to be created based in a tabular format with columns of task, hazard, severity, likelihood,
risk rating,control measure,control measure type,residual risk rating for the activity such as {input} in the {industry}.
Provide {number} distinct hazard based on the work area {condition} and I want you to take into external consideration, factors such as {factors}.
There can be multiple control measures to mitigate impact of each hazard. The risk rating is a product of severity and likelihood. 
Severity is from 1 to 5 (5 is high) and likelihood is from 1 to 5 (5 is high). 
Control measure type can be either elimination of hazards, substitution of activity, process measure to control the hazard, or Personal protective equipment 
for the person. When elimination of hazards is chosen then reduce the risk rating by 90% and provide residual rating in the table. 
Similarly, for substitution reduce by 75%, for process measure to control the hazard reduce by 50%, and for Personal protective equipment reduce by 25%.
When there are multiple controls measures for a hazard, then the residual risk calculation for first controls is applied on the original risk rating. 
However, for the subsequent controls to the same hazard, the residual risk calculation of the 2nd controls is applied on the residual risk of 1st controls.
The output should only be in a table format and no text.
"""

prompt1 = PromptTemplate(
    input_variables=["input","industry","condition","factors","number"],
    template=template1
)

chain1= LLMChain(
    llm=llm,
    prompt=prompt1,
    output_key="result"
)

template2 = """
Extract the following details from the provided {prop_soln} and Provide the output in a table format
"Task": ,
"Hazard": ,
"Severity": ,
"Likelihood":,
"risk rating":,
"control measure":,
"control measure type":,
"residual risk rating": 

"""

prompt2 = PromptTemplate(
    input_variables=["prop_soln"],
    template=template2
)

chain2 = LLMChain(
    llm = llm,
    prompt=prompt2,
    output_key="result"
)

chain = SequentialChain(
    chains=[chain1],
    input_variables=["input","industry","condition","factors","number"],
    output_variables=["result"]
)

def get_df_response(data):
    # Example tabular data (can be replaced with your actual LLM response)
    return pd.DataFrame(data)


st.header("Nexus Project")

inp = st.text_input("Activity", placeholder="Activity", label_visibility='visible')
ind = st.text_input("Industry", placeholder="Logistic", label_visibility='visible')
con = st.text_input("Condition", placeholder="Inside an enclosed space", label_visibility='visible')
factors = st.text_input("Factors influencing the activity", placeholder="Factors", label_visibility='visible')
num = st.slider("How many distinct hazards do you want ?", 1, 8, step=1)


if st.button("THINK", use_container_width=True):
    res = chain({"input" : inp, "industry":ind, "condition":con, "factors" : factors, "number" : num})

    st.write("")
    st.write(":blue[Response]")
    st.write("")
    st.markdown(type(res['result']))
    st.markdown(res['result'])
    
  

    
    


