# build_trip_maps.py
import csv, json, re
from collections import defaultdict, Counter

TRIPS = "trips.txt"
OUT   = "static/tripMaps.js"

def norm(s: str) -> str:
    s = (s or "").strip().lower()
    s = re.sub(r"[–—]", "-", s)     # normalize long dash to hyphen
    s = re.sub(r"\s+", " ", s)      # collapse spaces
    return s

tripIdMap = {}
counts_by_route_head = defaultdict(Counter)   # (route_id, norm_headsign) -> Counter({0:x,1:y})
repr_by_route_head   = {}                     # (route_id, norm_headsign) -> original headsign seen
routeToDirections    = defaultdict(lambda: defaultdict(set))  # route -> dir -> set(headsigns)

with open(TRIPS, newline="", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for row in reader:
        trip_id      = (row.get("trip_id") or "").strip()
        route_id     = (row.get("route_id") or "").strip()
        headsign_raw = (row.get("trip_headsign") or "").strip()
        dir_raw      = (row.get("direction_id") or "").strip()

        if not trip_id or not route_id:
            continue

        direction_id = int(dir_raw) if dir_raw in ("0","1") else None
        tripIdMap[trip_id] = {
            "route_id": route_id,
            "headsign": headsign_raw,
            "direction_id": direction_id
        }

        if headsign_raw and direction_id in (0,1):
            n = norm(headsign_raw)
            counts_by_route_head[(route_id, n)][direction_id] += 1
            # store a representative text for nicer labels
            repr_by_route_head.setdefault((route_id, n), headsign_raw)
            # collect for dropdowns (allow multiple headsigns per dir)
            routeToDirections[route_id][direction_id].add(headsign_raw)

# collapse to majority dir per (route, headsign)
headsignDirMajority = {}
for (route_id, nhead), ctr in counts_by_route_head.items():
    dir_majority = ctr.most_common(1)[0][0]
    headsignDirMajority.setdefault(route_id, {})[nhead] = {
        "dir": dir_majority,
        "text": repr_by_route_head[(route_id, nhead)]
    }

# convert sets to sorted lists for stable output
routeToDirections_serializable = {
    r: { str(d): sorted(list(hs)) for d, hs in dmap.items() }
    for r, dmap in routeToDirections.items()
}

with open(OUT, "w", encoding="utf-8") as js:
    js.write("const tripIdMap = ")
    js.write(json.dumps(tripIdMap, ensure_ascii=False, indent=2))
    js.write(";\n\nconst headsignDirMajority = ")
    js.write(json.dumps(headsignDirMajority, ensure_ascii=False, indent=2))
    js.write(";\n\nconst routeToDirections = ")
    js.write(json.dumps(routeToDirections_serializable, ensure_ascii=False, indent=2))
    js.write(";\n")
print(f"Wrote {OUT}")
