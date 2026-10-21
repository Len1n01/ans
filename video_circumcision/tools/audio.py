import json, subprocess, sys, os
os.chdir(sys.argv[1])
SC, AU, OUT = (sys.argv[2:5] + [None]*3)[:3] if len(sys.argv) > 2 else ("scenes.js", "audio", "out")
HEAD, TAIL, CRED = 0.5, 0.6, 14.0
ids = [l.split('id: "')[1].split('"')[0] for l in open(SC, encoding="utf-8") if l.strip().startswith('id: "s')]
parts, total, srt, n = [], 0.0, [], 1
def ts(x):
    h, r = divmod(x, 3600); m, s = divmod(r, 60)
    return f"{int(h):02d}:{int(m):02d}:{s:06.3f}".replace(".", ",")
os.makedirs(OUT + "/audio", exist_ok=True)
for i in ids:
    meta = json.load(open(f"{AU}/{i}.json", encoding="utf-8"))
    dur = HEAD + meta["duration"] + TAIL
    out = f"{OUT}/audio/{i}.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{AU}/{i}.wav", "-af", f"adelay={int(HEAD*1000)},apad", "-t", f"{dur:.3f}", "-ar", "48000", "-ac", "1", out], check=True)
    for s in meta["sentences"]:
        srt.append(f"{n}\n{ts(total + HEAD + s['start'])} --> {ts(total + HEAD + s['end'])}\n{s['text']}\n"); n += 1
    parts.append(out); total += dur
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=mono", "-t", str(CRED), OUT + "/audio/zz_credits.wav"], check=True)
parts.append(OUT + "/audio/zz_credits.wav"); total += CRED
open(OUT + "/audio/list.txt", "w").write("".join(f"file '{os.path.abspath(p)}'\n" for p in parts))
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", OUT + "/audio/list.txt", "-c", "pcm_s16le", OUT + "/voice.wav"], check=True)
# quiet ambient pad: A minor drone with slow swell
pad = ("aevalsrc='0.30*sin(2*PI*110*t)*(0.6+0.4*sin(2*PI*0.05*t))+0.22*sin(2*PI*164.81*t)*(0.6+0.4*sin(2*PI*0.037*t+1))"
       "+0.18*sin(2*PI*220*t)*(0.5+0.5*sin(2*PI*0.029*t+2))+0.10*sin(2*PI*261.63*t)*(0.5+0.5*sin(2*PI*0.021*t+3))':s=48000:d=" + f"{total:.2f}")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", pad, "-af",
    f"lowpass=f=700,volume=0.07,afade=t=in:d=4,afade=t=out:st={total-6:.2f}:d=6", OUT + "/pad.wav"], check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", OUT + "/voice.wav", "-i", OUT + "/pad.wav", "-filter_complex",
    "[0:a]loudnorm=I=-16:TP=-1.5:LRA=11,apad[v];[v][1:a]amix=inputs=2:duration=first:normalize=0[m]", "-map", "[m]", "-t", f"{total:.3f}", "-ar", "48000", "-ac", "2", OUT + "/mix.wav"], check=True)
open(OUT + "/subtitles.srt", "w", encoding="utf-8").write("\n".join(srt))
print("total", round(total, 2), "s")
