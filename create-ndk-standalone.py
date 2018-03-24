import os
import sys
import subprocess
import platform

print(platform.system())

ndk_root = None

env_probes = ['ANDROID_NDK_HOME', 'ANDROID_NDK_ROOT', 'NDK_ROOT']
for env_var in env_probes:
    if not ndk_root and env_var in os.environ:
        ndk_root = os.environ[env_var]
        break

curdir = os.path.dirname(os.path.abspath(__file__))
standalone_ndk = os.path.join(ndk_root, 'build/tools/make_standalone_toolchain.py') 
target_ndk_path = os.path.join(curdir, 'NDK')
if os.path.exists(standalone_ndk) and not os.path.exists(target_ndk_path):
    subprocess.Popen([sys.executable, standalone_ndk, '--api', '24',\
        '--arch', "arm64", '--install-dir', target_ndk_path])

usr_dir = os.path.expanduser("~")

toml_src = '''
[target.aarch64-linux-android]
ar = "{0}/bin/aarch64-linux-android-ar.cmd"
linker = "{0}/bin/aarch64-linux-android-clang.cmd"
'''.format(target_ndk_path.replace('\\','/'))
with open(os.path.join(usr_dir, '.cargo', 'config'), 'w') as toml:
    toml.write(toml_src)