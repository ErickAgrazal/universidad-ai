import openpyxl, json, sys, unicodedata, re

def norm(s):
    if s is None: return ""
    s = str(s).strip()
    s = unicodedata.normalize("NFKD", s).encode("ascii","ignore").decode().lower()
    s = re.sub(r"\s+"," ", s)
    return s

quiz = json.load(open("quiz.json"))
mc = quiz["mc"]
# map normalized question text -> {correct set, multi}
qmap = {}
for q in mc:
    opts = q["options"]
    correct = set(norm(opts[i]) for i in q["correct"])
    qmap[norm(q["q"])] = {"correct": correct, "multi": bool(q.get("multi")), "n": q["n"]}

dev_qs = [norm(q["q"]) for q in quiz["dev"]]

def load(path):
    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb.active
    rows = list(ws.iter_rows(values_only=True))
    hdr = rows[0]
    # build column index: header -> col
    H = {}
    for i,h in enumerate(hdr):
        if h is not None: H[str(h)] = i
    # answer col for each header that is NOT Points-/Feedback-
    def points_col(qtext):
        key = "Points - " + qtext
        return H.get(key)
    def ans_col(qtext):
        return H.get(qtext)
    students = []
    for r in rows[1:]:
        if r[4] is None: continue
        name = str(r[4]).strip()
        mc_total = 0; detail = {}
        for i,h in enumerate(hdr):
            hs = str(h) if h else ""
            if hs.startswith("Points - ") or hs.startswith("Feedback - "): continue
            nh = norm(hs)
            if nh in qmap:
                meta = qmap[nh]
                ans = r[i]
                if meta["multi"]:
                    sel = set(norm(x) for x in str(ans or "").split(";") if norm(x))
                    inter = sel & meta["correct"]
                    if sel == meta["correct"]: pts = 3
                    elif len(inter) >= 1: pts = 1
                    else: pts = 0
                    detail["Q%d(multi)"%meta["n"]] = (pts, sorted(sel))
                else:
                    pc = H.get("Points - "+hs)
                    fpts = r[pc] if pc is not None else None
                    pts = int(fpts) if isinstance(fpts,(int,float)) else 0
                    detail["Q%d"%meta["n"]] = pts
                mc_total += pts
        # dev answers
        devs = {}
        for i,h in enumerate(hdr):
            hs = str(h) if h else ""
            if hs.startswith("Points - ") or hs.startswith("Feedback - "): continue
            nh = norm(hs)
            if nh in dev_qs:
                idx = dev_qs.index(nh)
                devs["dev%d"%(21+idx)] = str(r[i] or "").strip()
        students.append({"name":name, "mc":mc_total, "forms_total": r[5], "dev21": devs.get("dev21",""), "dev22": devs.get("dev22",""), "detail":detail})
    return students

st = load(sys.argv[1])
print("Students:", len(st))
for s in st:
    print("\n=== %s | MC=%d/60 | Forms_total=%s ==="%(s["name"], s["mc"], s["forms_total"]))
    print("  multi:", {k:v for k,v in s["detail"].items() if "multi" in k})
