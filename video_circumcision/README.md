# Does Circumcision Count If a Non-Jew Performs It?

A ~17-minute 1080p explainer video (English narration, burned-in subtitles) on the
halachic question *milah al yedei goy* — from Genesis 17 and the Talmud (Avodah Zarah 27a)
to the Rambam, the Shulchan Aruch and the Rema — with the logic of each opinion written
and run as JavaScript on screen.

The video is an educational walk-through of the sources, not a halachic ruling.

## Outline

| Chapter | Scene | Topic |
|---|---|---|
| — | `s01_hook` | The hospital scenario, the question |
| 1 | `s02_covenant`, `s03_steps` | Covenant of Abraham; milah, periah, metzitzah, brachot (`brit-steps.js`) |
| 2 | `s04_who` | Who is fit to circumcise; Tzipporah |
| 3 | `s05_talmud`, `s06_code_rav` | Rav vs. Rabbi Yochanan (`avodah-zarah-27a.js`) |
| 4 | `s07_intent` | Intention: R. Yehudah vs. R. Yosei (`kavanah.js`) |
| 5 | `s08_rambam` | Lechatchila / bedieved (`rambam.js`) |
| 6 | `s09_sa`, `s10_hatafa` | Shulchan Aruch, Rema, hatafat dam brit (`shulchan-aruch.js`) |
| 7 | `s11_cases` | Six practical cases (`brit.js`) |
| 8 | `s12_practice`, `s13_outro` | Practical notes, summary |

All on-screen JS is actually executed at render time — the "terminal" shows real `console.log` output.

## How it is built

- `src/narration_en.json` — narration script per scene (`narration.json` — earlier Russian draft).
- `tools/tts_en.py` — narration via Edge TTS (`en-US-AndrewNeural`), sentence timings → subtitles.
- `tools/fetch2.py` + `src/assets2.json` — images from Library of Congress, Wellcome Collection, Cleveland Museum of Art (public domain / CC0 / CC BY).
- `tools/clips.sh` — archival footage from Internet Archive (public domain):
  "Jérusalem, 1918", "The Life of the Jews in Palestine" (1913), "A Pilgrimage Through Palestine" (1920).
- `src/scenes_en.js` — storyboard; every beat is tied to a narration sentence (`cue`).
- `src/engine.js` + `src/stage.html` — deterministic HTML/JS scene engine (`renderAt(t)`).
- `src/render.js` — Playwright captures frames at 25 fps → ffmpeg.
- `tools/audio.py` — voice + quiet ambient pad, −16 LUFS, `.srt` subtitles.

```bash
python3 tools/tts_en.py src/narration_en.json build/audio_en
LANG_VIDEO=en NODE_PATH=$(npm root -g) node src/render.js scenes
python3 tools/audio.py build scenes_en.js audio_en out_en
```

Full image/footage credits are in the closing titles of the video.
