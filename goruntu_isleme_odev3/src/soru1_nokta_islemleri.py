"""
Soru 1: Temel Nokta İşlemleri (25 Puan) Modülü.

Bu modül, bir görüntü üzerinde aşağıdaki nokta işlemlerini vektörize NumPy dizi
işlemleriyle (for döngüsü kullanmadan) uygulayan fonksiyonları içerir:
a) Parlaklık ayarlama fonksiyonu (7 puan) — 0-255 taşma (overflow) kontrollü
b) Kontrast ayarlama fonksiyonu (8 puan) — output = factor * (input - 128) + 128, taşma kontrollü
c) Görüntü negatif alma fonksiyonu (5 puan) — output = 255 - input
d) Eşikleme (Thresholding) fonksiyonu (5 puan) — eşik üstü 255, diğerleri 0
"""

import os
from typing import Dict, Optional
import numpy as np
import matplotlib.pyplot as plt


def parlaklik_ayarla(goruntu: np.ndarray, sabit_deger: Optional[float] = None) -> np.ndarray:
    """
    Soru 1a (7 Puan): Görüntünün tüm piksellerine sabit bir değer ekleyerek veya çıkararak
    parlaklığı ayarlar ve [0, 255] aralığında taşma (overflow/underflow) kontrolü yapar.

    Matematiksel Formül:
        output(x, y) = clip(input(x, y) + sabit_deger, 0, 255)

    Parametreler:
        goruntu (np.ndarray): Giriş görüntüsü (uint8, 0-255 aralığında NumPy dizisi).
        sabit_deger (Optional[float]): Eklenecek (pozitif) veya çıkarılacak (negatif) sabit değer.
            None verilirse kullanıcıdan konsol üzerinden alınır.

    Döndürür:
        np.ndarray: Parlaklığı ayarlanmış, [0, 255] aralığında uint8 görüntü matrisi.
    """
    if sabit_deger is None:
        girilen = input("Parlaklık için sabit değer girin (örn. +50 veya -40): ").strip()
        sabit_deger = float(girilen) if girilen else 50.0

    # uint8 taşmasını (modulo 256 sarmalanmasını) önlemek için önce float64 tipine dönüştürüyoruz
    goruntu_float = goruntu.astype(np.float64)

    # Vektörize NumPy toplama işlemi ve [0, 255] aralığına kırpma (overflow kontrolü)
    islenmis = np.clip(np.round(goruntu_float + float(sabit_deger)), 0, 255)
    return islenmis.astype(np.uint8)


def kontrast_ayarla(goruntu: np.ndarray, faktor: Optional[float] = None) -> np.ndarray:
    """
    Soru 1b (8 Puan): Verilen kontrast faktörüne göre görüntünün kontrastını ayarlar
    ve [0, 255] aralığında taşma (overflow) kontrolü uygular.

    Matematiksel Formül:
        output = factor * (input - 128) + 128

    Parametreler:
        goruntu (np.ndarray): Giriş görüntüsü (uint8 NumPy dizisi).
        faktor (Optional[float]): Kontrast çarpanı (örn. 1.5 kontrastı artırır, 0.5 azaltır).
            None verilirse kullanıcıdan konsol üzerinden alınır.

    Döndürür:
        np.ndarray: Kontrastı ayarlanmış, [0, 255] aralığında uint8 görüntü matrisi.
    """
    if faktor is None:
        girilen = input("Kontrast faktörü girin (örn. 1.5): ").strip()
        faktor = float(girilen) if girilen else 1.5

    if faktor < 0:
        raise ValueError("Kontrast faktörü negatif olamaz.")

    # Orta gri değeri (128) merkez alarak doğrusal kontrast ölçekleme formülünü uyguluyoruz
    goruntu_float = goruntu.astype(np.float64)
    sonuc = float(faktor) * (goruntu_float - 128.0) + 128.0

    # Taşma (overflow/underflow) kontrolü ile pikselleri [0, 255] aralığında tutuyoruz
    return np.clip(np.round(sonuc), 0, 255).astype(np.uint8)


def goruntu_negatifi_al(goruntu: np.ndarray) -> np.ndarray:
    """
    Soru 1c (5 Puan): 8-bit gri seviye görüntünün negatifini hesaplar.

    Matematiksel Formül:
        output = 255 - input

    Parametreler:
        goruntu (np.ndarray): Giriş görüntüsü (uint8 NumPy dizisi).

    Döndürür:
        np.ndarray: Negatifi alınmış uint8 görüntü matrisi.
    """
    # Vektörize çıkarma işlemiyle tüm pikselleri 255'ten çıkarıyoruz
    sonuc = 255 - goruntu.astype(np.int32)
    return np.clip(sonuc, 0, 255).astype(np.uint8)


def esikleme_uygula(goruntu: np.ndarray, esik_degeri: Optional[int] = None) -> np.ndarray:
    """
    Soru 1d (5 Puan): Verilen eşik (threshold) değerine göre görüntüyü ikili (binary)
    görüntüye dönüştürür. Eşik değerinden büyük pikseller 255, küçük veya eşit olanlar 0 yapılır.

    Matematiksel Formül:
        output(x, y) = 255  eğer input(x, y) > T
        output(x, y) = 0    eğer input(x, y) <= T

    Parametreler:
        goruntu (np.ndarray): Giriş görüntüsü (uint8 NumPy dizisi).
        esik_degeri (Optional[int]): Eşik değeri T (0-255 arası). None ise kullanıcıdan alınır.

    Döndürür:
        np.ndarray: Yalnızca 0 ve 255 değerlerinden oluşan uint8 ikili görüntü matrisi.
    """
    if esik_degeri is None:
        girilen = input("Eşik (threshold) değeri girin (0-255, örn. 128): ").strip()
        esik_degeri = int(girilen) if girilen else 128

    if not (0 <= int(esik_degeri) <= 255):
        raise ValueError("Eşik değeri 0 ile 255 arasında olmalıdır.")

    # np.where ile for döngüsü kullanmadan tüm pikselleri eşik değeriyle karşılaştırıyoruz
    return np.where(goruntu > int(esik_degeri), 255, 0).astype(np.uint8)


def soru1_tum_islemleri_uygula(
    goruntu: np.ndarray,
    parlaklik_artir: float = 50.0,
    parlaklik_azalt: float = -50.0,
    kontrast_artir: float = 1.5,
    kontrast_azalt: float = 0.6,
    esik_degeri: int = 128,
) -> Dict[str, np.ndarray]:
    """
    Soru 1'deki tüm nokta işlemlerini verilen görüntü üzerinde çalıştırır ve sonuçları döndürür.

    Parametreler:
        goruntu (np.ndarray): Giriş gri seviye görüntüsü.
        parlaklik_artir (float): Pozitif parlaklık değişim değeri (varsayılan: +50).
        parlaklik_azalt (float): Negatif parlaklık değişim değeri (varsayılan: -50).
        kontrast_artir (float): Kontrast artırma çarpanı (varsayılan: 1.5).
        kontrast_azalt (float): Kontrast azaltma çarpanı (varsayılan: 0.6).
        esik_degeri (int): Eşikleme değeri (varsayılan: 128).

    Döndürür:
        Dict[str, np.ndarray]: İşlem adı -> çıktı görüntüsü sözlüğü.
    """
    return {
        "orijinal": goruntu,
        "parlaklik_artirma": parlaklik_ayarla(goruntu, parlaklik_artir),
        "parlaklik_azaltma": parlaklik_ayarla(goruntu, parlaklik_azalt),
        "kontrast_artirma": kontrast_ayarla(goruntu, kontrast_artir),
        "kontrast_azaltma": kontrast_ayarla(goruntu, kontrast_azalt),
        "negatif": goruntu_negatifi_al(goruntu),
        "esikleme": esikleme_uygula(goruntu, esik_degeri),
    }


def soru1_gorsellestir(
    goruntu: np.ndarray,
    cikti_klasoru: str = "outputs/figures",
    parlaklik_degeri: float = 50.0,
    kontrast_faktoru: float = 1.5,
    esik_degeri: int = 128,
) -> Dict[str, str]:
    """
    Soru 1'in beklenen çıktısını (Orijinal görüntü ve her işlem sonrası görüntülerin yan yana
    gösterimi) ve detaylı karşılaştırma figürünü oluşturup kaydeder.

    Parametreler:
        goruntu (np.ndarray): Giriş gri seviye görüntüsü.
        cikti_klasoru (str): Figürlerin kaydedileceği klasör yolu.
        parlaklik_degeri (float): Parlaklık ayarlama sabiti (varsayılan: +50).
        kontrast_faktoru (float): Kontrast faktörü (varsayılan: 1.5).
        esik_degeri (int): Eşik değeri (varsayılan: 128).

    Döndürür:
        Dict[str, str]: Oluşturulan figür anahtarları ve dosya yolları.
    """
    os.makedirs(cikti_klasoru, exist_ok=True)
    sonuclar = soru1_tum_islemleri_uygula(
        goruntu,
        parlaklik_artir=parlaklik_degeri,
        parlaklik_azalt=-abs(parlaklik_degeri),
        kontrast_artir=kontrast_faktoru,
        kontrast_azalt=0.6,
        esik_degeri=esik_degeri,
    )

    # 1. Beklenen Çıktı: Orijinal görüntü ve 4 temel işlem yan yana (1x5 subplot)
    fig1, eksenler1 = plt.subplots(1, 5, figsize=(22, 4.8))
    fig1.suptitle(
        "Soru 1: Temel Nokta İşlemleri — Orijinal ve İşlenmiş Görüntülerin Yan Yana Karşılaştırması",
        fontsize=14,
        fontweight="bold",
        y=1.02,
    )

    yan_yana_listesi = [
        (sonuclar["orijinal"], "Orijinal Görüntü"),
        (sonuclar["parlaklik_artirma"], f"a) Parlaklık Ayarlama (+{int(parlaklik_degeri)})"),
        (sonuclar["kontrast_artirma"], f"b) Kontrast Ayarlama (k={kontrast_faktoru})"),
        (sonuclar["negatif"], "c) Görüntü Negatifi (255 - I)"),
        (sonuclar["esikleme"], f"d) Eşikleme (T={esik_degeri})"),
    ]

    for ax, (img, baslik) in zip(eksenler1, yan_yana_listesi):
        ax.imshow(img, cmap="gray", vmin=0, vmax=255)
        ax.set_title(
            f"{baslik}\n[Min:{int(np.min(img))}, Max:{int(np.max(img))}, Ort:{np.mean(img):.1f}]",
            fontsize=10.5,
            fontweight="bold",
        )
        ax.set_xlabel("X Koordinatı (Piksel)", fontsize=9)
        ax.set_ylabel("Y Koordinatı (Piksel)", fontsize=9)

    fig1.tight_layout()
    yan_yana_yol = os.path.join(cikti_klasoru, "soru1_nokta_islemleri_yan_yana.png")
    fig1.savefig(yan_yana_yol, dpi=150, bbox_inches="tight")
    plt.close(fig1)

    # 2. Detaylı Varyasyon Figürü: Artırma ve azaltma etkilerinin birlikte gösterimi (2x4 subplot)
    fig2, eksenler2 = plt.subplots(2, 4, figsize=(18, 9))
    fig2.suptitle(
        "Soru 1: Temel Nokta İşlemleri — Pozitif/Negatif Parlaklık ve Düşük/Yüksek Kontrast Analizi",
        fontsize=14,
        fontweight="bold",
    )

    detay_listesi = [
        (sonuclar["orijinal"], "Orijinal Görüntü"),
        (sonuclar["parlaklik_artirma"], f"Parlaklık Artırma (+{int(parlaklik_degeri)})"),
        (sonuclar["parlaklik_azaltma"], f"Parlaklık Azaltma (-{int(abs(parlaklik_degeri))})"),
        (sonuclar["negatif"], "Negatif Görüntü (255 - I)"),
        (sonuclar["kontrast_artirma"], f"Kontrast Artırma (k={kontrast_faktoru})"),
        (sonuclar["kontrast_azaltma"], "Kontrast Azaltma (k=0.6)"),
        (sonuclar["esikleme"], f"Eşikleme (T={esik_degeri})"),
        (esikleme_uygula(goruntu, 90), "Eşikleme (T=90)"),
    ]

    for ax, (img, baslik) in zip(eksenler2.ravel(), detay_listesi):
        ax.imshow(img, cmap="gray", vmin=0, vmax=255)
        ax.set_title(
            f"{baslik}\n[Min:{int(np.min(img))}, Max:{int(np.max(img))}, Ort:{np.mean(img):.1f}]",
            fontsize=10,
            fontweight="bold",
        )
        ax.set_xlabel("X Koordinatı (Piksel)", fontsize=9)
        ax.set_ylabel("Y Koordinatı (Piksel)", fontsize=9)

    fig2.tight_layout()
    detay_yol = os.path.join(cikti_klasoru, "soru1_nokta_islemleri_detayli.png")
    fig2.savefig(detay_yol, dpi=150, bbox_inches="tight")
    plt.close(fig2)

    return {
        "yan_yana": yan_yana_yol,
        "detayli": detay_yol,
    }
