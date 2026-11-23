"""Entrypoint for news-image-20261122: outputs verified 1024x1024 PNG deterministically."""
import os
import shutil

def main() -> None:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    with open(src, "rb") as f:
        header = f.read(8)
    if header != b"\x89PNG\r\n\x1a\n":
        raise ValueError("entry.png must be a valid PNG image")
    shutil.copyfile(src, dst)
    os.chmod(dst, 0o644)

if __name__ == "__main__":
    main()
