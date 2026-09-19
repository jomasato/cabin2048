"""Cut the shared part back out of index.html for publishing as an Artifact.

index.html is the source of truth. The Artifact host supplies its own
doctype/head/reset, so it wants the file without the standalone wrapper -
which is exactly what sits between the two markers.

    python tools/make_artifact.py            -> build/cabin2048.html
    python tools/make_artifact.py <out.html>
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
START = "<!-- shared:start"
END = "<!-- shared:end -->"


def main():
    src = io.open(os.path.join(HERE, "index.html"), encoding="utf-8").read()

    i = src.find(START)
    j = src.find(END)
    if i < 0 or j < 0:
        raise SystemExit("markers not found in index.html - did the wrapper get edited?")
    i = src.find("-->", i) + 3

    body = src[i:j].strip() + "\n"

    if len(sys.argv) > 1:
        out = os.path.abspath(sys.argv[1])
    else:
        out = os.path.join(HERE, "build", "cabin2048.html")
    if not os.path.isdir(os.path.dirname(out)):
        os.makedirs(os.path.dirname(out))

    io.open(out, "w", encoding="utf-8", newline="\n").write(body)
    print("wrote %s (%d bytes)" % (out, os.path.getsize(out)))


if __name__ == "__main__":
    main()
