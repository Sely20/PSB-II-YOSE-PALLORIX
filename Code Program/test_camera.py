import cv2


# =========================================================
# TEST KAMERA
# =========================================================

kamera = cv2.VideoCapture(1)

print("Kamera berhasil dibuka")
print("Tekan tombol q untuk keluar")

while True:

    berhasil, frame = kamera.read()

    if not berhasil:
        print("Gagal membaca kamera")
        break

    frame = cv2.flip(frame, 1)

    cv2.putText(
        frame,
        "YOSE Pallorix Camera Test",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2
    )

    cv2.imshow("Test Kamera", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

kamera.release()
cv2.destroyAllWindows()

print("Kamera ditutup")