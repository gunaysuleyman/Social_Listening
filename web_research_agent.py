import requests
import time
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langgraph.prebuilt import create_react_agent

load_dotenv()  

@tool
def serper_search(query: str) -> str:
    """
    Serper API ile web araması yapar ve sonuçları döner.
    """
    API_KEY = os.getenv("SERPER_API_KEY")  
    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "q": query
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        data = response.json()
        
        results = [item["snippet"] for item in data.get("organic", [])[:3]]
        return "\n".join(results) if results else "Sonuç bulunamadı."
    else:
        return f"Error: {response.status_code}, {response.text}"


model = ChatOpenAI(
    model="gpt-4o-mini",  
    temperature=0,
    openai_api_key=os.getenv("OPENAI_API_KEY")  
)


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Respond to the user's queries."),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

tools = [serper_search]


langgraph_agent_executor = create_react_agent(
    model=model,
    tools=tools
)


def answer_question_with_retries(question: str, max_retries: int = 3):
    """
    Kullanıcının sorusuna yanıt verir. 3 kez deneme yapar.
    """
    for attempt in range(max_retries):
        print(f"Deneme {attempt + 1}...")
        try:
            messages = langgraph_agent_executor.invoke({"messages": [("human", question)]})
            return messages["messages"][-1].content  
        except Exception as e:
            print(f"Hata: {str(e)}")
        time.sleep(1)  
    return "Sonuç bulunamadı."


def main():
    print("Merhaba! Sorularınızı sorabilirsiniz. Çıkmak için 'çıkış' yazın.")
    while True:
        question = input("Sorunuzu yazın: ")
        if question.lower() == "çıkış":
            print("Görüşmek üzere!")
            break
        print("Cevap aranıyor...")
        answer = answer_question_with_retries(question)
        print(f"Cevap: {answer}")
        print("-" * 50)

if __name__ == "__main__":
    main()