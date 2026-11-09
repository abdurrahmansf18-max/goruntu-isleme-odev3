"""
Soru 3: Kontrast Germe (Contrast Stretching) (15 Puan) Modülü.

Bu modül:
a) Görüntünün minimum ve maksimum piksel değerlerini bularak pikselleri [0, 255]
   aralığına doğrusal olarak genişleten manuel kontrast germe fonksiyonunu (10 puan)
b) Orijinal görüntü, işlenmiş görüntü ve her ikisinin manuel histogramlarını
   2x2 subplot düzeninde gösteren görselleştirme fonksiyonunu (5 puan)
içerir.
"""

import os
from typing import Tuple
import numpy as np
import matplotlib.pyplot as plt

from src.soru2_histogram_analizi import (
    manuel_histogram_hesapla,
    histogram_eksen_ciz,
    goruntu_istatistikleri_hesapla,
)


def manuel_kontrast_germe(goruntu: np.ndarray) -> Tuple[np.ndarray, int, int]:
    """
    Soru 3a (10 Puan): Görüntünün minimum ve maksimum piksel değerlerini bularak
    tüm pikselleri [0, 255] tam dinamik aralığına genişletir.

    Matematiksel Formül:
        output = ((input - min) / (max - min)) * 255

    Parametreler:
        goruntu (np.ndarray): Giriş gri seviye görüntüsü (uint8).

    Döndürür:
        Tuple[np.ndarray, int, int]:
            - gerilmis_goruntu (np.ndarray): [0, 255] aralığına genişletilmiş uint8 görüntü
            - min_deger (int): Orijinal görüntünün minimum piksel değeri
            - max_deger (int): Orijinal görüntünün maksimum piksel değeri
    """
    goruntu_float = goruntu.astype(np.float64)

    # Görüntünün minimum ve maksimum piksel değerlerini vektörize olarak buluyoruz
    min_deger = int(np.min(goruntu))
    max_deger = int(np.max(goruntu))

    # Eğer tüm pikseller aynı değere sahipse sıfıra bölmeyi önlemek için kontrol yapıyoruz
    if max_deger == min_deger:
        return np.zeros_like(goruntu, dtype=np.uint8), min_deger, max_deger

    # Doğrusal kontrast germe formülü: output = ((input - min) / (max - min)) * 255
    gerilmis = ((goruntu_float - float(min_deger)) / float(max_deger - min_deger)) * 255.0

    # Taşma kontrolü ve uint8 dönüşümü
    gerilmis_uint8 = np.clip(np.round(gerilmis), 0, 255).astype(np.uint8)
    return gerilmis_uint8, min_deger, max_deger


def soru3_gorsellestir(
    goruntu: np.ndarray,
    kayit_yolu: str = "outputs/figures/soru3_kontrast_germe_2x2.png",
    baslik_eki: str = "Düşük Kontrastlı Görüntü",
) -> Tuple[np.ndarray, str]:
    """
    Soru 3b (5 Puan): Orijinal görüntü, kontrast germe uygulanmış görüntü ve her ikisinin
    manuel hesaplanan histogramlarını 2x2 subplot düzeninde gösterir ve kaydeder.

    Parametreler:
        goruntu (np.ndarray): Düşük kontrastlı giriş görüntüsü.
        kayit_yolu (str): Kaydedilecek 2x2 figürün dosya yolu.
        baslik_eki (str): Figür başlığında belirtilecek görüntü açıklaması.

    Döndürür:
        Tuple[np.ndarray, str]: İşlenmiş görüntü ve kaydedilen figürün dosya yolu.
    """
    os.makedirs(os.path.dirname(os.path.abspath(kayit_yolu)), exist_ok=True)

    gerilmis, min_ilk, max_ilk = manuel_kontrast_germe(goruntu)
    hist_orijinal = manuel_histogram_hesapla(goruntu)
    hist_gerilmis = manuel_histogram_hesapla(gerilmis)

    ist_orijinal = goruntu_istatistikleri_hesapla(goruntu)
    ist_gerilmis = goruntu_istatistikleri_hesapla(gerilmis)

    # 2x2 subplot düzeni: Üstte görüntüler, altta histogramları
    fig, eksenler = plt.subplots(2, 2, figsize=(13, 10))
    fig.suptitle(
        f"Soru 3: Manuel Kontrast Germe (Contrast Stretching) — {baslik_eki}",
        fontsize=14,
        fontweight="bold",
    )

    # Sol Üst (0, 0): Orijinal Görüntü
    ax_img_orj = eksenler[0, 0]
    ax_img_orj.imshow(goruntu, cmap="gray", vmin=0, vmax=255)
    ax_img_orj.set_title(
        f"Orijinal Görüntü (Min: {min_ilk}, Max: {max_ilk}, σ: {ist_orijinal['standart_sapma']:.2f})",
        fontsize=11,
        fontweight="bold",
    )
    ax_img_orj.set_xlabel("X Koordinatı (Piksel)", fontsize=9.5)
    ax_img_orj.set_ylabel("Y Koordinatı (Piksel)", fontsize=9.5)

    # Sağ Üst (0, 1): Kontrast Germe Uygulanmış Görüntü
    ax_img_ger = eksenler[0, 1]
    ax_img_ger.imshow(gerilmis, cmap="gray", vmin=0, vmax=255)
    ax_img_ger.set_title(
        f"Kontrast Germe Sonrası (Min: {ist_gerilmis['min_deger']}, "
        f"Max: {ist_gerilmis['max_deger']}, σ: {ist_gerilmis['standart_sapma']:.2f})",
        fontsize=11,
        fontweight="bold",
    )
    ax_img_ger.set_xlabel("X Koordinatı (Piksel)", fontsize=9.5)
    ax_img_ger.set_ylabel("Y Koordinatı (Piksel)", fontsize=9.5)

    # Sol Alt (1, 0): Orijinal Görüntü Histogramı
    histogram_eksen_ciz(
        eksenler[1, 0],
        hist_orijinal,
        baslik=f"Orijinal Histogram — Dar Aralık [{min_ilk}, {max_ilk}]",
        renk="#e76f51",
    )

    # Sağ Alt (1, 1): İşlenmiş Görüntü Histogramı
    histogram_eksen_ciz(
        eksenler[1, 1],
        hist_gerilmis,
        baslik=(
            f"Kontrast Germe Sonrası Histogram — Tam Aralık "
            f"[{ist_gerilmis['min_deger']}, {ist_gerilmis['max_deger']}]"
        ),
        renk="#2a9d8f",
    )

    fig.tight_layout()
    fig.savefig(kayit_yolu, dpi=150, bbox_inches="tight")
    plt.close(fig)

    return gerilmis, kayit_yolu
