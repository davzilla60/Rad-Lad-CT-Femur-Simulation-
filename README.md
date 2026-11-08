# The Scanogram — CT Femur

An embeddable, single-file teaching simulator for the Rad-Lad website. Part of the "Scanogram" family
(circle of Willis, carotid, hand, knee, T-spine, CTPA, run-off, wrist, aorta). Marker: **Slice of the Thigh**.

## Flow

1. **Patient set-up** — the patient arrives supine, feet first, arms by the side and feet relaxed. Choose the **arms**
   (folded on the chest ✓ / by the side ✗ — hands beside the hips put streaks over the hip) and the **feet**
   (turned in ~15° and taped ✓ / relaxed, part marks — external rotation foreshortens the femoral neck). The 3-D room
   (`room3d.js`, three.js from jsDelivr; SVG fallback) shows each choice straight away; choices can be changed until
   `load`, but only the **first** pick of each is graded. `load` moves the table feet first to the knee lasers, then the
   mid-thigh to isocentre.
2. **Scanogram** — AP + lateral localisers (`scout`).
3. **Range + DFOV** — one box on the AP scanogram: height = scan range, width = square display FOV (512 matrix; AP
   centre automatic, lateral inset shows the depth covered). Ideal: above the acetabular roof → through the knee joint
   to the top of the tibial plateau; DFOV snug to the right thigh (≈ 195–220 mm here). The box starts too short at both
   ends and far too wide.
4. **Reconstruction** — kernel (bone / soft tissue) and slice thickness (1 / 3 / 5 mm), live preview of the proximal femur.
5. **Review** — axial, coronal and sagittal images rendered in the browser for the chosen range, DFOV, kernel and
   thickness; BONE / SOFT TISSUE windows; coronal hero; % score:
   arms 10 · feet 10 · hip limit 15 · knee limit 15 · dose/pelvis 5 · DFOV 25 · kernel 10 · thickness 10.

## Files

- `femur.embed.html` — self-contained deliverable (~6 MB, every image inlined); `index.html` = identical copy for one-drop hosting
- `femur.html` — source (loads `./assets/`, `assets/calib.js`, `room3d.js`); `python inline.py` rebuilds both
- `room3d.js` — procedural three.js CT room, supine feet first, `setPose({arms, feet})`. Bump `?v=N` in `femur.html` **and** `inline.py` together.
- `assets/` — `scout_ap/lat`, `ax_000…219` (native 2 mm axials, superior → inferior, HU-encoded JPEG), `cor_NN` / `sag_NN`
  (reformat slabs every 3 mm), `calib.json` / `calib.js` (geometry, per-slice tissue extent for DFOV judging, landmarks), logos
- `tools/load_vol.py` → `tools/gen_assets.py` — rebuild every image from the source DICOM (see CREDITS.md);
  `tools/patch_html.py` — the one-off conversion of the forked wrist page (kept for reference, do not re-run)

Landmarks (mm from the top of the scanogram, 440 mm long): femoral head dome 32, head centre 50, greater trochanter 47,
lesser trochanter 103, knee centre 398, distal condyles 428, tibial plateau to 440.

Debug hooks: `window.__scg` (`parse(cmd)`, `setBox({x0,x1,y0,y1})`, `computeScore()`, `clip()`, `extent()`),
`window.__room()` (`pose(0|2|3)`, `setPose({arms,feet})`, `cam([p],[t])`).

## Licence

The imaging is adapted from a **CC BY 4.0** dataset (HFValid collection, University of Bologna) — see CREDITS.md.
