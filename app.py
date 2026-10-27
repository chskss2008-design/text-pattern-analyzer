
from flask import Flask, render_template, request
from dfa import TextDFA
import re
from collections import Counter

app = Flask(__name__)

STOP_WORDS = {
    "the", "is", "am", "are", "was", "were", "a", "an",
    "and", "or", "but", "in", "on", "at", "to", "of",
    "for", "with", "by", "from", "as", "it", "this",
    "that", "be", "can", "will", "has", "have", "had",
    "these", "those", "their", "they", "them", "we", "you",
    "your", "our", "he", "she", "his", "her", "its"
}


def split_sentences(text):
    parts = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s.strip() for s in parts if s.strip()]


def summarize_text(text):
    sentences = split_sentences(text)

    if not sentences:
        return "", [], []

    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    useful_words = [w for w in words if w not in STOP_WORDS]
    frequency = Counter(useful_words)

    scores = []

    for sentence in sentences:
        sentence_words = re.findall(
            r'\b[a-zA-Z]+\b', sentence.lower()
        )

        meaningful = [
            w for w in sentence_words if w not in STOP_WORDS
        ]

        if meaningful:
            score = sum(frequency[w] for w in meaningful)
            score /= len(meaningful)
        else:
            score = 0

        scores.append(score)

    summary_count = max(1, (len(sentences) + 1) // 2)

    ranked = sorted(
        range(len(sentences)),
        key=lambda i: scores[i],
        reverse=True
    )

    selected = sorted(ranked[:summary_count])
    summary = " ".join(sentences[i] for i in selected)

    return summary, sentences, scores


def choose_dfa(text):
    words = re.findall(r"[a-zA-Z]+", text)
    sentences = split_sentences(text)

    # Choose the word-pattern DFA when the text
    # contains at least 3 words and 2 word boundaries.
    if len(words) >= 3 and len(re.findall(r"\s", text)) >= 2:
        return "word"

    return "sentence"


def convert_symbols(text, pattern_type):
    symbols = []

    if pattern_type == "sentence":
        for char in text:
            if char in ".!?":
                symbols.append("E")
            else:
                symbols.append("W")

    else:
        for char in text:
            if char.isalpha():
                symbols.append("L")
            elif char.isspace():
                symbols.append("S")
            else:
                symbols.append("O")

    return symbols


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/summarize", methods=["POST"])
def summarize():
    text = request.form.get("text", "").strip()

    if not text:
        return render_template(
            "index.html",
            error="Please enter some text."
        )

    summary, sentences, scores = summarize_text(text)

    pattern_type = choose_dfa(text)
    machine = TextDFA(pattern_type)

    symbols = convert_symbols(text, pattern_type)
    result = machine.process(symbols)

    return render_template(
        "index.html",
        original_text=text,
        summary=summary,
        sentence_results=[],
        dfa_states=result["states"],
        dfa_pattern=pattern_type,
        dfa_final_state=result["final_state"],
        dfa_accepted=result["accepted"],
        dfa_history=result["history"],
        dfa_symbols=symbols
    )


if __name__ == "__main__":
    app.run(debug=True)
