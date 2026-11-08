# Credits

## CT imaging — HFValid collection, subject Pat001

**Adapted from:** Aldieri A, La Mattina AA, Szyszko JA, Baruffaldi F, Viceconti M. *HFValid collection:
Hip-Fracture validation collection* [Dataset]. University of Bologna, AMS Acta, 2023.
https://doi.org/10.6092/unibo/amsacta/7277 — https://amsacta.unibo.it/id/eprint/7277/

- Subject Pat001: calibrated CT of the right femur, hip to knee (0.703 mm pixels, 2 mm slices), with a femur
  segmentation and anatomical landmarks. The collection's scans were acquired at the Rizzoli Orthopaedic Institute
  for hip-arthroplasty planning.
- Licence: **Creative Commons Attribution 4.0 International (CC BY 4.0)** — https://creativecommons.org/licenses/by/4.0/ .
  Use, including commercial use, is allowed with attribution, a link to the licence and an indication of changes.

### Changes made

1. **Scanograms** (`scout_ap`, `scout_lat`) are simulated line-integral projections through the CT volume — not
   acquired localisers — with the couch removed, padded with air and teal-tinted to match the sibling sims.
   The dataset's field is cropped near the midline, so the AP scanogram shows the right side only; that cut edge is faded.
2. **Axial images** are the native 2 mm slices (220 images); **coronal and sagittal reformats** are 1.4 mm slabs every
   3 mm with the 2 mm slice spacing linearly interpolated to 0.7 mm; all re-encoded as 8-bit JPEG with a piecewise HU mapping.
3. In the browser the images are cropped and resampled to the chosen DFOV, blurred (0.8 mm gaussian) to simulate a
   soft-tissue kernel, and averaged / smeared along the femur to simulate thicker slices. The thinnest source slices are
   2 mm, so the "1 mm" option displays the native 2 mm data.
4. If the arms are left by the side, streak artefacts and noise are added over the hip and upper thigh in the browser to
   simulate the hands in the beam — they are not present in the acquired data.
5. The femur segmentation and the dataset's landmark file were used only to place the anatomical landmarks used for
   grading (femoral head, trochanters, knee centre, condyles). The arm / foot positions and the clinical request are
   fictional; no fracture is marked in the source data.

Neither the dataset authors nor the University of Bologna endorse this simulator.

## Other artwork

- Patient-positioning scene (CT room, selectable arm and foot positions, feet-first table movement, lasers): original 3-D
  scene built procedurally in `room3d.js` — no third-party models, photos or textures. A simpler original SVG drawing is
  the fallback if WebGL or the CDN is unavailable.
- 3-D rendering: [three.js](https://threejs.org) r160 (MIT licence, (c) three.js authors), loaded at runtime from
  https://cdn.jsdelivr.net/npm/three@0.160.0/.
- Rad-Lad logo: property of Rad-Lad.
