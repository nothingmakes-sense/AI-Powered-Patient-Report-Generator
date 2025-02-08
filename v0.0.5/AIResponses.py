from ollama import chat
from ollama import ChatResponse


def AIResponse(ClientName,ClientSupportPlan):
    #if its the end of month
    #



    response: ChatResponse = chat(model='llama3.1', messages=[
    {
        'role': 'user',
        'content': 'You are a care provider. Your patient is ' + ClientName + '. They are on the ' + ClientSupportPlan + ' support plan. You are required to provide service based on the agency for persons with disabilities person-centered approach. What tasks did you assist with today? limit your responce to three paragraphs. How did they react to you assisting them? limit your responce to two paragraphs. Give me a problem, action, assistance, and solution(positive or negitive) for today. what is a random question you asked the patient and their response? limit your responce to one sentence',
    }

    ##low temp question from provider

    ##high temp answer from patient.

])
    return response