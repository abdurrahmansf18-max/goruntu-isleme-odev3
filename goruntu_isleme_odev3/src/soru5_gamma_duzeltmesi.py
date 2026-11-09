"""
Soru 5: Gamma Düzeltmesi (Gamma Correction) (15 Puan) Modülü.

Bu modül:
a) Kuvvet yasası dönüşümü (output = 255 * (input / 255)^gamma) uygulayan
   vektörize gamma düzeltme fonksiyonunu ve farklı gamma değerleri (0.5, 1.0, 1.5, 2.0, 2.5)
   için karşılaştırmalı görselleştirmeyi (10 puan)
b) Her gamma değerinin görüntü üzerindeki etkisini istatistiksel ve görsel olarak
   açıklayan, hangi durumda hangi gamma değerinin kullanılması gerektiğini raporlayan
   analiz fonksiyonunu (5 puan)
içerir.
"""

import os
from typing import Dict, List, Sequence, Tuple
import numpy as np
import matplotlib.pyplot as plt

from src.soru2_histogram_analizi import (
    manuel_histogram_hesapla,
    histogram_eksen_ciz,
    goruntu_istatistikleri_hesapla,
)

VARSAYILAN_GAMMA_DEGERLERI: Tuple[float, ...] = (0.5, 1.0, 1.5, 2.0, 2.5)


def gamma_duzeltmesi(goruntu: np.ndarray, gamma: float) -> np.ndarray:
    """
    Soru 5a (10 Puan): Görüntüye verilen gamma değeri ile kuvvet yasası (power-law)
    düzeltmesi uygular.

    Matematiksel Formül:
        output = 255 * (input / 255)^gamma

    Parametreler:
        goruntu (np.ndarray): Giriş gri seviye görüntüsü (uint8, 0-255).
        gamma (float): Pozitif gamma üs değeri (örn. 0.5, 1.0, 1.5, 2.0, 2.5).

    Döndürür:
        np.ndarray: Gamma düzeltmesi uygulanmış uint8 görüntü matrisi.
    """
    if gamma <= 0:
        raise ValueError("Gamma değeri pozitif (> 0) olmalıdır.")

    # Pikselleri [0, 1] aralığına normalize edip kuvvet fonksiyonunu vektörize uyguluyoruz
    normalize_giris = np.clip(goruntu.astype(np.float64), 0.0, 255.0) / 255.0
    cikis_float = 255.0 * np.power(normalize_giris, float(gamma))

    # Taşma kontrolü ile [0, 255] aralığında uint8 olarak döndürüyoruz
    return np.clip(np.round(cikis_float), 0, 255).astype(np.uint8)


def coklu_gamma_uygula(
    goruntu: np.ndarray,
    gamma_degerleri: Sequence[float] = VARSAYILAN_GAMMA_DEGERLERI,
) -> Dict[float, np.ndarray]:
    """
    Belirtilen tüm gamma değerleri için gamma düzeltmesi uygular ve sonuç sözlüğü döndürür.

    Parametreler:
        goruntu (np.ndarray): Giriş gri seviye görüntüsü.
        gamma_degerleri (Sequence[float]): Uygulanacak gamma değerleri dizisi.

    Döndürür:
        Dict[float, np.ndarray]: gamma -> işlenmiş görüntü eşleşmesi.
    """
    return {float(g): gamma_duzeltmesi(goruntu, float(g)) for g in gamma_degerleri}


def gamma_analizi_olustur(
    goruntu: np.ndarray,
    gamma_degerleri: Sequence[float] = VARSAYILAN_GAMMA_DEGERLERI,
) -> str:
    """
    Soru 5b (5 Puan): Her gamma değerinin (0.5, 1.0, 1.5, 2.0, 2.5) görüntü üzerindeki
    etkisini sayısal istatistiklerle birlikte açıklar ve hangi durumda hangi gamma
    değerinin kullanılması gerektiğini raporlar.

    Parametreler:
        goruntu (np.ndarray): Analiz edilecek giriş görüntüsü.
        gamma_degerleri (Sequence[float]): Değerlendirilecek gamma listesi.

    Döndürür:
        str: Ekrana yazdırılmaya ve rapora eklenmeye hazır analiz metni.
    """
    sonuclar = coklu_gamma_uygula(goruntu, gamma_degerleri)

    yorum_sozlugu = {
        0.5: (
            "Karanlık (düşük yoğunluklu) pikselleri güçlü biçimde genişletir, parlak bölgeleri sıkıştırır. "
            "Genel parlaklık artar ve gölgede kalan karanlık detaylar belirginleşir."
        ),
        1.0: (
            "Birim (doğrusal) dönüşümdür (output = input). Görüntünün parlaklık, kontrast ve "
            "histogram dağılımında hiçbir değişiklik meydana gelmez."
        ),
        1.5: (
            "Orta düzeyde karartma uygular; düşük tonları sıkıştırırken parlak tonların "
            "arasındaki kontrastı artırır. Hafif aşırı pozlanmış görüntülerde denge sağlar."
        ),
        2.0: (
            "Belirgin karartma sağlar; orta tonları koyu bölgeye çeker, çok parlak veya "
            "ağarmış (washed-out) bölgelerdeki detayların ayrışmasını kolaylaştırır."
        ),
        2.5: (
            "Güçlü karartma uygular; karanlık ve orta bölgeler 0'a yaklaşırken yalnızca "
            "yüksek parlaklıktaki detaylar korunur. Çok parlak/aşırı pozlanmış sahneler için uygundur."
        ),
    }

    satirlar: List[str] = [
        "=== Soru 5b: Gamma Düzeltmesi Analizi ve Kullanım Senaryoları ===",
        "",
        "1. Gamma Değerlerinin Görüntü İstatistikleri ve Görünüm Üzerindeki Etkisi:",
    ]

    for g in gamma_degerleri:
        ist = goruntu_istatistikleri_hesapla(sonuclar[float(g)])
        aciklama = yorum_sozlugu.get(
            round(float(g), 2),
            "γ < 1 görüntüyü aydınlatır, γ > 1 görüntüyü karartır.",
        )
        satirlar.append(
            f"  • Gamma (γ = {g:.1f}) -> Ortalama: {ist['ortalama']:.2f}, "
            f"Std. Sapma: {ist['standart_sapma']:.2f}, Entropi: {ist['entropi']:.4f} bit, "
            f"Min/Max: [{ist['min_deger']}, {ist['max_deger']}]\n"
            f"    Etki: {aciklama}"
        )

    satirlar.extend(
        [
            "",
            "2. Hangi Durumda Hangi Gamma Değeri Kullanılmalı?",
            "  • γ < 1 (örn. γ = 0.4 – 0.7, ödevde γ = 0.5): Az pozlanmış (underexposed), "
            "gece çekimi, kapalı mekan veya ters ışık nedeniyle gölgede kalmış KOYU görüntülerde "
            "karanlık bölgelerdeki gizli detayları ortaya çıkarmak için kullanılmalıdır.",
            "  • γ = 1.0: Görüntünün mevcut aydınlatma ve ton dağılımı dengeliyse, referans/orijinal "
            "durumu korumak için kullanılır.",
            "  • γ > 1 (örn. γ = 1.5, 2.0, 2.5): Aşırı pozlanmış (overexposed), yoğun güneş ışığı "
            "altında çekilmiş, parlama içeren veya soluk/ağarmış (washed-out) PARLAK görüntülerde "
            "parlak bölgelerdeki detayları geri kazanmak ve kontrastı güçlendirmek için kullanılmalıdır.",
        ]
    )

    analiz_metni = "\n".join(satirlar)
    print(analiz_metni)
    return analiz_metni


def soru5_gorsellestir(
    goruntu: np.ndarray,
    cikti_klasoru: str = "outputs/figures",
    gamma_degerleri: Sequence[float] = VARSAYILAN_GAMMA_DEGERLERI,
) -> Dict[str, str]:
    """
    Soru 5a & 5b: Farklı gamma değerleri (0.5, 1.0, 1.5, 2.0, 2.5) için elde edilen
    görüntüleri, histogramlarını ve kuvvet yasası dönüşüm eğrilerini görselleştirip kaydeder.

    Parametreler:
        goruntu (np.ndarray): Giriş gri seviye görüntüsü.
        cikti_klasoru (str): Figürlerin kaydedileceği klasör yolu.
        gamma_degerleri (Sequence[float]): Görselleştirilecek gamma değerleri.

    Döndürür:
        Dict[str, str]: Oluşturulan figürlerin dosya yolları.
    """
    os.makedirs(cikti_klasoru, exist_ok=True)
    sonuclar = coklu_gamma_uygula(goruntu, gamma_degerleri)

    # 1. Ana Görselleştirme: Üst satırda γ = 0.5, 1.0, 1.5, 2.0, 2.5 görüntüleri,
    # alt satırda her birinin manuel hesaplanan histogramları (2x5 subplot)
    sutun_sayisi = len(gamma_degerleri)
    fig1, eksenler = plt.subplots(2, sutun_sayisi, figsize=(4.2 * sutun_sayisi, 8.5))
    fig1.suptitle(
        "Soru 5: Farklı Gamma Değerleri (0.5, 1.0, 1.5, 2.0, 2.5) İçin Gamma Düzeltmesi ve Histogramlar",
        fontsize=14,
        fontweight="bold",
        y=1.01,
    )

    renkler = ["#2a9d8f", "#1f77b4", "#e9c46a", "#f4a261", "#e76f51"]
    for idx, g in enumerate(gamma_degerleri):
        img_g = sonuclar[float(g)]
        hist_g = manuel_histogram_hesapla(img_g)
        ist_g = goruntu_istatistikleri_hesapla(img_g)

        ax_ust = eksenler[0, idx]
        ax_alt = eksenler[1, idx]

        ax_ust.imshow(img_g, cmap="gray", vmin=0, vmax=255)
        etiket = " (Orijinal)" if abs(float(g) - 1.0) < 1e-9 else ""
        ax_ust.set_title(
            f"γ = {g:.1f}{etiket}\n[μ:{ist_g['ortalama']:.1f}, σ:{ist_g['standart_sapma']:.1f}]",
            fontsize=11,
            fontweight="bold",
        )
        ax_ust.set_xlabel("X Koordinatı (Piksel)", fontsize=9)
        ax_ust.set_ylabel("Y Koordinatı (Piksel)", fontsize=9)

        histogram_eksen_ciz(
            ax_alt,
            hist_g,
            baslik=f"Histogram (γ = {g:.1f}, H = {ist_g['entropi']:.2f} bit)",
            renk=renkler[idx % len(renkler)],
        )

    fig1.tight_layout()
    goruntuler_yol = os.path.join(cikti_klasoru, "soru5_gamma_duzeltmesi_karsilastirma.png")
    fig1.savefig(goruntuler_yol, dpi=150, bbox_inches="tight")
    plt.close(fig1)

    # 2. Gamma Dönüşüm Eğrileri Grafiği: s = 255 * (r / 255)^gamma
    fig2, ax_egri = plt.subplots(1, 1, figsize=(7.5, 6))
    r_degerleri = np.arange(256, dtype=np.float64)
    for idx, g in enumerate(gamma_degerleri):
        s_degerleri = 255.0 * np.power(r_degerleri / 255.0, float(g))
        cizgi_stili = "--" if abs(float(g) - 1.0) < 1e-9 else "-"
        ax_egri.plot(
            r_degerleri,
            s_degerleri,
            linestyle=cizgi_stili,
            linewidth=2.2,
            color=renkler[idx % len(renkler)],
            label=f"γ = {g:.1f}",
        )

    ax_egri.set_title(
        r"Soru 5: Gamma Kuvvet Yasası Dönüşüm Eğrileri — $output = 255 \times (input / 255)^\gamma$",
        fontsize=12,
        fontweight="bold",
    )
    ax_egri.set_xlabel("Giriş Piksel Değeri (input, 0 - 255)", fontsize=10.5)
    ax_egri.set_ylabel("Çıkış Piksel Değeri (output, 0 - 255)", fontsize=10.5)
    ax_egri.set_xlim(0, 255)
    ax_egri.set_ylim(0, 255)
    ax_egri.grid(True, linestyle="--", alpha=0.4)
    ax_egri.legend(title="Gamma Değeri", fontsize=10)

    fig2.tight_layout()
    egri_yol = os.path.join(cikti_klasoru, "soru5_gamma_donusum_egrileri.png")
    fig2.savefig(egri_yol, dpi=150, bbox_inches="tight")
    plt.close(fig2)

    return {
        "karsilastirma": goruntuler_yol,
        "donusum_egrileri": egri_yol,
    }
