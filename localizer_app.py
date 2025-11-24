import json
import re
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from openpyxl import Workbook

def strip_comments(text):
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
    out = []
    for line in text.splitlines():
        line = re.sub(r'//.*', '', line)
        if line.strip():
            out.append(line)
    return "\n".join(out)

def normalize(s):
    s = s.replace("\\n", "\n")
    s = s.replace("\n", "\\n")
    return s

def extract_dart_strings(path):
    with open(path, "r", encoding="utf-8") as f:
        t = strip_comments(f.read())
    pattern = r'"([^"\$]+)"\.tr'
    out = []
    for m in re.findall(pattern, t):
        out.append(normalize(m))
    return out

def extract_json_keys(path):
    with open(path, "r", encoding="utf-8") as f:
        t = strip_comments(f.read())
    data = json.loads(t)
    return list(data.keys())

def ask_languages_popup(root):
    win = tk.Toplevel(root)
    win.title("Language Codes")
    win.geometry("420x450")
    win.attributes("-topmost", True)

    frame = tk.Frame(win)
    frame.pack(expand=True, fill="both", padx=10, pady=10)

    txt = tk.Text(frame, height=20)
    txt.pack(expand=True, fill="both")

    val = tk.StringVar()

    def done(event=None):
        val.set(txt.get("1.0", tk.END))
        win.destroy()

    btn_frame = tk.Frame(win)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="OK", width=12, command=done).pack()

    win.bind("<Control-Return>", done)
    win.bind("<Command-Return>", done)

    root.wait_window(win)

    raw = val.get()
    raw = re.sub(r'//.*', '', raw)
    raw = re.sub(r'/\*.*?\*/', '', raw, flags=re.DOTALL)

    codes = []
    codes += re.findall(r"Locale\('([a-zA-Z\-]+)'\)", raw)
    codes += re.findall(r'"([a-zA-Z\-]+)"', raw)
    codes += re.findall(r'\b([a-zA-Z]{2,3}(?:-[A-Za-z0-9]+)?)\b', raw)

    codes = sorted(list(set([c for c in codes if len(c) >= 2])))

    return codes


def build_excel(keys, codes, save_path):
    wb = Workbook()
    ws = wb.active
    header = ["en", "en"] + codes
    ws.append(header)
    r = 2
    for k in keys:
        row = [k, k]
        for lang in codes:
            row.append('=GOOGLETRANSLATE($A' + str(r) + ', "en", "' + lang + '")')
        ws.append(row)
        r += 1
    wb.save(save_path)

def create_app():
    root = tk.Tk()
    root.title("Localization Tool")
    root.geometry("500x400")

    selected_file = tk.StringVar()
    log = tk.StringVar()

    def log_msg(msg):
        log.set(msg)

    def choose_dart():
        p = filedialog.askopenfilename(filetypes=[("Dart files", "*.dart")])
        if p:
            selected_file.set(p)
            log_msg("Dart file selected")

    def choose_json():
        p = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if p:
            selected_file.set(p)
            log_msg("JSON file selected")

    def convert_to_json():
        p = selected_file.get()
        if not p:
            messagebox.showerror("Error", "No file selected")
            return
        try:
            items = extract_dart_strings(p)
            save = filedialog.asksaveasfilename(defaultextension=".json")
            if save:
                data = {s: s for s in items}
                raw = json.dumps(data, ensure_ascii=False, indent=2)
                raw = raw.replace("\\\\n", "\\n")
                with open(save, "w", encoding="utf-8") as f:
                    f.write(raw)
                log_msg("JSON saved")
        except:
            messagebox.showerror("Error", "Conversion failed")

    def generate_excel():
        p = selected_file.get()
        if not p:
            messagebox.showerror("Error", "No file selected")
            return
        try:
            keys = extract_dart_strings(p) if p.endswith(".dart") else extract_json_keys(p)
            codes = ask_languages_popup(root)
            save = filedialog.asksaveasfilename(defaultextension=".xlsx")
            if save:
                build_excel(keys, codes, save)
                log_msg("Excel saved")
        except:
            messagebox.showerror("Error", "Failed to generate Excel")

    ttk.Button(root, text="Select Dart File", command=choose_dart).pack(pady=10)
    ttk.Button(root, text="Select JSON File", command=choose_json).pack(pady=10)
    ttk.Button(root, text="Convert Dart → JSON", command=convert_to_json).pack(pady=10)
    ttk.Button(root, text="Generate translation.xlsx", command=generate_excel).pack(pady=10)

    tk.Label(root, textvariable=log, fg="green").pack(pady=20)
    root.mainloop()

create_app()
