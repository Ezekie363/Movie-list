import os
import json
import re

DATA_DIR = "data"
OUTPUT = "docs/movies.json"

movies = []

for root, _, files in os.walk(DATA_DIR):
    for file in files:
        if file.endswith(".md"):
            path = os.path.join(root, file)

            with open(path, "r", encoding="utf-8") as f:
                content = f.read()

                title_match = re.search(r"# 🎬 (.+?) \((\d{4})\)", content)
                rating_match = re.search(r"评分（1-10）：\s*(\d+\.?\d*)", content)
                tags_match = re.search(r"标签：(.+)", content)

                if title_match:
                    title = title_match.group(1)
                    year = int(title_match.group(2))
                else:
                    continue

                rating = float(rating_match.group(1)) if rating_match else 0

                tags = []
                if tags_match:
                    tags = [t.replace("#", "").strip() for t in tags_match.group(1).split()]

                movies.append({
                    "title": title,
                    "year": year,
                    "rating": rating,
                    "tags": tags
                })

os.makedirs("docs", exist_ok=True)

with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(movies, f, ensure_ascii=False, indent=2)

print("movies.json generated!")
