import json
import re
import tkinter as tk
from tkinter import filedialog
from openpyxl import Workbook

def choose():
    print("1. Process Dart file")
    print("2. Process JSON file")
    return input("Select: ").strip()

def select_file(ftype):
    root = tk.Tk()
    root.withdraw()
    if ftype == "dart":
        return filedialog.askopenfilename(filetypes=[("Dart files", "*.dart")])
    if ftype == "json":
        return filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    return None

def select_save(ext):
    root = tk.Tk()
    root.withdraw()
    if ext == "json":
        return filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
    if ext == "xlsx":
        return filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
    return None

def strip_comments(text):
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
    cleaned = []
    for line in text.splitlines():
        line = re.sub(r'//.*', '', line)
        if line.strip() != "":
            cleaned.append(line)
    return "\n".join(cleaned)

def normalize(s):
    s = s.replace("\\n", "\n")
    s = s.replace("\n", "\\n")
    return s

def extract_dart(text):
    text = strip_comments(text)
    pattern = r'"([^"\$]+)"\.tr'
    out = []
    for m in re.findall(pattern, text):
        out.append(normalize(m))
    return out

def extract_json_keys(path):
    with open(path, "r", encoding="utf-8") as f:
        raw = f.read()
    raw = strip_comments(raw)
    data = json.loads(raw)
    return list(data.keys())

def ask_langs():
    print("Paste the supported languages list below. Finish with an empty line:")
    lines = []
    while True:
        l = input()
        if l.strip() == "":
            break
        lines.append(l)

    text = "\n".join(lines)
    text = re.sub(r'//.*', '', text)
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)

    codes = re.findall(r"Locale\('([a-zA-Z\-]+)'\)", text)
    codes += re.findall(r'"([a-zA-Z\-]+)"', text)

    codes = sorted(list(set(codes)))

    print("Detected language codes:")
    for c in codes:
        print(c)

    return codes

def build_excel(keys, codes):
    wb = Workbook()
    ws = wb.active
    ws.append(["Key"] + codes)
    for k in keys:
        ws.append([k] + [""] * len(codes))
    return wb

def handle_dart():
    print("Choose Dart file")
    path = select_file("dart")
    if not path:
        print("No file selected")
        return

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    items = extract_dart(content)

    print("1. Print extracted strings")
    print("2. Convert to JSON")
    print("3. Generate translation.xlsx")
    choice = input("Select: ").strip()

    if choice == "1":
        for s in items:
            print(s)
        return

    if choice == "2":
        save = select_save("json")
        if not save:
            print("No destination selected")
            return
        data = {s: s for s in items}
        raw = json.dumps(data, ensure_ascii=False, indent=2)
        raw = raw.replace("\\\\n", "\\n")
        with open(save, "w", encoding="utf-8") as f:
            f.write(raw)
        print("Saved:", save)
        return

    if choice == "3":
        codes = ask_langs()
        wb = build_excel(items, codes)
        save = select_save("xlsx")
        if not save:
            print("No destination selected")
            return
        wb.save(save)
        print("Saved:", save)
        return

def handle_json():
    print("Choose JSON file")
    path = select_file("json")
    if not path:
        print("No file selected")
        return

    keys = extract_json_keys(path)

    print("1. Print all strings")
    print("2. Generate translation.xlsx")
    choice = input("Select: ").strip()

    if choice == "1":
        for k in keys:
            print(k)
        return

    if choice == "2":
        codes = ask_langs()
        wb = build_excel(keys, codes)
        save = select_save("xlsx")
        if not save:
            print("No destination selected")
            return
        wb.save(save)
        print("Saved:", save)
        return

def main():
    c = choose()
    if c == "1":
        handle_dart()
    elif c == "2":
        handle_json()
    else:
        print("Invalid option")

if __name__ == "__main__":
    main()
