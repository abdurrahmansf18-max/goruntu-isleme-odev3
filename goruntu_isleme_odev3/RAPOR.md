# Görüntü İşleme 3. Ödevi — Teknik Analiz ve Deneysel Sonuç Raporu

**Ders:** Yapay Zeka Mühendisliği — Görüntü İşleme  
**Öğretim Üyesi:** Dr. Öğr. Üyesi Ramin Abbaszadi  
**Ödev Konusu:** Nokta İşlemleri ve Histogram İşleme  

---

## 1. Giriş ve Yöntem

Bu çalışmada, 8-bit gri seviye görüntüler ($L = 256$, piksel değer aralığı $[0, 255]$) üzerinde uzamsal (spatial) alanda doğrudan piksel yoğunluklarını dönüştüren **nokta işlemleri (point processing)** ve **histogram işleme (histogram processing)** algoritmaları sıfırdan geliştirilmiştir.

Tüm algoritmalar ödevin teknik gereksinimlerine tam uyumlu olarak:
1. Her soru ve alt işlem için ayrı, modüler Python fonksiyonları halinde (`src/` altında) tasarlanmış,
2. Açıklayıcı `docstring` ve adım adım kod içi yorumlarla belgelendirilmiş,
3. Piksel düzeyinde klasik `for` döngüleri yerine vektörize `NumPy` dizi (`ndarray`) işlemleriyle gerçeklenmiş,
4. `cv2.calcHist()` ve `cv2.equalizeHist()` gibi hazır histogram fonksiyonları kullanılmadan matematiksel tanımlarından sıfırdan yazılmıştır.

---

## 2. Soru 1: Temel Nokta İşlemleri Analizi (25 Puan)

### 2.1. Matematiksel Formüller ve Taşma (Overflow) Kontrolü

8-bit görüntülerde aritmetik işlemler sonrasında piksel değerlerinin $0$'ın altına düşmesini (underflow) veya $255$'in üzerine çıkmasını (overflow) engellemek için işlem öncesinde veri tipi `float64`/`int32` uzayına genişletilmiş ve işlem sonunda kırpma (clipping) fonksiyonu uygulanmıştır:

$$\text{clip}(x, 0, 255) = \min(\max(\text{round}(x), 0), 255)$$

1. **a) Parlaklık Ayarlama (7 Puan):**
   $$s(x, y) = \text{clip}(r(x, y) + b, \; 0, \; 255)$$
   Burada $b > 0$ histogramı sağa (parlak bölgeye) kaydırırken, $b < 0$ histogramı sola (karanlık bölgeye) kaydırır.
2. **b) Kontrast Ayarlama (8 Puan):**
   $$s(x, y) = \text{clip}(\text{factor} \times (r(x, y) - 128) + 128, \; 0, \; 255)$$
   Orta gri seviyesi ($128$) sabit merkez alınarak $\text{factor} > 1$ için dinamik aralık genişletilir (kontrast artar), $0 < \text{factor} < 1$ için dinamik aralık merkeze doğru daraltılır (kontrast azalır).
3. **c) Görüntü Negatif Alma (5 Puan):**
   $$s(x, y) = 255 - r(x, y)$$
   Karanlık pikselleri parlak, parlak pikselleri karanlık yaparak histogramı $127.5$ eksenine göre simetrik ters çevirir. Standart sapma ve Shannon entropisi değişmez.
4. **d) Eşikleme / Thresholding (5 Puan):**
   $$s(x, y) = \begin{cases} 255, & r(x, y) > T \\ 0, & r(x, y) \le T \end{cases}$$
   Gri seviye görüntüyü yalnızca $\{0, 255\}$ değerlerinden oluşan ikili (binary) görüntüye indirger; entropi en fazla $1.0\text{ bit}$ olabilir.

### 2.2. Soru 1 Sayısal Sonuçlar Tablosu

| İşlem | Parametre | Ortalama ($\mu$) | Standart Sapma ($\sigma$) | Entropi ($H$, bit) | Min | Max |
|---|---|---:|---:|---:|---:|---:|
| Orijinal Görüntü | — | 124.1990 | 47.8996 | 7.4505 | 20 | 245 |
| Parlaklık Artırma | $b = +50$ | 173.8508 | 47.2662 | 7.2386 | 70 | 255 |
| Parlaklık Azaltma | $b = -50$ | 74.7610 | 46.9572 | 7.0841 | 0 | 195 |
| Kontrast Artırma | $\text{factor} = 1.5$ | 122.3672 | 71.2072 | 7.2449 | 0 | 255 |
| Kontrast Azaltma | $\text{factor} = 0.6$ | 125.7191 | 28.7409 | 6.6510 | 63 | 198 |
| Görüntü Negatifi | $255 - I$ | 130.8010 | 47.8996 | 7.4505 | 10 | 235 |
| Eşikleme (Thresholding) | $T = 128$ | 128.4737 | 127.4963 | 1.0000 | 0 | 255 |

---

## 3. Soru 2: Histogram Analizi ve Görüntü İstatistikleri (20 Puan)

### 3.1. Vektörize Manuel Histogram Hesaplama (`manuel_histogram_hesapla`)

Hazır fonksiyonlar ve `for` döngüleri kullanılmadan, $M \times N$ boyutlu düzleştirilmiş piksel vektörü $\mathbf{r} \in \{0, \dots, 255\}^{MN \times 1}$ ile seviye vektörü $\mathbf{k} = [0, 1, \dots, 255] \in \{0, \dots, 255\}^{1 \times 256}$ arasında `NumPy` broadcasting karşılaştırması yapılarak her gri seviyenin frekansı hesaplanmıştır:

$$h(k) = n_k = \sum_{i=0}^{MN-1} \mathbb{I}(\mathbf{r}_i = k), \quad k \in \{0, 1, \dots, 255\}$$

### 3.2. Görüntü İstatistikleri Formülleri (`goruntu_istatistikleri_hesapla`)

- **Ortalama (Mean):** $\mu = \frac{1}{MN} \sum_{x=0}^{M-1}\sum_{y=0}^{N-1} I(x, y)$
- **Standart Sapma (Standard Deviation):** $\sigma = \sqrt{\frac{1}{MN} \sum_{x=0}^{M-1}\sum_{y=0}^{N-1} (I(x, y) - \mu)^2}$
- **Shannon Entropisi (Entropy):** $p(k) = \frac{n_k}{MN}$ olmak üzere $H = -\sum_{k: p(k) > 0} p(k) \log_2 p(k)$
- **Minimum ve Maksimum:** $I_{\min} = \min(I), \quad I_{\max} = \max(I)$

### 3.3. Test Görüntülerinin İstatistiksel Karşılaştırması

| Test Görüntüsü | Kullanım Amacı | Ortalama ($\mu$) | Std. Sapma ($\sigma$) | Entropi ($H$, bit) | Min | Max |
|---|---|---:|---:|---:|---:|---:|
| `normal_goruntu` | Genel testler | 124.1990 | 47.8996 | 7.4505 | 20 | 245 |
| `dusuk_kontrast` | Kontrast germe | 122.7864 | 12.7847 | 5.5419 | 95 | 155 |
| `koyu_goruntu` | Histogram eşitleme | 23.4577 | 14.4147 | 5.3214 | 8 | 88 |
| `yuksek_kontrast` | Dayanıklılık testi | 116.2227 | 97.4824 | 5.0144 | 0 | 255 |
| `sentetik_dusuk_kontrast` | Seçenek 3 sentetik test | 124.4375 | 14.3935 | 5.6433 | 100 | 149 |

---

## 4. Soru 3: Manuel Kontrast Germe (Contrast Stretching) Analizi (15 Puan)

Dar bir yoğunluk aralığına sıkışmış görüntülerin dinamik aralığını doğrusal olarak $[0, 255]$ aralığına açmak için aşağıdaki dönüşüm uygulanmıştır:

$$\text{output}(x, y) = \left(\frac{\text{input}(x, y) - I_{\min}}{I_{\max} - I_{\min}}\right) \times 255$$

| Görüntü | Durum | Ortalama ($\mu$) | Std. Sapma ($\sigma$) | Entropi ($H$, bit) | Min | Max |
|---|---|---:|---:|---:|---:|---:|
| Doğal Düşük Kontrastlı | İşlem Öncesi | 122.7864 | 12.7847 | 5.5419 | 95 | 155 |
| Doğal Düşük Kontrastlı | **Kontrast Germe Sonrası** | **118.0880** | **54.2817** | **5.5419** | **0** | **255** |
| Sentetik Düşük Kontrastlı | İşlem Öncesi | 124.4375 | 14.3935 | 5.6433 | 100 | 149 |
| Sentetik Düşük Kontrastlı | **Kontrast Germe Sonrası** | **127.1742** | **74.9456** | **5.6433** | **0** | **255** |

**Teknik Yorum:** Doğrusal kontrast germe birebir (one-to-one) ölçekleme yaptığı için piksellerin dinamik aralığını $[0, 255]$'e genişletir ve standart sapmayı ($\sigma$) yaklaşık $4.25$ kat artırarak görsel netliği belirgin biçimde iyileştirir; buna karşılık farklı yoğunluk seviyeleri birleştirilmediğinden **Shannon entropisi ($5.5419\text{ bit}$) birebir korunur**.

---

## 5. Soru 4: Sıfırdan Histogram Eşitleme (Histogram Equalization) Analizi (25 Puan)

Histogram eşitleme algoritması aşağıdaki 5 adımla sıfırdan gerçeklenmiştir:
1. Görüntünün manuel histogramının hesaplanması: $n_j = h(j), \; j \in \{0, \dots, 255\}$
2. Olasılık yoğunluk fonksiyonunun (PDF) hesabı: $p_r(r_j) = \frac{n_j}{MN}$
3. Normalize edilmiş kümülatif histogramın (CDF) hesabı: $C(k) = \sum_{j=0}^{k} \frac{n_j}{MN}$
4. Dönüşüm fonksiyonunun oluşturulması ($L = 256$):
   $$s_k = \text{round}\left((L - 1) \sum_{j=0}^{k} \frac{n_j}{MN}\right) = \text{round}(255 \cdot C(k))$$
5. Vektörize LUT dizinleme (`donusum_fonksiyonu_sk[goruntu]`) ile tüm piksellerin dönüştürülmesi.

| Görüntü | Durum | Ortalama ($\mu$) | Std. Sapma ($\sigma$) | Entropi ($H$, bit) | Min | Max |
|---|---|---:|---:|---:|---:|---:|
| Koyu Görüntü | İşlem Öncesi | 23.4577 | 14.4147 | 5.3214 | 8 | 88 |
| Koyu Görüntü | **Histogram Eşitleme Sonrası** | **131.9299** | **70.5988** | **5.2878** | **25** | **255** |
| Düşük Kontrastlı Görüntü | İşlem Öncesi | 122.7864 | 12.7847 | 5.5419 | 95 | 155 |
| Düşük Kontrastlı Görüntü | **Histogram Eşitleme Sonrası** | **130.5576** | **73.5960** | **5.5312** | **0** | **255** |

**Teknik Yorum:** Koyu görüntüde $[8, 88]$ aralığına sıkışmış olan pikseller doğrusal olmayan CDF dönüşümüyle $[25, 255]$ aralığına yayılmış, kümülatif dağılım fonksiyonu (CDF) ideal doğrusal köşegene yaklaşmış ve karanlıkta seçilemeyen tüm detaylar görünür hale gelmiştir.

---

## 6. Soru 5: Gamma Düzeltmesi ve Etkilerinin Analizi (15 Puan)

### 6.1. Matematiksel Model

$$\text{output}(x, y) = 255 \times \left(\frac{\text{input}(x, y)}{255}\right)^\gamma$$

### 6.2. Her Gamma Değerinin Görüntü Üzerindeki Etkisi

| Gamma ($\gamma$) | Ortalama ($\mu$) | Std. Sapma ($\sigma$) | Entropi ($H$, bit) | Min | Max | Görüntü ve Histogram Üzerindeki Etkisi |
|---:|---:|---:|---:|---:|---:|---|
| **0.5** | 174.16 | 36.58 | 6.9443 | 71 | 250 | **Aydınlatma ve Karanlık Bölge Genişletme:** Dönüşüm eğrisi birim doğrunun ($\gamma=1$) üzerinde içbükey (concave) seyreder. Karanlık gri seviyeler arasındaki farklar genişletilirken parlak tonlar sıkıştırılır; histogram sağa (yüksek parlaklığa) kayar ve gölgede kalan detaylar ortaya çıkar. |
| **1.0** | 124.20 | 47.90 | 7.4505 | 20 | 245 | **Birim (Özdeşlik) Dönüşümü:** $\text{output} = \text{input}$ olduğundan görüntüde, kontrastta ve histogramda hiçbir değişiklik oluşturmaz; referans görüntüyü temsil eder. |
| **1.5** | 91.64 | 49.29 | 7.2899 | 6 | 240 | **Hafif Karartma ve Parlak Bölge Kontrast Artışı:** Dönüşüm eğrisi birim doğrunun altına iner. Orta ve karanlık tonlar hafifçe koyulaşırken parlak bölgelerin dinamik aralığı genişler; standart sapma $47.90$'dan $49.29$'a yükselir. |
| **2.0** | 69.46 | 46.88 | 7.0837 | 2 | 235 | **Belirgin Karartma:** Histogram sola (düşük yoğunluk bölgesine) doğru kayar. Orta tonlar belirgin biçimde koyulaşır; buna karşın yüksek parlaklıktaki (180–255) detayların birbirinden ayrışması güçlenir. |
| **2.5** | 53.83 | 43.22 | 6.8248 | 0 | 231 | **Güçlü Karartma (Yüksek Üs Etkisi):** Düşük ve orta yoğunluklu pikseller $0$'a yakın bölgeye sıkıştırılır, ortalama parlaklık $53.83$'e düşer. Yalnızca en parlak bölgelerdeki yapısal detaylar seçilebilir kalır. |

### 6.3. Hangi Durumda Hangi Gamma Değeri Kullanılmalı?

1. **$\gamma < 1$ (Örn. $\gamma = 0.5$) Kullanılması Gereken Durumlar:**
   - **Az pozlanmış (underexposed)** kamera görüntülerinde,
   - Gece çekimlerinde, yetersiz aydınlatmalı kapalı ortam fotoğraflarında veya ters ışık (backlight) nedeniyle nesnelerin karanlıkta kaldığı sahnelerde,
   - Tıbbi görüntüleme ve uydu görüntülerinde koyu gölge bölgelerindeki düşük yoğunluklu yapıların görünür kılınması gerektiğinde kullanılmalıdır.
2. **$\gamma = 1.0$ Kullanılması Gereken Durumlar:**
   - Aydınlatma ve kontrast dağılımı halihazırda dengeli olan görüntülerde veya kalibrasyon/referans karşılaştırmalarında orijinal veriyi bozmamak için kullanılır.
3. **$\gamma > 1$ (Örn. $\gamma = 1.5, 2.0, 2.5$) Kullanılması Gereken Durumlar:**
   - **Aşırı pozlanmış (overexposed)** veya yoğun ışık altında çekildiği için ağarmış/soluklaşmış (washed-out) görüntülerde,
   - Parlak yüzey yansımaları nedeniyle üst gri seviyelerde ($200-255$) sıkışmış detayların kontrastını artırıp geri kazanmak istendiğinde (hafif parlama için $\gamma = 1.5$, orta düzey aşırı pozlama için $\gamma = 2.0$, çok şiddetli parlama için $\gamma = 2.5$) kullanılmalıdır.
