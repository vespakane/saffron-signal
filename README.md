# saffron-signal

A two-sided messaging mock-up. Add suppliers, message them as yourself from the **Me** side, then switch to the **Suppliers** side to reply as each supplier. Photos, unread badges and read ticks all work; everything is stored in the browser.

Open `index.html` in a browser (best on an iPhone, or in a desktop browser where it renders inside a phone frame).

## Editing

- `src/src.html` is the page template; `src/assets.json` holds the embedded images.
- Run `python3 src/build.py` to regenerate `index.html`.
- `src/make_assets.py` rebuilds `assets.json` from reference screenshots placed in the repo root (not committed).
