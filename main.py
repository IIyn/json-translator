import json
import asyncio
from googletrans import Translator

# Instanciate translator
translator = Translator()

DEFAULT_TARGET="fr"
DEFAULT_SOURCE="en"

async def translate_text(text, target_lang="fr", source_lang=DEFAULT_TARGET):
    """
    Asynchronously translates a string
    """
    try:
        # wait for the translation result
        translated = await translator.translate(text, src=DEFAULT_TARGET ,dest=target_lang)
        return translated.text
    except Exception as e:
        print(f"Failed to translate '{text}': {e}")
        return text  # Return original text in case of error

async def recursive_translate(data, target_lang=DEFAULT_TARGET, source_lang=DEFAULT_TARGET):
    """
    Recursively goes through the JSON and translate all strings (strings, lists, dicts)
    """
    if isinstance(data, dict):
        result = {}
        for key, value in data.items():
            result[key] = await recursive_translate(value, target_lang, source_lang)
        return result
    elif isinstance(data, list):
        return [await recursive_translate(item, target_lang, source_lang) for item in data]
    elif isinstance(data, str):
        return await translate_text(data, target_lang)
    else:
        return data

async def main():
    # Load the JSON file
    with open("translate_me.json", "r", encoding="utf-8") as file:
        json_data = json.load(file)

    # Ask the user for the target and source languages
    target_language = input("Enter the target language code (e.g., 'fr' for French): ")
    source_language = input("Enter the source language code (e.g., 'en' for English): ")

    # Recursively translate the file
    translated_data = await recursive_translate(json_data, target_lang=target_language, source_lang=source_language)

    # Save the translation into a new JSON file
    with open("translated.json", "w", encoding="utf-8") as file:
        json.dump(translated_data, file, ensure_ascii=False, indent=4)

    print("Translation done, check out translated.json")

# Run the asynchonous main function
if __name__ == "__main__":
    asyncio.run(main())
