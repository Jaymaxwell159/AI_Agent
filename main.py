import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import system_prompt  # Make sure to import your system prompt
import functions.get_files_info
from functions.get_files_info import call_function
from functions.print_verbose_content import print_verbose_content

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

available_functions = types.Tool(
    function_declarations=[
        functions.get_files_info.schema_get_files_info,
        functions.get_files_info.schema_get_files_content,
        functions.get_files_info.schema_write_file,
        functions.get_files_info.schema_run_python_file,
    ]
)

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

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

    print_verbose_content("", verbose, f"User prompt: {prompt}")

    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]

    res = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )
    
    # Check for function calls
    if hasattr(res, "function_calls") and res.function_calls:
        for function_call_part in res.function_calls:
            print_verbose_content(
                f" - Calling function: {function_call_part.name}",
                verbose,
                f"Calling function: {function_call_part.name}({function_call_part.args})",
            )
            function_responses = call_function(function_call_part, verbose=verbose)
    else:
        print(res.text)

    if verbose:
        promt_token_count = res.usage_metadata.prompt_token_count
        response_token_count = res.usage_metadata.candidates_token_count
        print(f"Prompt tokens: {promt_token_count}")
        print(f"Response tokens: {response_token_count}")


if __name__ == "__main__":
    main()
