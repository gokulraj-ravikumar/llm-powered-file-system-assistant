import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from fs_tools import read_file, list_files, write_file, search_in_file

load_dotenv()
client = OpenAI()


tools = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Reads the content of a specified file and returns it along with metadata.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "The path to the file to read, e.g., 'resumes/john_doe.pdf' or './data/info.txt'."
                    }
                },
                "required": ["filepath"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "Lists all files in a specific directory. Can optionally filter by file extension.",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": "The path to the directory to scan, e.g., 'resumes' or './data'."
                    },
                    "extension": {
                        "type": "string",
                        "description": "Optional file extension to filter by (e.g., 'pdf', 'txt'). Do not include the dot."
                    }
                },
                "required": ["directory"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Writes content to a specified file. It will automatically create any missing directories in the path. If the file already exists, it will be overwritten.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "The path to the file to write to, e.g., 'output/result.txt' or './data/new_info.txt'."
                    },
                    "content": {
                        "type": "string",
                        "description": "The content to write into the file."
                    }
                },
                "required": ["filepath", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_in_file",
            "description": "Searches for a specific keyword or phrase within a file and returns the lines containing the matches.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "The path to the file to search in, e.g., 'resumes/john_doe.pdf' or './data/info.txt'."
                    },
                    "keyword": {
                        "type": "string",
                        "description": "The keyword or phrase to search for within the file."
                    }
                },
                "required": ["filepath", "keyword"]
            }
        }
    } 

]


available_functions = {
    "read_file": read_file,
    "list_files": list_files,
    "write_file": write_file,
    "search_in_file": search_in_file
}

messages = [
    {
        "role": "system", 
        "content": (
            "You are a helpful file management assistant. Use the provided tools to help the user manage their local files. "
            "IMPORTANT RULES: "
            "1. If the user asks to create or save a file, you MUST use the write_file tool. Do not just print the content to the chat. "
            "2. You can chain multiple tools together if needed. "
            "3. When outputting URLs or links, NEVER use Markdown hyperlink formatting (e.g., example.com). Always output the raw URL as plain text. "
            "4. If the user asks to read or search a resume but doesn't specify a folder, assume it is located in the 'resumes/' directory. "
            "5. If the user asks to create or save a new file but doesn't specify a folder, always save it inside the 'output/' directory. "
            "6. NEVER hallucinate or make up content for summaries. You MUST use the read_file tool to read the actual document before writing a summary about it."
        )
    }
]

def ask_assistant(user_prompt: str):
    # 1. Add the user's question to the memory
    messages.append({"role": "user", "content": user_prompt})

    # 2. Enter the Agentic Loop
    while True:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )
        
        response_message = response.choices[0].message
        
        # 3. BASE CASE: If the LLM does NOT ask for a tool, the loop ends!
        if not response_message.tool_calls:
            final_answer = response_message.content
            # Save the final answer to memory so it remembers the conversation
            messages.append({"role": "assistant", "content": final_answer})
            return final_answer

        # 4. IF WE ARE HERE: The LLM asked for one or more tools.
        # We append its request to memory so it doesn't lose context.
        messages.append(response_message)
        
        # Loop through the requested tools and execute them
        for tool_call in response_message.tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            
            print(f"--> [System] Executing tool: {function_name} with args: {function_args}")
            
            # Execute the Python function!
            function_response = function_to_call(**function_args)
            
            # Send the result back to the LLM's memory
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": json.dumps(function_response),
                }
            )
            
