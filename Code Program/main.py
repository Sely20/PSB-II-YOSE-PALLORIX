import cv2
import numpy as np

from roi_tangan import ambil_roi_tangan
from ekstraksi_warna import ekstraksi_fitur
from deteksi_anemia import klasifikasi_anemia
from validasi_tangan import validasi_tangan


# =====================================================
# BUKA KAMERA
# =====================================================

def buka_kamera():

    kamera_index = [1, 0, 2]

    for idx in kamera_index:

        cap = cv2.VideoCapture(idx, cv2.CAP_DSHOW)

        if cap.isOpened():

            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

            cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
            cap.set(cv2.CAP_PROP_AUTO_WB, 1)

            cap.set(cv2.CAP_PROP_BRIGHTNESS, 128)
            cap.set(cv2.CAP_PROP_CONTRAST, 128)
            cap.set(cv2.CAP_PROP_SATURATION, 128)

            for _ in range(10):
                cap.read()

            ret, frame = cap.read()

            if ret:
                print(f"Kamera aktif di index {idx}")
                return cap

            cap.release()

    return None


# =====================================================
# START KAMERA
# =====================================================

cap = buka_kamera()

if cap is None:
    print("Kamera tidak terbaca.")
    exit()


# =====================================================
# DEFAULT STATE
# =====================================================

status = "TEKAN SPACE UNTUK SCAN"
warna  = (255, 255, 0)
score  = 0
sudah_scan = False

fitur = {
    "R": 0, "G": 0, "B": 0,
    "L_star": 0, "a_star": 0,
    "redness_ratio": 0,
    "pallor_index": 0,
    "r_norm": 0, "g_norm": 0
}


# =====================================================
# CEK TANGAN LIVE (tanpa tekan space)
# =====================================================

def cek_tangan_live(roi):

    if roi is None or roi.size == 0:
        return False

    brightness = np.mean(roi)
    if brightness < 40:
        return False

    ycrcb = cv2.cvtColor(roi, cv2.COLOR_BGR2YCrCb)

    lower_skin = np.array([0, 120, 70], dtype=np.uint8)
    upper_skin = np.array([255, 190, 150], dtype=np.uint8)

    mask = cv2.inRange(ycrcb, lower_skin, upper_skin)

    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    skin_pixels  = cv2.countNonZero(mask)
    total_pixels = roi.shape[0] * roi.shape[1]
    skin_ratio   = skin_pixels / total_pixels

    return skin_ratio >= 0.10


# =====================================================
# FUNGSI GAMBAR PANEL INFO
# =====================================================

def gambar_panel(frame, fitur, status, warna, score, ada_tangan, sudah_scan):

    h, w = frame.shape[:2]

    rasio_rg = fitur["R"] / (fitur["G"] + 1) if fitur["G"] > 0 else 0

    # ---- INDIKATOR TANGAN (pojok kanan atas) ----
    if ada_tangan:
        indikator_warna = (0, 200, 0)
        indikator_teks  = "TANGAN TERDETEKSI"
    else:
        indikator_warna = (0, 0, 255)
        indikator_teks  = "TANGAN TIDAK ADA"

    cv2.putText(frame, indikator_teks,
                (w - 250, 30), cv2.FONT_HERSHEY_SIMPLEX,
                0.55, indikator_warna, 2)

    # ---- STATUS ----
    # Kalau belum scan dan tidak ada tangan, tampilkan peringatan
    if not sudah_scan and not ada_tangan:
        tampil_status = "LETAKKAN TANGAN DI ROI"
        tampil_warna  = (0, 200, 255)
    elif not sudah_scan and ada_tangan:
        tampil_status = "TEKAN SPACE UNTUK SCAN"
        tampil_warna  = (255, 255, 0)
    else:
        tampil_status = status
        tampil_warna  = warna

    cv2.putText(frame, f"Status : {tampil_status}",
                (20, 40), cv2.FONT_HERSHEY_SIMPLEX,
                0.75, tampil_warna, 2)

    # ---- GARIS PEMISAH ----
    cv2.line(frame, (20, 55), (w - 20, 55), (80, 80, 80), 1)

    # ---- RGB ----
    cv2.putText(frame, f"R : {fitur['R']}",
                (20, 85), cv2.FONT_HERSHEY_SIMPLEX,
                0.6, (100, 100, 255), 2)

    cv2.putText(frame, f"G : {fitur['G']}",
                (20, 115), cv2.FONT_HERSHEY_SIMPLEX,
                0.6, (100, 255, 100), 2)

    cv2.putText(frame, f"B : {fitur['B']}",
                (20, 145), cv2.FONT_HERSHEY_SIMPLEX,
                0.6, (255, 150, 100), 2)

    # ---- GARIS PEMISAH ----
    cv2.line(frame, (20, 160), (w - 20, 160), (80, 80, 80), 1)

    # ---- LAB ----
    cv2.putText(frame, f"L* : {fitur['L_star']}",
                (20, 190), cv2.FONT_HERSHEY_SIMPLEX,
                0.6, (255, 255, 255), 2)

    cv2.putText(frame, f"a* : {fitur['a_star']}",
                (20, 220), cv2.FONT_HERSHEY_SIMPLEX,
                0.6, (255, 255, 255), 2)

    # ---- GARIS PEMISAH ----
    cv2.line(frame, (20, 235), (w - 20, 235), (80, 80, 80), 1)

    # ---- FITUR PALLOR ----
    cv2.putText(frame, f"Redness : {fitur['redness_ratio']}",
                (20, 265), cv2.FONT_HERSHEY_SIMPLEX,
                0.6, (255, 255, 255), 2)

    cv2.putText(frame, f"Pallor  : {fitur['pallor_index']}",
                (20, 295), cv2.FONT_HERSHEY_SIMPLEX,
                0.6, (255, 255, 255), 2)

    cv2.putText(frame, f"R/G     : {rasio_rg:.4f}",
                (20, 325), cv2.FONT_HERSHEY_SIMPLEX,
                0.6, (255, 255, 255), 2)

    # ---- SCORE BAR ----
    cv2.line(frame, (20, 345), (w - 20, 345), (80, 80, 80), 1)

    cv2.rectangle(frame, (20, 360), (w - 20, 380), (60, 60, 60), -1)

    bar_width = int((w - 40) * score)
    bar_width = min(bar_width, w - 40)

    if score >= 0.50:
        bar_color = (0, 200, 0)
    else:
        bar_color = (0, 0, 220)

    if bar_width > 0:
        cv2.rectangle(frame, (20, 360), (20 + bar_width, 380), bar_color, -1)

    cv2.putText(frame, f"Score : {score}",
                (20, 400), cv2.FONT_HERSHEY_SIMPLEX,
                0.6, (0, 255, 255), 2)

    cv2.putText(frame, "Score >= 0.50 : NORMAL  |  Score < 0.50 : TERINDIKASI ANEMIA",
                (20, 425), cv2.FONT_HERSHEY_SIMPLEX,
                0.38, (160, 160, 160), 1)

    # ---- PETUNJUK ----
    cv2.line(frame, (20, 438), (w - 20, 438), (80, 80, 80), 1)

    cv2.putText(frame, "SPACE = SCAN    Q = EXIT",
                (20, 460), cv2.FONT_HERSHEY_SIMPLEX,
                0.6, (200, 200, 200), 1)

    return frame


# =====================================================
# MAIN LOOP
# =====================================================

while True:

    ret, frame = cap.read()

    if not ret:
        print("Frame gagal dibaca.")
        break

    frame = cv2.flip(frame, 1)

    roi, frame = ambil_roi_tangan(frame)

    # Cek tangan live setiap frame (tanpa tekan space)
    ada_tangan = cek_tangan_live(roi)

    # Kalau tangan dicabut setelah scan, reset status
    if not ada_tangan and sudah_scan:
        sudah_scan = False
        status = "TEKAN SPACE UNTUK SCAN"
        warna  = (255, 255, 0)
        score  = 0
        fitur = {
            "R": 0, "G": 0, "B": 0,
            "L_star": 0, "a_star": 0,
            "redness_ratio": 0,
            "pallor_index": 0,
            "r_norm": 0, "g_norm": 0
        }

    key = cv2.waitKey(1) & 0xFF

    # ==========================================
    # SCAN (tekan SPACE)
    # ==========================================

    if key == ord(' '):

        if not ada_tangan:
            # Tidak ada tangan, jangan scan
            print("Tidak ada tangan di ROI, scan dibatalkan.")

        else:
            print("\n--- SCANNING ---")

            valid, pesan = validasi_tangan(roi)

            if valid:

                fitur  = ekstraksi_fitur(roi)
                status, warna, score = klasifikasi_anemia(fitur)
                sudah_scan = True

                print(f"Status  : {status}")
                print(f"Score   : {score}")
                print(f"R={fitur['R']} G={fitur['G']} B={fitur['B']}")
                print(f"a*={fitur['a_star']}  redness={fitur['redness_ratio']}  pallor={fitur['pallor_index']}")

            else:
                status     = pesan
                warna      = (0, 255, 255)
                score      = 0
                sudah_scan = False

                fitur = {
                    "R": 0, "G": 0, "B": 0,
                    "L_star": 0, "a_star": 0,
                    "redness_ratio": 0,
                    "pallor_index": 0,
                    "r_norm": 0, "g_norm": 0
                }

                print(f"Validasi gagal: {pesan}")

    elif key == ord('q'):
        break

    # ==========================================
    # GAMBAR PANEL INFO
    # ==========================================

    frame = gambar_panel(frame, fitur, status, warna, score, ada_tangan, sudah_scan)

    cv2.imshow("YOSE Pallorix", frame)


# =====================================================
# RELEASE
# =====================================================

cap.release()
cv2.destroyAllWindows()
print("Program selesai.")