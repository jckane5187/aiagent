import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
import argparse
from prompts import system_prompt
from call_functions import available_functions

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if api_key == None:
    raise RuntimeError("no api key found")

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()
user_prompt = args.user_prompt

messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

client = genai.Client(api_key=api_key)
model = "gemini-2.5-flash"
response = client.models.generate_content(model=model, contents=messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt))
if response.usage_metadata == None:
    raise RuntimeError("failed API request detected")

if args.verbose:
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

if not response.function_calls:
    print(response.text)
else:
    for func in response.function_calls:
        print(f'Calling function: {func.name}({func.args})')
    print(response.text)


def main():
    pass


if __name__ == "__main__":
    main()
