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

        print(f"👉 正在处理: {path}")

        try:
            # ✅ 自动去 BOM
            with open(path, "r", encoding="utf-8-sig") as f:
                content = f.read()
        except Exception as e:
            print(f"❌ 读取失败: {file} | {e}")
            continue

        # =========================
        # 标题解析（更宽松）
        # =========================
        title = "未知"
        year = 0

        title_match = re.search(r"^#\s*🎬\s*(.*?)\s*\((\d{4})\)\s*$",
        content,
        re.MULTILINE
        )

        if title_match:
            title = title_match.group(1).strip()
            year = int(title_match.group(2))
        else:
            print(f"⚠️ 标题解析失败: {file}")

        # =========================
        # 评分（容错）
        # =========================
        rating = extract(r"评分.*?[:：]\s*([0-9.]+)", content, "0")
        try:
            rating = float(rating)
        except:
            rating = 0

        # =========================
        # 标签（容错）
        # =========================
        tags_line = extract(r"标签[:：]\s*(.+)", content, "")
        tags = [
            t.replace("#", "").strip()
            for t in re.split(r"[#\s]+", tags_line)
            if t.strip()
        ]

        # =========================
        # 支持 - 和 * + 中英文冒号
        # =========================
        director = extract(r"[-*]\s*导演[:：]\s*(.+)", content, "未知")
        actors = extract(r"[-*]\s*主演[:：]\s*(.+)", content, "未知")
        genre = extract(r"[-*]\s*类型[:：]\s*(.+)", content, "未知")

        # =========================
        # 防止空标题写入垃圾数据
        # =========================
        if title == "未知":
            print(f"⛔ 跳过无效文件: {file}")
            continue

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

        print(f"✅ 成功解析: {title}")

# =========================
# 输出 JSON
# =========================
os.makedirs("docs", exist_ok=True)

with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(movies, f, ensure_ascii=False, indent=2)

print(f"\n🎉 最终生成 {len(movies)} 条电影数据")
