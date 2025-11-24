# 🌐 Localization Extractor & Translation Generator

A simple tool to extract strings from Dart/JSON files and generate a translation-ready Excel sheet.

## 📦 Requirements

* **Python**
* Install dependency:

  ```
  python -m pip install openpyxl
  ```

## 🚀 How to Use

1. Run the script:

   ```
   python extract_strings.py
   ```

2. Choose:

   * **1️⃣ Process Dart file**
   * **2️⃣ Process JSON file**

3. Select an action:

   * 🔍 Print extracted strings
   * 📄 Convert to JSON
   * 📊 Generate translation.xlsx

4. When prompted, paste your language codes in any format:

   ```
   en
   es
   af
   ar
   ...
   ```

   The tool auto-detects and sorts them.

## 📊 translation.xlsx Format

* **Column A** → English source
* **Column B** → Copy of English (editable)
* **Other columns** → Auto Google Translate formulas:

  ```
  =GOOGLETRANSLATE($A2, "en", "<lang>")
  ```

## ☁️ Translate in Google Sheets

1. Upload the generated XLSX to Google Drive
2. Open in **Google Sheets** – translations auto-fill
3. Review/edit
4. Download as XLSX

## 🔄 Convert XLSX → JSON

Use this tool to generate per-language JSONs:
👉 [https://muslimeclix.github.io/flutter-localization-converter/](https://muslimeclix.github.io/flutter-localization-converter/)

