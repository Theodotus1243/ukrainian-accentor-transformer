import fileinput
from os.path import join, dirname

with open(join(dirname(__file__), "version.py"), "r", encoding="utf-8") as v:
    for line in v.readlines():
        if line.startswith("__version__"):
            if '"' in line:
                version = line.split('"')[1]
            else:
                version = line.split("'")[1]

if "a" not in version:
    parts = version.split('.')
    parts[-1] = str(int(parts[-1]) + 1)
    version = '.'.join(parts)
    version = f"{version}a0"
else:
    post = version.split("a")[1]
    new_post = int(post) + 1
    version = version.replace(f"a{post}", f"a{new_post}")

for line in fileinput.input(join(dirname(__file__), "version.py"), inplace=True):
    if line.startswith("__version__"):
        print(f"__version__ = \"{version}\"")
    else:
        print(line.rstrip('\n'))
