from check_keys_match_in_string import HelperClass
import os


class LocalizableStringsChecker:
    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.expected_dict = {}
        self.expected_keys = []
        self.expected_values = []
        self.english_duplicates = []
        self.load_expected_keys()
    
    def load_expected_keys(self):
        """Load the expected keys from the English .strings file."""
        try:
            file_path = os.path.join(self.root_dir, 'en.lproj', 'Localizable.strings')
            self.expected_dict, self.english_duplicates = HelperClass.parse_strings_file(file_path)
            self.expected_keys = list(self.expected_dict.keys())
            self.expected_values = list(self.expected_dict.values())
            
            if self.english_duplicates:
                print(f"English file has duplicate keys: {', '.join(self.english_duplicates)}")
            else:
                print("English file has no duplicate keys.")
        except Exception as e:
            print(f"Error loading English file: {str(e)}")
            self.expected_dict = {}
            self.expected_keys = []
            self.expected_values = []
            self.english_duplicates = []
    
    def check_files_for_missing_duplicates(self, languages):
        """Check if all localization files have the expected keys and detect duplicates."""    
        for lang in languages:
            folder = f"{lang}.lproj"
            file_path = os.path.join(self.root_dir, folder, 'Localizable.strings')
        
            if os.path.exists(file_path):
                file_keys_data, duplicates = HelperClass.parse_strings_file(file_path)
                missing_keys = [key for key in self.expected_keys if key not in file_keys_data]

                if missing_keys:  
                    print(f"File '{lang}' is missing the following keys and values: {', '.join(missing_keys)}", sep="\n")
                elif duplicates:
                    print(f"File '{lang}' has duplicate keys: {', '.join(duplicates)}")
                else:
                    print(f"File '{lang}' has no duplicates and no missing values!!")
                    # Pass dictionaries instead of value lists
                    # HelperClass.check_for_word_count_similarity(self.expected_dict, file_keys_data, lang, 1.4)
                
                if duplicates:
                    print(f"File '{lang}' has duplicate keys: {', '.join(duplicates)}")
            else:
                print(f"File '{lang}' does not exist.")

    def check_files_for_missing_duplicates_agent(self, languages):
        all_issues = []
        for lang in languages:
            folder = f"{lang}.lproj"
            file_path = os.path.join(self.root_dir, folder, 'Localizable.strings')
            
            if os.path.exists(file_path):
                file_keys_data, duplicates = HelperClass.parse_strings_file(file_path)
                missing_keys = [key for key in self.expected_keys if key not in file_keys_data]
                if missing_keys:
                    print(f"File '{lang}' is missing: {', '.join(missing_keys)}")
                if duplicates:
                    print(f"File '{lang}' has duplicates: {', '.join(duplicates)}")
                else:
                    # supported_langs: ['de', 'ja', 'en', 'es', 'it', 'sv', 'ko', 'pt-BR', 'ru', 'fr', 'nl']
                    # fr, it,de,ja,sv,nl, ko, 
                    if lang == "ru":
                        issues = HelperClass.check_for_word_count_similarity_agent(self.expected_dict, file_keys_data, lang, 1.4, self.root_dir)
                        all_issues.extend(issues)
        return all_issues

    def get_supported_languages(self,directory):
        return [name.split(".lproj")[0] for name in os.listdir(directory) if name.endswith(".lproj")  and name != "English.lproj"]

# Usage example
if __name__ == "__main__":
    root_dir = '/Users/project/ZCleaner-ios/core/source/RonBlocker/RonBlocker'
    checker = LocalizableStringsChecker(root_dir)
    supported_langs = checker.get_supported_languages(root_dir)
    print(f"supported_langs: {supported_langs}")
    # pending
    # strings to convert Korean, portuguese , Spanish, Turkish, Chinese simplified

    checker.check_files_for_missing_duplicates(supported_langs)

    issues = [] #checker.check_files_for_missing_duplicates_agent(supported_langs)
    if issues:
        from agent_langchain import process_localization_issues
        process_localization_issues(issues)
    else:
        print("No issues to process!")


    '''
    Dutch-- done
    Korean -- done
    Portuguese -- done
    Simplified Chinese (need to discuss)
    Spanish -- done
    Swedish -- done
    '''


# ex_value
# de has total 217 words that has more character from english values
# fr has total 231 words that has more character from english values


# ex_value+5
# de has total 123 words that has more character from english values

# fr has total 139 words that has more character from english values

# # Define the root directory containing all .strings files

# root_dir = '/Users/project/ZCleaner-ios/core/source/RonBlocker/RonBlocker'

# # Load the expected keys from English strings file
# try:
#     expected_keys, english_duplicates = HelperClass.parse_strings_file(os.path.join(root_dir, 'en.lproj', 'Localizable.strings'))
#     expected_keys = list(expected_keys.keys())

#     if english_duplicates:
#         print(f"English file has duplicate keys: {', '.join(english_duplicates)}")
#     else:
#         print("English file has no duplicate keys.")
        
# except Exception as e:
#     print(f"Error loading English file: {str(e)}")
#     expected_keys = []
#     english_duplicates = []

# # Check if all files have all expected keys and detect duplicates
# for lang in ['de', 'fr', 'it', 'es']:
#     folder = f"{lang}.lproj"
#     file_path = os.path.join(root_dir, folder, 'Localizable.strings')
    
#     if os.path.exists(file_path):
#         file_data, duplicates = HelperClass.parse_strings_file(file_path)
#         missing_keys = [key for key in expected_keys if key not in file_data]
        
#         if missing_keys:
#             print(f"File '{lang}' is missing the following keys: {', '.join(missing_keys)}")
#         else:
#             print(f"File '{lang}' is ok!")

#         if duplicates:
#             print(f"File '{lang}' has duplicate keys: {', '.join(duplicates)}")
#     else:
#         print(f"File '{lang}' does not exist.")