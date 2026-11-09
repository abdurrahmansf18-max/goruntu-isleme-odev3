"""
Soru 4: Histogram Eşitleme (Histogram Equalization) (25 Puan) Modülü.

Bu modül, cv2.equalizeHist() gibi hazır fonksiyonları ve for döngülerini kullanmadan,
tamamen sıfırdan NumPy dizi işlemleriyle:
a) Histogram eşitleme algoritmasını 5 adımda uygulayan fonksiyonu (20 puan):
   1. Sıfırdan implementasyon
   2. Görüntünün manuel histogramının (n_j) hesaplanması
   3. Normalize edilmiş kümülatif histogramın (CDF) hesaplanması
   4. Dönüşüm fonksiyonunun oluşturulması: s_k = (L - 1) * sum_{j=0}^{k} (n_j / MN)
   5. Her pikselin dönüşüm tablosu (LUT) ile dönüştürülmesi
b) Orijinal ve eşitlenmiş görüntüleri yan yana, histogramlarını altlarına (2x2 subplot)
   ekleyerek karşılaştıran görselleştirme fonksiyonunu (5 puan)
içerir.
"""

import os
from typing import Dict, Tuple
import numpy as np
import matplotlib.pyplot as plt

from src.soru2_histogram_analizi import (
    manuel_histogram_hesapla,
    histogram_eksen_ciz,
    goruntu_istatistikleri_hesapla,
)


def manuel_histogram_esitleme(goruntu: np.ndarray) -> Tuple[np.ndarray, Dict[str, np.ndarray]]:
    """
    Soru 4a (20 Puan): 8-bit gri seviye görüntü üzerinde sıfırdan histogram eşitleme
    algoritmasını uygular.

    Algoritma Adımları:
        1. Görüntünün 256 seviyeli histogramını (n_j) manuel olarak hesapla.
        2. Toplam piksel sayısına (M * N) bölerek olasılık yoğunluk fonksiyonunu (PDF: n_j / MN)
           ve kümülatif toplam ile normalize kümülatif histogramı (CDF) hesapla.
        3. Dönüşüm fonksiyonunu oluştur: s_k = (L - 1) * sum_{j=0}^{k} (n_j / MN), burada L = 256.
        4. Vektörize NumPy dizinleme (lookup table) ile her pikseli yeni gri seviyesine dönüştür.

    Parametreler:
        goruntu (np.ndarray): Giriş gri seviye görüntüsü (uint8, L=256 seviye).

    Döndürür:
        Tuple[np.ndarray, Dict[str, np.ndarray]]:
            - esitlenmis_goruntu (np.ndarray): Histogramı eşitlenmiş uint8 görüntü matrisi
            - ara_veriler (Dict[str, np.ndarray]): 'orijinal_histogram', 'pdf', 'cdf',
              'donusum_fonksiyonu_sk', 'esitlenmis_histogram' dizilerini içeren sözlük
    """
    if goruntu.ndim != 2:
        raise ValueError("Histogram eşitleme için giriş görüntüsü 2 boyutlu gri seviye olmalıdır.")

    # Adım 1 & 2: Görüntünün histogramını (n_j) sıfırdan hesaplıyoruz
    orijinal_histogram = manuel_histogram_hesapla(goruntu)
    toplam_piksel_mn = float(goruntu.size)

    # Adım 3: Normalize edilmiş histogram (PDF: p_r(r_j) = n_j / MN) ve
    # normalize edilmiş kümülatif histogram (CDF: sum_{j=0}^{k} n_j / MN)
    pdf = orijinal_histogram.astype(np.float64) / toplam_piksel_mn
    cdf = np.cumsum(pdf)

    # Adım 4: Dönüşüm fonksiyonu s_k = (L - 1) * sum_{j=0}^{k} (n_j / MN), L = 256 => L - 1 = 255
    l_eksi_1 = 255.0
    donusum_fonksiyonu_sk = np.clip(np.round(l_eksi_1 * cdf), 0, 255).astype(np.uint8)

    # Adım 5: Her pikseli for döngüsü kullanmadan NumPy ileri indeksleme (LUT) ile dönüştürüyoruz
    temiz_giris = np.clip(goruntu, 0, 255).astype(np.uint8)
    esitlenmis_goruntu = donusum_fonksiyonu_sk[temiz_giris]

    esitlenmis_histogram = manuel_histogram_hesapla(esitlenmis_goruntu)

    ara_veriler = {
        "orijinal_histogram": orijinal_histogram,
        "pdf": pdf,
        "cdf": cdf,
        "donusum_fonksiyonu_sk": donusum_fonksiyonu_sk,
        "esitlenmis_histogram": esitlenmis_histogram,
    }
    return esitlenmis_goruntu, ara_veriler


def soru4_gorsellestir(
    goruntu: np.ndarray,
    kayit_yolu: str = "outputs/figures/soru4_histogram_esitleme_2x2.png",
    cdf_kayit_yolu: str = "outputs/figures/soru4_cdf_ve_donusum_egrisi.png",
    baslik_eki: str = "Koyu Görüntü",
) -> Tuple[np.ndarray, Dict[str, str]]:
    """
    Soru 4b (5 Puan): Orijinal ve eşitlenmiş görüntüleri yan yana, her ikisinin
    histogramlarını altlarına (2x2 subplot) yerleştirerek karşılaştırır ve kaydeder.
    Ayrıca normalize kümülatif histogram (CDF) ve s_k dönüşüm fonksiyonunu ayrı bir
    analiz figüründe görselleştirir.

    Parametreler:
        goruntu (np.ndarray): Giriş gri seviye görüntüsü.
        kayit_yolu (str): 2x2 karşılaştırma figürünün kaydedileceği dosya yolu.
        cdf_kayit_yolu (str): CDF ve dönüşüm fonksiyonu grafiğinin dosya yolu.
        baslik_eki (str): Başlıkta yer alacak görüntü tipi açıklaması.

    Döndürür:
        Tuple[np.ndarray, Dict[str, str]]: Eşitlenmiş görüntü ve kaydedilen figür yolları.
    """
    os.makedirs(os.path.dirname(os.path.abspath(kayit_yolu)), exist_ok=True)

    esitlenmis, ara = manuel_histogram_esitleme(goruntu)
    ist_orj = goruntu_istatistikleri_hesapla(goruntu)
    ist_esit = goruntu_istatistikleri_hesapla(esitlenmis)

    # 1. Beklenen Çıktı: 2x2 Subplot (Üstte Orijinal ve Eşitlenmiş Görüntü, Altta Histogramları)
    fig1, eksenler = plt.subplots(2, 2, figsize=(13.5, 10))
    fig1.suptitle(
        f"Soru 4: Sıfırdan Histogram Eşitleme (Histogram Equalization) — {baslik_eki}",
        fontsize=14,
        fontweight="bold",
    )

    # Sol Üst (0, 0): Orijinal Görüntü
    ax_orj = eksenler[0, 0]
    ax_orj.imshow(goruntu, cmap="gray", vmin=0, vmax=255)
    ax_orj.set_title(
        f"Orijinal Görüntü (μ: {ist_orj['ortalama']:.1f}, σ: {ist_orj['standart_sapma']:.1f}, "
        f"H: {ist_orj['entropi']:.2f} bit)",
        fontsize=11,
        fontweight="bold",
    )
    ax_orj.set_xlabel("X Koordinatı (Piksel)", fontsize=9.5)
    ax_orj.set_ylabel("Y Koordinatı (Piksel)", fontsize=9.5)

    # Sağ Üst (0, 1): Eşitlenmiş Görüntü
    ax_esit = eksenler[0, 1]
    ax_esit.imshow(esitlenmis, cmap="gray", vmin=0, vmax=255)
    ax_esit.set_title(
        f"Histogram Eşitlenmiş Görüntü (μ: {ist_esit['ortalama']:.1f}, "
        f"σ: {ist_esit['standart_sapma']:.1f}, H: {ist_esit['entropi']:.2f} bit)",
        fontsize=11,
        fontweight="bold",
    )
    ax_esit.set_xlabel("X Koordinatı (Piksel)", fontsize=9.5)
    ax_esit.set_ylabel("Y Koordinatı (Piksel)", fontsize=9.5)

    # Sol Alt (1, 0): Orijinal Görüntü Histogramı
    histogram_eksen_ciz(
        eksenler[1, 0],
        ara["orijinal_histogram"],
        baslik=f"Orijinal Görüntü Histogramı (Min:{ist_orj['min_deger']}, Max:{ist_orj['max_deger']})",
        renk="#6c757d",
    )

    # Sağ Alt (1, 1): Eşitlenmiş Görüntü Histogramı
    histogram_eksen_ciz(
        eksenler[1, 1],
        ara["esitlenmis_histogram"],
        baslik=f"Eşitlenmiş Görüntü Histogramı (Min:{ist_esit['min_deger']}, Max:{ist_esit['max_deger']})",
        renk="#198754",
    )

    fig1.tight_layout()
    fig1.savefig(kayit_yolu, dpi=150, bbox_inches="tight")
    plt.close(fig1)

    # 2. Ek Analiz Grafiği: Normalize Kümülatif Histogram (CDF) ve Dönüşüm Fonksiyonu s_k
    seviyeler = np.arange(256)
    esit_cdf = np.cumsum(ara["esitlenmis_histogram"].astype(np.float64) / float(esitlenmis.size))

    fig2, (ax_cdf, ax_lut) = plt.subplots(1, 2, figsize=(13, 4.8))
    fig2.suptitle(
        f"Soru 4: Kümülatif Dağılım Fonksiyonu (CDF) ve Dönüşüm Eğrisi s_k — {baslik_eki}",
        fontsize=13,
        fontweight="bold",
    )

    ax_cdf.plot(seviyeler, ara["cdf"], color="#d62828", linewidth=2.0, label="Orijinal CDF")
    ax_cdf.plot(seviyeler, esit_cdf, color="#198754", linewidth=2.0, label="Eşitlenmiş CDF")
    ax_cdf.plot(
        seviyeler,
        seviyeler / 255.0,
        color="#495057",
        linestyle="--",
        linewidth=1.3,
        label="İdeal Doğrusal CDF",
    )
    ax_cdf.set_title("Normalize Kümülatif Histogram (CDF) Karşılaştırması", fontsize=11, fontweight="bold")
    ax_cdf.set_xlabel("Piksel Yoğunluk Değeri r_k (0 - 255)", fontsize=9.5)
    ax_cdf.set_ylabel("Kümülatif Olasılık P(r <= r_k)", fontsize=9.5)
    ax_cdf.set_xlim(0, 255)
    ax_cdf.set_ylim(0, 1.05)
    ax_cdf.grid(True, linestyle="--", alpha=0.4)
    ax_cdf.legend(loc="lower right", fontsize=9)

    ax_lut.plot(
        seviyeler,
        ara["donusum_fonksiyonu_sk"],
        color="#00509d",
        linewidth=2.2,
        label=r"$s_k = (L-1) \sum_{j=0}^{k} \frac{n_j}{MN}$",
    )
    ax_lut.plot(seviyeler, seviyeler, color="#adb5bd", linestyle="--", label="Birim Dönüşüm (s_k = r_k)")
    ax_lut.set_title("Histogram Eşitleme Dönüşüm Fonksiyonu (s_k)", fontsize=11, fontweight="bold")
    ax_lut.set_xlabel("Giriş Gri Seviyesi r_k (0 - 255)", fontsize=9.5)
    ax_lut.set_ylabel("Çıkış Gri Seviyesi s_k (0 - 255)", fontsize=9.5)
    ax_lut.set_xlim(0, 255)
    ax_lut.set_ylim(0, 255)
    ax_lut.grid(True, linestyle="--", alpha=0.4)
    ax_lut.legend(loc="lower right", fontsize=9.5)

    fig2.tight_layout()
    fig2.savefig(cdf_kayit_yolu, dpi=150, bbox_inches="tight")
    plt.close(fig2)

    return esitlenmis, {
        "karsilastirma_2x2": kayit_yolu,
        "cdf_ve_donusum": cdf_kayit_yolu,
    }
