from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Static input prompt
input_prompt = """
You are an expert in nutritionist where you need to see the food items from the image 
                and calculate the total calories, also provide the details of every food 
                is below format 
                
                1. Item 1 no of calories 
                2. Item 2 no of calories
                ----
                ----

"""

# Function to get response from Gemini model
def get_gemini_response(input_prompt, image_parts, user_input, model_id):
    try:
        model = genai.GenerativeModel(model_id)  # Using the model
        response = model.generate_content([input_prompt, image_parts[0], user_input])  # Getting the response from the model
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# Function to setup uploaded image for the API call
def input_image_setup(uploaded_file):
    if uploaded_file:
        return [{"mime_type": uploaded_file.type, "data": uploaded_file.getvalue()}]  # Returning image data
    raise FileNotFoundError("No image uploaded.")

# Function to list available models (for debugging purposes)
def list_available_models():
    try:
        models = genai.list_models()  # Listing the available models
        st.write("Available Models and Their Details:")
        for model in models:
            st.write(f"Model ID: {model.name}")
            st.write(f"Model Display Name: {model.display_name}")
            st.write(f"Description: {model.description}")
            st.write("---")
    except Exception as e:
        st.error(f"Error listing models: {e}")

# Streamlit App setup
st.set_page_config(page_title="AI Nutritionist App")

st.title("AI Nutritionist App")  # App heading
input_text = st.text_input("Custom Prompt (Optional): ", key="input")  # Custom prompt input
uploaded_file = st.file_uploader("Upload an image of food...", type=["jpg", "jpeg", "png"])  # File upload button

# If an image is uploaded, display it
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

# Button to get total calories from the uploaded image
if st.button("Tell me the total calories"):
    if uploaded_file:
        with st.spinner("Analyzing the image..."):
            try:
                image_data = input_image_setup(uploaded_file)  # Setting up image data
                # Using the correct multimodal model
                model_id = 'models/gemini-1.5-pro-latest'  # Multimodal model ID
                response = get_gemini_response(input_prompt, image_data, input_text, model_id)  # Getting the response
                st.subheader("AI Analysis Result:")
                st.write(response)  # Displaying the model's response
            except Exception as e:
                st.error(f"Error: {str(e)}")
    else:
        st.warning("Please upload an image first.")  # Warning if no image is uploaded

# Button to list all available models (for debugging or exploring)
if st.button("List Available Models"):
    list_available_models()
