import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import system_promt  # Make sure to import your system prompt
from functions.get_files_info import schema_get_files_info

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
    ]
)

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

def main():
    print("Hello from ai-agent!")
    
    if len(sys.argv) < 2:
        print("error: No prompt provided")
        sys.exit(1)
    
    verbose = False
    if "--verbose" in sys.argv:
        verbose = True
        sys.argv.remove("--verbose")  # remove so it doesn’t mess with the prompt

    prompt = sys.argv[1]

    if verbose:
        print(f"User prompt: {prompt}")
    
    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]        

    res = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_promt),
    )
    
    # Check for function calls
    if hasattr(res, "function_calls") and res.function_calls:
        for function_call_part in res.function_calls:
            print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(res.text)
    
    if verbose:
        promt_token_count = res.usage_metadata.prompt_token_count
        response_token_count = res.usage_metadata.candidates_token_count
        print(f"Prompt tokens: {promt_token_count}")
        print(f"Response tokens: {response_token_count}")


if __name__ == "__main__":
    main()
