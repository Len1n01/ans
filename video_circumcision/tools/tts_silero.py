import sys, json, os, re, wave
import numpy as np, torch
torch.set_num_threads(4)
SR, GAP_S, GAP_P = 48000, 0.32, 0.12
SPEAKER = os.environ.get("SPK", "aidar")
# speech-only fixes: transliteration stress marks and words the model can't read
FIX = [
 (r"JavaScript", "джаваскр+ипт"), (r"\bintent\b", "«намерение»"), (r"назовём её brit", "назовём её брит"),
 (r"брит мила", "брит мил+а"), (r"брит милы", "брит мил+ы"), (r"брит милу", "брит мил+у"),
 (r"\bМила\b", "мил+а"), (r"\bмила\b", "мил+а"), (r"\bприя\b", "при+я"), (r"\bприи\b", "при+и"), (r"\bприю\b", "при+ю"), (r"\bприи\b", "при+и"),
 (r"мецица", "мециц+а"), (r"моэль", "мо+эль"), (r"моэля", "мо+эля"), (r"моэли", "мо+эли"),
 (r"Рамбам", "Рамб+ам"), (r"Шулхан Арух", "Шулх+ан Ар+ух"), (r"\bРема\b", "Р+ема"), (r"\bРеме\b", "Р+еме"), (r"\bРемы\b", "Р+емы"),
 (r"хатафат дам брит", "хат+афат дам брит"), (r"лехатхила", "лехатхил+а"), (r"бедиэвад", "бедиэв+ад"),
 (r"Ципор", "Цип+ор"), (r"Авода Зара", "Авод+а З+ара"), (r"Йоханан", "Йох+анан"), (r"Ицхак", "Иц+хак"),
 (r"Гризим", "Гриз+им"), (r"кавана", "кав+ана"), (r"Тосафот", "Тос+афот"), (r"Шамай", "Шам+ай"), (r"Гилель", "Гил+ель"),
 (r"Йоре Деа", "Й+оре Де+а"), (r"Иссерлес", "+Иссерлес"), (r"Мапа", "М+апа"), (r"Мишне Тора", "Мишн+е Тор+а"),
 (r"Йом Кипур", "Йом Кип+ур"), (r"хималь имоль", "хим+оль им+оль"), (r"Йегуда", "Йег+уда"), (r"Йоси", "Й+оси"),
 (r"кутим", "кут+им"), (r"барайту", "бар+айту"), (r"галах", "гал+ах"), (r"гиюр", "ги+юр"), (r"Каро", "К+аро"), (r"Цфат", "Цфат"),
 (r"Маймона", "Маймон+а"), (r"Дару бар Папа", "Д+ару бар П+апа"), (r"Ципоры", "Цип+оры"), (r"\bТор", "Т+ор"), (r"Мишны", "Мишн+ы"),
 (r"бракха", "брах+а"), (r"кошерн", "кош+ерн"), (r"\bгер", "гер"), (r"\bгере\b", "г+ере"), (r"Тур\b", "Тур"),
]
def speech(s):
    for a, b in FIX: s = re.sub(a, b, s)
    return s.replace("++", "+")
m = torch.package.PackageImporter(sys.argv[3]).load_pickle("tts_models", "model")
def tts(text):
    a = m.apply_tts(text=text, speaker=SPEAKER, sample_rate=SR, put_accent=True, put_yo=True).numpy()
    return a
def sentences(text): return [s for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s]
def subparts(s):  # silero limit ~ 800 chars; also split long sentences on ':' / ';'
    if len(s) < 700: return [s]
    return re.split(r"(?<=[:;])\s+", s)
def main(src, outdir):
    os.makedirs(outdir, exist_ok=True)
    only = set(sys.argv[4:])
    for sc in json.load(open(src, encoding="utf-8")):
        if only and sc["id"] not in only: continue
        buf, sents, t = [], [], 0.0
        for s in sentences(sc["text"]):
            pieces = [tts(speech(p)) for p in subparts(s)]
            a = np.concatenate(pieces)
            # trim leading/trailing near-silence a bit
            nz = np.where(np.abs(a) > 0.01)[0]
            if len(nz): a = a[max(0, nz[0] - 1200): nz[-1] + 2400]
            gap = GAP_S + (0.15 if s.endswith("?") else 0)
            sents.append({"start": round(t, 3), "end": round(t + len(a) / SR, 3), "text": s})
            buf += [a, np.zeros(int(gap * SR), dtype=np.float32)]; t += len(a) / SR + gap
        audio = np.concatenate(buf)
        audio = audio / max(1e-6, np.abs(audio).max()) * 0.89
        w = wave.open(f"{outdir}/{sc['id']}.wav", "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((audio * 32767).astype(np.int16).tobytes()); w.close()
        json.dump({"id": sc["id"], "duration": round(len(audio) / SR, 3), "sentences": sents},
                  open(f"{outdir}/{sc['id']}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("ok", sc["id"], round(len(audio) / SR, 1), flush=True)
main(*sys.argv[1:3])
