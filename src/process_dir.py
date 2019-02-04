import glob
import sys
import subprocess


files = glob.glob(sys.argv[1] + "/*")
for i in files:
    print(i)
    subprocess.run(["python", "find_dice.py", "-i", i, "-o", sys.argv[2]])
