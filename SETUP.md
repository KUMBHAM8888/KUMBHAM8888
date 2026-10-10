# Setup (about 5 minutes)

1. **Create the special repo** on GitHub named exactly `KUMBHAM8888` (same as your username), Public, with a README. Whatever is in its README shows on your profile page.

2. **Copy these files into it** (keep the folder structure):
   ```
   README.md
   profile-card.svg
   generate_card.py
   .github/workflows/update-game.yml
   ```

3. **Put your face in the ASCII portrait** (optional but it's the best part):
   ```
   pip install pillow
   python generate_card.py --photo your-photo.jpg
   ```
   Use a front-facing photo with a plain background. This overwrites `profile-card.svg`.
   To change any text on the card, edit the `CONFIG` block at the top of `generate_card.py` and re-run.

4. **Push**, then go to the repo's **Actions** tab → *Update Space Shooter Game* → **Run workflow**.
   It creates `game.gif` (the rocket shooting your contribution graph) and refreshes it daily.

5. Open `github.com/KUMBHAM8888` — done.
