def analyze_text(text: str) -> dict:
    if not text.strip():
        raise ValueError("Текст не повинен бути порожнім")

    words = text.split()
    clean_words = [word.strip(".,!?;:()[]{}\"'").lower() for word in words]
    clean_words = [word for word in clean_words if word]

    word_count = len(clean_words)


    unique_words = len(set(word.strip(".,!?;:()[]{}\"'") for word in words))

    longest_word = max(
    (word.strip(".,!?;:()[]{}\"'") for word in words),
    key=len
)

    average_word_length = round(
        sum(len(word) for word in clean_words) / word_count, 2
    )

    letters = [
        char.lower()
        for char in text
        if char.isalpha()
    ]

    most_common_letter = max(set(letters), key=letters.count) if letters else None

    return {
        "word_count": word_count,
        "unique_words": unique_words,
        "longest_word": longest_word,
        "average_word_length": average_word_length,
        "most_common_letter": most_common_letter,
    }