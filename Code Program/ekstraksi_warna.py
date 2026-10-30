import cv2
import numpy as np


def ekstraksi_fitur(roi):

    # ==================================
    # REDUKSI NOISE
    # ==================================

    roi = cv2.GaussianBlur(roi, (5, 5), 0)

    # ==================================
    # RGB
    # ==================================

    B = np.mean(roi[:, :, 0])
    G = np.mean(roi[:, :, 1])
    R = np.mean(roi[:, :, 2])

    brightness_index = (R + G + B) / 3

    # ==================================
    # NORMALIZED RGB
    # ==================================

    total = R + G + B + 1

    r_norm = R / total
    g_norm = G / total
    b_norm = B / total

    # ==================================
    # LAB
    # ==================================

    roi_lab = cv2.cvtColor(roi, cv2.COLOR_BGR2LAB)

    L_star = np.mean(roi_lab[:, :, 0])

    a_star = np.mean(roi_lab[:, :, 1]) - 128

    b_star = np.mean(roi_lab[:, :, 2]) - 128

    # ==================================
    # FITUR PALLOR
    # ==================================

    redness_ratio = r_norm - g_norm

    pallor_index = L_star - abs(a_star)

    rasio_rg = R / (G + 1)

    rasio_rb = R / (B + 1)

    # ==================================
    # RETURN
    # ==================================

    fitur = {

        "R": round(R, 2),
        "G": round(G, 2),
        "B": round(B, 2),

        "r_norm": round(r_norm, 4),
        "g_norm": round(g_norm, 4),
        "b_norm": round(b_norm, 4),

        "L_star": round(L_star, 2),
        "a_star": round(a_star, 2),
        "b_star": round(b_star, 2),

        "redness_ratio": round(redness_ratio, 4),

        "pallor_index": round(pallor_index, 4),

        "brightness_index": round(brightness_index, 2),

        "rasio_rg": round(rasio_rg, 4),

        "rasio_rb": round(rasio_rb, 4)
    }

    return fitur