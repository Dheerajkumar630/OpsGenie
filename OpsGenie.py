import streamlit as st
import pandas as pd
import google.generativeai as genai
import os

# Configure page layout to be wider
st.set_page_config(layout="wide")

# Configure API key (use environment variables for security)
api_key = os.getenv("GENAI_API_KEY",
                    "AIzaSyAjI68HV0sCLFW9G5tVWJOlcWh2QbQm74w")  # Retrieve API key from environment variable
if not api_key:
    st.error("API key not set. Please set the 'GENAI_API_KEY' environment variable.")
else:
    genai.configure(api_key=api_key)  # Use the API key

# Model configuration (outside the function for efficiency)
generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 2048  # Adjust as needed
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config=generation_config,
)


def process_data_and_prompt(df, prompt):
    """Processes DataFrame and prompt with Gemini, handling visuals."""
    if df is not None:  # Check if a DataFrame was provided
        df_string = df.to_string()  # Or another suitable string representation
        full_prompt = f"{prompt}\n\nData:\n{df_string}"
    else:
        full_prompt = prompt  # Use the prompt directly if no DataFrame

    chat_session = model.start_chat(history=[])  # New session for each prompt
    response = chat_session.send_message(full_prompt)
    return response.text


# Custom CSS for layout
st.markdown("""
   <style>
   .main {
       padding: 0;
   }
   .stTextArea textarea {
       border-radius: 10px;
   }
   .stButton button {
       border-radius: 20px;
       width: 100px !important;
       height: 45px !important;
   }
   div[data-testid="stSidebarContent"] {
       background-color: white !important;  /* Changed to white */
   }
   section[data-testid="stSidebar"] {
       background-color: white !important;  /* Changed to white */
   }
   .st-emotion-cache-1v04i6g {
       color: black !important;
   }
   .st-emotion-cache-1v04i6g p {
       color: black !important;
   }
   button.st-emotion-cache-1aw8i8e {
       color: black !important;
   }
   .st-emotion-cache-u8hs99 {
       color: black !important;
   }
   .st-emotion-cache-u8hs99 svg {
       fill: black !important;
   }
   .st-emotion-cache-u8hs99 path {
       fill: black !important;
   }
   button[kind="secondary"] svg path {
       fill: black !important;
   }

   /* Style for main container to allow absolute positioning */
   .stMainBlockContainer {
       position: relative;
   }


   .st-emotion-cache-7czcpc evl31sl1 {
        left: 500px;
   }

   /* Style for OpsGenie logo container */
   .opsgenie-logo {
       position: absolute;
       top: 0;
       left: 500px;
       z-index: 1000;
       padding: 10px;
   }
   </style>
""", unsafe_allow_html=True)

# Sidebar for file upload and data preview
with st.sidebar:
    # Add Innovapptive logo
    image_path = "innovapptive logo.png"  # Update path to your image
    try:
        st.image(image_path, width=250)
    except Exception as e:
        st.error(f"Error loading image: {e}")
        st.title("Data Upload")  # Fallback if image fails to load

    uploaded_file = st.file_uploader("Upload CSV", type="csv")
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
        except pd.errors.ParserError:
            st.error("Invalid CSV format.")
            df = None
        except Exception as e:
            st.error(f"An error occurred: {e}")
            df = None
    else:
        df = None

# Add OpsGenie logo directly in main container
st.markdown('<div class="opsgenie-logo">', unsafe_allow_html=True)
ops_genie_image_path = "OpsGenie-Logo-3.png"
try:
    st.image(ops_genie_image_path, width=180)
except Exception as e:
    st.error(f"Error loading image: {e}")
    st.title("OpsGenie Assistant")
st.markdown('</div>', unsafe_allow_html=True)

# Create a container for chat history
chat_container = st.container()

# Display chat history and responses
with chat_container:
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    for message in st.session_state.chat_history:
        st.write(message)

# Input area at the bottom
with st.container():
    st.markdown("<br>" * 2, unsafe_allow_html=True)  # Add some space

    # Create a horizontal container for prompt and button
    input_container = st.container()

    # Use columns with different ratio for better layout
    with input_container:
        col1, col2 = st.columns([15, 2])  # Changed from [20, 1] to [15, 2]

        with col1:
            prompt = st.text_area("", placeholder="Enter your prompt here...", height=100, label_visibility="collapsed")

        with col2:
            # Add some vertical space to align button with textarea
            st.markdown("<br>", unsafe_allow_html=True)
            submit_button = st.button("Submit", type="primary")

if submit_button and prompt:
    with st.spinner("Processing..."):
        try:
            output = process_data_and_prompt(df, prompt)
            st.write("Response:")
            st.write(output)
        except Exception as e:
            st.error(f"An error occurred: {e}")
elif submit_button:
    st.warning("Please enter a prompt.")
