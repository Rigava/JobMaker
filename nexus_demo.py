import streamlit as st
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain

key =st.secrets.API_KEY

llm = ChatGroq(temperature=0,groq_api_key = key,model_name = 'llama-3.1-70b-versatile')

template1 = """
I have a risk assessment to be created based in a tabular format with columns of task, hazard, severity, likelihood,
risk rating,control measure,control measure type,residual risk rating for the activity such as {input}.
Provide {number} distinct hazard and I want you to take into external consideration, factors such as {factors}.
There can be multiple control measures to mitigate impact of each hazard. The risk rating is a product of severity and likelihood. 
Severity is from 1 to 5 (5 is high) and likelihood is from 1 to 5 (5 is high). 
Control measure type can be either elimination of hazards, substitution of activity, process measure to control the hazard, or Personal protective equipment 
for the person. When elimination of hazards is chosen then reduce the risk rating by 90% and provide residual rating in the table. 
Similarly, for substitution reduce by 75%, for process measure to control the hazard reduce by 50%, and for Personal protective equipment reduce by 25%.

"""

prompt1 = PromptTemplate(
    input_variables=["input", "factors", "number"],
    template=template1
)

chain1= LLMChain(
    llm=llm,
    prompt=prompt1,
    output_key="result"
)
chain = SequentialChain(
    chains=[chain1],
    input_variables=["input", "factors", "number"],
    output_variables=["result"]
)

st.header("Nexus Project")

inp = st.text_input("Activity", placeholder="Activity", label_visibility='visible')
factors = st.text_input("Factors influencing the activity", placeholder="Factors", label_visibility='visible')
num = st.slider("How many distinct solutions do you want ?", 2, 5, step=1)


if st.button("THINK", use_container_width=True):
    res = chain({"input" : inp, "factors" : factors, "number" : num})

    st.write("")
    st.write(":blue[Response]")
    st.write("")

    st.markdown(res['result'])
