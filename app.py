from dotenv import load_dotenv

load_dotenv()

import base64
import streamlit as st 
import os
import io
from PIL import Image
import pdf2image 
import google.generativeai as genai 

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input,pdf_content,prompt):
    model=genai.GenerativeModel('gemini-pro-vision')
    responce=model.generate_content([input,pdf_content[0],prompt])
    return responce.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        ## Convert the PDF to image
        images=pdf2image.convert_from_bytes(uploaded_file.read())

        first_page=Image[0]
        
        # Convert to bytes
        img_byte_arr =io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode() # encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
## Streamlit App
st.set_page_config(page_title="Smart Resume Analyzer & Enhancer")
st.header("Smart Resume Analyzer and Enhancer")
input_text = st.text_area("Job Description: ", key="input")

##uploaded_file = st.file_uploader("Upload Resume", type=["pdf"], key="pdf")
uploaded_file=st.file_uploader("Upload your resume(PDF)...",type=["pdf"])



if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")


submit1 = st.button("Tell Me About the Resume")

submit2 = st.button("How Can I Improve My Resume")

submit3 = st.button("Percentage match")

input_prompt1 = """
you are an experienced HR With Tech Experience to the filed of any job role from Data Science,full stack,web development
,Big Data Engineering 
DEVOPS,Data Analyst,your task is to review the provide resume the job description for this profiles.
please share your professional evaluation on whether the cadidate's profile aligns with the role.
Highlight the strengths and weaknesses of the applicant in relation to the specidied job requirements.
"""

input_prompt3 = """
Your are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of any one job role Data Science,full stack,web development
,Big Data Engineering,DEVOPS,Data Analyst and deep ATS functionality,
your task is to evaluate the resume against the provided job description. give me tha percentage of match if the resume matches job description.
First the output should come as percentage and then keywords missing and last final thoughts.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader("The Response is ")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt3,pdf_content,input_text)
        st.subheader("The Response is ")
        st.write(response)
    else:
        st.write("Please upload the resume")