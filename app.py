import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf

from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_repsonse(input):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text



input_prompt = """
Hey! Act as a skilled and experienced ATS (Application Tracking System) with expertise in the tech field, 
including software engineering, data science, data analysis, and big data engineering. 
Your task is to evaluate resumes based on the given job description. 
Keep in mind that the job market is highly competitive, and your goal is to provide the best assistance for improving the resumes. 
Assign a percentage matching score based on the JD and identify any missing keywords with high accuracy.

Please provide your evaluation in a single string with the following structure:
{"JD Match": "%", "Missing Keywords": [], "Profile Summary": ""}
"""


st.title("IntelliScan ATS")
st.text("Revitalize Your CV with ATS Optimization")
jd=st.text_area("Paste the Job Description")
uploaded_file=st.file_uploader("Upload Your Resume or CV",type="pdf",help="Please uplaod the pdf")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text=input_pdf_text(uploaded_file)
        response=get_gemini_repsonse(input_prompt)
        st.subheader(response)