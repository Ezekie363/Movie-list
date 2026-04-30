import os
import json
import re

DATA_DIR = "data"
OUTPUT = "docs/movies.json"

movies = []

def extract(pattern, text, default=""):
    match = re.search(pattern, text, re.MULTILINE)
    return match.group(1).strip() if match else default

for root, _, files in os.walk(DATA_DIR):
    category = os.path.basename(root)
    for file in files:
        if not file.endswith(".md"):
            continue

        path = os.path.join(root, file)

        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
        except:
            continue

        # 标题（支持中英文）
        title_match = re.search(r"#\s*🎬\s*(.+?)\s*\((\d{4})\)", content)
        if not title_match:
            continue

        title = title_match.group(1).strip()
        year = int(title_match.group(2))

        rating = extract(r"评分（1-10）：\s*([0-9.]+)", content, "0")
        try:
            rating = float(rating)
        except:
            rating = 0

        tags_line = extract(r"标签：(.+)", content)
        tags = [t.replace("#", "").strip() for t in tags_line.split() if t]

        director = extract(r"- 导演：(.+)", content)
        actors = extract(r"- 主演：(.+)", content)
        genre = extract(r"- 类型：(.+)", content)

        movies.append({
            "title": title,
            "year": year,
            "category": category,
            "rating": rating,
            "tags": tags,
            "director": director,
            "actors": actors,
            "genre": genre
        })

# 确保 docs 存在
os.makedirs("docs", exist_ok=True)

# 写入 JSON
with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(movies, f, ensure_ascii=False, indent=2)

print(f"✅ Generated {len(movies)} movies")
