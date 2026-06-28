import os
import subprocess
import shutil
import re

cwd = os.getcwd()
home = os.path.expanduser("~")
template_path = home + "/.local/share/godot/export_templates/4.7.stable"
build_dir = cwd + "/khayel/android/build"

os.makedirs(build_dir, exist_ok=True)

src = template_path + "/android_source.zip"
dst = build_dir + "/android_source.zip"
shutil.copy2(src, dst)
print("android_source.zip copied")

os.chdir(build_dir)
subprocess.run(["unzip", "-qo", "android_source.zip"], check=True)
os.remove("android_source.zip")

for root, dirs, files in os.walk("."):
    for fname in files:
        if fname == "project.godot":
            os.remove(os.path.join(root, fname))
            print("deleted:", os.path.join(root, fname))

# استخرج الإصدار من Godot binary
godot_bin = cwd + "/godot"
result = subprocess.run(
    [godot_bin, "--version"],
    capture_output=True, text=True
)
version_raw = result.stdout.strip() + result.stderr.strip()
print("Godot version output:", repr(version_raw))

match = re.search(r'(\d+\.\d+\.stable)', version_raw)
if match:
    version = match.group(1)
else:
    version = "4.7.stable"

print("Using version:", version)

# كتابة .build_version في مكانه الصحيح
with open(".build_version", "w") as f:
    f.write(version)

with open(".build_version", "r") as f:
    content = f.read()
print("build_version:", repr(content))
print("size:", os.path.getsize(".build_version"), "bytes")

# الإصلاح الجوهري: إنشاء ملف _was_built داخل android/build
# هذا ما يبحث عنه Godot للتأكد من تثبيت الـ template
with open("_was_built", "w") as f:
    f.write("")
print("_was_built created")

# أعد للمسار الأصلي
os.chdir(cwd)

# أخبر Godot أن android template مثبت عبر .godot folder
godot_dir = cwd + "/khayel/.godot"
os.makedirs(godot_dir, exist_ok=True)

android_cfg = godot_dir + "/android_build_version.cfg"
with open(android_cfg, "w") as f:
    f.write(version)

print("android_build_version.cfg written:", version)

# تحقق نهائي
print("=== التحقق النهائي ===")
print("build_version:", open(build_dir + "/.build_version").read())
print("_was_built:", os.path.exists(build_dir + "/_was_built"))
print("android_build_version.cfg:", open(android_cfg).read())
