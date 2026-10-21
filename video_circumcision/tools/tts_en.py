import sys, ssl, json, asyncio, os, re, subprocess
import edge_tts.communicate as c
c._SSL_CTX = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")
import edge_tts
VOICE, RATE, GAP = "en-US-AndrewNeural", "-3%", 0.25
def chunks(text, limit=260):
    out, cur = [], ""
    for s in re.split(r"(?<=[.!?])\s+", text):
        if cur and len(cur) + len(s) > limit: out.append(cur); cur = s
        else: cur = (cur + " " + s).strip()
    return out + ([cur] if cur else [])
async def synth(text):
    for attempt in range(30):
        try:
            data, subs = bytearray(), []
            async for ch in edge_tts.Communicate(text, VOICE, rate=RATE, boundary="SentenceBoundary").stream():
                if ch["type"] == "audio": data += ch["data"]
                elif ch["type"] == "SentenceBoundary":
                    subs.append([ch["offset"] / 1e7, (ch["offset"] + ch["duration"]) / 1e7, ch["text"]])
            if len(data) > 1000: return bytes(data), subs
        except Exception:
            pass
        await asyncio.sleep(min(2 + attempt, 10))
    raise SystemExit("failed: " + text[:50])
def run(*a): subprocess.run(["ffmpeg", "-v", "error", "-y", *a], check=True)
def dur(p): return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",p]))
async def main(src, outdir):
    tmp = f"{outdir}/parts"; os.makedirs(tmp, exist_ok=True)
    sil = f"{tmp}/gap.wav"
    run("-f", "lavfi", "-i", f"anullsrc=r=48000:cl=mono", "-t", str(GAP), sil)
    for s in json.load(open(src, encoding="utf-8")):
        out = f"{outdir}/{s['id']}.wav"; meta = f"{outdir}/{s['id']}.json"
        if os.path.exists(meta): continue
        off, sents, lst = 0.0, [], []
        for i, ch in enumerate(chunks(s["text"])):
            data, subs = await synth(ch)
            mp3 = f"{tmp}/{s['id']}_{i:02d}.mp3"; wav = mp3[:-4] + ".wav"
            open(mp3, "wb").write(data); run("-i", mp3, "-ar", "48000", "-ac", "1", wav)
            for a, b, t in subs: sents.append({"start": round(off + a, 3), "end": round(off + b, 3), "text": t})
            off += dur(wav) + GAP; lst += [wav, sil]
        open(f"{tmp}/list.txt", "w").write("".join(f"file '{os.path.abspath(p)}'\n" for p in lst))
        run("-f", "concat", "-safe", "0", "-i", f"{tmp}/list.txt", "-c", "pcm_s16le", out)
        json.dump({"id": s["id"], "duration": dur(out), "sentences": sents}, open(meta, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("ok", s["id"], round(dur(out), 1), flush=True)
asyncio.run(main(*sys.argv[1:]))
