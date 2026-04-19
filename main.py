from llm_file_assistant import ask_assistant

def run_cli():
    print("File Assistant initialized. Type 'exit' to quit.\n")
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break
            
        print("Assistant is thinking...")
        
        answer = ask_assistant(user_input)
        
        print(f"\nAssistant: {answer}\n")
        print("-" * 50)

if __name__ == "__main__":
    run_cli()