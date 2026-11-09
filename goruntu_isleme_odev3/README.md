# Görüntü İşleme 3. Ödevi — Nokta İşlemleri ve Histogram İşleme

**Ders:** Yapay Zeka Mühendisliği — Görüntü İşleme  
**Öğretim Üyesi:** Dr. Öğr. Üyesi Ramin Abbaszadi  
**Konu:** Nokta İşlemleri ve Histogram İşleme

---

## 1. Ödev Kapsamı ve Teknik Gereksinimlere Uyum

Bu ödevde görüntü işlemenin temel konuları olan **nokta işlemleri** ve **histogram işleme** teknikleri Python kullanılarak sıfırdan gerçeklenmiştir:

1. **Her soru için ayrı fonksiyon:** Soru 1–5 ve alt şıklarının tamamı `src/` dizini altında ayrı modül ve fonksiyonlar olarak yazılmıştır.
2. **Açıklayıcı `docstring` ve yorumlar:** Tüm fonksiyonlarda matematiksel formülleri, parametreleri ve dönüş değerlerini açıklayan `docstring` ve kod içi yorumlar yer almaktadır.
3. **NumPy Array İşlemleri (`for` döngüsüz):** Hesaplamaların tamamında piksel düzeyinde `for` döngülerinden kaçınılmış, vektörize `NumPy` dizi işlemleri kullanılmıştır.
4. **Sıfırdan İmplementasyon:** Histogram hesaplama ve histogram eşitleme işlemlerinde `cv2.calcHist()` veya `cv2.equalizeHist()` gibi hazır fonksiyonlar kullanılmamış, algoritmalar sıfırdan implement edilmiştir.
5. **Görselleştirme Standartları:** Tüm grafik ve subplot çıktılarında başlık ve X/Y eksen etiketleri eksiksiz olarak eklenmiştir.

---

## 2. Dosya ve Klasör Yapısı

```text
goruntu_isleme_odev3/
├── main.py                              # Tüm soruları (Soru 1–5) sırasıyla çalıştıran ana betik
├── README.md                            # Proje dokümantasyonu, kullanım kılavuzu ve sonuç özeti
├── RAPOR.md                             # Detaylı ödev raporu (İstatistik tabloları ve Soru 5b analizi)
├── Rapor.pdf                            # Görselleri, istatistikleri ve analizleri içeren PDF rapor
├── requirements.txt                     # Gerekli Python kütüphaneleri
├── src/
│   ├── __init__.py
│   ├── soru1_nokta_islemleri.py         # Soru 1: Parlaklık, kontrast, negatif alma, eşikleme (25 Puan)
│   ├── soru2_histogram_analizi.py       # Soru 2: Manuel histogram ve görüntü istatistikleri (20 Puan)
│   ├── soru3_kontrast_germe.py          # Soru 3: Manuel kontrast germe ve 2x2 subplot (15 Puan)
│   ├── soru4_histogram_esitleme.py      # Soru 4: Sıfırdan histogram eşitleme ve 2x2 subplot (25 Puan)
│   ├── soru5_gamma_duzeltmesi.py        # Soru 5: Gamma düzeltmesi ve gamma analizi (15 Puan)
│   └── test_goruntuleri.py              # Test görüntülerini hazırlama ve okuma/yazma modülü
├── data/
│   └── test_images/                     # Test görüntüleri (normal, düşük kontrastlı, koyu, yüksek kontrastlı, sentetik)
└── outputs/
    ├── istatistik_ve_analiz_raporu.txt  # Ekrana yazdırılan istatistiklerin ve gamma analizinin metin çıktısı
    └── figures/                         # Soru 1–5 için üretilen tüm görselleştirme çıktıları (PNG)
```

---

## 3. Kurulum ve Çalıştırma

### Kurulum
```bash
pip install numpy matplotlib pillow opencv-python
```

### Çalıştırma
Tüm soruları varsayılan parametrelerle çalıştırmak, istatistikleri ekrana yazdırmak ve görselleri `outputs/figures/` klasörüne kaydetmek için:
```bash
python main.py
```

Soru 1 parametrelerini (parlaklık sabiti, kontrast faktörü, eşik değeri) kullanıcıdan interaktif olarak almak için:
```bash
python main.py --interaktif
```

veya komut satırı argümanlarıyla çalıştırmak için:
```bash
python main.py --parlaklik 50 --kontrast 1.5 --esik 128
```

---

## 4. Sorular, Uygulanan Formüller ve Sonuçlar

### Soru 1: Temel Nokta İşlemleri (25 Puan) — `src/soru1_nokta_islemleri.py`
- **a) Parlaklık ayarlama (`parlaklik_ayarla`):** $\text{output} = \text{clip}(\text{input} + b, 0, 255)$
- **b) Kontrast ayarlama (`kontrast_ayarla`):** $\text{output} = \text{clip}(\text{factor} \times (\text{input} - 128) + 128, 0, 255)$
- **c) Görüntü negatif alma (`goruntu_negatifi_al`):** $\text{output} = 255 - \text{input}$
- **d) Eşikleme (`esikleme_uygula`):** $\text{output} = 255 \text{ (eğer } \text{input} > T\text{)}, \text{ aksi halde } 0$
- **Görsel Çıktı:** `outputs/figures/soru1_nokta_islemleri_yan_yana.png`

---

### Soru 2: Histogram Analizi ve Görselleştirme (20 Puan) — `src/soru2_histogram_analizi.py`
- **a) Manuel Histogram (`manuel_histogram_hesapla`, `histogram_ciz`):** Hazır fonksiyon kullanılmadan her gri seviyenin ($0-255$) frekansı $n_k$ vektörize olarak hesaplanmış ve çizdirilmiştir.
- **b) Görüntü İstatistikleri (`goruntu_istatistikleri_hesapla`):**

| Görüntü | Ortalama (Mean) | Standart Sapma (Std) | Entropi (bit) | Min | Max |
|---|---:|---:|---:|---:|---:|
| Normal Görüntü (`normal_goruntu`) | 124.1990 | 47.8996 | 7.4505 | 20 | 245 |
| Düşük Kontrastlı (`dusuk_kontrast`) | 122.7864 | 12.7847 | 5.5419 | 95 | 155 |
| Koyu Görüntü (`koyu_goruntu`) | 23.4577 | 14.4147 | 5.3214 | 8 | 88 |
| Yüksek Kontrastlı (`yuksek_kontrast`) | 116.2227 | 97.4824 | 5.0144 | 0 | 255 |
| Sentetik Düşük Kontrast (`sentetik_dusuk_kontrast`) | 124.4375 | 14.3935 | 5.6433 | 100 | 149 |

- **Görsel Çıktılar:** `outputs/figures/soru2_histogram_ve_istatistikler.png`, `outputs/figures/soru2_dort_goruntu_tipi_histogram_analizi.png`

---

### Soru 3: Kontrast Germe (15 Puan) — `src/soru3_kontrast_germe.py`
- **a) Manuel Kontrast Germe (`manuel_kontrast_germe`):** $\text{output} = \frac{\text{input} - \min}{\max - \min} \times 255$
- Düşük kontrastlı görüntünün `[95, 155]` olan piksel aralığı `[0, 255]` tam dinamik aralığına genişletilmiş, standart sapması `12.78`'den `54.28`'e yükselmiştir.
- **b) Görselleştirme (2x2 subplot):** `outputs/figures/soru3_kontrast_germe_2x2.png`

---

### Soru 4: Histogram Eşitleme (25 Puan) — `src/soru4_histogram_esitleme.py`
- **a) Sıfırdan Histogram Eşitleme (`manuel_histogram_esitleme`):**
  1. Görüntünün manuel histogramı ($n_j$) hesaplanır.
  2. Normalize kümülatif histogram ($\text{CDF}_k = \sum_{j=0}^{k} \frac{n_j}{MN}$) hesaplanır.
  3. Dönüşüm fonksiyonu oluşturulur: $s_k = (L - 1) \sum_{j=0}^{k} \frac{n_j}{MN}$ ($L = 256$).
  4. Tüm pikseller dönüşüm tablosu ile yeni değerlerine eşlenir.
- **b) Karşılaştırma (2x2 subplot):** `outputs/figures/soru4_histogram_esitleme_2x2.png`

---

### Soru 5: Gamma Düzeltmesi (15 Puan) — `src/soru5_gamma_duzeltmesi.py`
- **a) Gamma Düzeltme Fonksiyonu (`gamma_duzeltmesi`):** $\text{output} = 255 \times (\text{input} / 255)^\gamma$
- **Görsel Çıktılar:** `outputs/figures/soru5_gamma_duzeltmesi_karsilastirma.png`, `outputs/figures/soru5_gamma_donusum_egrileri.png`
- **b) Analiz:**

| Gamma ($\gamma$) | Ortalama | Std. Sapma | Entropi (bit) | Min / Max | Görüntü Üzerindeki Etkisi |
|---:|---:|---:|---:|---:|---|
| **0.5** | 174.16 | 36.58 | 6.9443 | 71 / 250 | Karanlık pikselleri genişletir, genel parlaklığı artırır ve gölgedeki detayları belirginleştirir. |
| **1.0** | 124.20 | 47.90 | 7.4505 | 20 / 245 | Birim dönüşümdür ($\text{output} = \text{input}$); görüntüyü değiştirmez. |
| **1.5** | 91.64 | 49.29 | 7.2899 | 6 / 240 | Orta düzeyde karartma uygular, parlak bölgelerdeki kontrastı artırır. |
| **2.0** | 69.46 | 46.88 | 7.0837 | 2 / 235 | Belirgin karartma sağlar; ağarmış (washed-out) parlak bölgelerdeki detayları ayrıştırır. |
| **2.5** | 53.83 | 43.22 | 6.8248 | 0 / 231 | Güçlü karartma uygular; karanlık ve orta tonları bastırıp yalnızca en parlak detayları korur. |

- **Hangi durumda hangi gamma değeri kullanılmalı?**
  - **$\gamma < 1$ (örn. $\gamma = 0.5$):** Az pozlanmış (underexposed), gece çekimi veya kapalı ortamda çekilmiş **karanlık görüntülerde** karanlık bölgelerdeki detayları ortaya çıkarmak için kullanılmalıdır.
  - **$\gamma = 1.0$:** Aydınlatması dengeli olan görüntülerde orijinal durumu korumak için kullanılır.
  - **$\gamma > 1$ (örn. $\gamma = 1.5, 2.0, 2.5$):** Aşırı pozlanmış (overexposed), yoğun ışık altında çekilmiş veya soluk/ağarmış **parlak görüntülerde** parlak bölgelerdeki kontrastı ve detayları geri kazanmak için kullanılmalıdır.
