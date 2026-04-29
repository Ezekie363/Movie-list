import os
import json
import re

REVIEW_DIR = "reviews"
OUTPUT = "docs/reviews.json"

reviews = []

def extract(pattern, text, default=""):
    match = re.search(pattern, text, re.MULTILINE)
    return match.group(1).strip() if match else default

for file in os.listdir(REVIEW_DIR):
    if not file.endswith(".md"):
        continue

    path = os.path.join(REVIEW_DIR, file)

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    title = extract(r"# 🎬 (.+)", content)
    review = extract(r"## 💭 观后感\n([\s\S]*)", content)

    reviews.append({
        "title": title,
        "review": review
    })

os.makedirs("docs", exist_ok=True)

with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(reviews, f, ensure_ascii=False, indent=2)

print(f"✅ Generated {len(reviews)} reviews")
