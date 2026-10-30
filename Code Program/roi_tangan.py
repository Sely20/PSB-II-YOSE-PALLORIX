import cv2


# =====================================================
# AMBIL ROI TELAPAK TANGAN
# =====================================================

def ambil_roi_tangan(frame):

    tinggi, lebar, _ = frame.shape

    # ==========================================
    # UKURAN ROI
    # ==========================================

    roi_w = 240
    roi_h = 240

    # ==========================================
    # POSISI ROI TENGAH
    # ==========================================

    center_x = lebar // 2
    center_y = tinggi // 2

    x1 = center_x - (roi_w // 2)
    y1 = center_y - (roi_h // 2)

    x2 = x1 + roi_w
    y2 = y1 + roi_h

    # ==========================================
    # BOUNDARY CHECK
    # ==========================================

    x1 = max(0, x1)
    y1 = max(0, y1)

    x2 = min(lebar, x2)
    y2 = min(tinggi, y2)

    # ==========================================
    # AMBIL ROI
    # ==========================================

    roi = frame[y1:y2, x1:x2]

    # ==========================================
    # VISUAL ROI
    # ==========================================

    cv2.rectangle(
        frame,
        (x1, y1),
        (x2, y2),
        (0, 255, 0),
        2
    )

    cv2.putText(
        frame,
        "ROI PALMAR",
        (x1, y1 - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 255, 0),
        2
    )

    return roi, frame