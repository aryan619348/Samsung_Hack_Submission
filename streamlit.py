import streamlit as st
import os
import json
import pandas as pd
import plotly.graph_objects as go
from call_processing import processing

def file_selector(folder_path='calls_recorded/'):
    filenames = os.listdir(folder_path)
    selected_filename = st.selectbox('Select a file', filenames)
    return os.path.join(folder_path, selected_filename)

filename = file_selector()
st.write('You selected `%s`' % filename)

if st.button('Process the file'):
    st.write("Processing")
    temp_json = processing(filename)
    answer = json.loads(temp_json)

    # Summary tab
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Summary", "Query Type", "Agent Score", "Advice to Agent", "Next Step", "Email"])
    with tab1:
        st.subheader(':blue[Summary]')
        st.write(answer["Summary"], "\n\n\n")
        st.subheader(':blue[Problem]')
        st.write(answer["ProblemsFacedByCustomer"], "\n\n\n")
        st.subheader(':blue[Solution]')
        st.write(answer["SolutionFound"])

    # Query Type tab
    with tab2:
        st.subheader(':orange[Query Type]')
        query_types = {
            "Order_related_query": answer.get("Order_related_query", False),
            "Product_related_queries": answer.get("Product_related_queries", False),
            "Refund_related_queries": answer.get("Refund_related_queries", False),
            "Shipping_related_queries": answer.get("Shipping_related_queries", False),
            "Solution_found": answer.get("Solution_found", False)
        }
        st.table(query_types)
    # Agent Score tab
    with tab3:
        tab7, tab8= st.tabs(["Average", "Individual"])
        with tab7:
            st.subheader(':green[Cummulated Agent Score]')
            communication_score = (answer["Communication"]["Clarity"] + answer["Communication"]["Tone"] + answer["Communication"]["Active Listening"]) / 3
            knowledge_score = (answer["Knowledge"]["Product/Service understanding"] + answer["Knowledge"]["Accuracy"]) / 2
            problem_solving_score = (answer["Problem Solving"]["Effectiveness"] + answer["Problem Solving"]["Proactive approach"]) / 2
            overall_score = (communication_score + knowledge_score + problem_solving_score + answer["Adherence"] + (answer["Empathy"]["Displays empathy"] + answer["Empathy"]["Customer focus"]) / 2 + (answer["Closure"]["Ends calls well"] + answer["Closure"]["Follow-up if needed"]) / 2) / 6

            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="Overall Score", value=round(overall_score, 2), delta=None)
                st.metric(label="Communication Score", value=round(communication_score, 2), delta=None)
                st.metric(label="Knowledge Score", value=round(knowledge_score, 2), delta=None)
                st.metric(label="Problem Solving Score", value=round(problem_solving_score, 2), delta=None)
            with col2:
                fig = go.Figure(data=[
                    go.Bar(name='Score', x=['Communication', 'Knowledge', 'Problem Solving', 'Adherence', 'Empathy', 'Closure'], y=[communication_score, knowledge_score, problem_solving_score, answer["Adherence"], (answer["Empathy"]["Displays empathy"] + answer["Empathy"]["Customer focus"]) / 2, (answer["Closure"]["Ends calls well"] + answer["Closure"]["Follow-up if needed"]) / 2])
                ])
                fig.update_layout(height=400, width=500)
                st.plotly_chart(fig, use_container_width=True)
        with tab8:
            st.subheader(':green[Communication]')
            st.write("Clarity -", answer["Communication"]["Clarity"])
            st.write("Tone -", answer["Communication"]["Tone"])
            st.write("Active Listening -", answer["Communication"]["Active Listening"],"\n")
            st.subheader(':green[Knowledge]')
            st.write("Product/Service understanding -", answer["Knowledge"]["Product/Service understanding"])
            st.write("Accuracy -", answer["Knowledge"]["Accuracy"])
            st.subheader(':green[Problem Solving:]')
            st.write("Effectiveness -", answer["Problem Solving"]["Effectiveness"])
            st.write("Proactive approach -", answer["Problem Solving"]["Proactive approach"])
            st.subheader(':green[Adherence]')
            st.write("\nAdherence -", answer["Adherence"])
            st.subheader(':green[Empathy]')
            st.write("Displays empathy -", answer["Empathy"]["Displays empathy"])
            st.write("Customer focus -", answer["Empathy"]["Customer focus"])
            st.subheader(':green[Closure]')
            st.write("Ends calls well -", answer["Closure"]["Ends calls well"])
            st.write("Follow-up if needed -", answer["Closure"]["Follow-up if needed"])

    # Advice to Agent tab
    with tab4:
        st.subheader(':purple[Advice to Agent]')
        st.write(answer["CustomerAgentAdvice"])

    # Next Step tab
    with tab5:
        st.subheader(':blue[Next Step]')
        st.write(answer["NextSteps"])

    # Email tab
    with tab6:
        st.subheader(':orange[Email]')
        st.write('*Subject*:-', answer["SubjectLine"])
        st.write(answer["Email"])

