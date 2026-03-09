import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a specified python file relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to the python file that will be executed by this function, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Additional, optional arguments that are provided to extend the 'commands' list within the function, which are used to run the python files",
                items=types.Schema(
                    type=types.Type.STRING,
                ),
            ),
        },
        required=["file_path"]
    ),
)

def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs

        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target_file.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", target_file]
        if args:
            command.extend(args)

        completed_process = subprocess.run(command, capture_output=True, cwd=working_dir_abs, text=True, timeout=30)

        output = []
        if completed_process.returncode != 0:
            output.append(f'Process exited with code {completed_process.returncode}')
        if not completed_process.stdout and not completed_process.stderr:
            output.append("No output produced")
        if completed_process.stdout:
            output.append(f'\nSTDOUT:{completed_process.stdout}')
        if completed_process.stderr:
            output.append(f'\nSTDERR:{completed_process.stderr}')
        
        
        return "\n".join(output)
    
    except Exception as e:
        return f'Error: executing Python file: {e}'
