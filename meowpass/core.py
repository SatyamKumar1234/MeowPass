import json
import itertools
import random

def load_data(filename="data.json"):
    """Loads user data from an external JSON file."""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        return "JSON_ERROR"

def generate_base_words(data):
    """Creates a simple list of core words from personal data."""
    base_words = set()
    all_keywords = [item.lower() for sublist in data.values() for item in sublist]
    base_words.update(all_keywords)
    for word1, word2 in itertools.permutations(all_keywords, 2):
        base_words.add(word1 + word2)
    return list(base_words)

def apply_mangling_rules(words):
    """Applies systematic rules to a list of words."""
    final_passwords = set(words)
    common_years = ["1990", "1995", "1999", "2000", "2001", "2010", "2020", "2023", "2024"]
    common_symbols = ['!', '@', '#', '$', '%', '&', '*', '?']
    l33t_map = {'a': '@', 'e': '3', 'i': '1', 'l': '1', 'o': '0', 's': '$'}
    words_to_mangle = random.sample(words, min(len(words), 500))

    for word in words_to_mangle:
        variations = {word, word.capitalize(), word.upper()}
        l33t_word = "".join([l33t_map.get(char, char) for char in word])
        variations.add(l33t_word)
        for var_word in list(variations):
            for year in common_years: final_passwords.add(var_word + year)
            for i in range(0, 1000): final_passwords.add(var_word + str(i))
            for symbol in common_symbols: final_passwords.add(var_word + symbol); final_passwords.add(symbol + var_word)
    return list(final_passwords)

def enhance_with_ai(base_wordlist, data, console, provider_choice, api_key, num_passwords, model_name=None):
    """Uses an AI provider to enhance the wordlist creatively."""
    data_str = json.dumps(data, indent=2)
    sample_str = ", ".join(random.sample(base_wordlist, min(len(base_wordlist), 200)))
    prompt = (
        f"You are a cybersecurity expert specializing in password cracking psychology. Analyze the target's personal data and the provided list of computer-generated password guesses."
        f"\nYour task is to generate {num_passwords} *new*, creative, human-like password variations that a machine would likely miss."
        f"\n\n--- Target's Data ---\n{data_str}"
        f"\n\n--- Computer Guess Sample ---\n{sample_str}"
        f"\n\nGenerate {num_passwords} new, creative passwords. Return ONLY a comma-separated list and nothing else."
    )
    ai_generated_passwords = []

    if provider_choice == '1':
        try:
            import google.generativeai as genai
            with console.status("[bold green]Contacting Google Gemini API...[/]"):
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-pro')
                response = model.generate_content(prompt)
                ai_passwords_text = response.text
                ai_generated_passwords = [p.strip() for p in ai_passwords_text.split(',')]
        except ImportError: return "GEMINI_NOT_INSTALLED", []
        except Exception as e: return f"API_ERROR: {e}", []
    
    elif provider_choice == '2':
        try:
            import openai
            with console.status("[bold purple]Contacting OpenRouter API...[/]"):
                client = openai.OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)
                response = client.chat.completions.create(model=model_name, messages=[{"role": "user", "content": prompt}])
                ai_passwords_text = response.choices[0].message.content
                ai_generated_passwords = [p.strip() for p in ai_passwords_text.split(',')]
        except ImportError: return "OPENAI_NOT_INSTALLED", []
        except Exception as e: return f"API_ERROR: {e}", []
    
    return "SUCCESS", list(set(base_wordlist + ai_generated_passwords))