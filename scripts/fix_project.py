import os
import shutil
import subprocess
import re

cwd = os.getcwd()

# === copy plugins ===
plugins_src = "khayel/addons/plugins"
plugins_dst = "khayel/android/plugins"
if os.path.exists(plugins_src):
    os.makedirs(plugins_dst, exist_ok=True)
    for item in os.listdir(plugins_src):
        s = os.path.join(plugins_src, item)
        d = os.path.join(plugins_dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)
    print("Plugins copied:")
    print(os.listdir(plugins_dst))
else:
    print("No addons/plugins folder")

# === export_presets.cfg ===
cfg = "khayel/export_presets.cfg"
with open(cfg, "r") as f:
    content = f.read()

# === LamoushiAds ===
if "plugins/LamoushiAds=true" in content:
    print("LamoushiAds already enabled")
elif "plugins/LamoushiAds" in content:
    content = content.replace("plugins/LamoushiAds=false", "plugins/LamoushiAds=true")
    print("LamoushiAds enabled")
else:
    content = content.replace("[preset.0.options]", "[preset.0.options]\nplugins/LamoushiAds=true")
    print("LamoushiAds added")

# === ETC2/ASTC ===
godot_cfg = "khayel/project.godot"
with open(godot_cfg, "r") as f:
    godot_content = f.read()

if "import_etc2_astc=true" in godot_content:
    print("ETC2/ASTC already enabled")
elif "import_etc2_astc=false" in godot_content:
    godot_content = godot_content.replace("import_etc2_astc=false", "import_etc2_astc=true")
    with open(godot_cfg, "w") as f:
        f.write(godot_content)
    print("ETC2/ASTC enabled")
else:
    with open(godot_cfg, "a") as f:
        f.write("\n[rendering]\n\ntextures/vram_compression/import_etc2_astc=true\n")
    print("ETC2/ASTC added")

# === export_presets.cfg paths ===
repo = os.path.basename(os.environ.get("GITHUB_REPOSITORY", "BuildAPK/BuildAPK"))
apk_path = f"/home/runner/work/{repo}/{repo}/build/android/Khayel_Final.apk"

os.makedirs(os.path.dirname(apk_path), exist_ok=True)

# إعادة قراءة المحتوى بعد تعديل LamoushiAds
with open(cfg, "r") as f:
    content = f.read()

# إصلاح export_path
content = re.sub(r'export_path=.*', f'export_path="{apk_path}"', content)
print("export_path:", apk_path)

# إصلاح custom_template
content = re.sub(r'custom_template/debug=.*', 'custom_template/debug=""', content)
content = re.sub(r'custom_template/release=.*', 'custom_template/release=""', content)

# إصلاح gradle_build_directory
content = re.sub(
    r'gradle_build/gradle_build_directory=.*',
    'gradle_build/gradle_build_directory="res://android/build"',
    content
)
print("gradle_build_directory set to res://android/build")

# إصلاح use_gradle_build
if "gradle_build/use_gradle_build=true" in content:
    print("use_gradle_build already true")
else:
    content = re.sub(
        r'gradle_build/use_gradle_build=.*',
        'gradle_build/use_gradle_build=true',
        content
    )
    print("use_gradle_build set to true")

with open(cfg, "w") as f:
    f.write(content)

# تحقق نهائي
print("\n=== التحقق النهائي ===")
print("export_path:", apk_path)

# طباعة الأسطر المهمة من الملف
with open(cfg, "r") as f:
    for line in f:
        if any(k in line for k in ["export_path", "gradle_build", "use_gradle"]):
            print(line.rstrip())
