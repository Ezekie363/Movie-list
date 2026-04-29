import os
import json

REVIEWS_DIR = "reviews"
OUTPUT = "docs/reviews.json"

reviews = []

for file in os.listdir(REVIEWS_DIR):
    if not file.endswith(".md"):
        continue

    path = os.path.join(REVIEWS_DIR, file)

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    title = ""
    rating = ""
    review = ""

    lines = content.split("\n")

    for i, line in enumerate(lines):
        if line.startswith("title:"):
            title = line.replace("title:", "").strip()

        elif line.startswith("rating:"):
            rating = line.replace("rating:", "").strip()

        elif line.startswith("review:"):
            review = "\n".join(lines[i+1:]).strip()

    reviews.append({
        "title": title,
        "rating": rating,
        "review": review
    })

os.makedirs("docs", exist_ok=True)

with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(reviews, f, ensure_ascii=False, indent=2)

print("✅ reviews.json generated")
