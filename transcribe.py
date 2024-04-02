import os
import assemblyai as aai
from dotenv import load_dotenv
load_dotenv()
import os
from langchain.chat_models import ChatOpenAI
from langchain.schema.messages import HumanMessage, AIMessage
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from elevenlabs import generate,Voice, VoiceSettings
from elevenlabs.client import ElevenLabs
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

from call_processing import append_to_file
import base64
from call_processing import processing


client_11 = ElevenLabs(api_key="0ad35bc556e29c959b2d69f1a95094be")
model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
embeddings = OpenAIEmbeddings()
db = FAISS.load_local("faiss_zorbo_index", embeddings,allow_dangerous_deserialization=True)
retriever = db.as_retriever()


# conversation=[{"role": "system", "content": "You are a helpful assistant."}]

# You are anprofessional call center agent. Provide excellent customer service following training guidelines:

# 1.Maintain formal and professional tone throughout. Respond in Hinglish unless otherwise specified.
# 2.Listen actively, repeat back inquiry to confirm understanding.
# 3.Provide empathetic acknowledgment of customer's situation.
# 4.Ask clarifying questions to gather additional information as needed.
# 5.Investigate thoroughly and provide clear solution/next steps.
# 6.Confirm proposed resolution is satisfactory and address any remaining concerns.
# 7.Thank customer, close positively offering further assistance.
# 8.Maintain formal and professional tone throughout. Respond in Hinglish unless otherwise specified.
# 9.if you dont have access or know the information just tell the customer that you dont have the info
# 10.Dont tell the customer to wait for an information either you have it or not give the answer immediately


template = """
You are a customer support agent that helps with user query by answering this {question} in a  crisp and professional manner and answer only about the question
answer every question in hinglish in 2 sentences or less
answer every question using the below context:
{context} 
"""
prompt = ChatPromptTemplate.from_template(template)

retrieval_chain = (
    {"context": retriever,"question":RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)


aai.settings.api_key=os.getenv('ASSEMBLYAI_API_KEY')

TWILLIO_SAMPLE_RATE = 8000 #FREQUENCY IN HERTZ
sessionid=0
def answer_call(answer):
    audio = client_11.text_to_speech.convert(
    text=answer,
    output_format= 'ulaw_8000',  
    voice_id='EXAVITQu4vr4xnSDxMaL',
    voice_settings=VoiceSettings(stability=0.71, similarity_boost=0.5, style=0.0, use_speaker_boost=True),
    model_id='eleven_multilingual_v1',
    )
    with open("output_audio.ulaw", "wb") as audio_file:
        for chunk in audio:
            audio_file.write(chunk)

def on_open(session_opened: aai.RealtimeSessionOpened):
    global sessionid
    sessionid=session_opened.session_id
    print("Session ID:",session_opened.session_id)

def on_data(transcript: aai.RealtimeTranscript):
    if not transcript.text:
        return
    
    if isinstance(transcript, aai.RealtimeFinalTranscript):
        user_question= "User Input = "+ transcript.text + "\r\n"
        append_to_file(sessionid,user_question)
        print(user_question)
        #llm_answer=retrieval_chain.invoke(transcript.text)
        answer=""
        print("Answer =" )
        for chunk in retrieval_chain.stream(transcript.text):
            answer+= chunk
            print(chunk, end="", flush=True)
        print("\n")
        # answer= "Answer = "+ llm_answer + "\r\n"
        append_to_file(sessionid,answer)
        answer_call(answer)
    else:
        print(transcript.text, end="\r")

def on_error(error: aai.RealtimeError):
    print("An error occured:", error)


def on_close():
    print(sessionid)
    #processing(sessionid)
    print("Closing Session")



class TwilioTranscriber(aai.RealtimeTranscriber):
    def __init__(self):
        super().__init__(
            on_data=on_data,
            on_error=on_error,
            on_open=on_open, 
            on_close=on_close,
            sample_rate=TWILLIO_SAMPLE_RATE,
            encoding=aai.AudioEncoding.pcm_mulaw
        )