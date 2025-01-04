import streamlit as st
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain

key =st.secrets.API_KEY

llm = ChatGroq(temperature=0,groq_api_key = key,model_name = 'llama-3.1-70b-versatile')

template1 = """
I have a risk assessment to be created based in a tabular format with columns of task, hazard, severity, likelihood,
risk rating,control measure,control measure type,residual risk rating for the activity such as {input}.
Provide {number} distinct control and I want you to take into external consideration, factors such as {factors}
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
factors = st.text_input("Hazards concerning the input", placeholder="Hazards", label_visibility='visible')
num = st.slider("How many distinct solutions do you want ?", 2, 5, step=1)


if st.button("THINK", use_container_width=True):
    res = chain({"input" : inp, "factors" : factors, "number" : num})

    st.write("")
    st.write(":blue[Response]")
    st.write("")

    st.markdown(res['result'])
