from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("Google_API_key"))

# Initialize the Generative Model
model = genai.GenerativeModel('gemini-1.5-flash')

def get_gemini_response(input_text, image_data, prompt):
    response = model.generate_content([input_text, image_data[0], prompt])
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit page configuration
st.set_page_config(page_title="Multilanguage Invoice Extractor")

# Header for the app
st.header("Multilanguage Invoice Extractor")

# User input for prompt
input_text = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an image of the invoice...", type=["jpg", "jpeg", "png"])
image = ""

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

# Button for submission
submit = st.button("Tell me about the invoice")

# Input prompt for the model
input_prompt = """
You are an expert in understanding invoices. We will upload an image of an invoice, and you will have to answer any questions based on the uploaded invoice image.
"""

if submit:
    try:
        image_data = input_image_details(uploaded_file)
        response = get_gemini_response(input_text, image_data, input_prompt)
        st.subheader("The response is:")
        st.write(response)
    except Exception as e:
        st.error(f"An error occurred: {e}")
