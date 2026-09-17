# mixsite

A tiny, independent site for sharing private mixes with clients. No accounts,
no third-party service, no AI in the loop after this point — just a GitHub
repo and a script.

Every mix gets its own page with a waveform player and a unique link. There's
no shared list of all your mixes anywhere on the site, so a client with one
link can't stumble onto anyone else's.

## How it works

- `template/player_template.html` — the player page, waveform + play button
- `add_mix.py` — run this locally to add a new mix
- `audio/` — where the actual audio files live
- `mixes/` — one generated HTML page per mix, e.g. `mixes/xJ4kLm2p.html`

Running the script copies your audio file into `audio/`, generates a new
page in `mixes/` with that file loaded into the player, and (if you're using
git) commits and pushes it. It then prints the link you send to your client.

## One-time setup

1. Create a new **public** GitHub repo (needs to be public for GitHub Pages
   to serve it for free). Call it whatever you want, e.g. `mixsite`.
2. Push this folder to that repo:
   ``` 
   cd mixsite
   git init
   git add .
   git commit -m "initial commit"
   git branch -M main
   git remote add origin https://github.com/yourname/mixsite.git
   git push -u origin main
   ```
3. On GitHub: **Settings → Pages → Build and deployment → Source: Deploy from
   a branch → Branch: main / (root)**. Save. GitHub gives you a URL like
   `https://yourname.github.io/mixsite`. It takes a minute or two to go live
   the first time.

## Adding a mix

```
python3 add_mix.py "Song Title - Mix v3" ~/Desktop/song_mixv3.mp3
```

First time you run it, it'll ask for your GitHub Pages URL from step 3 above
and remember it. Every run after that just needs the title and the file.

It prints a link at the end, something like:

```
https://yourname.github.io/mixsite/mixes/xJ4kLm2p.html
```

That's what you send the client.

## Worth knowing

- The repo has to be public for free GitHub Pages, which means the audio
  files are technically reachable by anyone who has the exact link — same
  model as a WeTransfer or Dropbox share link. The mix ID is a random
  8-character string, not guessable, and it's never listed anywhere public.
  Don't post the links anywhere public and this stays effectively private.
- If a client leaks a link, that one mix is exposed, not the others. Nothing
  connects the mixes to each other.
- To take a mix down later, just delete its `.html` file from `mixes/` and
  its audio file from `audio/`, commit, push.
- GitHub has a 100MB per-file limit and is unhappy with binary-heavy repos
  after a while, so this is built for reference mixes, not full mastered
  albums or huge stem bundles.
