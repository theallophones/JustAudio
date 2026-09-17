#!/usr/bin/env python3
"""
add_mix.py — add a new private mix and get a shareable link.

Usage:
    python3 add_mix.py "Track Title" /path/to/file.mp3

First run will ask for your site's base URL (your GitHub Pages address)
and remember it in config.txt. After that, just run it with a title and
a file every time you want to share a new mix.

Run this from inside the mixsite folder (the one with audio/, mixes/, template/).
"""
import argparse
import secrets
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TEMPLATE = ROOT / "template" / "player_template.html"
AUDIO_DIR = ROOT / "audio"
MIXES_DIR = ROOT / "mixes"
CONFIG = ROOT / "config.txt"


def get_base_url(cli_value):
    if cli_value:
        CONFIG.write_text(cli_value.strip().rstrip("/") + "\n")
        return cli_value.strip().rstrip("/")
    if CONFIG.exists():
        return CONFIG.read_text().strip()
    print("First time setup: what's your GitHub Pages URL for this site?")
    print("e.g. https://yourname.github.io/mixsite")
    url = input("> ").strip().rstrip("/")
    CONFIG.write_text(url + "\n")
    return url


def make_id():
    # short, random, unguessable — this is what keeps a mix private
    return secrets.token_urlsafe(6).replace("_", "").replace("-", "")[:8]


def escape_for_js_string(text):
    return text.replace("\\", "\\\\").replace('"', '\\"')


def main():
    parser = argparse.ArgumentParser(description="Add a new private mix and get a shareable link.")
    parser.add_argument("title", help="Track / mix title, shown to the client")
    parser.add_argument("audio_file", help="Path to the audio file (mp3, wav, m4a, etc.)")
    parser.add_argument("--base-url", help="Your site's base URL (only needed once)", default=None)
    parser.add_argument("--no-git", action="store_true", help="Skip git add/commit/push")
    args = parser.parse_args()

    audio_path = Path(args.audio_file).expanduser()
    if not audio_path.exists():
        sys.exit(f"Can't find {audio_path}")

    base_url = get_base_url(args.base_url)
    mix_id = make_id()
    ext = audio_path.suffix.lower()
    audio_dest_name = f"{mix_id}{ext}"

    AUDIO_DIR.mkdir(exist_ok=True)
    MIXES_DIR.mkdir(exist_ok=True)

    shutil.copy2(audio_path, AUDIO_DIR / audio_dest_name)

    template_html = TEMPLATE.read_text(encoding="utf-8")
    page_html = template_html.replace(
        "__TITLE__", escape_for_js_string(args.title)
    ).replace(
        "__AUDIO_SRC__", f"../audio/{audio_dest_name}"
    )
    (MIXES_DIR / f"{mix_id}.html").write_text(page_html, encoding="utf-8")

    link = f"{base_url}/mixes/{mix_id}.html"

    if not args.no_git and (ROOT / ".git").exists():
        try:
            subprocess.run(["git", "add", "audio", "mixes"], cwd=ROOT, check=True)
            subprocess.run(["git", "commit", "-m", f"Add mix: {args.title}"], cwd=ROOT, check=True)
            subprocess.run(["git", "push"], cwd=ROOT, check=True)
            print("Pushed to GitHub.\n")
        except subprocess.CalledProcessError as e:
            print(f"Git step didn't go through ({e}). Push manually when you're ready.\n")

    print("Share this link with your client:")
    print(link)


if __name__ == "__main__":
    main()
