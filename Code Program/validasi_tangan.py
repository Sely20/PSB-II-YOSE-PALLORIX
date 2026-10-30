import cv2
import numpy as np


# =====================================================
# VALIDASI ROI TELAPAK TANGAN
# =====================================================

def validasi_tangan(roi):

    # ==========================================
    # CEK BRIGHTNESS
    # ==========================================

    brightness = np.mean(roi)

    if brightness < 40:

        return False, "TERLALU GELAP"

    # ==========================================
    # KONVERSI YCrCb
    # ==========================================

    ycrcb = cv2.cvtColor(roi, cv2.COLOR_BGR2YCrCb)

    # ==========================================
    # RANGE WARNA KULIT
    # dibuat lebih fleksibel
    # ==========================================

    lower_skin = np.array([0, 120, 70], dtype=np.uint8)

    upper_skin = np.array([255, 190, 150], dtype=np.uint8)

    # ==========================================
    # MASK KULIT
    # ==========================================

    mask = cv2.inRange(
        ycrcb,
        lower_skin,
        upper_skin
    )

    # ==========================================
    # REDUKSI NOISE
    # ==========================================

    kernel = np.ones((3, 3), np.uint8)

    mask = cv2.morphologyEx(
        mask,
        cv2.MORPH_OPEN,
        kernel
    )

    # ==========================================
    # HITUNG SKIN PIXEL
    # ==========================================

    skin_pixels = cv2.countNonZero(mask)

    total_pixels = roi.shape[0] * roi.shape[1]

    skin_ratio = skin_pixels / total_pixels

    # ==========================================
    # DEBUG RATIO
    # ==========================================

    print(f"Skin Ratio : {skin_ratio:.2f}")

    # ==========================================
    # VALIDASI
    # ==========================================

    if skin_ratio < 0.10:

        return False, "TANGAN TIDAK TERDETEKSI"

    return True, "TANGAN VALID"