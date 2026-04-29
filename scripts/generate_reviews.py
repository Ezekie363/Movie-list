import os
import json

REVIEWS_DIR = "reviews"
OUTPUT = "docs/reviews.json"

reviews = []

# ✅ 防止目录不存在
if not os.path.exists(REVIEWS_DIR):
    print("⚠️ reviews 目录不存在")
    os.makedirs("docs", exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False, indent=2)
    exit()

for file in os.listdir(REVIEWS_DIR):
    if not file.endswith(".md"):
        continue

    path = os.path.join(REVIEWS_DIR, file)

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    title = ""
    rating = 0
    review = ""

    lines = content.split("\n")

    for i, line in enumerate(lines):
        if line.startswith("title:"):
            title = line.replace("title:", "").strip()

        elif line.startswith("rating:"):
            try:
                rating = float(line.replace("rating:", "").strip())
            except:
                rating = 0

        elif line.startswith("review:"):
            review = "\n".join(lines[i+1:]).strip()
            break  # ✅ 找到就结束，避免吃多余内容

    # ✅ 跳过无效数据
    if not title:
        continue

    reviews.append({
        "title": title,
        "rating": rating,
        "review": review
    })

# ✅ 确保 docs 存在
os.makedirs("docs", exist_ok=True)

# ✅ 写入 JSON
with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(reviews, f, ensure_ascii=False, indent=2)

print(f"✅ Generated {len(reviews)} reviews")
