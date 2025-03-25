from collections import defaultdict
import os
import json

class HelperClass:
    
    def parse_strings_file(file_path):
        """Parses an iOS/macOS .strings file into a dictionary and detects duplicates."""
        strings_dict = {}
        duplicates = []
        key_counts = defaultdict(int)
        

        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('"') and '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip().strip('"')
                    value = value.strip().strip('";')

                    key_counts[key] += 1
                    if key_counts[key] > 1:
                        duplicates.append(key)

                    strings_dict[key] = value

        return strings_dict, duplicates
    
    @staticmethod
    def check_for_word_count_similarity(expected_dict, translated_dict, cur_file_name, length_threshold):
        """Compare word counts between English and translated values for matching keys."""
        total_number_of_words = 0
        print(f"{cur_file_name} word count checking..")

        missing_keys_if_any = []
        print(f"{cur_file_name}")
        for key, ex_value in expected_dict.items():
            if key in translated_dict:
                translated_value = translated_dict[key]
                len_of_ex_value = len(ex_value)
                len_of_translated_value = len(translated_value)
                
                if len_of_translated_value > length_threshold * len_of_ex_value:
                    total_number_of_words += 1
                    print(f"{cur_file_name} {key} = '{translated_value}' has {len_of_translated_value - len_of_ex_value} more chars than English value '{ex_value}'")
                    # print(f"{key} = '{translated_value}', english:'{ex_value}'")
                    # print(f"{key} = '{ex_value}'")

            else:
                missing_keys_if_any.append(key)
            
            if len(missing_keys_if_any):
                print(f"not found these keys in  {cur_file_name}: {missing_keys_if_any}")
        
        if total_number_of_words > 0:
            print("############################################################")
            print(f"{cur_file_name} has total {total_number_of_words} entries with more characters than English values")
            print("############################################################")
        else:
            print("All Good!!")
            print("##########################################################################")

    @staticmethod
    def check_for_word_count_similarity_agent(expected_dict, translated_dict, cur_file_name, length_threshold, root_dir):
        """Compare word counts and return issues for the agent."""
        issues = []  # List to collect problematic strings
        total_number_of_words = 0
        print(f"{cur_file_name} word count checking..")

        # Load or initialize change tracking file
        change_file = os.path.join('/Users/tushar/Desktop/py/agent_translated_keys_files', f"{cur_file_name}_changes.json")
        try:
            with open(change_file, 'r', encoding='utf-8') as f:
                changed_keys = json.load(f)
        except FileNotFoundError:
            changed_keys = {}

        for key, ex_value in expected_dict.items():
            if key in translated_dict and key not in changed_keys:
                translated_value = translated_dict[key]
                len_of_ex_value = len(ex_value)
                len_of_translated_value = len(translated_value)
                
                if len_of_translated_value > length_threshold * len_of_ex_value:
                    total_number_of_words += 1
                    issue = {
                        "file": os.path.join(root_dir, f"{cur_file_name}.lproj", "Localizable.strings"),
                        "key": key,
                        "original": translated_value,
                        "english": ex_value,
                        "length_diff": len_of_translated_value - len_of_ex_value,
                        "max_length": int(len_of_ex_value * length_threshold),
                        "language": cur_file_name
                    }
                    issues.append(issue)
                    # print(f"{cur_file_name} {key} = '{translated_value}' has {len_of_translated_value - len_of_ex_value} more chars than English value '{ex_value}'")

        if total_number_of_words > 0:
            # print(f"{cur_file_name} has total {total_number_of_words} entries with more characters than English values")
            print(f"{total_number_of_words}")
        else:
            print("All Good!!")
        
        return issues
            













# import os
# import plistlib

# # Define the root directory containing all .strings files
# root_dir = '/Users/project/ZCleaner-ios/core/source/RonBlocker/RonBlocker'

# # Load the expected keys from input/english.strings
# with open(os.path.join(root_dir, 'de.lproj', 'Localizable.strings'), 'rb') as f:
#     english_data = plistlib.load(f)
# expected_keys = list(english_data.keys())

# # Check if all files have all expected keys
# for filename in os.listdir(root_dir):
#     if filename.endswith('.strings'):
#         with open(os.path.join(root_dir, filename), 'rb') as f:
#             file_data = plistlib.load(f)
#             missing_keys = [key for key in expected_keys if key not in file_data]
#             if missing_keys:
#                 print(f"File {filename} is missing the following keys: {', '.join(missing_keys)}")


# import os
# import plistlib

# # Define the root directory containing all .strings files
# root_dir = '/Users/project/ZCleaner-ios/core/source/RonBlocker/RonBlocker'

# # Load the expected keys from input/english.strings
# try:
#     expected_keys = list(plistlib.load(open(os.path.join(root_dir, 'en.lproj', 'Localizable.strings'), 'rb')).keys())
# except Exception as e:
#     print(f"Error loading file: {str(e)}")

# # Check if all files have all expected keys
# for lang in ['de', 'fr']:  # Add more languages as needed
#     for folder in [f"{lang}.lproj" for lang in ['de', 'fr']]:  # Add more languages as needed
#         file_path = os.path.join(root_dir, folder, 'Localizable.strings')
#         if os.path.exists(file_path):
#             with open(file_path, 'rb') as f:
#                 print("###############")
#                 print(file_path)
#                 print("###############")
#                 file_data = plistlib.load(f)
#                 missing_keys = [key for key in expected_keys if key not in file_data]
#                 if missing_keys:
#                     print(f"File {file_path} is missing the following keys: {', '.join(missing_keys)}")
#         else:
#             print(f"File {file_path} does not exist.")






