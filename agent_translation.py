from crewai import Agent, Task, Crew
from langchain_community.llms import Ollama

# Connect to local Llama 3
llm = Ollama(model="llama3:latest", base_url="http://localhost:11434")

# Define the agent
translator_agent = Agent(
    role="Localization Optimizer",
    goal="Translate and shorten localization strings to match length constraints",
    backstory="An AI expert in multilingual optimization",
    llm=llm,
    verbose=True
)

# Function to update .strings file
def update_strings_file(issue, new_string):
    file_path = issue["file"]
    key = issue["key"]
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Find and replace the line
        for i, line in enumerate(lines):
            if line.strip().startswith(f'"{key}" ='):
                lines[i] = f'"{key}" = "{new_string}";\n'
                break
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        return f"Updated {file_path} with {key}: {new_string}"
    except Exception as e:
        return f"Error updating {file_path}: {str(e)}"

# Create tasks dynamically
def create_task(issue):
    return Task(
        description=f"""
        The string '{issue['original']}' in {issue['file']} (key: {issue['key']}) 
        exceeds the English value '{issue['english']}' by {issue['length_diff']} characters.
        Translate and shorten it to under {issue['max_length']} characters while preserving meaning.
        Example: 'Bonjour le monde c'est long' -> 'Salut monde'.
        Return only the new string.
        """,
        agent=translator_agent,
        expected_output=f"A string under {issue['max_length']} characters"
    )

# Main function to process issues
def process_localization_issues(issues):
    """Process localization issues with the agent and update files."""
    if not issues:
        print("No issues provided to process!")
        return
    
    # Create tasks for each issue
    tasks = [create_task(issue) for issue in issues]
    
    # Assemble and run the crew
    crew = Crew(agents=[translator_agent], tasks=tasks, verbose=2)
    results = crew.kickoff()

    # Update files with results
    for issue, result in zip(issues, results):
        new_string = result.strip()  # Clean up the output
        if len(new_string) <= issue["max_length"]:
            update_result = update_strings_file(issue, new_string)
            print(update_result)
        else:
            print(f"Failed to shorten '{issue['original']}' to under {issue['max_length']} chars: '{new_string}'")

if __name__ == "__main__":
    # For standalone testing
    sample_issues = [
        {
            "file": "fr.lproj/Localizable.strings",
            "key": "greeting",
            "original": "Bonjour le monde c'est long",
            "english": "Hello world",
            "length_diff": 11,
            "max_length": 15
        }
    ]
    process_localization_issues(sample_issues)