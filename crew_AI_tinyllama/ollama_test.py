from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="tinyllama")
response = llm.invoke("What's a healthy breakfast?")
print(response)
