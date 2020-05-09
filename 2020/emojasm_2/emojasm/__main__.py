from io import StringIO

import argparse
from emojasm.run import run

ap = argparse.ArgumentParser()
ap.add_argument("file", type=argparse.FileType(encoding="utf-8"))
ap.add_argument("--d0", help="Initial data tape 0")
ap.add_argument("--d1", help="Initial data tape 1")
ap.add_argument("--d2", help="Initial data tape 2")
ap.add_argument("-m", help="Maximum instructions to run", type=int, default=200)
ap.add_argument("-n", help="Disallow reading input", default=True, action="store_false")
args = ap.parse_args()

src = args.file.read()
initial_data = (args.d0, args.d1, args.d2)

print(" ".join(hex(ord(c))[2:] for c in src))
run(src, initial_data, args.m, args.n)
