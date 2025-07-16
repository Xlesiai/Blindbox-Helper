# 🎁 Xiaohongshu Blind Box Parser (ONGOING)

**Find your favorite figures before unboxing!**  
This project extracts, cleans, and structures blind box post data from Xiaohongshu to help collectors identify which figure is inside—**based on weight, shaking behavior, and box feel**.

---

## 📦 What It Does

This script parses user-shared social media posts about blind boxes (e.g., One Piece × Labubu), extracting **useful physical cues** like:

- ✅ **Weight** of the box (in grams)
- ✅ **Shaking direction and intensity** (up/down, left/right, etc.)
- ✅ **Filling tightness** (e.g., "full", "loose", "obstruction")
- ✅ **Accessory sounds** (e.g., "sound of desiccant", "card rattle")
- ✅ **Heuristics to identify the character inside**

---

## 🧠 Why It Matters

Blind box collectors rely on subtle physical clues to guess what's inside. This tool helps:

- 📊 **Aggregate community knowledge**
- 🔍 **Identify patterns by weight & feel**
- 🏆 **Increase your odds of pulling your favorite character**

---

## 🚀 How It Works

1. **Scrapes post text** (Xiaohongshu post descriptions, images, and video)
2. **Normalizes names** (e.g., "Trafalgar Rowe" → "Trafalgar Law")
3. **Removes filler and marketing sentences**
4. **Extracts structured data**: character name, weight, and box feel
5. **(Optional)** Outputs to CSV or JSON

---

## 🧰 Tech Stack

- **Python 3.9+**

  - `re` — for regular expression parsing
  - `rapidfuzz` — for fuzzy name matching
  - `ollama` for AI text extraction
  - `deep_translator` - to translate text from chinese to english
  - `pydantic` - used to format ai model response

- **Optional**
  - `pandas` (optional) — for structured output
  - `sentence-transformers` (optional) — for semantic deduplication

---

## 📤 Example Output (JSON)

```json
{
  "name": "Tony Tony Chopper",
  "weight": 133.4,
  "feel": {
    "shake": "slightly up and down",
    "boxed": "bottom",
    "tightness": "full",
    "obstruction": true
  }
}
```
