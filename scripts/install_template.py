import os
import subprocess
import shutil

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

with open(".build_version", "w") as f:
    f.write("4.7.stable")

with open(".build_version", "r") as f:
    content = f.read()
print("build_version:", repr(content))
print("size:", os.path.getsize(".build_version"), "bytes")
