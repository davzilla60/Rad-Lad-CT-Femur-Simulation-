"""Read Pat001 CT DICOM -> work/vol.npy (int16, z index 0 = inferior/knee end as in the DICOM, i.e. instance order)."""
import glob, os, numpy as np, pydicom
SRC = r"D:\Prometheus\CT\Femur\Patient Group 1\HFValid_Collection_dataset_v2\HFValid_Collection\Subjects\Subjects\Pat001 - DICOM\CT"
fs = sorted(glob.glob(os.path.join(SRC, "*.dcm")))
ds = [pydicom.dcmread(f) for f in fs]
ds.sort(key=lambda d: float(d.ImagePositionPatient[2]))
v = np.stack([d.pixel_array.astype(np.int16) * int(d.RescaleSlope) + int(d.RescaleIntercept) for d in ds])
print(v.shape, v.min(), v.max(), ds[0].ImagePositionPatient, ds[-1].ImagePositionPatient)
np.save(os.path.join(os.path.dirname(__file__), "..", "work", "vol.npy"), v)
