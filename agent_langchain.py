from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
import json

llm = Ollama(model="llama3:latest", base_url="http://localhost:11434")

# """
#     you are a expert translator who can tranlate english to any language while keeping the meaing intact in terms of IOS/apple device 
#     and enviorment and keeping the meaning of the enlgish why it is written like that in mind, while translating.
#     The string '{original}' in {language} exceeds the English value '{english}' in length.
#     Shorten it to under {max_length} characters while keeping it in {language} and preserving meaning.
#     Example: 'Bonjour le monde c'est long' (French) -> 'Salut monde' (French).
#     Return only the new string. the new string only, don't return the explaination and single quotes or double "" , 
#     if not possible to convert then only give explaniation also don't translate the word if it changes the meaning. keeping the meaning
#     intact while translating is the most important thing to consider before doing it.
#     """
prompt = PromptTemplate(
    input_variables=["original", "english", "max_length", "language"],
    template="""You are an expert translator specializing in iOS/Apple device environments. 
    Your task is to adapt strings while preserving the exact meaning and intent of the English version in terms of UI/UX of the device and 
    its intended purpose (e.g., UI labels, alerts) within the Apple ecosystem. 
    The string '{original}' in {language} exceeds the English value '{english}' in length. 
    Shorten it to under {max_length} characters by finding synonyms or rephrasing in {language}, 
    keeping the meaning intact based strictly on '{english}'. Do not hallucinate or alter the meaning. 
    For example: 'Bonjour le monde c'est long' (French) -> 'Salut monde' (French, using 'Salut' as a synonym for 'Bonjour'). 
    Return only the new string with no quotes or explanation if possible. 
    If shortening within {max_length} characters compromises the meaning, 
    return only an explanation (e.g., 'Cannot shorten without losing meaning').

    Meaning preservation is the top priority even after translation.

    Follow these steps:
    1. Understand the meaning of the English value '{english}' in the context of iOS UI/UX and its intended purpose.
    2. Analyze the meaning of the translated value '{original}' in {language}.
    3. Identify synonyms or rephrasings of the English value that preserve its meaning, then adapt them into {language}.
    4. Select the option that fits within {max_length} characters without losing the original intent.
    5. the return translation only be in {language} not in english or any other language.
    """

#     template=
#    """ You are an expert translator specializing in iOS/Apple device environments. 
#    Your task is to adapt strings while preserving the exact meaning and intent of the English version, 
#    considering its purpose (e.g., UI labels, alerts) in the Apple ecosystem. 
#    The string '{original}' in {language} exceeds the English value '{english}' in length. 
#    Shorten it to under {max_length} characters while keeping it in {language}. 
#    Do not hallucinate or alter the meaning—base the output strictly on '{english}'. 
#    For example: 'Bonjour le monde c'est long' (French) -> 'Salut monde' (French). 
#    Return only the new string with no quotes or explanation if possible. 
#    If shortening within {max_length} characters compromises the meaning, 
#    return only an explanation (e.g., 'Cannot shorten without losing meaning'). 
#    Meaning preservation is the top priority."""
)

translation_chain = LLMChain(llm=llm, prompt=prompt)

# Function to update .strings file
def update_strings_file(issue, new_string):
    file_path = issue["file"]
    key = issue["key"]
    language = issue["language"]
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        for i, line in enumerate(lines):
            if line.strip().startswith(f'"{key}" ='):
                lines[i] = f'"{key}" = "{new_string}";\n'
                break
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        return f"Updated {file_path} with {key}: {new_string}"
    except Exception as e:
        return f"Error updating {file_path}: {e}"
    
# Function to save translated string in file (as cache) 
def save_change_to_file(issue, new_string, root_dir):
    language = issue["language"]
    key = issue["key"]
    change_file = os.path.join(root_dir, f"{language}_changes.json")
    try:
        with open(change_file, 'r', encoding='utf-8') as f:
            changed_keys = json.load(f)
    except FileNotFoundError:
        changed_keys = {}
    
    changed_keys[key] = {"original": issue["original"], "new": new_string}
    with open(change_file, 'w', encoding='utf-8') as f:
        json.dump(changed_keys, f, ensure_ascii=False, indent=4)
    
    return f"Logged change in {change_file} for {key}: {new_string}"


# Main function to process issues
def process_localization_issues(issues):
    if not issues:
        print("No issues provided!")
        return
    
    for issue in issues:
        try:
            new_string = translation_chain.run(
                original=issue["original"],
                english=issue["english"],
                max_length=issue["max_length"],
                language=issue["language"]
            ).strip()
            
            if new_string.startswith("Cannot shorten") or "meaning" in new_string.lower():
                print(f"Skipped '{issue['original']}' in {issue['file']}: {new_string}")
            elif len(new_string) <= issue["max_length"]:
                update_result = update_strings_file(issue, new_string)
                if "Updated" in update_result:
                    save_result = save_change_to_file(issue, new_string, "/Users/tushar/Desktop/py/agent_translated_keys_files")
                    print(f"{update_result} | {save_result}")
                else:
                    print(update_result)
            else:
                print(f"Failed to shorten '{issue['original']}' to {issue['max_length']} chars: '{new_string}'")
        except Exception as e:
            print(f"Error processing {issue['file']} key {issue['key']}: {e}")
