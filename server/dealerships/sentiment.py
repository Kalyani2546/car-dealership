POSITIVE_WORDS = {
    "amazing", "awesome", "best", "brilliant", "excellent", "fantastic",
    "friendly", "good", "great", "helpful", "love", "perfect", "recommend",
    "smooth", "wonderful",
}
NEGATIVE_WORDS = {
    "awful", "bad", "broken", "disappointed", "hate", "horrible", "poor",
    "rude", "terrible", "worst",
}


def analyze_sentiment(text):
    words = {word.strip(".,!?;:()[]{}\"'").lower() for word in text.split()}
    score = len(words & POSITIVE_WORDS) - len(words & NEGATIVE_WORDS)
    label = "positive" if score > 0 else "negative" if score < 0 else "neutral"
    return {"label": label, "score": score}
