from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI,OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
import json
from call_process_templates import summary_prompt, analysis_prompt, customer_agent_analysis,customer_agent_advice,steps_prompt,email_prompt

from dotenv import load_dotenv
load_dotenv()

template = """
{input_prompt}
{call_text}
"""
prompt= ChatPromptTemplate.from_template(template)
model = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)
retrieval_chain = (
{"call_text": RunnablePassthrough(),"input_prompt": RunnablePassthrough()}
| prompt
| model
| StrOutputParser()
)

def append_to_file(filename, content):
    filename= "calls_recorded/" +str(filename) + ".txt"
    try:
        with open(filename, 'a') as file:
            file.write(content + '\n')
        #print(f"Appended '{content}' to {filename}")
    except IOError:
        print("Error: Could not append to file")

def extract_text_from_txt(filename):
    # filename= str(filename) + ".txt"
    try:
        with open(filename, 'r') as file:
            text = file.read()
            return text
    except FileNotFoundError:
        return "File not found."
    
def processing(filename):
    print(filename)
    call_text = extract_text_from_txt(filename)
    # print(call_text)
    answer1=retrieval_chain.invoke({"input_prompt": summary_prompt, "call_text": call_text})
    answer2=retrieval_chain.invoke({"input_prompt": analysis_prompt, "call_text": call_text})
    answer3=retrieval_chain.invoke({"input_prompt": customer_agent_analysis, "call_text": call_text})
    answer4=retrieval_chain.invoke({"input_prompt": customer_agent_advice, "call_text": call_text})
    answer5=retrieval_chain.invoke({"input_prompt": steps_prompt, "call_text": call_text})
    answer6=retrieval_chain.invoke({"input_prompt": email_prompt, "call_text": call_text})
    json_objects = [answer1, answer2, answer3, answer4, answer5, answer6]
    combined_obj = {}
    for answer in json_objects:
        js_obj = json.loads(answer)
        combined_obj.update(js_obj)
    
    combined_obj["id"] = str(filename)
    combined_json = json.dumps(combined_obj)
    print(combined_json)
    return combined_json









