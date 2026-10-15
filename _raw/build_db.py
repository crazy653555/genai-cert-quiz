# -*- coding: utf-8 -*-
import re, sqlite3, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 生成式AI考試/
QUIZ_DIR = os.path.join(ROOT, "考試題目")
SITE_DIR = os.path.join(ROOT, "複習測驗網站")
DB_PATH = os.path.join(SITE_DIR, "quiz.db")

# (filename, source label, default topic if file has no internal unit headers)
SOURCE_MAP = [
    ("題庫01.md", "題庫01", "綜合"),
    ("題庫02.md", "題庫02", "倫理與法律"),
    ("題庫03.md", "題庫03", "應用技能"),
    ("題庫04.md", "題庫04", "能力強化"),
    ("題庫05.md", "題庫05", "基礎知識"),
    ("題庫06.md", "題庫06", None),  # topic derived per-question from 單元 headers
    ("題庫07.md", "題庫07", "綜合"),
    ("題庫08.md", "題庫08", "綜合"),
    ("題庫09.md", "題庫09", "白話拆解 × 認證實戰：鑑別式與生成式 AI"),
    ("題庫10.md", "題庫10", "白話拆解 × 認證實戰：鑑別式與生成式 AI"),
    ("題庫11.md", "題庫11", "白話拆解 × 認證實戰：鑑別式與生成式 AI"),
    ("題庫12.md", "題庫12", "綜合"),
    ("題庫13.md", "題庫13", "白話拆解 × 認證實戰：鑑別式與生成式 AI"),
]

Q_HEADER = re.compile(r"^##\s*第(\d+)題\s*$", re.MULTILINE)
UNIT_HEADER = re.compile(r"^##\s*單元[一二三四五六七八九十]+\s*(.+?)\s*$", re.MULTILINE)

UNIT_TOPIC_NORMALIZE = {
    "生成式AI基礎知識": "基礎知識",
    "生成式AI能力強化": "能力強化",
    "生成式AI應用技能": "應用技能",
    "生成式AI倫理與法律": "倫理與法律",
}


def build_unit_topic_map(text):
    """Return {question_id: topic} based on nearest preceding '## 單元X ...' header."""
    unit_matches = list(UNIT_HEADER.finditer(text))
    q_matches = list(Q_HEADER.finditer(text))
    mapping = {}
    for qm in q_matches:
        qid = int(qm.group(1))
        current_topic = None
        for um in unit_matches:
            if um.start() < qm.start():
                raw = um.group(1).strip()
                current_topic = UNIT_TOPIC_NORMALIZE.get(raw, raw)
            else:
                break
        mapping[qid] = current_topic
    return mapping


def parse_file(path, source, default_topic):
    with open(path, encoding="utf-8") as f:
        text = f.read()

    unit_topic_map = build_unit_topic_map(text) if default_topic is None else {}

    matches = list(Q_HEADER.finditer(text))
    records = []
    for i, m in enumerate(matches):
        qid = int(m.group(1))
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        block = text[start:end]

        qm = re.search(r"題目：(.+?)(?:\n\n|\nA\.)", block, re.DOTALL)
        question = qm.group(1).strip() if qm else None

        opts = {}
        for letter in "ABCD":
            om = re.search(rf"^{letter}\.\s*(.+)$", block, re.MULTILINE)
            opts[letter] = om.group(1).strip() if om else None

        am = re.search(r"\*\*正確答案：([A-D])\.\s*(.+?)\*\*", block)
        correct = am.group(1) if am else None

        dm = re.search(r"> ⚠️ 爭議備註：(.+?)(?=\n\n解析：|\Z)", block, re.DOTALL)
        caveat = dm.group(1).strip() if dm else None
        caveat = re.sub(r"\n>\s*", " ", caveat) if caveat else None

        em = re.search(r"解析：(.+?)(?=\n\n---|\Z)", block, re.DOTALL)
        explanation = em.group(1).strip() if em else None

        topic = default_topic if default_topic is not None else unit_topic_map.get(qid, "其他")

        if re.search(r"^>\s*🚫\s*重複排除", block, re.MULTILINE):
            print(f"  skip (duplicate, excluded from DB): #{qid}")
            continue

        records.append({
            "id": qid,
            "source": source,
            "topic": topic,
            "question": question,
            "option_a": opts["A"],
            "option_b": opts["B"],
            "option_c": opts["C"],
            "option_d": opts["D"],
            "correct_option": correct,
            "explanation": explanation,
            "has_caveat": 1 if caveat else 0,
            "caveat_note": caveat,
        })
    return records


def main():
    all_records = []
    for fname, source, default_topic in SOURCE_MAP:
        path = os.path.join(QUIZ_DIR, fname)
        if not os.path.exists(path):
            print("MISSING", path)
            continue
        recs = parse_file(path, source, default_topic)
        print(fname, "->", len(recs), "questions")
        all_records.extend(recs)

    problems = []
    seen_ids = set()
    for r in all_records:
        for key in ("question", "option_a", "option_b", "option_c", "option_d", "correct_option", "explanation", "topic"):
            if not r[key]:
                problems.append((r["id"], key, "MISSING"))
        if r["id"] in seen_ids:
            problems.append((r["id"], "id", "DUPLICATE"))
        seen_ids.add(r["id"])

    if problems:
        print("=== PARSE PROBLEMS ===")
        for p in problems:
            print(p)
    else:
        print("All records parsed cleanly:", len(all_records))

    os.makedirs(SITE_DIR, exist_ok=True)
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE questions (
            id              INTEGER PRIMARY KEY,
            source          TEXT NOT NULL,
            topic           TEXT NOT NULL,
            question        TEXT NOT NULL,
            option_a        TEXT NOT NULL,
            option_b        TEXT NOT NULL,
            option_c        TEXT NOT NULL,
            option_d        TEXT NOT NULL,
            correct_option  TEXT NOT NULL CHECK (correct_option IN ('A','B','C','D')),
            explanation     TEXT NOT NULL,
            has_caveat      INTEGER NOT NULL DEFAULT 0,
            caveat_note     TEXT
        )
    """)
    cur.execute("CREATE INDEX idx_questions_source ON questions(source)")
    cur.execute("CREATE INDEX idx_questions_topic ON questions(topic)")

    cur.executemany("""
        INSERT INTO questions
        (id, source, topic, question, option_a, option_b, option_c, option_d,
         correct_option, explanation, has_caveat, caveat_note)
        VALUES
        (:id, :source, :topic, :question, :option_a, :option_b, :option_c, :option_d,
         :correct_option, :explanation, :has_caveat, :caveat_note)
    """, all_records)

    conn.commit()

    cur.execute("SELECT COUNT(*), SUM(has_caveat) FROM questions")
    total, caveats = cur.fetchone()
    print("DB total rows:", total, "| rows with caveat:", caveats)

    cur.execute("SELECT source, COUNT(*) FROM questions GROUP BY source ORDER BY MIN(id)")
    for row in cur.fetchall():
        print(" source:", row)

    cur.execute("SELECT topic, COUNT(*) FROM questions GROUP BY topic ORDER BY MIN(id)")
    for row in cur.fetchall():
        print(" topic:", row)

    conn.close()
    print("DB written to:", DB_PATH)


if __name__ == "__main__":
    main()
