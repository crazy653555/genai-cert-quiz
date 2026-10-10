import re, glob, os

os.makedirs("transcripts", exist_ok=True)

for path in sorted(glob.glob("subs/*.vtt")):
    base = os.path.basename(path)
    idx_id = base.split(".")[0]  # e.g. 01_V1iHrnvOBKQ
    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines()

    texts = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith("WEBVTT") or line.startswith("Kind:") or line.startswith("Language:"):
            continue
        if "-->" in line:
            continue
        if re.match(r"^\d+$", line):
            continue
        texts.append(line)

    # dedupe consecutive duplicate lines
    dedup = []
    for t in texts:
        if not dedup or dedup[-1] != t:
            dedup.append(t)

    full = "".join(dedup)
    out_path = f"transcripts/{idx_id}.txt"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(full)

print("done", len(glob.glob("subs/*.vtt")))
