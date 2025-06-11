import openai
import subprocess


openai.api_key = ".."

def get_plan_from_ai(task):
    return """PLAN:
1. Create a file named hello_agent.py
2. Write code to print "Hello from AI agent"
3. Run the file

COMMANDS:
1. echo print("Hello from AI agent") > hello_agent.py
2. python hello_agent.py
"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Free tier
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

def execute_commands(commands):
    for idx, cmd in enumerate(commands):
        print(f"\n Running: {cmd}")
        result = subprocess.run(cmd, shell=True)
        if result.returncode != 0:
            print(" Command failed.")
            return False
    return True

def main():
    task = input(" Enter your task for the AI Agent: ")
    ai_response = get_plan_from_ai(task)
    print("\n AI Agent Response:\n")
    print(ai_response)

    confirm = input("\n Approve plan? (yes/no): ")
    if confirm.lower() != "yes":
        print(" Exiting.")
        return

    
    lines = ai_response.splitlines()
    commands = []
    start_collecting = False
    for line in lines:
        if "COMMANDS:" in line:
            start_collecting = True
            continue
        if start_collecting:
            if line.strip() == "":
                break
            parts = line.strip().split(". ", 1)
            if len(parts) == 2:
                commands.append(parts[1])

    success = execute_commands(commands)

    if success:
        print(" Task completed successfully.")
    else:
        retry = input(" Task failed. Do you want to retry with error details? (yes/no): ")
        if retry.lower() == "yes":
            reason = input(" Enter the reason it failed or error message: ")
            main()  # Retry
        else:
            print(" Exiting. Bye.")

if __name__ == "__main__":
    main()
