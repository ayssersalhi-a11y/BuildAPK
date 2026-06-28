# scripts/fix_gdffmpeg.py
import os

path = "khayel/addons/gdffmpeg/gdffmpeg.gdextension"

if not os.path.exists(path):
    print("NOT FOUND:", path)
    exit(0)

with open(path, "r") as f:
    content = f.read()

print("=== before ===")
print(content)

# الحل الجذري: اكتب الملف من الصفر بدون أي مكتبة linux
new_content = """[configuration]
entry_symbol = "gdextension_init"
compatibility_minimum = "4.1"

[libraries]
windows.x86_64 = ""
macos.x86_64 = ""
android.arm64 = ""
android.x86_64 = ""
"""

with open(path, "w") as f:
    f.write(new_content)

print("=== after ===")
print(new_content)
