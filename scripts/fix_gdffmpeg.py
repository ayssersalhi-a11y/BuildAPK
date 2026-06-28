import os
import shutil

cwd = os.getcwd()

# 1. احذف المجلد كلياً
addon_dir = "khayel/addons/gdffmpeg"
if os.path.exists(addon_dir):
    shutil.rmtree(addon_dir)
    print("DELETED:", addon_dir)
else:
    print("Already gone:", addon_dir)

# 2. أزل المرجع من project.godot
project_file = "khayel/project.godot"
with open(project_file, "r") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if "gdffmpeg" in line.lower():
        print("REMOVED from project.godot:", repr(line.strip()))
        continue
    new_lines.append(line)

with open(project_file, "w") as f:
    f.writelines(new_lines)

# 3. أزل المرجع من أي ملف .cfg أو .tres
for root, dirs, files in os.walk("khayel"):
    # تجاهل .godot cache
    dirs[:] = [d for d in dirs if d != ".godot"]
    for fname in files:
        if fname.endswith((".cfg", ".tres", ".tscn", ".gd")):
            fpath = os.path.join(root, fname)
            try:
                with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                if "gdffmpeg" in content.lower():
                    new_content = "\n".join(
                        line for line in content.splitlines()
                        if "gdffmpeg" not in line.lower()
                    )
                    with open(fpath, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    print("Cleaned gdffmpeg from:", fpath)
            except Exception as e:
                print("Skip:", fpath, e)

print("=== gdffmpeg fully removed ===")

# تحقق نهائي
remaining = []
for root, dirs, files in os.walk("khayel"):
    dirs[:] = [d for d in dirs if d != ".godot"]
    for fname in files:
        fpath = os.path.join(root, fname)
        try:
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                if "gdffmpeg" in f.read().lower():
                    remaining.append(fpath)
        except:
            pass

if remaining:
    print("WARNING - gdffmpeg still found in:")
    for r in remaining:
        print(" ", r)
else:
    print("CLEAN - No gdffmpeg references remain")
