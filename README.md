# 🌐 Localization Extractor & Translation Generator

Extract localization strings from Dart/JSON files, generate translation-ready Excel sheets, and convert final translations into JSON.

---

# 🖥️ Desktop App (Windows)

A ready-to-use **Windows Desktop Application** is available.

### 👉 **[Download Localizer.exe]([[https://github.com/A13u13akar-npc/Flutter-Localization-Converter/raw/main/dist/Localizer.exe](https://github.com/A13u13akar-npc/Flutter-Localization-Converter/tree/main/dist/localizer](https://github.com/A13u13akar-npc/Flutter-Localization-Converter/blob/main/dist/localizer/localizer.zip)))**

No Python required — just download and run.

---

# 🍎 Desktop App (macOS)

A ready-to-use **macOS Application** is available.

### 👉 **[Download Localizer.app (macOS)](https://github.com/A13u13akar-npc/Flutter-Localization-Converter/raw/main/dist/mac-build.zip)**

This is a zipped `.app` bundle.
Unzip it and run `localizer_app.app` on macOS.

---

# 💻 Command-Line Tool (Cross-Platform)

If you prefer using the CLI version, use the included script:

```
extract_strings.py
```

## 📦 Requirements

* **Python**
* Install dependency:

```
python -m pip install openpyxl
```

---

# 🚀 How to Use (CLI Version)

1. Run:

```
python extract_strings.py
```

2. Choose:

* 1️⃣ Process Dart file
* 2️⃣ Process JSON file

3. Select an action:

* 🔍 Print extracted strings
* 📄 Convert to JSON
* 📊 Generate translation.xlsx

4. Paste your language codes in any format:

```
en
es
af
ar
...
```

The tool auto-detects and sorts them.

---

# 📊 translation.xlsx Format

* **Column A** → English source
* **Column B** → Editable English copy
* **Remaining columns** → Google Translate formulas:

```
=GOOGLETRANSLATE($A2, "en", "<lang>")
```

---

# ☁️ Translate in Google Sheets

1. Upload the generated XLSX to Google Drive
2. Open in **Google Sheets** (auto-fills translations)
3. Review or edit manually
4. Download as XLSX

---

# 🔄 Convert XLSX → JSON

Use the built-in tool or this web tool to convert your completed translations into JSON files, both work great:

👉 [https://muslimeclix.github.io/flutter-localization-converter/](https://muslimeclix.github.io/flutter-localization-converter/)
