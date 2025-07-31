def classify(text: str, topics: list[str]) -> str:
    from difflib import get_close_matches
    matches = get_close_matches(text.split("\n")[0], topics, n=1)
    return matches[0] if matches else "Unclassified"
