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

# === LamoushiAds ===
cfg = "khayel/export_presets.cfg"
with open(cfg, "r") as f:
    content = f.read()

if "plugins/LamoushiAds=true" in content:
    print("LamoushiAds already enabled")
elif "plugins/LamoushiAds" in content:
    content = content.replace("plugins/LamoushiAds=false", "plugins/LamoushiAds=true")
    with open(cfg, "w") as f:
        f.write(content)
    print("LamoushiAds enabled")
else:
    content = content.replace("[preset.0.options]", "[preset.0.options]\nplugins/LamoushiAds=true")
    with open(cfg, "w") as f:
        f.write(content)
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
keystore_path = cwd + "/khayel/script/lamoushi.keystore.jks"

os.makedirs(os.path.dirname(apk_path), exist_ok=True)

with open(cfg, "r") as f:
    content = f.read()

content = re.sub(r'export_path=.*', f'export_path="{apk_path}"', content)
content = re.sub(r'custom_template/debug=.*', 'custom_template/debug=""', content)
content = re.sub(r'custom_template/release=.*', 'custom_template/release=""', content)

# الإصلاح الجوهري: تحديد مسار android/build
content = re.sub(
    r'gradle_build/gradle_build_directory=.*',
    'gradle_build/gradle_build_directory="res://android/build"',
    content
)
print("gradle_build_directory set to res://android/build")

content += "\n"
content += 'keystore/debug="' + keystore_path + '"\n'
content += 'keystore/debug_user="lamoushi_key"\n'
content += 'keystore/debug_password="24ay58s.s24er58"\n'
content += 'keystore/release="' + keystore_path + '"\n'
content += 'keystore/release_user="lamoushi_key"\n'
content += 'keystore/release_password="24ay58s.s24er58"\n'

with open(cfg, "w") as f:
    f.write(content)

print("export_path:", apk_path)
print("keystore:", keystore_path)
if os.path.exists(keystore_path):
    print("Keystore found")
else:
    print("KEYSTORE NOT FOUND!")
