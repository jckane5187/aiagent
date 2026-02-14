import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if api_key == None:
    raise RuntimeError("no api key found")

client = genai.Client(api_key=api_key)
model = "gemini-2.5-flash"
response = client.models.generate_content(model=model, contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.")
print(response.text)

def main():
    print("Hello from aiagent!")


if __name__ == "__main__":
    main()
