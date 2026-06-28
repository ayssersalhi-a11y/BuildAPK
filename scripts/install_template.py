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

# ← الإصلاح: اقرأ الإصدار من ملف version.txt داخل التيمبليت نفسه
version_file = template_path + "/version.txt"
if os.path.exists(version_file):
    with open(version_file, "r") as f:
        version = f.read().strip()
    print("Version from template:", repr(version))
else:
    # fallback: استخرج من Godot binary
    godot_bin = cwd + "/godot"
    result = subprocess.run(
        [godot_bin, "--version"],
        capture_output=True, text=True
    )
    version_raw = (result.stdout + result.stderr).strip()
    print("Godot version output:", repr(version_raw))

    # يطابق: 4.7.stable.official.abc1234 أو 4.7.stable.mono.abc
    match = re.search(r'([\d]+\.[\d]+\.stable[^\s]*)', version_raw)
    version = match.group(1) if match else "4.7.stable.official"
    print("Parsed version:", version)

# اكتب .build_version
with open(".build_version", "w", newline="\n") as f:
    f.write(version)

print("build_version written:", repr(version))
print("size:", os.path.getsize(".build_version"), "bytes")

with open("_was_built", "w") as f:
    f.write("")
print("_was_built created")

os.chdir(cwd)

godot_dir = cwd + "/khayel/.godot"
os.makedirs(godot_dir, exist_ok=True)

android_cfg = godot_dir + "/android_build_version.cfg"
with open(android_cfg, "w", newline="\n") as f:
    f.write(version)

print("android_build_version.cfg written:", version)

# تحقق نهائي
print("=== التحقق النهائي ===")
v1 = open(build_dir + "/.build_version").read()
v2 = open(android_cfg).read()
print("build_version:", repr(v1))
print("android_build_version.cfg:", repr(v2))
print("match:", v1 == v2)
if v1 != v2:
    raise RuntimeError("VERSION MISMATCH - سيفشل البناء!")
