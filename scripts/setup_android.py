import os
import subprocess

cwd = os.getcwd()
android_home = os.environ.get("ANDROID_HOME", "/home/runner/android-sdk")
keystore_path = cwd + "/khayel/script/lamoushi.keystore.jks"

config_dir = os.path.expanduser("~/.config/godot")
os.makedirs(config_dir, exist_ok=True)

settings_path = config_dir + "/editor_settings-4.7.tres"

content = '[gd_resource type="EditorSettings" format=3]\n'
content += "\n"
content += "[resource]\n"
content += 'export/android/sdk_path = "' + android_home + '"\n'
content += 'export/android/debug_keystore = "' + keystore_path + '"\n'
content += 'export/android/debug_keystore_user = "lamoushi_key"\n'
content += 'export/android/debug_keystore_pass = "24ay58s.s24er58"\n'

with open(settings_path, "w") as f:
    f.write(content)

print("editor_settings written:")
print(content)
