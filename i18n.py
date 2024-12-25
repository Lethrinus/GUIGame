import os
import glob

class I18N:
    def __init__(self, language_code, language_folder="languages"):
        self.language_folder = language_folder
        if language_code in self.get_available_languages():
            self.translations = self.load_data_from_file(language_code)
        else:
            print(f"Unsupported language: {language_code}. Falling back to 'en'.")
            self.translations = self.load_data_from_file('en')

    @staticmethod
    def get_available_languages(language_folder="languages"):
        language_files = glob.glob(os.path.join(language_folder, "data_*.lng"))
        language_codes = [
            os.path.basename(f).replace("data_", "").replace(".lng", "")
            for f in language_files
        ]
        return language_codes

    def load_data_from_file(self, language_code):
        language_file = os.path.join(self.language_folder, f"data_{language_code}.lng")
        language_data = {}
        try:
            with open(language_file, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and "=" in line:
                        key, val = line.split("=", 1)
                        language_data[key.strip()] = val.strip()
        except FileNotFoundError:
            raise ValueError(f"Language file {language_file} not found.")
        except Exception as e:
            raise ValueError(f"Error reading language file {language_file}: {e}")

        return language_data

try:
    i18n = I18N("en", language_folder="languages")
except Exception as e:
    print(f"Error loading language: {e}")
    exit()