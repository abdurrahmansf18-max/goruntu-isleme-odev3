"""
Soru 2: Histogram Analizi ve Görselleştirme (20 Puan) Modülü.

Bu modül, hazır histogram fonksiyonları (cv2.calcHist, np.histogram, plt.hist vb.)
ve klasik for döngüleri kullanmadan, tamamen vektörize NumPy dizi işlemleriyle:
a) Gri seviye görüntüsünün manuel histogramını hesaplayan ve grafiğini çizen fonksiyonları (8 puan)
b) Ortalama (mean), standart sapma (standard deviation), Shannon entropisi ve
   minimum/maksimum piksel değerlerini hesaplayıp ekrana/rapora yazdıran fonksiyonları (12 puan)
içerir.
"""

import math
import os
from typing import Dict, Optional
import numpy as np
import matplotlib.pyplot as plt


def manuel_histogram_hesapla(goruntu: np.ndarray) -> np.ndarray:
    """
    Soru 2a (8 Puan): 8-bit gri seviye bir görüntünün 256 seviyeli (0-255) histogramını
    hazır fonksiyon (cv2.calcHist, np.histogram vb.) ve for döngüsü kullanmadan,
    vektörize NumPy karşılaştırma (broadcasting) ile sıfırdan hesaplar.

    Matematiksel Tanım:
        h(k) = n_k = sum_{x=0}^{M-1} sum_{y=0}^{N-1} I(goruntu(x, y) == k),  k in {0, 1, ..., 255}

    Parametreler:
        goruntu (np.ndarray): Gri seviye görüntü matrisi (uint8, 0-255).

    Döndürür:
        np.ndarray: 256 elemanlı (int64) piksel frekans dizisi.
    """
    if goruntu.ndim != 2:
        raise ValueError("Histogram hesaplama için giriş görüntüsü 2 boyutlu (gri seviye) olmalıdır.")

    # Görüntüyü 1B vektöre (MN, 1) dönüştürüп 0..255 gri seviye satır vektörü (1, 256) ile
    # karşılaştırarak her gri seviyenin kaç kez tekrarlandığını toplam olarak buluyoruz.
    duz_pikseller = np.clip(goruntu, 0, 255).astype(np.uint8).ravel()
    gri_seviyeler = np.arange(256, dtype=np.uint8)

    # Bellek dostu ve tamamen vektörize NumPy yayınlama (broadcasting) işlemi
    eslesme_matrisi = duz_pikseller[:, np.newaxis] == gri_seviyeler[np.newaxis, :]
    histogram = np.sum(eslesme_matrisi, axis=0, dtype=np.int64)
    return histogram


def histogram_eksen_ciz(
    ax: plt.Axes,
    histogram: np.ndarray,
    baslik: str = "Gri Seviye Histogramı",
    renk: str = "#1f77b4",
) -> None:
    """
    Manuel hesaplanmış 256 elemanlı histogram dizisini verilen Matplotlib eksenine (Axes)
    hazır plt.hist() kullanmadan çubuk ve zarf grafiği olarak çizer.

    Parametreler:
        ax (plt.Axes): Çizimin yapılacağı Matplotlib ekseni.
        histogram (np.ndarray): 256 elemanlı manuel hesaplanmış frekans dizisi.
        baslik (str): Grafiğin başlığı.
        renk (str): Çubuk rengi kodu.
    """
    seviyeler = np.arange(256)
    ax.bar(seviyeler, histogram, width=1.0, color=renk, alpha=0.75, edgecolor="none", label="Piksel Frekansı")
    ax.plot(seviyeler, histogram, color="#0d3b66", linewidth=0.9, alpha=0.85)
    ax.set_xlim(0, 255)
    ax.set_title(baslik, fontsize=11, fontweight="bold")
    ax.set_xlabel("Piksel Yoğunluk Değeri (0 - 255)", fontsize=9.5)
    ax.set_ylabel("Piksel Sayısı (Frekans)", fontsize=9.5)
    ax.grid(True, linestyle="--", alpha=0.35)


def histogram_ciz(
    goruntu: np.ndarray,
    kayit_yolu: Optional[str] = None,
    baslik: str = "Görüntü Histogram Analizi",
) -> np.ndarray:
    """
    Soru 2a (8 Puan): Bir gri seviye görüntünün histogramını manuel olarak hesaplar
    ve orijinal görüntüyle birlikte histogram grafiğini çizer.

    Parametreler:
        goruntu (np.ndarray): Gri seviye görüntü matrisi.
        kayit_yolu (Optional[str]): Grafiğin kaydedileceği dosya yolu (None ise kaydedilmez).
        baslik (str): Figür ana başlığı.

    Döndürür:
        np.ndarray: Hesaplanan 256 elemanlı histogram dizisi.
    """
    histogram = manuel_histogram_hesapla(goruntu)

    fig, (ax_img, ax_hist) = plt.subplots(1, 2, figsize=(13, 4.8))
    fig.suptitle(baslik, fontsize=13, fontweight="bold")

    ax_img.imshow(goruntu, cmap="gray", vmin=0, vmax=255)
    ax_img.set_title("Gri Seviye Görüntü", fontsize=11, fontweight="bold")
    ax_img.set_xlabel("X Koordinatı (Piksel)", fontsize=9.5)
    ax_img.set_ylabel("Y Koordinatı (Piksel)", fontsize=9.5)

    histogram_eksen_ciz(ax_hist, histogram, baslik="Manuel Hesaplanan Histogram (0-255)")

    fig.tight_layout()
    if kayit_yolu:
        os.makedirs(os.path.dirname(os.path.abspath(kayit_yolu)), exist_ok=True)
        fig.savefig(kayit_yolu, dpi=150, bbox_inches="tight")
    plt.close(fig)

    return histogram


def goruntu_istatistikleri_hesapla(goruntu: np.ndarray) -> Dict[str, float]:
    """
    Soru 2b (12 Puan): Bir gri seviye görüntünün temel istatistiklerini
    (ortalama, standart sapma, entropi, minimum ve maksimum piksel değerleri)
    vektörize NumPy dizi işlemleriyle hesaplar.

    Matematiksel Formüller:
        - Ortalama (Mean): mu = (1 / MN) * sum(I(x, y))
        - Standart Sapma (Std): sigma = sqrt((1 / MN) * sum((I(x, y) - mu)^2))
        - Olasılık Dağılımı: p(k) = n_k / (M * N)
        - Entropi (Shannon): H = -sum_{k: p(k) > 0} p(k) * log2(p(k))
        - Minimum ve Maksimum: min(I), max(I)

    Parametreler:
        goruntu (np.ndarray): Gri seviye görüntü matrisi (uint8).

    Döndürür:
        Dict[str, float]: 'ortalama', 'standart_sapma', 'entropi', 'min_deger', 'max_deger'
        anahtarlarını içeren istatistik sözlüğü.
    """
    goruntu_float = goruntu.astype(np.float64)
    toplam_piksel = float(goruntu_float.size)

    # 1. Ortalama (Mean) hesabı
    ortalama = float(np.sum(goruntu_float) / toplam_piksel)

    # 2. Standart sapma (Standard Deviation) hesabı
    varyans = float(np.sum((goruntu_float - ortalama) ** 2) / toplam_piksel)
    standart_sapma = math.sqrt(varyans)

    # 3. Entropi (Shannon Entropy) hesabı — manuel histogram üzerinden olasılık dağılımı p(k)
    histogram = manuel_histogram_hesapla(goruntu)
    olasiliklar = histogram.astype(np.float64) / toplam_piksel
    pozitif_olasiliklar = olasiliklar[olasiliklar > 0.0]
    entropi = -float(np.sum(pozitif_olasiliklar * np.log2(pozitif_olasiliklar)))

    # 4. Minimum ve maksimum piksel değerleri
    min_deger = int(np.min(goruntu))
    max_deger = int(np.max(goruntu))

    return {
        "ortalama": ortalama,
        "standart_sapma": standart_sapma,
        "entropi": entropi,
        "min_deger": min_deger,
        "max_deger": max_deger,
    }


def istatistikleri_yazdir(goruntu_adi: str, istatistikler: Dict[str, float]) -> str:
    """
    Soru 2b: Hesaplanan görüntü istatistiklerini düzenli tablo formatında ekrana yazdırır
    ve raporlama için metin olarak döndürür.

    Parametreler:
        goruntu_adi (str): İncelenen görüntünün adı veya açıklaması.
        istatistikler (Dict[str, float]): goruntu_istatistikleri_hesapla() çıktısı.

    Döndürür:
        str: Biçimlendirilmiş istatistik metni.
    """
    satirlar = [
        f"=== Görüntü İstatistikleri: {goruntu_adi} ===",
        f"  • Ortalama (Mean)                : {istatistikler['ortalama']:.4f}",
        f"  • Standart Sapma (Std Deviation) : {istatistikler['standart_sapma']:.4f}",
        f"  • Entropi (Shannon Entropy, bit) : {istatistikler['entropi']:.4f}",
        f"  • Minimum Piksel Değeri          : {int(istatistikler['min_deger'])}",
        f"  • Maksimum Piksel Değeri         : {int(istatistikler['max_deger'])}",
    ]
    metin = "\n".join(satirlar)
    print(metin)
    return metin


def soru2_gorsellestir(
    test_goruntuleri: Dict[str, np.ndarray],
    cikti_klasoru: str = "outputs/figures",
) -> Dict[str, str]:
    """
    Soru 2 kapsamında hem tekil normal görüntünün histogram+istatistik grafiğini
    hem de dört temel test görüntüsü tipinin (Normal, Düşük Kontrastlı, Koyu, Yüksek Kontrastlı)
    histogram ve istatistik karşılaştırma figürünü oluşturup kaydeder.

    Parametreler:
        test_goruntuleri (Dict[str, np.ndarray]): Test görüntüleri sözlüğü.
        cikti_klasoru (str): Figürlerin kaydedileceği klasör yolu.

    Döndürür:
        Dict[str, str]: Kaydedilen figür yolları.
    """
    os.makedirs(cikti_klasoru, exist_ok=True)

    # 1. Normal görüntü için detaylı histogram ve istatistik özeti
    normal_img = test_goruntuleri["normal_goruntu"]
    tekil_yol = os.path.join(cikti_klasoru, "soru2_histogram_ve_istatistikler.png")
    hist_normal = manuel_histogram_hesapla(normal_img)
    ist_normal = goruntu_istatistikleri_hesapla(normal_img)

    fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.2))
    fig1.suptitle(
        "Soru 2: Manuel Histogram Hesaplama ve Görüntü İstatistikleri Analizi",
        fontsize=14,
        fontweight="bold",
    )

    ax1.imshow(normal_img, cmap="gray", vmin=0, vmax=255)
    ax1.set_title(
        f"Orijinal Gri Seviye Görüntü ({normal_img.shape[1]}x{normal_img.shape[0]})",
        fontsize=11,
        fontweight="bold",
    )
    ax1.set_xlabel("X Koordinatı (Piksel)", fontsize=9.5)
    ax1.set_ylabel("Y Koordinatı (Piksel)", fontsize=9.5)

    histogram_eksen_ciz(ax2, hist_normal, baslik="Manuel Hesaplanan Histogram Grafiği")
    ax2.axvline(
        ist_normal["ortalama"],
        color="#d62828",
        linestyle="--",
        linewidth=1.6,
        label=f"Ortalama (μ = {ist_normal['ortalama']:.2f})",
    )
    bilgi_kutusu = (
        f"Ortalama (μ) : {ist_normal['ortalama']:.2f}\n"
        f"Std. Sapma (σ): {ist_normal['standart_sapma']:.2f}\n"
        f"Entropi (H)   : {ist_normal['entropi']:.4f} bit\n"
        f"Min / Max     : {ist_normal['min_deger']} / {ist_normal['max_deger']}"
    )
    ax2.text(
        0.97,
        0.95,
        bilgi_kutusu,
        transform=ax2.transAxes,
        fontsize=9.5,
        verticalalignment="top",
        horizontalalignment="right",
        bbox={"boxstyle": "round,pad=0.5", "facecolor": "#f8f9fa", "edgecolor": "#adb5bd"},
    )
    ax2.legend(loc="upper left", fontsize=9)

    fig1.tight_layout()
    fig1.savefig(tekil_yol, dpi=150, bbox_inches="tight")
    plt.close(fig1)

    # 2. Dört önerilen test görüntüsü tipinin histogram ve istatistik karşılaştırması (4x2 subplot)
    fig2, eksenler = plt.subplots(4, 2, figsize=(14, 16))
    fig2.suptitle(
        "Soru 2: Dört Farklı Test Görüntüsü Tipinin Histogram ve İstatistik Karşılaştırması",
        fontsize=14,
        fontweight="bold",
        y=0.995,
    )

    goruntu_tipleri = [
        ("normal_goruntu", "Normal Görüntü (Genel Testler)", "#1f77b4"),
        ("dusuk_kontrast", "Düşük Kontrastlı Görüntü (Kontrast Germe İçin)", "#ff7f0e"),
        ("koyu_goruntu", "Koyu Görüntü (Histogram Eşitleme İçin)", "#2ca02c"),
        ("yuksek_kontrast", "Yüksek Kontrastlı Görüntü (Dayanıklılık Testi)", "#9467bd"),
    ]

    for satir_idx, (anahtar, etiket, renk) in enumerate(goruntu_tipleri):
        img = test_goruntuleri[anahtar]
        hist = manuel_histogram_hesapla(img)
        ist = goruntu_istatistikleri_hesapla(img)

        ax_sol = eksenler[satir_idx, 0]
        ax_sag = eksenler[satir_idx, 1]

        ax_sol.imshow(img, cmap="gray", vmin=0, vmax=255)
        ax_sol.set_title(etiket, fontsize=11, fontweight="bold")
        ax_sol.set_xlabel("X Koordinatı (Piksel)", fontsize=9)
        ax_sol.set_ylabel("Y Koordinatı (Piksel)", fontsize=9)

        histogram_eksen_ciz(
            ax_sag,
            hist,
            baslik=(
                f"Histogram — μ:{ist['ortalama']:.1f}, σ:{ist['standart_sapma']:.1f}, "
                f"H:{ist['entropi']:.2f} bit, Min/Max:[{ist['min_deger']},{ist['max_deger']}]"
            ),
            renk=renk,
        )

    fig2.tight_layout()
    coklu_yol = os.path.join(cikti_klasoru, "soru2_dort_goruntu_tipi_histogram_analizi.png")
    fig2.savefig(coklu_yol, dpi=150, bbox_inches="tight")
    plt.close(fig2)

    return {
        "tekil": tekil_yol,
        "coklu": coklu_yol,
    }
