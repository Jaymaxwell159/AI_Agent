import os
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
