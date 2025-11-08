from langchain_amvera import ChatAmvera
from config import settings


def get_ollama_llm():
    return ChatAmvera(model=settings.llm_model, api_token=settings.llm_api_key)


if __name__ == "__main__":
    llm = get_ollama_llm()
    response = llm.invoke("Кто ты?")
    print(response.content)
