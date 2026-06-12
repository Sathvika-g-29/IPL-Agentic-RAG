import hashlib
import math
import re


EMBEDDING_DIMENSION = 128


def tokenize(text: str) -> list[str]:
    words = re.findall(r"\b[a-z0-9]+\b", text.lower())
    normalized_words = []

    for word in words:
        if len(word) > 3 and word.endswith("s"):
            word = word[:-1]

        normalized_words.append(word)

    return normalized_words


def word_to_index(word: str) -> int:
    digest = hashlib.md5(word.encode("utf-8")).hexdigest()
    return int(digest, 16) % EMBEDDING_DIMENSION


def word_to_sign(word: str) -> int:
    digest = hashlib.sha1(word.encode("utf-8")).hexdigest()
    value = int(digest, 16)
    return 1 if value % 2 == 0 else -1


def embed_text(text: str) -> list[float]:
    vector = [0.0] * EMBEDDING_DIMENSION

    for word in tokenize(text):
        index = word_to_index(word)
        sign = word_to_sign(word)
        vector[index] += sign

    length = math.sqrt(sum(value * value for value in vector))

    if length == 0:
        return vector

    return [value / length for value in vector]
