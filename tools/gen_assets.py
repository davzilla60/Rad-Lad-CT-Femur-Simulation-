"""Build every image asset for the CT femur simulator from HFValid Pat001.

Source: Aldieri A, La Mattina AA, Szyszko JA, Baruffaldi F, Viceconti M. HFValid collection: Hip-Fracture
validation collection [Dataset]. University of Bologna, AMS Acta, 2023. doi:10.6092/unibo/amsacta/7277 (CC BY 4.0).
Pat001 = calibrated CT of a RIGHT femur, hip -> knee, 0.703125 mm pixels, 2 mm slices, field cropped by the
dataset to the right side (x = -183.2 .. -3.2 mm LPS, i.e. lateral skin -> near the midline). Read through the
DICOM conversion in "Pat001 - DICOM" (tools/load_vol.py -> work/vol.npy, z index 0 = inferior; work/seg.npy = femur mask).

Outputs (../assets):
  scout_ap.jpg   simulated AP topogram (line integrals through the volume), PX mm/pixel, superior at the top,
                 patient's right on the viewer's left; PAD_AP mm of air added laterally, the medial edge of the
                 image is where the dataset's field ends.
  scout_lat.jpg  simulated lateral topogram, anterior on the left, PAD_LAT mm of air either side.
  ax_NNN.jpg     every native 2 mm axial slice, superior -> inferior, 256 x 331 native grid, HU encoded with HU_LUT.
  cor_NN.jpg     coronal slabs every STEP mm (front -> back), z resampled to PX.
  sag_NN.jpg     sagittal slabs every STEP mm (lateral -> medial), anterior on the left, z resampled to PX.
  calib.json/js  geometry, per-slice "needed" tissue extent for DFOV judgements, landmarks.

Run:  python -I tools/gen_assets.py   (needs numpy, opencv-python; run tools/load_vol.py first)
"""
import os, json
import numpy as np, cv2

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, "..", "work")
OUT = os.path.join(HERE, "..", "assets")
SP, DZ = 0.703125, 2.0
PX = 0.7                          # scout / MPR pixel (mm)
STEP = 3.0                        # reformat interval (mm)
PAD_AP, PAD_AP_R = 50.0, 6.0      # air added lateral / medial of the field on the AP scout (mm)
PAD_LAT = 34.0
HU_LUT = [(-1000, 0), (-200, 40), (300, 140), (2400, 255)]
MU = 0.0192 / 1000
MED_CAP = 176.0                   # medial skin of the right thigh (mm from the lateral field edge) - beyond it the
                                  # thighs touch / the pelvis continues past the dataset's crop
AP_CAP = 175.0                    # deepest AP extent a unilateral femur DFOV is judged on (hip level: buttock/abdomen)


def hu_to_byte(h):
    xs = [p[0] for p in HU_LUT]; ys = [p[1] for p in HU_LUT]
    return np.clip(np.rint(np.interp(h, xs, ys)), 0, 255).astype(np.uint8)


def tint(g):
    g = g.astype(np.float32) / 255
    return (np.stack([g * .95, g * .97, g * .78], -1) * 255).astype(np.uint8)


def body_mask(sl):
    m = (sl > -400).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7)))
    n, lab, st, _ = cv2.connectedComponentsWithStats(m, 8)
    keep = np.zeros_like(m)
    for i in range(1, n):                       # body / limbs; drops the table, its pad and the calibration rods
        if st[i, cv2.CC_STAT_AREA] >= 1500:
            keep[lab == i] = 1
    return keep, lab, st


def main():
    os.makedirs(OUT, exist_ok=True)
    v = np.load(os.path.join(WORK, "vol.npy")).astype(np.float32)   # (nz, ny, nx), z0 = inferior
    seg = np.load(os.path.join(WORK, "seg.npy"))
    v = v[::-1].copy(); seg = seg[::-1].copy()                       # index 0 = superior from here on
    v[v < -1000] = -1000
    nz, ny, nx = v.shape
    FX, FY, H_MM = nx * SP, ny * SP, nz * DZ

    # body-only volume for the topograms (no couch)
    fz = np.nonzero(seg.any((1, 2)))[0]
    def fem_box(z):
        zz = int(fz[np.argmin(np.abs(fz - z))])
        ys, xs = np.nonzero(seg[zz]); return xs.min() * SP, (xs.max() + 1) * SP, ys.min() * SP, (ys.max() + 1) * SP
    def limb_label(z, lab, st):
        fb = fem_box(z)
        cx, cy = int((fb[0] + fb[1]) / 2 / SP), int((fb[2] + fb[3]) / 2 / SP)
        return lab[cy, cx] if lab[cy, cx] else 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
    vb = np.full_like(v, -1000)                  # the right leg / body only: no couch, no stray left-knee edge
    for z in range(nz):
        m, lab, st = body_mask(v[z]); L = limb_label(z, lab, st); vb[z][lab == L] = v[z][lab == L]

    def topo(p, w_px_mm, pad_l, pad_r, fade_r):
        img = p
        h, w = img.shape
        img = cv2.resize(img, (int(round(w * w_px_mm / PX)), int(round(h * DZ / PX))), interpolation=cv2.INTER_CUBIC)
        img = cv2.GaussianBlur(img, (0, 0), 0.7)
        rng = np.random.default_rng(7)
        img = img + rng.normal(0, 0.02, img.shape).astype(np.float32) * np.sqrt(np.maximum(img, 0.05))
        body = img[img > 0.15 * img.max()]
        lo, hi = np.percentile(body, 1), np.percentile(body, 99.9)
        out = np.clip((img - lo * 0.6) / (hi - lo * 0.6), 0, 1) ** 1.35       # soft tissue grey, bone bright
        if fade_r:                                                    # soften the dataset's medial crop edge
            r = int(round(fade_r / PX)); ramp = np.linspace(1, 0.55, r)
            out[:, -r:] *= ramp[None, :]
        out = (out * 255).astype(np.uint8)
        out = cv2.copyMakeBorder(out, 0, 0, int(round(pad_l / PX)), int(round(pad_r / PX)), cv2.BORDER_CONSTANT, value=0)
        return tint(out)

    mu = np.maximum(vb + 1000, 0) * MU
    ap = mu.sum(1) * SP                         # (nz, nx)  patient right (x0) on the left
    lat = mu.sum(2) * SP                        # (nz, ny)  anterior (y0) on the left
    a = topo(ap, SP, PAD_AP, PAD_AP_R, 14)
    l = topo(lat, SP, PAD_LAT, PAD_LAT, 0)
    cv2.imwrite(os.path.join(OUT, "scout_ap.jpg"), a, [cv2.IMWRITE_JPEG_QUALITY, 88])
    cv2.imwrite(os.path.join(OUT, "scout_lat.jpg"), l, [cv2.IMWRITE_JPEG_QUALITY, 88])
    SW, SWL = a.shape[1] * PX, l.shape[1] * PX
    print("scouts", a.shape, l.shape, round(SW, 1), round(SWL, 1))

    # ---- axial slices, superior -> inferior ----
    ax = []
    for k in range(nz):
        cv2.imwrite(os.path.join(OUT, f"ax_{k:03d}.jpg"), hu_to_byte(v[k]), [cv2.IMWRITE_JPEG_QUALITY, 88])
        m, lab, st = body_mask(v[k])
        fb = fem_box(k); L = limb_label(k, lab, st)
        ys, xs = np.nonzero(lab == L)
        x0, x1 = xs.min() * SP, min((xs.max() + 1) * SP, MED_CAP)
        y0, y1 = ys.min() * SP, (ys.max() + 1) * SP
        if y1 - y0 > AP_CAP:                                          # centre the judged depth on the femur
            c = (fb[2] + fb[3]) / 2; y0, y1 = max(y0, c - AP_CAP / 2), min(y1, c + AP_CAP / 2)
        ax.append({"z": round((k + 0.5) * DZ, 2), "ext": [round(PAD_AP + x0, 1), round(PAD_AP + x1, 1), round(y0, 1), round(y1, 1)]})
    E = np.array([q["ext"] for q in ax], float)
    for i in range(len(ax)):
        ax[i]["ext"] = [round(float(x), 1) for x in np.median(E[max(0, i - 2):i + 3], axis=0)]
    print("axial", len(ax))

    # ---- reformats: z resampled from 2 mm to PX (linear) ----
    zh = int(round(H_MM / PX))
    def zres(img):          # img (nz, n) -> (zh, n*SP/PX)
        return cv2.resize(img, (int(round(img.shape[1] * SP / PX)), zh), interpolation=cv2.INTER_LINEAR)

    tissue = (vb > -400)
    yz = np.nonzero(tissue.any((0, 2)))[0]; xz = np.nonzero(tissue.any((0, 1)))[0]
    cor_y, sag_x = [], []
    y_mm, i = yz.min() * SP, 0
    while y_mm <= (yz.max() + 1) * SP:
        yi = int(round(y_mm / SP))
        sl = v[:, max(0, yi - 1):yi + 1, :].mean(1)
        cv2.imwrite(os.path.join(OUT, f"cor_{i:02d}.jpg"), hu_to_byte(zres(sl)), [cv2.IMWRITE_JPEG_QUALITY, 86])
        cor_y.append(round(y_mm, 2)); y_mm += STEP; i += 1
    x_mm, i = xz.min() * SP, 0
    while x_mm <= (xz.max() + 1) * SP:
        xi = int(round(x_mm / SP))
        sl = v[:, :, max(0, xi - 1):xi + 1].mean(2)
        cv2.imwrite(os.path.join(OUT, f"sag_{i:02d}.jpg"), hu_to_byte(zres(sl)), [cv2.IMWRITE_JPEG_QUALITY, 86])
        sag_x.append(round(PAD_AP + x_mm, 2)); x_mm += STEP; i += 1
    print("coronal", len(cor_y), "sagittal", len(sag_x))

    # landmarks, mm from the superior edge (z index 0 = top of the top slice)
    top_edge = -1.25 + DZ / 2                                       # LPS z of the scout's top edge
    lm = {
        "head_top": round((fz.min()) * DZ, 1),                      # first slice with femur (femoral head dome)
        "head_ctr": round(top_edge - (-50.4298), 1),               # dataset landmark file (Pat001_palp.inp)
        "gt": round(top_edge - (-47.2958), 1),
        "lt": 103.0,                                                 # medial bulge of the mask (lesser trochanter)
        "knee_ctr": round(top_edge - (-398.1065), 1),
        "condyle_bot": round((fz.max() + 1) * DZ, 1),               # last slice with femur
    }
    calib = {
        "source": "HFValid collection Pat001 (Aldieri et al. 2023, doi:10.6092/unibo/amsacta/7277, CC BY 4.0)",
        "sp": SP, "dz": DZ, "px": PX, "step": STEP, "field_x": round(FX, 3), "field_y": round(FY, 3),
        "pad_ap": PAD_AP, "pad_lat": PAD_LAT, "scout_w_mm": round(SW, 2), "scout_lat_w_mm": round(SWL, 2),
        "scout_h_mm": round(H_MM, 2), "img_w": nx, "img_h": ny, "hu_lut": HU_LUT,
        "landmarks": lm, "ax": ax, "cor_y": cor_y, "sag_x": sag_x,
    }
    with open(os.path.join(OUT, "calib.json"), "w") as f:
        json.dump(calib, f, separators=(",", ":"))
    with open(os.path.join(OUT, "calib.js"), "w") as f:
        f.write("window.SCG_CALIB=" + json.dumps(calib, separators=(",", ":")) + ";\n")
    print("landmarks", lm, "field", round(FX, 1), "x", round(FY, 1))


if __name__ == "__main__":
    main()
