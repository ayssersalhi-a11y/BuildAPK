import os

path = "khayel/addons/gdffmpeg/gdffmpeg.gdextension"

if not os.path.exists(path):
    print("NOT FOUND:", path)
    exit(0)

with open(path, "r") as f:
    lines = f.readlines()

print("=== before ===")
for line in lines:
    print(repr(line))

new_lines = []
for line in lines:
    if "linux" in line.lower() and "=" in line:
        key = line.split("=")[0].strip()
        new_lines.append(key + ' = ""\n')
        print("PATCHED:", repr(line), "->", repr(key + ' = ""\n'))
    else:
        new_lines.append(line)

with open(path, "w") as f:
    f.writelines(new_lines)

print("=== after ===")
with open(path, "r") as f:
    print(f.read())
