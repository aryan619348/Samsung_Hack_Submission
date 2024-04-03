# Python Repo Setup Guide

Welcome to the final Submision of the Samsung Generative AI Hackathon-Voice Technology


To execute the code you need to setup the following please:

1. **Setup Twilio Account:**
[![IMAGE ALT TEXT HERE](http://img.youtube.com/vi/dYdb7bicVyo/0.jpg)](http://www.youtube.com/watch?v=dYdb7bicVyo)

2. Setup Ngrok: [Ngrok Documentation](https://ngrok.com/download)

3. Get API Key for Assembly AI: [Assembly AI Documentation](https://www.assemblyai.com/docs/api-reference)

4. Get API Key for ElevenLabs: [ElevenLabs API Documentation](https://elevenlabs.io/api)

5. Get API Key for OpenAI: [OpenAI API Documentation](https://platform.openai.com/docs/api-reference)



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




