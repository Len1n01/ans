import json, sys, os, time, urllib.request
spec = json.load(open(sys.argv[1])); out = sys.argv[2]; os.makedirs(out, exist_ok=True)
cp = f"{out}/credits.json"; cr = json.load(open(cp)) if os.path.exists(cp) else {}
for k, (url, credit) in spec.items():
    fn = f"{out}/{k}.jpg"
    if os.path.exists(fn) and os.path.getsize(fn) > 5000: cr[k] = {"file": f"{k}.jpg", "credit": credit}; continue
    for i in range(4):
        try:
            data = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "CircVideoBot/1.0"}), timeout=120).read()
            open(fn, "wb").write(data); cr[k] = {"file": f"{k}.jpg", "credit": credit}; print("ok", k, len(data)); break
        except Exception as e:
            print("retry", k, e); time.sleep(5)
json.dump(cr, open(cp, "w"), ensure_ascii=False, indent=1)
