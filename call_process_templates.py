#all the prompts we are using

summary_prompt="""give a summary of the call, point out the problems the customer is facing, and if a solution was found out. give the output in this json format only:
{
    "Summary": "",
    "ProblemsFacedByCustomer": "",
    "SolutionFound": ""
}

"""

analysis_prompt="""
for the below conversation please provide the following criterias as True/Fasle and mention make sure to answer all the below:
{
    "Sentiment": "",
    "Order_related_query": "",
    "Product_related_queries": "",
    "Refund_related_queries": "",
    "Shipping_related_queries": "",
    "Solution_found": "",
    "Customer_emotion": "",
    "Agent_emotion_throughout_the_call": ""
}
make sure that the output is in JSON format

"""

customer_agent_analysis= """
Please conduct an analysis of the customer service agent based on the call below measure the following and give out put in JSON format, give them a score out of 10:
{
    "Communication": {
        "Clarity": "",
        "Tone": "",
        "Active Listening": ""
    },
    "Knowledge": {
        "Product/Service understanding": "",
        "Accuracy": ""
    },
    "Problem Solving": {
        "Effectiveness": "",
        "Proactive approach": ""
    },
    "Adherence": "",
    "Empathy": {
        "Displays empathy": "",
        "Customer focus": ""
    },
    "Closure": {
        "Ends calls well": "",
        "Follow-up if needed": ""
    }
}

make sure that the output is in the JSON format given above
"""
customer_agent_advice="""
Based on the call below please suggest some ways the customer service agent can improve.
make sure you only give suggestions based on the call below and not generic information

Give the output in JSON format
{
    "CustomerAgentAdvice": ""
}
"""

steps_prompt= """
    for the given customer interactions create actionable steps that the company will now take help the customer resolve the issue. be professional and use simple language to help them understand the next steps.
    Give output in JSON format:
    {
        "NextSteps": ""
    }
"""
email_prompt= """
for the given below conversation create an email draft that will be sent to the customer 
first give a subject line.
then explain the next steps that will be taken to solve their issue.
make sure to be professional and sympathetic towards the customer.
Give output in JSON format:
    {
        "SubjectLine": "",
        "Email": ""
    }
"""