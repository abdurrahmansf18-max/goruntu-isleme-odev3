# Hedefler

Bu dosya projenin aktif hedeflerini, önceliklerini ve başarı ölçütlerini içerir.

## Aktif hedefler

1. **Docker konteyner ortamının kontrolü ve hazırlanması:** Yerel makineye kurulum yapmadan, mevcut Docker konteynerleri çakışma açısından kontrol edilerek Python görüntü işleme kütüphanelerini (`numpy`, `matplotlib`, `pillow`, `opencv-python`) içeren konteyner ortamının hazırlanması.
2. **Soru 1 — Temel Nokta İşlemleri (25 Puan):**
   - Parlaklık ayarlama fonksiyonu (7p, `0-255` taşma kontrollü).
   - Kontrast ayarlama fonksiyonu (8p, `output = factor * (input - 128) + 128`, taşma kontrollü).
   - Görüntü negatif alma fonksiyonu (5p, `output = 255 - input`).
   - Eşikleme (Thresholding) fonksiyonu (5p, eşik üstü `255`, altı `0`).
   - Orijinal ve işlenmiş görüntülerin yan yana gösterilmesi.
3. **Soru 2 — Histogram Analizi ve Görselleştirme (20 Puan):**
   - Gri seviye görüntünün histogramını hazır fonksiyon kullanmadan manuel hesaplayan ve grafiğini çizen fonksiyon (8p).
   - Ortalama (`mean`), standart sapma (`standard deviation`), entropi ve minimum/maksimum piksel değerlerini hesaplayan fonksiyonun yazılıp sonuçların ekrana ve rapora eklenmesi (12p).
4. **Soru 3 — Kontrast Germe (Contrast Stretching) (15 Puan):**
   - `output = ((input - min) / (max - min)) * 255` formülüyle manuel kontrast germe fonksiyonu (10p).
   - Orijinal görüntü, işlenmiş görüntü ve her ikisinin histogramlarının `2x2` subplot'ta gösterilmesi (5p).
5. **Soru 4 — Histogram Eşitleme (Histogram Equalization) (25 Puan):**
   - Sıfırdan histogram eşitleme algoritması: histogram hesaplama, normalize kümülatif histogram hesaplama, dönüşüm fonksiyonu (`s_k = (L-1) * Σ(nj / MN)`) oluşturma ve pikselleri dönüştürme (20p).
   - Orijinal ve eşitlenmiş görüntüler ile histogramlarının `2x2` subplot'ta karşılaştırılması (5p).
6. **Soru 5 — Gamma Düzeltmesi (15 Puan):**
   - `output = 255 * (input / 255)^gamma` formülüyle `0.5, 1.0, 1.5, 2.0, 2.5` gamma değerleri için düzeltme ve görselleştirme fonksiyonu (10p).
   - Her gamma değerinin görüntü üzerindeki etkisinin ve hangi durumda hangi gamma değerinin kullanılacağının analizi (5p).
7. **Test görüntüleri ve dokümantasyon:** Düşük kontrastlı, koyu, normal ve yüksek kontrastlı test görüntüleriyle algoritmaların doğrulanması; `README` ve rapor dokümantasyonunun tamamlanması.

## Öncelik sırası

1. **Docker konteyner çakışma kontrolü ve ortam hazırlığı:** Yerel kurulum yasağı nedeniyle kod çalıştırmadan önce ilk adımdır.
2. **Temel algoritmaların doğru implementasyonu (%50 ağırlık):** Özellikle diğer sorulara temel oluşturan manuel histogram hesaplama (Soru 2a) ile en yüksek puanlı Soru 1 (25p) ve Soru 4 (25p).
3. **Kod kalitesi (%20 ağırlık) ve Görselleştirme (%20 ağırlık):** Vektörize `NumPy` kullanımı, `docstring`/yorumlar ve başlıklı/etiketli subplot çıktıları.
4. **Dokümantasyon ve raporlama (%10 ağırlık):** İstatistik sonuçları, gamma analizi ve `README` dosyası.

## Başarı ölçütleri

- **Doğruluk (%50):** Tüm nokta işlemleri ve histogram algoritmalarının hazır fonksiyon (`cv2.calcHist`, `cv2.equalizeHist`) kullanılmadan, verilen formüllere ve `0-255` sınırlarına tam uyumlu çalışması.
- **Kod Kalitesi (%20):** Her soru için ayrı fonksiyon, açıklayıcı `docstring`, kod içi yorumlar ve `for` döngülerinden kaçınan `NumPy` dizi işlemleri.
- **Görselleştirme (%20):** Yan yana ve `2x2` subplot grafiklerinin başlık ve eksen etiketleriyle net biçimde sunulması.
- **Dokümantasyon (%10):** `README`, kod içi açıklamalar, istatistik çıktıları ve gamma analizi yorumlarının eksiksiz tamamlanması.
- **Ortam kuralına uyum:** Yerel makineye hiçbir kurulum yapılmadan tüm sürecin çakışma kontrolü yapılmış Docker konteyneri içinde yürütülmesi.

## Zaman sınırları

- **Son teslim tarihi:** `28.11.2026` (3 hafta).

## Tamamlanan veya geçerliliğini yitiren hedefler

- `09.11.2026` — Ana proje talimatlarının (`CLAUDE.md`) ve proje bağlam dosyalarının (`context/`) ödev gereksinimlerine ve Docker konteyner kurallarına göre yapılandırılması (**tamamlandı**).
- `09.11.2026` — Mevcut Docker konteynerlerinin (`portainer`, `ads-cv-lab` vb.) kontrol edilerek çakışmasız `goruntu-isleme-odev3` (`ads-cv-lab:py3.12.10`) konteyner ortamının doğrulanması (**tamamlandı**).
- `09.11.2026` — `goruntu_isleme_odev3/` klasörü altında Soru 1–5 tüm görüntü işleme modüllerinin, test görüntülerinin, 10 birim/AST kural testinin, 11 yüksek çözünürlüklü karşılaştırma figürünün ve `README.md` / `RAPOR.md` dokümantasyonunun tamamlanması (**tamamlandı**).

