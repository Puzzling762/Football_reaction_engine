import re

SAVE_PATH = "C:\\Users\\raj37\\OneDrive\\Documents\\FIFA 14\\Career 20250920004212#Career - Manager Progress 1"


def extract_printable_strings(data, min_len=4):
    pattern = re.compile(rb'[\x20-\x7e]{%d,}' % min_len)
    return [s.decode('utf-8', errors='replace') for s in pattern.findall(data)]

with open(SAVE_PATH, 'rb') as f:
    data = f.read()

strings = extract_printable_strings(data, min_len=4)

with open("extracted_strings.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(strings))

print("Strings extracted. Check extracted_strings.txt for table names, players, and teams.")
