import string

import torch
from textblob import Word
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Below this, a suggestion is more likely to be noise than a genuine fix.
MIN_CONFIDENCE = 0.9

class SpellCheckerModule:
    def __init__(self):
        # Load grammar correction model
        self.tokenizer = AutoTokenizer.from_pretrained("prithivida/grammar_error_correcter_v1")
        self.model = AutoModelForSeq2SeqLM.from_pretrained("prithivida/grammar_error_correcter_v1")

    def correct_spell(self, text):
        """Correct spelling word by word, without mangling words already right.

        TextBlob's dictionary is lowercase and ranked by frequency, so asking it
        about a capitalised word gives the wrong answer: "She" scores 0.04 while
        "The" scores 0.83, and a naive per-word pass rewrites the start of most
        sentences. Look the word up in lowercase, restore the original casing,
        and only substitute when the suggestion is both different and confident.
        """
        corrected = []
        for token in text.split():
            core = token.strip(string.punctuation)
            if not core or not core.isalpha():
                corrected.append(token)
                continue

            suggestion, confidence = Word(core.lower()).spellcheck()[0]
            if suggestion == core.lower() or confidence < MIN_CONFIDENCE:
                corrected.append(token)          # already a word, or too unsure
                continue

            if core.isupper():
                suggestion = suggestion.upper()
            elif core[0].isupper():
                suggestion = suggestion.capitalize()
            corrected.append(token.replace(core, suggestion))
        return " ".join(corrected)

    def correct_grammar(self, text):
        # Ensure input is a string
        if not isinstance(text, str) or not text.strip():
            return "Invalid input for grammar correction."

        # Encode input with prefix required by the model
        inputs = self.tokenizer.encode("gec: " + text, return_tensors="pt")

        # Generate corrected output
        with torch.no_grad():
            outputs = self.model.generate(
                inputs,
                max_length=128,
                num_beams=5,
                early_stopping=True,
                no_repeat_ngram_size=2
            )

        # Decode and return the corrected sentence
        corrected = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return corrected

if __name__ == "__main__":
    checker = SpellCheckerModule()

    test_text = "He go to school every day and she have a apple."
    print("Original:", test_text)

    corrected_spelling = checker.correct_spell(test_text)
    print("Corrected Spelling:", corrected_spelling)

    corrected_grammar = checker.correct_grammar(corrected_spelling)
    print("Corrected Grammar:", corrected_grammar)
