import os
import tkinter as tk
from tkinter import filedialog, messagebox
import csv
from pathlib import Path

input_folder = Path("input_texts")
output_file = Path("Αποτελέσματα.txt")

# Πλήκτρα για παύσεις
watched_keys = {".", "!", "@", "#", "%", "&", "(", ")", "Backspace",
                "[", "]", "|", "/", "<", ">", "?", "Enter"}

# Αντιστοίχιση keycodes με σύμβολα
key_mapping = {
    "8": "Backspace", "9": "Tab", "13": "Enter", "16": "Shift", "17": "Ctrl",
    "18": "Alt", "19": "Pause/break", "20": "Caps Lock", "27": "Esc",
    "32": "Spacebar", "33": "Page up", "34": "Page down", "35": "End",
    "36": "Home", "37": "Left Arrow", "38": "Up Arrow", "39": "Right Arrow",
    "40": "Down Arrow", "44": "Print-Screen", "45": "Insert", "46": "Delete",
    "48": ")", "49": "!", "50": "@", "51": "#", "52": "$", "53": "%", "54": "^",
    "55": "&", "56": "*", "57": "(", "91": "Left Windows", "92": "Right Windows",
    "93": "Application (menu key)", "112": "F1", "113": "F2", "114": "F3", "115": "F4",
    "116": "F5", "117": "F6", "118": "F7", "119": "F8", "120": "F9", "121": "F10",
    "122": "F11", "123": "F12", "144": "Num Lock", "145": "Scroll Lock",
    "160": "Left Shift", "161": "Right Shift", "162": "Left Ctrl", "163": "Right Ctrl",
    "164": "Left Alt", "165": "Right Alt",
}

# Όλα τα πλήκτρα για προβολή
all_symbols = {
    "8": "Backspace", "9": "Tab", "13": "Enter", "16": "Shift", "17": "Ctrl",
    "18": "Alt", "19": "Pause/break", "20": "Caps Lock", "27": "Esc",
    "32": "Spacebar", "33": "Page up", "34": "Page down", "35": "End",
    "36": "Home", "37": "Left Arrow", "38": "Up Arrow", "39": "Right Arrow",
    "40": "Down Arrow", "44": "Print-Screen", "45": "Insert", "46": "Delete",
    "48": ")", "49": "!", "50": "@", "51": "#", "52": "$", "53": "%", "54": "^",
    "55": "&", "56": "*", "57": "(", "91": "Left Windows", "92": "Right Windows",
    "93": "Application (menu key)", "112": "F1", "113": "F2", "114": "F3", "115": "F4",
    "116": "F5", "117": "F6", "118": "F7", "119": "F8", "120": "F9", "121": "F10",
    "122": "F11", "123": "F12", "144": "Num Lock", "145": "Scroll Lock",
    "160": "Left Shift", "161": "Right Shift", "162": "Left Ctrl", "163": "Right Ctrl",
    "164": "Left Alt", "165": "Right Alt", "96": "0", "97": "1", "98": "2", "99": "3",
    "100": "4", "101": "5", "102": "6", "103": "7", "104": "8", "105": "9", "106": "*",
    "107": "+", "108": "Separator", "109": "-",
    "186": ";", "187": "=", "189": "_",
    "192": "`", "219": "[", "220": "\\", "221": "]", "222": "'"
}




def analyze_files(input_folder):
    output_file = Path(input_folder)/"Αποτελέσματα.txt"
    txt_files = [f for f in Path(input_folder).glob("*.txt") if f.name != "Αποτελέσματα.txt"]

    if not txt_files:
        messagebox.showwarning("Σφάλμα", "Λάθος αρχείο!")
        return

    first_file = True

    with output_file.open("w", encoding="utf-8", newline='') as outfile:
        writer = csv.writer(outfile)

        # Δημιουργούμε λίστα με μοναδικά πλήκτρα, χωρίς διπλότυπα και με διατήρηση σειράς
        seen = set()
        keys_to_show = []
        for symbol in all_symbols.values():
            if symbol not in seen:
                seen.add(symbol)
                keys_to_show.append(symbol)

        for filepath in txt_files:
            key_counts = {}
            pause_after_keys = {k: 0 for k in watched_keys}
            total_keys_pressed = 0
            gender = "Unknown"
            previous_key = None
            previous_time = None

            with filepath.open("r", encoding="utf-8") as infile:
                lines = infile.readlines()

            data_start_index = 0
            for i, line in enumerate(lines):
                clean_line = line.strip().strip('"')
                if clean_line.lower().startswith("gender"):
                    gender = clean_line
                elif clean_line and (clean_line.startswith("74") or clean_line[0].isdigit()):
                    data_start_index = i
                    break

            with filepath.open("r", encoding="utf-8") as infile:
                for _ in range(data_start_index):
                    next(infile)

                reader = csv.reader(infile)
                shift_pressed = False

                for row in reader:
                    if len(row) < 4:
                        continue
                    try:
                        keycode_str = row[0].strip()
                        timestamp = float(row[2])
                        event_type = row[3].strip('"')
                    except ValueError:
                        continue

                    if event_type not in ("dn", "up"):
                        continue

                    if keycode_str == "16":
                        if event_type == "dn":
                            shift_pressed = True
                        elif event_type == "up":
                            shift_pressed = False

                    symbol = all_symbols.get(keycode_str, key_mapping.get(keycode_str, keycode_str))

                    if symbol in keys_to_show:
                        key_counts[symbol] = key_counts.get(symbol, 0) + 1
                        total_keys_pressed += 1

                    if previous_key in watched_keys and previous_time is not None:
                        if (timestamp - previous_time) > 5.0:
                            pause_after_keys[previous_key] += 1

                    previous_time = timestamp
                    previous_key = symbol

            if first_file:
                writer.writerow(keys_to_show)

            key_counts_line = []
            for key in keys_to_show:
                count = key_counts.get(key, 0)
                if count > 0 and total_keys_pressed > 0:
                    key_counts_line.append(f"{count / total_keys_pressed:.3f}")
                else:
                    key_counts_line.append("")
            writer.writerow(key_counts_line)

            pause_keys_ordered = ["!", "Enter", "Spacebar", "Delete", ".", "Tab", "(", ")", "?"]
            if first_file:
                writer.writerow(pause_keys_ordered)

            MIN_KEY_PRESSES = 5
            line = []
            for k in pause_keys_ordered:
                count = key_counts.get(k, 0)
                pauses = pause_after_keys.get(k, 0)
                if count >= MIN_KEY_PRESSES:
                    ratio = pauses / count
                    line.append(f"{ratio:.3f}" if ratio > 0 else "")
                else:
                    line.append("")
            writer.writerow(line)

            gender = gender.replace("Gender:", "").strip()
            outfile.write(f"{gender}\n")

            first_file = False




def browse_folder():
    folder = filedialog.askdirectory()
    if folder:
        entry_folder.delete(0, tk.END)
        entry_folder.insert(0, folder)

def run_analysis():
    input_folder = entry_folder.get()
    if not os.path.isdir(input_folder):
        messagebox.showerror("Σφάλμα",  "Διάλεξε τον σωστό φάκελο!")
        return

    analyze_files(input_folder)
    output_file=Path(input_folder)/"Αποτελέσματα.txt"
    os.startfile(output_file)



root = tk.Tk()
root.title("Ανάλυση αρχείων")
root.geometry("500x200")

label = tk.Label(root, text="Επιλέξτε φάκελο", font=("Arial", 11))
label.pack()

frame = tk.Frame(root)
frame.pack()

entry_folder = tk.Entry(frame, width=40)
entry_folder.pack(side=tk.LEFT, padx=5)

browse_btn = tk.Button(frame, text="Αναζήτηση", command=browse_folder)
browse_btn.pack(side=tk.LEFT)

analyze_btn = tk.Button(root, text="Εκτέλεση Ανάλυσης", command=run_analysis, bg="#4CAF50", fg="white", font=("Arial", 11))
analyze_btn.pack(pady=20)

# Εκκίνηση του GUI
root.mainloop()