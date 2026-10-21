// Usage:
//   node render.js preview <sceneId> <t1,t2,...>   -> out/preview/<id>_<t>.jpg
//   node render.js scenes [id ...]                 -> out/scenes/<id>.mp4 (video only)
const fs = require("fs");
const path = require("path");
const { spawn } = require("child_process");
const { chromium } = require("playwright");

const ROOT = __dirname;
const FPS = 25, HEAD = 0.5, TAIL = 0.6, CREDITS_DUR = 14;
const EN = process.env.LANG_VIDEO === "en";
const scenes = require(EN ? "./scenes_en.js" : "./scenes.js");
const AUDIO = EN ? "audio_en" : "audio", OUT = EN ? "out_en" : "out";
const credits = JSON.parse(fs.readFileSync(path.join(ROOT, "assets/credits.json"), "utf8"));

const CLIPS = {
  wall1918: "«Jérusalem, 1918», newsreel — Internet Archive (public domain)",
  wall1918b: "«Jérusalem, 1918», newsreel — Internet Archive (public domain)",
  oldcity: "«Jérusalem, 1918», newsreel — Internet Archive (public domain)",
  panorama: "«Jérusalem, 1918», newsreel — Internet Archive (public domain)",
  arrival: "«The Life of the Jews in Palestine» (1913) — Internet Archive (public domain)",
  telaviv: "«The Life of the Jews in Palestine» (1913) — Internet Archive (public domain)",
  children13: "«The Life of the Jews in Palestine» (1913) — Internet Archive (public domain)",
  gymnasia: "«The Life of the Jews in Palestine» (1913) — Internet Archive (public domain)",
  pil_wall: "«A Pilgrimage Through Palestine» (1920) — Internet Archive (public domain)",
  pil_jer: "«A Pilgrimage Through Palestine» (1920) — Internet Archive (public domain)",
};

function assets() {
  const A = {};
  for (const [k, v] of Object.entries(credits)) A[k] = { src: `assets/${v.file}`, credit: v.credit };
  for (const [k, c] of Object.entries(CLIPS)) {
    const frames = fs.readdirSync(path.join(ROOT, "clips", k)).filter(f => f.endsWith(".jpg")).length;
    A[k] = { dir: `clips/${k}`, frames, fps: FPS, credit: c };
  }
  return A;
}

function creditsScene() {
  const seen = new Set(), lines = [];
  const used = JSON.stringify(scenes);
  const pick = (obj, f) => Object.entries(obj).filter(([k]) => used.includes(`"${k}"`)).map(([, v]) => f(v));
  for (const v of [...pick(credits, c => c.credit), ...pick(CLIPS, c => c)]) if (!seen.has(v)) { seen.add(v); lines.push(v); }
  return {
    def: { id: "s14_credits", chapter: "", beats: [{ type: "credits", title: EN ? "Image & footage sources" : "Источники изображений и видео", lines,
      note: EN ? "Texts: Torah (Genesis 17, Exodus 4), Talmud (Avodah Zarah 27a, Shabbat 135a), Rambam (Laws of Circumcision 2:1), Shulchan Aruch and Rema (Yoreh Deah 264:1, 268:1). Narration: synthetic voice. This video is not a halachic ruling."
        : "Тексты: Тора (Бытие 17, Исход 4), Талмуд (Авода Зара 27а, Шабат 135а), Рамбам (Законы обрезания 2:1), Шулхан Арух и Рема (Йоре Деа 264:1, 268:1). Озвучка — синтез речи Silero. Видео не является галахическим решением." }] },
    meta: { id: "s14_credits", duration: CREDITS_DUR - HEAD - TAIL, sentences: [] },
  };
}

function plan() {
  const list = scenes.map(def => ({ def, meta: JSON.parse(fs.readFileSync(path.join(ROOT, AUDIO, def.id + ".json"), "utf8")) }));
  list.push(creditsScene());
  let off = 0;
  for (const s of list) { s.dur = HEAD + s.meta.duration + TAIL; s.offset = off; off += s.dur; }
  return { list, total: off };
}

async function openPage(browser) {
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  page.on("pageerror", e => console.error("PAGE ERROR", e.message));
  page.on("console", m => { if (m.type() === "error") console.error("console:", m.text()); });
  await page.goto("file://" + path.join(ROOT, "stage.html"));
  return page;
}

async function load(page, s, total, A) {
  return page.evaluate(([def, meta, info]) => window.loadScene(def, meta, info),
    [s.def, s.meta, { assets: A, offset: s.offset, total }]);
}

async function renderScene(browser, s, total, A) {
  const page = await openPage(browser);
  const dur = await load(page, s, total, A);
  const n = Math.round(dur * FPS);
  const out = path.join(ROOT, OUT + "/scenes", s.def.id + ".mp4");
  const ff = spawn("ffmpeg", ["-v", "error", "-y", "-f", "image2pipe", "-framerate", String(FPS), "-c:v", "mjpeg", "-i", "-",
    "-frames:v", String(n), "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", "-r", String(FPS), out], { stdio: ["pipe", "inherit", "inherit"] });
  const t0 = Date.now();
  for (let i = 0; i < n; i++) {
    await page.evaluate(t => window.renderAt(t), i / FPS);
    const buf = await page.screenshot({ type: "jpeg", quality: 92 });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once("drain", r));
    if (i % 250 === 0) console.log(`${s.def.id} ${i}/${n} ${((Date.now() - t0) / 1000).toFixed(0)}s`);
  }
  ff.stdin.end();
  await new Promise(r => ff.on("close", r));
  await page.close();
  console.log("done", s.def.id, n, "frames");
}

(async () => {
  const [mode, ...args] = process.argv.slice(2);
  const { list, total } = plan();
  const A = assets();
  const browser = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium-1194/chrome-linux/chrome", args: ["--allow-file-access-from-files"] });
  if (mode === "plan") {
    for (const s of list) console.log(s.def.id, s.offset.toFixed(1), s.dur.toFixed(1));
    console.log("TOTAL", (total / 60).toFixed(2), "min");
  } else if (mode === "preview") {
    fs.mkdirSync(path.join(ROOT, OUT + "/preview"), { recursive: true });
    const s = list.find(x => x.def.id === args[0]);
    const page = await openPage(browser);
    const dur = await load(page, s, total, A);
    let ts = (args[1] || "").split(",").filter(Boolean).map(Number);
    if (args[1] === "beats") ts = (await page.evaluate(() => window.__beats)).map(([a, b]) => Math.min(b - 0.6, a + Math.max(2.5, (b - a) * 0.7)));
    for (const t of ts.length ? ts : [1, dur / 2, dur - 1]) {
      await page.evaluate(t => window.renderAt(t), t);
      await page.screenshot({ path: path.join(ROOT, OUT + "/preview", `${s.def.id}_${t.toFixed(1)}.jpg`), type: "jpeg", quality: 80 });
    }
    console.log("dur", dur.toFixed(2));
  } else if (mode === "scenes") {
    fs.mkdirSync(path.join(ROOT, OUT + "/scenes"), { recursive: true });
    const todo = list.filter(s => !args.length || args.includes(s.def.id));
    const workers = Number(process.env.WORKERS || 3);
    let next = 0;
    await Promise.all(Array.from({ length: workers }, async () => {
      while (next < todo.length) { const s = todo[next++]; await renderScene(browser, s, total, A); }
    }));
  }
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
