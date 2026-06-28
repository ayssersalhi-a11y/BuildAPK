import os

path = "khayel/addons/gdffmpeg/gdffmpeg.gdextension"

if not os.path.exists(path):
    print("gdffmpeg.gdextension not found")
    exit(0)

with open(path, "r") as f:
    content = f.read()

print("=== before ===")
print(content)

lines = content.splitlines()
new_lines = []
for line in lines:
    if "linux" in line.lower() and "=" in line:
        key = line.split("=")[0].strip()
        new_lines.append(key + ' = ""')
    else:
        new_lines.append(line)

result = "\n".join(new_lines) + "\n"

with open(path, "w") as f:
    f.write(result)

print("=== after ===")
print(result)
