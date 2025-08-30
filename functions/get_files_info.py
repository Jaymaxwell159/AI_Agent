import subprocess
import os
from google.genai import types
from config import MAX_FILE_CHARACTERS

def get_files_info(working_directory, directory="."):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_target_dir = os.path.abspath(os.path.join(working_directory, directory))

        # Ensure the target directory is within the working directory
        if not abs_target_dir.startswith(abs_working_dir):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(abs_target_dir):
            return f'Error: Directory "{directory}" does not exist or is not a directory'
        
        result = []
        for entry in os.listdir(abs_target_dir):
            entry_path = os.path.join(abs_target_dir, entry)
            try:
                is_dir = os.path.isdir(entry_path)
                file_size = os.path.getsize(entry_path)
                result.append(f"- {entry}: file_size={file_size} bytes, is_dir={is_dir}")
            except Exception as e:
                result.append(f"Error: Could not access '{entry}': {e}")

        return "\n".join(result)
    except Exception as e:
        return

def get_file_content(working_directory, file_path):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
        
        if not abs_file_path.startswith(abs_working_dir):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        with open(abs_file_path, "r", encoding="utf-8") as f:
            content = f.read(MAX_FILE_CHARACTERS + 1)
            if len(content) > MAX_FILE_CHARACTERS:
                return content[:MAX_FILE_CHARACTERS] + f"[...File \"{file_path}\" truncated at {MAX_FILE_CHARACTERS} characters]."
            return content
    except Exception as e:
        return f"Error: {e}"
    
def write_file(working_directory, file_path, content):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        
        abs_file_path = os.path.abspath(os.path.join(working_directory, file_path)) 
        if not abs_file_path.startswith(abs_working_dir):
            return f'Error: Cannot write to \"{file_path}\" as it is outside the permitted working directory'
        parent_dir = os.path.dirname(abs_file_path)
        if not os.path.isdir(parent_dir):
            return f'Error: Parent directory does not exist for \"{file_path}\"'
        
        with open(abs_file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f'Successfully wrote to \"{file_path}\" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"

def run_python_file(working_directory, file_path, args=[]):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
        if not abs_file_path.startswith(abs_working_dir):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.exists(abs_file_path):
            return f'Error: File "{file_path}" not found.'
        if not abs_file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'
        completed_process = subprocess.run(
            ["python", abs_file_path] + args,
            check=False,
            cwd=abs_working_dir,
            capture_output=True,
            text=True,
            timeout=30
        )
        output_lines = []
        output_lines.append(f"STDOUT:\n{completed_process.stdout}")
        output_lines.append(f"STDERR:\n{completed_process.stderr}")
        if completed_process.returncode != 0:
            output_lines.append(f"Process exited with code {completed_process.returncode}")
        output_str = "\n".join(output_lines).strip()
        if not completed_process.stdout and not completed_process.stderr:
            return "No output produced."
        return output_str
    except Exception as e:
        return f"Error: executing Python file: {e}"
    


schema_get_files_info = {
    "name": "get_files_info",
    "description": "Lists files in the specified directory along with their sizes, constrained to the working directory.",
    "parameters": {
        "type": "object",
        "properties": {
            "directory": {
                "type": "string",
                "description": "The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            },
        },
    },
}

schema_get_files_content = {
    "name": "get_file_content",
    "description": "Retrieves the content of a file, constrained to the working directory.",
    "parameters": {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "The path to the file to read, relative to the working directory.",
            },
        },
    },  
}    

schema_run_python_file = {
    "name": "run_python_file",  
    "description": "Executes a Python file, constrained to the working directory.",
    "parameters": { 
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "The path to the Python file to execute, relative to the working directory.",
            },
            "args": {
                "type": "array",
                "items": {
                    "type": "string"
                },
                "description": "Optional arguments to pass to the Python script."
            }
        },
    },
}

schema_write_file = {
    "name": "write_file",   
    "description": "Writes content to a file, constrained to the working directory.",
    "parameters": { 
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "The path to the file to write, relative to the working directory.",
            },
            "content": {
                "type": "string",
                "description": "The content to write to the file.",
            },
        },
    },
}

def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    function_args = dict(function_call_part.args)
    function_args["working_directory"] = "./calculator"
    func_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file,
    }
    func = func_map.get(function_name)
    if func:
        function_result = func(**function_args)
        # Create a Content object representing the tool's response, using Part.from_function_response to format the function result.
        response_content = types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result},
                )
            ],
        )
    else:
        # Create a Content object for error handling when the function name is unknown.
        response_content = types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    # Check for function_response in parts
    part = response_content.parts[0]
    if not hasattr(part, "function_response") or not hasattr(part.function_response, "response"):
        raise RuntimeError("Fatal: No function_response.response found in Content part.")
    if verbose and "result" in part.function_response.response:
        print(f"Function call result: {part.function_response.response['result']}")
    return response_content