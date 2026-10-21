// Deterministic scene engine: loadScene(def, meta, info) then renderAt(t) per frame.
(() => {
  const HEAD = 0.5, TAIL = 0.6, XF = 0.5;
  const stage = document.getElementById("stage");
  const subsEl = document.querySelector("#subs span");
  const progEl = document.getElementById("progress");
  const chapEl = document.getElementById("chapter");
  let S = null;

  const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
  const ease = x => x < 0.5 ? 2 * x * x : 1 - Math.pow(-2 * x + 2, 2) / 2;
  const esc = s => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  const h = (html) => { const d = document.createElement("div"); d.innerHTML = html.trim(); return d.firstElementChild; };

  // ---------- timing ----------
  function cueTime(cue, meta, fallback) {
    if (cue == null) return fallback;
    if (typeof cue === "number") return cue;
    const norm = s => s.toLowerCase().replace(/ё/g, "е").replace(/[^a-zа-я0-9 ]/g, " ").replace(/\s+/g, " ").trim();
    const c = norm(cue);
    for (const s of meta.sentences) if (norm(s.text).includes(c)) return HEAD + s.start - 0.1;
    throw new Error("cue not found: " + cue);
  }

  // ---------- syntax highlight ----------
  const KW = new Set("const let var function return if else for of in new true false null undefined while class this".split(" "));
  function tokenize(code) {
    const re = /(\/\/[^\n]*)|("(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*'|`(?:[^`\\]|\\.)*`)|(\b\d+(?:\.\d+)?\b)|([A-Za-z_$][\w$]*)|(=>|===|!==|&&|\|\||[{}()[\];,.:?=!<>+\-*\/|])|(\s+)|(.)/gsu;
    const toks = []; let m;
    while ((m = re.exec(code))) {
      const [t] = m; let cls = "";
      if (m[1]) cls = "c"; else if (m[2]) cls = "s"; else if (m[3]) cls = "n";
      else if (m[4]) {
        if (KW.has(t)) cls = (t === "true" || t === "false") ? "b" : "k";
        else if (/^\s*\(/.test(code.slice(re.lastIndex))) cls = "f";
      } else if (m[5]) cls = "p";
      toks.push([t, cls]);
    }
    return toks;
  }
  function highlight(toks, n) {
    let out = "", used = 0;
    for (const [t, cls] of toks) {
      if (used >= n) break;
      const piece = [...t].slice(0, n - used).join("");
      used += [...piece].length;
      out += cls ? `<span class="tok-${cls}">${esc(piece)}</span>` : esc(piece);
    }
    return out;
  }

  // ---------- fake console ----------
  function inspect(v, top = true) {
    if (typeof v === "string") return top ? v : `'${v}'`;
    if (typeof v === "boolean" || typeof v === "number" || v == null) return String(v);
    if (Array.isArray(v)) return "[ " + v.map(x => inspect(x, false)).join(", ") + " ]";
    return "{ " + Object.entries(v).map(([k, x]) => `${/^[\wа-яё$]+$/i.test(k) ? k : `'${k}'`}: ${inspect(x, false)}`).join(", ") + " }";
  }
  function runCode(code) {
    const groups = [];
    const fake = { log: (...a) => groups.push(a.map(x => inspect(x)).join(" ")) };
    new Function("console", code)(fake);
    return groups;
  }
  function colorOut(line) {
    return esc(line)
      .replace(/\btrue\b|✔[^|]*/g, m => `<span class="out-true">${m}</span>`)
      .replace(/\bfalse\b|✘[^|]*/g, m => `<span class="out-false">${m}</span>`)
      .replace(/'([^']*)'/g, `<span class="tok-s">'$1'</span>`);
  }

  // ---------- builders ----------
  function imgBox(src, cover) {
    return `<div class="bgfill" style="background-image:url('${src}')"></div>
      <div class="kb ${cover ? "cover" : ""}"><img src="${src}"></div><div class="vignette"></div>`;
  }
  const at = (b, key, meta, dflt) => cueTime(b[key], meta, dflt);

  function build(b, meta, info) {
    const A = info.assets;
    const credit = k => A[k] ? `<div class="credit">${esc(A[k].credit)}</div>` : "";
    let el;
    switch (b.type) {
      case "title":
        el = h(`<div class="beat">${b.img ? imgBox(A[b.img].src, true) + '<div class="dim"></div>' : ""}
          <div class="title-wrap">${b.num ? `<div class="chapter-num">${esc(b.num)}</div>` : ""}
          ${b.he ? `<div class="he">${esc(b.he)}</div>` : ""}<div class="t">${b.title}</div>
          ${b.sub ? `<div class="s">${b.sub}</div>` : ""}<div class="rule"></div></div>${b.img ? credit(b.img) : ""}</div>`);
        break;
      case "image":
        el = h(`<div class="beat">${imgBox(A[b.img].src, b.cover)}<div class="shade-bottom"></div>
          ${b.main || b.kicker ? `<div class="caption">${b.kicker ? `<div class="kicker">${esc(b.kicker)}</div>` : ""}
          ${b.main ? `<div class="main">${b.main}</div>` : ""}${b.sub ? `<div class="sub">${b.sub}</div>` : ""}</div>` : ""}
          ${credit(b.img)}</div>`);
        break;
      case "video":
        el = h(`<div class="beat"><div class="kb cover"><img></div><div class="shade-bottom"></div>
          ${b.main ? `<div class="caption">${b.kicker ? `<div class="kicker">${esc(b.kicker)}</div>` : ""}<div class="main">${b.main}</div>
          ${b.sub ? `<div class="sub">${b.sub}</div>` : ""}</div>` : ""}${credit(b.clip)}</div>`);
        break;
      case "quote":
        el = h(`<div class="beat">${b.img ? imgBox(A[b.img].src, true) + '<div class="dim strong"></div>' : ""}<div class="quote">
          <div class="he">${esc(b.he)}</div><div class="ru">${b.ru}</div><div class="src">${esc(b.src)}</div></div>
          ${b.img ? credit(b.img) : ""}</div>`);
        break;
      case "split":
        el = h(`<div class="beat"><div class="bgfill" style="background-image:url('${A[b.img].src}')"></div>
          <div class="split"><div class="pic"><img src="${A[b.img].src}"></div><div>
          ${b.kicker ? `<div class="kicker">${esc(b.kicker)}</div>` : ""}<h2>${b.title}</h2>
          <ul class="items">${(b.items || []).map(i => `<li>${i.html}</li>`).join("")}</ul></div></div>${credit(b.img)}</div>`);
        break;
      case "cards":
        el = h(`<div class="beat">${b.img ? `<div class="bgfill" style="background-image:url('${A[b.img].src}')"></div>` : ""}
          <div class="cards">${b.title ? `<h2>${b.title}</h2>` : ""}<div class="row">${b.cards.map(c =>
          `<div class="card ${c.cls || ""}"><div class="k">${esc(c.k || "")}</div><div class="h">${c.h}</div>
           ${c.he ? `<div class="he">${esc(c.he)}</div>` : ""}${c.p ? `<p>${c.p}</p>` : ""}
           ${c.verdict ? `<div class="verdict">${c.verdict}</div>` : ""}</div>`).join("")}</div></div></div>`);
        break;
      case "drop":
        el = h(`<div class="beat"><div class="drop-scene">
          <div class="drop-col bad"><svg width="260" height="260" viewBox="0 0 260 260"><circle cx="130" cy="130" r="110" fill="none" stroke="#ff6b6b" stroke-width="8"/>
            <path d="M70 190 L190 70" stroke="#ff6b6b" stroke-width="10" stroke-linecap="round"/><text x="130" y="150" text-anchor="middle" font-size="64" fill="#f3ead7" font-family="JetBrains Mono">✂</text></svg>
            <div class="h">Повторное обрезание</div><p>Крайней плоти уже нет — повторять нечего</p><div class="verdict" style="color:var(--red)">✘ не делают</div></div>
          <div class="drop-col good"><svg width="260" height="260" viewBox="0 0 260 260"><circle cx="130" cy="130" r="110" fill="none" stroke="#6fdc8c" stroke-width="8"/>
            <path class="drop" d="M130 60 C130 60 85 120 85 150 a45 45 0 0 0 90 0 C175 120 130 60 130 60 Z" fill="#c0392b"/></svg>
            <div class="h">Хатафат дам брит</div><p>Одна капля крови — «запечатать» завет</p><div class="verdict" style="color:var(--green)">✔ так поступают</div></div>
          </div></div>`);
        break;
      case "code": {
        const outs = runCode(b.code);
        b._outs = outs; b._toks = tokenize(b.code); b._len = [...b.code].length;
        el = h(`<div class="beat"><div class="code-wrap ${b.stack ? "stack" : ""}" style="${b.cols ? `grid-template-columns:${b.cols};` : ""}">
          <div class="win"><div class="bar"><span class="dot" style="background:#ff5f57"></span><span class="dot" style="background:#febc2e"></span>
            <span class="dot" style="background:#28c840"></span><span class="fname">${esc(b.file)}</span></div><pre class="src" style="${b.font ? `font-size:${b.font}px` : ""}"></pre></div>
          <div class="win console"><div class="bar"><span class="fname">Terminal — node ${esc(b.file)}</span></div><pre class="out" style="${b.consoleFont ? `font-size:${b.consoleFont}px` : ""}"></pre></div>
          </div></div>`);
        break;
      }
      case "credits":
        el = h(`<div class="beat"><div class="credits"><h2>${b.title}</h2><div class="cols">${b.lines.map(l => `<div>${esc(l)}</div>`).join("")}</div>
          ${b.note ? `<p class="note">${b.note}</p>` : ""}</div></div>`);
        break;
      default: throw new Error("unknown beat " + b.type);
    }
    return el;
  }

  // ---------- public ----------
  window.loadScene = async (def, meta, info) => {
    stage.innerHTML = "";
    const dur = HEAD + meta.duration + TAIL + (def.extra || 0);
    const beats = def.beats.map(b => ({ ...b }));
    beats.forEach((b, i) => { b.start = i === 0 ? 0 : at(b, "cue", meta, b.at); });
    beats.forEach((b, i) => { b.end = i + 1 < beats.length ? beats[i + 1].start : dur; });
    for (const b of beats) {
      b.el = build(b, meta, info); stage.appendChild(b.el);
      if (b.items) b._items = b.items.map((it, k) => ({ el: b.el.querySelectorAll(".items li")[k], t: cueTime(it.cue, meta, b.start + 0.6 + k * 0.5) }));
      if (b.cards) b._cards = b.cards.map((c, k) => ({ el: b.el.querySelectorAll(".card")[k], t: cueTime(c.cue, meta, b.start + 0.5 + k * 0.6) }));
      if (b.type === "code") {
        b._t0 = b.start + 0.7;
        b._t1 = b.typeUntil ? cueTime(b.typeUntil, meta) : b._t0 + b._len / (b.cps || 38);
        const n = b._outs.length;
        const ot = b.outCues || [];
        b._outT = b._outs.map((_, k) => ot[k] != null ? Math.max(b._t1 + 0.4 + k * 0.4, cueTime(ot[k], meta)) : b._t1 + 0.6 + k * Math.max(0.5, (b.end - b._t1 - 2.5) / Math.max(1, n)));
      }
      if (b.type === "video") { b._img = b.el.querySelector("img"); b._clip = info.assets[b.clip]; }
    }
    // subtitles: split long sentences into chunks proportional to length
    const subs = [];
    for (const s of meta.sentences) {
      const words = s.text.split(/\s+/); const chunks = []; let cur = "";
      for (const w of words) { if (cur && (cur + " " + w).length > 72) { chunks.push(cur); cur = w; } else cur = (cur + " " + w).trim(); }
      if (cur) chunks.push(cur);
      if (chunks.length > 1 && chunks[chunks.length - 1].length < 28) { const t = chunks.pop(); chunks[chunks.length - 1] += " " + t; }
      const total = chunks.reduce((a, c) => a + c.length, 0); let t = s.start;
      for (const c of chunks) { const d = (s.end - s.start) * c.length / total; subs.push({ a: HEAD + t, b: HEAD + t + d, text: c }); t += d; }
    }
    S = { def, meta, info, beats, dur, subs };
    window.__beats = beats.map(b => [b.start, b.end]);
    chapEl.textContent = def.chapter || "";
    await Promise.all([...stage.querySelectorAll("img")].filter(i => i.src).map(i => i.decode().catch(() => {})));
    for (const b of beats) if (b.type === "image" && b.cover !== false) {
      const im = b.el.querySelector(".kb img");
      if (im.naturalWidth / im.naturalHeight >= 1.25) b.el.querySelector(".kb").classList.add("cover");
    }
    await document.fonts.ready;
    return dur;
  };

  window.renderAt = async (t) => {
    const { beats, dur, subs, info } = S;
    const sceneFade = clamp(t / 0.45) * clamp((dur - t) / 0.45);
    stage.style.opacity = sceneFade; chapEl.style.opacity = sceneFade * (S.def.chapter ? 1 : 0);
    const waits = [];
    for (const b of beats) {
      const vis = (t >= b.start - XF && t < b.end + XF);
      let o = 0;
      if (vis) o = clamp((t - b.start) / XF + (b.start === 0 ? 1 : 0)) * (b.end >= dur ? 1 : clamp((b.end + XF - t) / XF));
      b.el.style.opacity = o; b.el.style.display = o > 0 ? "" : "none";
      if (o <= 0) continue;
      const lt = t - b.start, span = Math.max(1, b.end - b.start), p = clamp(lt / span);
      const kb = b.el.querySelector(".kb img");
      if (kb && b.type !== "video") {
        const z0 = b.z0 ?? 1.0, z1 = b.z1 ?? 1.08;
        const z = z0 + (z1 - z0) * p;
        kb.style.transform = `scale(${z}) translate(${(b.dx || 0) * p}px, ${(b.dy || 0) * p}px)`;
      }
      if (b.type === "title") {
        const r = b.el.querySelector(".rule"); r.style.width = 360 * ease(clamp((lt - 0.4) / 1.2)) + "px";
        const tw = b.el.querySelector(".title-wrap"); tw.style.transform = `translateY(${20 * (1 - ease(clamp(lt / 1.2)))}px)`;
      }
      if (b.type === "quote") {
        const ru = b.el.querySelector(".ru"); ru.style.opacity = clamp((lt - 1.0) / 0.8);
        b.el.querySelector(".src").style.opacity = clamp((lt - 1.6) / 0.8);
      }
      if (b._items) for (const it of b._items) { const q = ease(clamp((t - it.t) / 0.5)); it.el.style.opacity = q; it.el.style.transform = `translateX(${(1 - q) * 30}px)`; }
      if (b._cards) for (const c of b._cards) { const q = ease(clamp((t - c.t) / 0.6)); c.el.style.opacity = q; c.el.style.transform = `translateY(${(1 - q) * 30}px)`; }
      if (b.type === "drop") {
        const cols = b.el.querySelectorAll(".drop-col");
        cols[0].style.opacity = ease(clamp(lt / 0.6));
        cols[1].style.opacity = ease(clamp((lt - (b.second ?? 3)) / 0.6));
        const d = b.el.querySelector(".drop"); const pulse = 1 + 0.06 * Math.sin(lt * 3);
        d.style.transformOrigin = "130px 150px"; d.style.transform = `scale(${pulse})`;
      }
      if (b.type === "code") {
        const n = Math.floor(b._len * clamp((t - b._t0) / Math.max(0.1, b._t1 - b._t0)));
        const typing = t < b._t1 + 0.3;
        const caret = (typing || Math.floor(t * 2) % 2 === 0) ? `<span class="caret"></span>` : "";
        b.el.querySelector(".src").innerHTML = highlight(b._toks, n) + caret;
        let lines = [`<span class="out-line prompt">$ node ${esc(b.file)}</span>`];
        b._outs.forEach((g, k) => { if (t >= b._outT[k]) for (const ln of g.split("\n")) lines.push(`<span class="out-line">${colorOut(ln)}</span>`); });
        const max = b.maxLines || 16; if (lines.length > max) lines = lines.slice(lines.length - max);
        b.el.querySelector(".out").innerHTML = lines.join("");
      }
      if (b.type === "video") {
        const c = b._clip; const idx = Math.min(c.frames - 1, Math.floor(Math.max(0, lt + XF) * c.fps * (b.speed || 1)) % c.frames);
        const src = `${c.dir}/f${String(idx + 1).padStart(5, "0")}.jpg`;
        if (!b._img.src.endsWith(src)) { b._img.src = src; waits.push(b._img.decode().catch(() => {})); }
        b._img.style.transform = `scale(${1.02 + 0.04 * p})`;
      }
    }
    const s = subs.find(x => t >= x.a && t < x.b);
    subsEl.textContent = s ? s.text : "";
    progEl.style.width = (1920 * (info.offset + t) / info.total) + "px";
    await Promise.all(waits);
  };
})();
