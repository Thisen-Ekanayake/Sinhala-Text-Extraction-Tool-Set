import os
import re
import json
from tkinter import Tk, filedialog

def clean_sinhala_text(text):
    # Keep Sinhala letters \u0D80-\u0DFF, space, ., ,, !, (), and basic punctuation
    cleaned = re.sub(r'[^ \u0D80-\u0DFF\.\,\!\(\)]', '', text)
    # Remove usernames and emojis (already handled by regex above)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned

def get_word_count(text):
    return len(text.split())

def process_file(filepath, file_number):
    basename = os.path.basename(filepath)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    comments = []

    if filepath.endswith('.json'):
        try:
            data = json.loads(content)
            # Assuming the comments are in a list of dicts or plain list
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        for value in item.values():
                            comments.append(str(value))
                    else:
                        comments.append(str(item))
            elif isinstance(data, dict):
                for value in data.values():
                    comments.append(str(value))
        except Exception as e:
            print(f"Failed to parse JSON in {basename}: {e}")
            return
    else:
        comments = content.splitlines()

    cleaned_comments = [clean_sinhala_text(c) for c in comments if clean_sinhala_text(c)]
    full_cleaned_text = '\n'.join(cleaned_comments)
    word_count = get_word_count(full_cleaned_text)

    txt_filename = f"{file_number:02d}_txt_word_count_{word_count}.txt"
    json_filename = f"{file_number:02d}_json_word_count_{word_count}.json"

    with open(txt_filename, 'w', encoding='utf-8') as f:
        f.write(full_cleaned_text)

    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(cleaned_comments, f, ensure_ascii=False, indent=2)

    print(f"Processed: {basename} → {txt_filename}, {json_filename}")

def main():
    Tk().withdraw()
    filepaths = filedialog.askopenfilenames(title="Select comment files (.txt or .json)",
                                            filetypes=[("Text & JSON files", "*.txt *.json")])
    for i, filepath in enumerate(filepaths, 1):
        process_file(filepath, i)

if __name__ == "__main__":
    main()
