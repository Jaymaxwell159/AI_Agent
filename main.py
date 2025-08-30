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

    for _ in range(20):  # Limit to 20 iterations to avoid infinite loops
        try:
            res = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt
                ),
            )

            # First, handle function calls if they exist
            if hasattr(res, "function_calls") and res.function_calls:
                for function_call_part in res.function_calls:
                    # Execute the function
                    # Print the function being called
                    print(f" - Calling function: {function_call_part.name}")
                    response_content = call_function(
                        function_call_part, verbose=verbose
                    )
                    print_verbose_content(
                        "",
                        verbose,
                        f"Response part: {response_content.parts[0]}\n",
                    )
                    # Append function response as user message
                    response_text = str(response_content.parts[0])
                    messages.append(types.Content(
                        role="user",
                        parts=[types.Part(text=response_text)]
                    ))
                # After function calls, we need to continue the loop to let the model process the results
                continue

            # Then handle candidates (model's responses)
            if hasattr(res, "candidates"):
                for candidate in res.candidates:
                    if hasattr(candidate, "content") and candidate.content:
                        print_verbose_content(
                            "", verbose, f"Content: {candidate.content}\n"
                        )
                        candidate_text = res.text if res.text else str(candidate.content)
                        messages.append(types.Content(
                            role="model",
                            parts=[types.Part(text=candidate_text)]
                        ))

            # Check if we have a final response
            if res.text:
                print("\nFinal response:")
                print(res.text)
                break
        except Exception as e:
            print(f"Error during generation: {e}")
            break

    if verbose:
        promt_token_count = res.usage_metadata.prompt_token_count
        response_token_count = res.usage_metadata.candidates_token_count
        print(f"Prompt tokens: {promt_token_count}")
        print(f"Response tokens: {response_token_count}")


if __name__ == "__main__":
    main()
