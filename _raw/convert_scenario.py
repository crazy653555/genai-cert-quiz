# -*- coding: utf-8 -*-
"""Convert 生成式AI_情境模擬考題100題.md (folded-details format) into 考試題目/題庫09.md.

Re-runnable: always regenerates 題庫09.md from the raw file. Explanations are kept in full,
only markdown/LaTeX markup is converted to plain text (the quiz site renders plain text).
"""
import re, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_CANDIDATES = [
    os.path.join(ROOT, "_raw", "生成式AI_情境模擬考題100題.md"),
    os.path.join(ROOT, "考試題目", "生成式AI_情境模擬考題100題.md"),
]
OUT_PATH = os.path.join(ROOT, "考試題目", "題庫09.md")
ID_OFFSET = 259  # 原檔第001題 -> 第260題
BOOK = "白話拆解 × 認證實戰：鑑別式與生成式 AI"

# {原檔題號: 爭議備註}（題號 = 原檔題號，輸出題號 = 原檔題號 + ID_OFFSET）
CAVEATS = {
    9: "SHAP 本身也能解釋單筆預測（局部解釋），並非只能做整體貢獻度；「LIME＝單筆、SHAP＝全局」是筆記的簡化分工，依此作答即可。",
    14: "選項B所述「臺灣《個資法》第5條規範明確告知目的」不精確：第5條為誠實信用與不得逾越特定目的必要範圍原則，告知義務規定於第8、9條。其餘選項錯誤明顯，B仍為最佳答案。",
    16: "Amazon CodeWhisperer 已於2024年併入並更名為 Amazon Q Developer，考題仍沿用舊名。",
    18: "加拿大《人工智慧與數據法》(AIDA) 隨 C-27 法案於2025年1月國會休會而失效，「加拿大強制要求高風險AI稽核」的描述已過時；其餘選項錯誤明顯，B仍為最佳答案。",
    31: "梯度爆炸的標準解法是梯度裁剪（Gradient Clipping）；L1/L2 正則化與 Dropout 主要用於抑制過擬合，對梯度爆炸僅有間接幫助。依四選項比較，A仍為最佳答案。",
    34: "Sora 實際採用 Diffusion Transformer（DiT），Transformer 本身就是執行去噪的主幹網路；「Diffusion 畫圖、Transformer 只指揮不動手」是筆記的簡化比喻。",
    36: "原始題幹「目前模型กำลัง針對」夾雜亂碼泰文，已校正為「目前模型正在針對」，不影響題意與答案。",
    47: "神經風格轉換實際上是從多個網路層（含淺層與深層）計算 Gram 矩陣擷取風格，並非僅用較淺層；「深層抓內容、淺層抓風格」為筆記的簡化說法，且選項C為其顛倒版本，依此作答即可。",
    55: "Runway Gen-2 實際是以潛在擴散模型（Latent Diffusion）為基礎；「GAN＋自動編碼器」是考題沿用的標準答案，選項B本身也已加註說明。",
    91: "最早期的 Deepfake 換臉程式主要採用自動編碼器（Autoencoder）架構，GAN 常用於提升逼真度；「Deepfake 基於 GAN」為認證考試的標準答案。",
}

# 原檔文字錯誤校正 [(錯誤, 校正)]，需同時在 CAVEATS 註明
TEXT_FIXES = [("目前模型กำลัง針對", "目前模型正在針對")]

LATEX_MAP = [
    (r"\sim", "～"), (r"\times", "×"), (r"\mu", "μ"), (r"\sigma", "σ"),
    ("R^2", "R²"), ("10^2", "10²"), ("V_1", "V₁"),
]


def plain(s):
    """Strip markdown/LaTeX markup to plain text."""
    s = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", s)  # [text](link) -> text
    s = s.replace("**", "").replace("`", "")

    def latex(m):
        t = m.group(1)
        t = re.sub(r"\\text\{([^}]*)\}", r"\1", t)
        for a, b in LATEX_MAP:
            t = t.replace(a, b)
        return re.sub(r"\s+", " ", t).strip()

    s = re.sub(r"\$([^$\n]+)\$", latex, s)
    return s


def bullet(line):
    """'* foo' -> '・foo', keeping indentation of nested bullets."""
    m = re.match(r"^(\s*)\* (.*)$", line)
    return f"{m.group(1)}・{m.group(2)}" if m else line


def convert_block(num, block):
    lines = block.split("\n")
    opt_idx = next(i for i, l in enumerate(lines) if re.match(r"^\* \([A-D]\) ", l))
    stem_lines = [plain(bullet(l)).rstrip() for l in lines[:opt_idx] if l.strip()]
    stem = "\n".join(stem_lines)

    opts = {}
    for l in lines[opt_idx:]:
        m = re.match(r"^\* \(([A-D])\) (.*)$", l)
        if m:
            opts[m.group(1)] = plain(m.group(2)).strip()
    assert list(opts) == list("ABCD"), (num, opts.keys())

    dm = re.search(r"<details>.*?</summary>\s*(.*?)</details>", block, re.DOTALL)
    details = dm.group(1)
    am = re.search(r"^#### ✅ 正確答案：\(([A-D])\)\s*$", details, re.MULTILINE)
    answer = am.group(1)
    details = details[am.end():]

    exp_lines = []
    for l in details.split("\n"):
        if not l.strip():
            if exp_lines and exp_lines[-1] != "":
                exp_lines.append("")
            continue
        h = re.match(r"^#### (.*)$", l)
        if h:
            if exp_lines and exp_lines[-1] != "":
                exp_lines.append("")
            exp_lines.append(f"【{plain(h.group(1)).strip()}】")
            continue
        exp_lines.append(plain(bullet(l)).rstrip())
    explanation = "\n".join(exp_lines).strip()
    # 解析內不可出現會被 parser 誤判的行首
    assert not re.search(r"^(?:[A-D]\.|---|## )", explanation, re.MULTILINE), num

    qid = num + ID_OFFSET
    out = [f"## 第{qid}題", f"題目：{stem}", ""]
    out += [f"{k}. {v}" for k, v in opts.items()]
    out += ["", f"**正確答案：{answer}. {opts[answer]}**", ""]
    if num in CAVEATS:
        out += [f"> ⚠️ 爭議備註：{CAVEATS[num]}", ""]
    out += [f"解析：{explanation}", "", "---", ""]
    return "\n".join(out), answer


def main():
    raw = next((p for p in RAW_CANDIDATES if os.path.exists(p)), None)
    if not raw:
        sys.exit("raw file not found")
    with open(raw, encoding="utf-8") as f:
        text = f.read()
    for wrong, right in TEXT_FIXES:
        assert wrong in text, wrong
        text = text.replace(wrong, right)

    heads = list(re.finditer(r"^### 第 (\d+) 題\s*$", text, re.MULTILINE))
    parts = [
        f"# {BOOK} - 情境模擬題 (第{1 + ID_OFFSET}-{len(heads) + ID_OFFSET}題)",
        "",
        f"> 來源：使用者依書籍《{BOOK}》自建筆記所產生的情境模擬考題（原檔：_raw/生成式AI_情境模擬考題100題.md，由 _raw/convert_scenario.py 轉換）。",
        "",
    ]
    answers = {}
    for i, h in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        md, ans = convert_block(int(h.group(1)), text[h.end():end])
        parts.append(md)
        answers[int(h.group(1))] = ans

    with open(OUT_PATH, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(parts))
    print(f"Wrote {OUT_PATH}: {len(heads)} questions, caveats: {len(CAVEATS)}")
    with open(OUT_PATH, encoding="utf-8") as f:
        body = re.sub(r"^\*\*正確答案：.*\*\*$", "", f.read(), flags=re.MULTILINE)
    leftover = re.findall(r".{0,20}(?:\*\*|`|\$|file:///|\\).{0,20}", body)
    print("leftover markup:", len(leftover), leftover[:10])


if __name__ == "__main__":
    main()
