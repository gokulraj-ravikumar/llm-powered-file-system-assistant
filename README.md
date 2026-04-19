# LLM-Powered File System Assistant

## Overview

The LLM-Powered File System Assistant is an intelligent command-line application that combines Large Language Models (LLMs) with dynamic file system operations. This project leverages OpenAI's language models and function calling capabilities to provide a natural language interface for file management and content analysis.

Users can interact with the assistant using plain English queries to read, list, search, and analyze files across the file system. The assistant intelligently determines which file operations to perform based on user intent and returns contextual responses.

## Features

- **Natural Language Interface**: Communicate with the assistant using conversational English queries
- **Multi-Format File Support**: Parse and read content from multiple file formats including TXT, PDF, and DOCX
- **File System Operations**: 
  - Read file contents with metadata
  - List files in directories with optional filtering
  - Search for text within files
  - Write content to files
- **OpenAI Integration**: Utilizes OpenAI's GPT models with function calling for intelligent task execution
- **Interactive CLI**: User-friendly command-line interface for real-time interaction
- **Metadata Extraction**: Automatically extracts and provides file metadata including size, type, and modification time

## Project Structure

```
llm-powered-file-system-assistant/
├── main.py                  # Entry point for the CLI application
├── llm_file_assistant.py   # Core LLM assistant logic with function definitions
├── fs_tools.py             # File system utility functions and parsers
├── requirements.txt        # Project dependencies
├── README.md              # This file
├── resumes/               # Sample directory containing resume files
└── output/                # Output directory for processed results
```

## Installation

### Prerequisites

- Python 3.8 or higher
- OpenAI API key

### Setup Steps

1. Clone or download the project repository
2. Navigate to the project directory
3. Create a virtual environment (recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Create a `.env` file in the project root and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

### Running the Assistant

Start the CLI application by running:
```
python main.py
```

The assistant will initialize and display a prompt. You can then enter queries in natural language.

### Example Queries

- "List all files in the resumes directory"
- "Read the content of Priya_Ramachandran_Java_Developer.txt"
- "Search for 'Python' in all resume files"
- "What are the skills mentioned in the Cloud Architect resumes?"
- "Create a summary of the AI ML Engineer resume"

### Interactive Session Example

```
File Assistant initialized. Type 'exit' to quit.

You: List all resume files
Assistant is thinking...
Assistant: I found the following resume files in the resumes directory:
- Dinesh_Subramanian_iOS_Developer.txt
- Kanimozhi_Ramachandran_Data_Engineer.txt
- Murugan_S_Cloud_Architect.txt
- Priya_Ramachandran_Java_Developer.txt
- Surya_M_Cloud_Architect.txt
- Surya_Ramachandran_Frontend_Developer.txt
- Vignesh_Natarajan_AI_ML_Engineer.txt

You: exit
Goodbye!
```

## Available Tools

The assistant has access to the following file system tools:

### read_file
Reads and returns the complete content of a specified file along with metadata (filename, type, size, modification time).

### list_files
Lists all files in a specified directory. Supports optional filtering by file extension.

### search_in_file
Searches for specific text or patterns within a file and returns matching results with context.

### write_file
Writes content to a file, supporting both creation of new files and modification of existing files.

## Dependencies

- **openai>=1.0.0**: OpenAI Python client library for API integration
- **python-dotenv>=1.0.0**: Environment variable management for API keys
- **pypdf>=4.0.0**: PDF file parsing and text extraction
- **python-docx>=1.1.0**: Microsoft Word document (.docx) reading

## Technical Details

### Function Calling Architecture

The assistant leverages OpenAI's function calling feature to dynamically invoke file system operations. The implementation follows these steps:

1. User submits a natural language query
2. The LLM analyzes the query and determines required function calls
3. Relevant file system tools are executed with appropriate parameters
4. Results are returned to the LLM for final processing
5. The assistant provides a contextual response to the user

### Supported File Types

- Text files (.txt)
- PDF documents (.pdf)
- Word documents (.docx)

## Configuration

### Environment Variables

Create a `.env` file in the project root directory with the following variable:

```
OPENAI_API_KEY=your_openai_api_key
```

The application uses `python-dotenv` to load these environment variables automatically.

### Model Configuration

By default, the assistant uses OpenAI's latest available GPT model. This can be modified in the `llm_file_assistant.py` file if needed.

## Use Cases

- **Resume Analysis**: Analyze multiple resume files to extract skills, experience, and qualifications
- **Documentation Management**: Search and retrieve information across multiple documentation files
- **Content Organization**: Organize and categorize file contents using natural language queries
- **Data Extraction**: Extract specific information from various document formats
- **Report Generation**: Create summaries and reports based on file contents

## Limitations

- Requires an active OpenAI API account and valid credentials
- PDF parsing depends on the quality and format of the PDF document
- Encrypted PDF files cannot be processed
- API costs apply based on OpenAI's usage-based pricing model

## Future Enhancements

- Support for additional file formats (Excel, JSON, CSV)
- Batch processing capabilities for multiple files
- Caching mechanism for frequently accessed files
- Custom model fine-tuning support
- Web interface alternative to CLI
- Integration with cloud storage services

## Troubleshooting

**Issue**: "Invalid API key" error
- Ensure your OpenAI API key is correctly set in the `.env` file
- Verify that the key has appropriate permissions

**Issue**: "File not found" error
- Check that the file path is correct and relative to the project directory
- Ensure the file exists before attempting to read it

**Issue**: "No text found in PDF" error
- Some PDF files may be scanned images without selectable text
- OCR capabilities would be needed to process such files
