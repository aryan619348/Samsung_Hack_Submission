# Python Repo Setup Guide

Follow these steps to set up and run the Python repository:

1. **Clone Repository:**
   ```bash
   git clone https://github.com/your-repo.git

2. **Install Requirements:**
    ```bash
    pip install -r requirements.txt

3. **Create Environment File:**

    ```bash
    NGROK_AUTHTOKEN=""
    TWILIO_ACCOUNT_SID=""
    TWILIO_API_KEY_SID=""
    TWILIO_API_SECRET=""
    ASSEMBLYAI_API_KEY=""
    TWILIO_NUMBER=""
    OPENAI_API_KEY=""

4. Start Ngrok:

    ```bash
    ngrok http 5000

5. Run Python Application:

    ```bash
    python main.py


6. Make a Call:
Call your Twilio number and engage in the conversation.

7. Run Streamlit Application:

    ```bash
    streamlit run streamlit.py




