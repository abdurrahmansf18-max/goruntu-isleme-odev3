"""
Test Görüntüleri Hazırlama ve Okuma/Yazma Modülü.

Ödev belgesinde önerilen dört temel test görüntüsü tipini (normal, düşük kontrastlı,
koyu ve yüksek kontrastlı) ve Seçenek 3'teki sentetik düşük kontrastlı görüntüyü
hazırlar, kaydeder ve gri seviye NumPy dizisi olarak yükler.
"""

import os
import urllib.request
from typing import Dict
import numpy as np
from PIL import Image


def goruntu_oku_gri(dosya_yolu: str) -> np.ndarray:
    """
    Verilen dosya yolundaki görüntüyü gri seviye (8-bit, 0-255) NumPy dizisi olarak okur.

    Parametreler:
        dosya_yolu (str): Okunacak görüntü dosyasının yolu.

    Döndürür:
        np.ndarray: (H, W) boyutlarında, uint8 veri tipinde gri seviye görüntü matrisi.
    """
    if not os.path.exists(dosya_yolu):
        raise FileNotFoundError(f"Görüntü dosyası bulunamadı: {dosya_yolu}")

    # PIL Image ile görüntüyü açıp 'L' (8-bit gri seviye) moduna dönüştürüyoruz
    with Image.open(dosya_yolu) as img:
        gri_img = img.convert("L")
        return np.array(gri_img, dtype=np.uint8)


def goruntu_kaydet_gri(goruntu: np.ndarray, dosya_yolu: str) -> None:
    """
    Gri seviye NumPy dizisini belirtilen dosya yoluna görüntü olarak kaydeder.

    Parametreler:
        goruntu (np.ndarray): Kaydedilecek (H, W) boyutlu görüntü dizisi.
        dosya_yolu (str): Kaydedilecek hedef dosya yolu.
    """
    os.makedirs(os.path.dirname(os.path.abspath(dosya_yolu)), exist_ok=True)
    # Taşma kontrolü ile [0, 255] uint8 formatını garanti altına alıyoruz
    temiz_goruntu = np.clip(goruntu, 0, 255).astype(np.uint8)
    Image.fromarray(temiz_goruntu, mode="L").save(dosya_yolu)


def sentetik_temel_sahne_olustur(boyut: int = 512) -> np.ndarray:
    """
    İnternet bağlantısı olmadığında bile zengin frekans ve ton dağılımı sunan,
    tamamen vektörize NumPy dizi işlemleriyle oluşturulmuş test sahnesi üretir.

    Parametreler:
        boyut (int): Kare görüntünün kenar uzunluğu (varsayılan: 512).

    Döndürür:
        np.ndarray: (boyut, boyut) şeklinde uint8 gri seviye sahne görüntüsü.
    """
    # Koordinat ızgaralarını for döngüsü kullanmadan np.linspace ve np.meshgrid ile üretiyoruz
    eksen = np.linspace(-1.0, 1.0, boyut, dtype=np.float64)
    x, y = np.meshgrid(eksen, eksen)
    r = np.sqrt(x ** 2 + y ** 2)

    # Yumuşak arka plan gradyanı ve sinüzoidal doku bileşeni
    arka_plan = 120.0 + 45.0 * x + 35.0 * y
    doku = 22.0 * np.sin(8.0 * np.pi * x) * np.cos(8.0 * np.pi * y)

    # Geometrik nesneler (halkalar, parlak disk, koyu gölge bölgesi ve dama deseni)
    dis_halka = np.where((r >= 0.38) & (r <= 0.68), 45.0 * np.cos(18.0 * r), 0.0)
    ic_parlak_daire = np.where(r < 0.28, 70.0 * (1.0 - (r / 0.28) ** 2), 0.0)
    koyu_dikdortgen = np.where((x > -0.82) & (x < -0.35) & (y > 0.30) & (y < 0.80), -65.0, 0.0)
    parlak_dikdortgen = np.where((x > 0.32) & (x < 0.82) & (y < -0.30) & (y > -0.82), 60.0, 0.0)

    # İnce detay testi için dama tahtası bölgesi
    dama_maskesi = (x > 0.30) & (x < 0.82) & (y > 0.30) & (y < 0.82)
    dama_degeri = np.where(
        ((np.floor((x + 1.0) * 16.0) + np.floor((y + 1.0) * 16.0)) % 2) == 0,
        40.0,
        -40.0,
    )
    dama_katmani = np.where(dama_maskesi, dama_degeri, 0.0)

    # Sabit tohumlu hafif Gauss gürültüsü ile gerçekçi sensör dokusu ekleme
    rng = np.random.default_rng(42)
    gurultu = rng.normal(0.0, 4.0, size=(boyut, boyut))

    birlesik = (
        arka_plan
        + doku
        + dis_halka
        + ic_parlak_daire
        + koyu_dikdortgen
        + parlak_dikdortgen
        + dama_katmani
        + gurultu
    )
    return np.clip(np.round(birlesik), 0, 255).astype(np.uint8)


def klasik_referans_goruntu_getir(hedef_klasor: str) -> np.ndarray:
    """
    Klasik test görüntüsünü (Lena) çevrim içi kaynaktan indirir veya mevcutsa diskten okur;
    çevrim dışı ortamda ise zengin sentetik sahneye geri döner.

    Parametreler:
        hedef_klasor (str): Görüntülerin saklanacağı klasör yolu.

    Döndürür:
        np.ndarray: 512x512 boyutunda uint8 gri seviye referans görüntü.
    """
    os.makedirs(hedef_klasor, exist_ok=True)
    normal_yol = os.path.join(hedef_klasor, "normal_goruntu.png")

    if os.path.exists(normal_yol):
        return goruntu_oku_gri(normal_yol)

    # OpenCV resmi deposundaki standart Lena görüntüsünü indirmeyi dener
    url = "https://raw.githubusercontent.com/opencv/opencv/master/samples/data/lena.jpg"
    try:
        istek = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(istek, timeout=6) as yanit:
            veri = yanit.read()
        gecici_yol = os.path.join(hedef_klasor, "_ham_referans.jpg")
        with open(gecici_yol, "wb") as f:
            f.write(veri)
        referans = goruntu_oku_gri(gecici_yol)
        os.remove(gecici_yol)
    except Exception:
        # Çevrim dışıysa deterministik zengin sahne üretir
        referans = sentetik_temel_sahne_olustur(512)

    goruntu_kaydet_gri(referans, normal_yol)
    return referans


def test_goruntulerini_hazirla(hedef_klasor: str = "data/test_images") -> Dict[str, np.ndarray]:
    """
    Ödevde önerilen tüm test görüntüsü tiplerini oluşturur, diske kaydeder ve sözlük olarak döndürür:
    1. normal_goruntu: Genel testler için standart dinamik aralıklı görüntü
    2. dusuk_kontrast: Kontrast germe için [95, 155] aralığına sıkıştırılmış düşük kontrastlı görüntü
    3. koyu_goruntu: Histogram eşitleme için düşük parlaklık [10, 85] bölgesine yığılmış koyu görüntü
    4. yuksek_kontrast: Algoritmaların dayanıklılığını test için uç değerlere çekilmiş görüntü
    5. sentetik_dusuk_kontrast: Ödev Seçenek 3'teki np.random.randint(100, 150, (256, 256)) görüntüsü

    Parametreler:
        hedef_klasor (str): Test görüntülerinin kaydedileceği dizin yolu.

    Döndürür:
        Dict[str, np.ndarray]: Görüntü adı -> gri seviye NumPy matrisi eşleşmesi.
    """
    os.makedirs(hedef_klasor, exist_ok=True)

    # 1. Normal görüntü (Genel testler için)
    normal = klasik_referans_goruntu_getir(hedef_klasor)
    normal_float = normal.astype(np.float64)
    n_min = float(np.min(normal_float))
    n_max = float(np.max(normal_float))
    norm_0_1 = (normal_float - n_min) / max(n_max - n_min, 1.0)

    # 2. Düşük kontrastlı görüntü (Kontrast germe için: pikseller [95, 155] aralığına sıkıştırılır)
    dusuk_kontrast = np.clip(np.round(95.0 + norm_0_1 * (155.0 - 95.0)), 0, 255).astype(np.uint8)
    goruntu_kaydet_gri(dusuk_kontrast, os.path.join(hedef_klasor, "dusuk_kontrast.png"))

    # 3. Koyu görüntü (Histogram eşitleme için: gamma=2.6 ile koyu bölgeye [8, 88] sıkıştırılır)
    koyu_goruntu = np.clip(np.round(8.0 + (norm_0_1 ** 2.6) * 80.0), 0, 255).astype(np.uint8)
    goruntu_kaydet_gri(koyu_goruntu, os.path.join(hedef_klasor, "koyu_goruntu.png"))

    # 4. Yüksek kontrastlı görüntü (Dayanıklılık testi için: S-eğrisi / güçlü kontrast)
    merkezli = (norm_0_1 - 0.5) * 2.8
    yuksek_kontrast = np.clip(np.round((merkezli + 0.5) * 255.0), 0, 255).astype(np.uint8)
    goruntu_kaydet_gri(yuksek_kontrast, os.path.join(hedef_klasor, "yuksek_kontrast.png"))

    # 5. Ödev Seçenek 3'te verilen Python ile sentetik düşük kontrastlı test görüntüsü
    np.random.seed(42)
    sentetik_dusuk_kontrast = np.random.randint(100, 150, (256, 256), dtype=np.uint8)
    goruntu_kaydet_gri(
        sentetik_dusuk_kontrast,
        os.path.join(hedef_klasor, "sentetik_dusuk_kontrast.png"),
    )

    return {
        "normal_goruntu": normal,
        "dusuk_kontrast": dusuk_kontrast,
        "koyu_goruntu": koyu_goruntu,
        "yuksek_kontrast": yuksek_kontrast,
        "sentetik_dusuk_kontrast": sentetik_dusuk_kontrast,
    }
