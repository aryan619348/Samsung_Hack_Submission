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
    NGROK_AUTHTOKEN="2d9Jj4yeUn3EaAcCC9AXwjcf63n_4CR1GbUEmGgzwgt21JBh1"
    TWILIO_ACCOUNT_SID="SK52c10592ad96aee73a43c73b481d58f3"
    TWILIO_API_KEY_SID="wT00V5gPqeFYPAFubgBDIrx6C24RQKGF"
    TWILIO_API_SECRET="wT00V5gPqeFYPAFubgBDIrx6C24RQKGF"
    ASSEMBLYAI_API_KEY="3cb72195eb7445668b39da19c9c3cee0"
    TWILIO_NUMBER="+14843783308"
    OPENAI_API_KEY="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"

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




