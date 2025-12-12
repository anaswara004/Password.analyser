import math
import re
def calculate_entropy(password):
    charset = 0
    if re.search(r"[a-z]", password): charset += 26
    if re.search(r"[A-Z]", password): charset += 26
    if re.search(r"[0-9]", password): charset += 10
    if re.search(r"[^a-zA-Z0-9]", password): charset += 32

    if charset == 0:
        return 0
    return len(password) * math.log2(charset)
def load_wordlist(path="wordlist.txt"):
    try:
        with open(path, "r") as f:
            return [w.strip().lower() for w in f.readlines()]
    except:
        return []


def dictionary_penalty(password, words):
    p = password.lower()
    for w in words:
        if w in p:
            return 20
    return 0


def sequence_penalty(password):
    sequences = ["1234", "abcd", "qwerty", "password"]
    for seq in sequences:
        if seq in password.lower():
            return 15
    return 0


def repetition_penalty(password):
    if re.search(r"(..+)\1", password):
        return 10
    return 0


def classify_score(score):
    if score < 28: return "Very Weak"
    if score < 36: return "Weak"
    if score < 60: return "Moderate"
    if score < 128: return "Strong"
    return "Very Strong"


def analyze_password(password):
    words = load_wordlist()

    entropy = calculate_entropy(password)
    penalty = (
        dictionary_penalty(password, words) +
        sequence_penalty(password) +
        repetition_penalty(password)
    )

    final_score = max(0, entropy - penalty)
    strength = classify_score(final_score)

    return {
        "entropy": round(entropy, 2),
        "penalties": penalty,
        "final_score": round(final_score, 2),
        "strength": strength
    }


if __name__ == "__main__":
    pwd = input("Enter password: ")
    result = analyze_password(pwd)
    print(result)