def klasifikasi_anemia(fitur):

    redness_ratio = fitur["redness_ratio"]
    pallor_index  = fitur["pallor_index"]
    L_star        = fitur["L_star"]
    a_star        = fitur["a_star"]
    R             = fitur["R"]
    G             = fitur["G"]
    B             = fitur["B"]

    score = 0

    # =============================================
    # FITUR 1: a* LAB
    # Dikalibrasi ulang — threshold dinaikkan
    # karena kamera natural nilai a* lebih tinggi
    # Normal sehat: a* > 4
    # Borderline   : a* 2-4
    # Pucat        : a* < 2
    # =============================================
    if a_star > 4.0:
        score += 0.30
    elif a_star > 2.0:
        score += 0.20
    elif a_star > 1.0:
        score += 0.10

    # =============================================
    # FITUR 2: REDNESS RATIO
    # Dikalibrasi ulang dari data aktual
    # Normal sehat: redness > 0.04
    # Borderline  : redness 0.02-0.04
    # Pucat       : redness < 0.02
    # =============================================
    if redness_ratio > 0.04:
        score += 0.25
    elif redness_ratio > 0.02:
        score += 0.15
    elif redness_ratio > 0.005:
        score += 0.05

    # =============================================
    # FITUR 3: PALLOR INDEX
    # Dikalibrasi ulang — range kamera natural
    # Normal sehat: pallor < 185
    # Borderline  : pallor 185-192
    # Pucat       : pallor > 192
    # =============================================
    if pallor_index < 185:
        score += 0.20
    elif pallor_index < 192:
        score += 0.10

    # =============================================
    # FITUR 4: LUMINANCE L*
    # Dikalibrasi ulang — range kamera natural
    # Normal sehat: L* < 188
    # Borderline  : L* 188-194
    # Pucat       : L* > 194
    # =============================================
    if L_star < 188:
        score += 0.10
    elif L_star < 194:
        score += 0.05

    # =============================================
    # FITUR 5: DOMINASI R terhadap G
    # R/G > 1.07 = merah dominan = sehat
    # Diturunkan dari 1.10 supaya lebih sensitif
    # =============================================
    rasio_rg = R / (G + 1)
    rasio_rb = R / (B + 1)

    if rasio_rg > 1.07 and rasio_rb > 1.00:
        score += 0.10

    # =============================================
    # KLASIFIKASI FINAL
    # =============================================
    if score >= 0.50:
        status = "NORMAL"
        warna  = (0, 200, 0)

    else:
        status = "TERINDIKASI ANEMIA"
        warna  = (0, 0, 255)

    return status, warna, round(score, 4)