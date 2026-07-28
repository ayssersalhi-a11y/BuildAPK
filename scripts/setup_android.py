# scripts/setup_android.py
import os

cwd = os.getcwd()
android_home = "/home/runner/android-sdk"

config_dir = os.path.expanduser("~/.config/godot")
os.makedirs(config_dir, exist_ok=True)

settings_path = config_dir + "/editor_settings-4.7.tres"

content = '[gd_resource type="EditorSettings" format=3]\n\n[resource]\n'
content += f'export/android/sdk_path = "{android_home}"\n'
content += 'export/android/force_system_user = false\n'
content += 'export/android/use_custom_build = true\n'

with open(settings_path, "w") as f:
    f.write(content)

print("Settings written:")
print(content)
