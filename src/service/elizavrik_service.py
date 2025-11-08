
from langgraph.graph import StateGraph, END, START
from langchain_core.prompts import PromptTemplate

from pydantic import BaseModel


from src.service.external_api_service import ExternalApi
from src.service.ollama_service import get_ollama_llm
from src.templates.weather import weather_forecast_template


class State(BaseModel):
    question: str | None = None
    type: str | None = None
    city: str | None = None
    weather: dict | None = None
    answer: str | None = None
    end: bool | None = None


class Elizavrik():
    def __init__(self):
        self.llm = get_ollama_llm()
        self.workflow = self._create_workflow()
        self.external_api = ExternalApi()

    def _create_workflow(self) -> StateGraph:
        workflow = StateGraph(State)

        workflow.add_node("get_weather_api", self._get_weather_api)
        workflow.add_node("get_weater_forecast", self._get_weater_forecast)

        workflow.add_edge(START, "get_weather_api")
        workflow.add_edge("get_weather_api", "get_weater_forecast")
        workflow.add_edge("get_weater_forecast", END)

        return workflow.compile()

    def _get_weather_api(self, state: State) -> dict:
        weather_data = self.external_api.get_curent_weather(state.city).compact_weather()
        return {"weather": weather_data}

    def _get_weater_forecast(self, state: State):

        prompt = PromptTemplate(
            input_variables=["weather_data"],
            template=weather_forecast_template
        )

        message = prompt.format(weather_data=state.weather)
        message = self.llm.invoke(message)

        return {"answer": message.content}

    def run(self, city: str, question: str = None):
        initial_state = State(
            question=question,
            city=city,
            type="weather_forecast"
        )

        result = self.workflow.invoke(initial_state)
        return result


if __name__ == "__main__":
    elizavrik = Elizavrik()

    city = input("Введите город")
    result = elizavrik.run(city=city, question="Какая погода?")

    print("Финальный ответ:", result["answer"])
