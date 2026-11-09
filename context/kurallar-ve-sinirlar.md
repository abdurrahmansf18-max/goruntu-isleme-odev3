# Kurallar ve Sınırlar

Bu dosya projede her zaman dikkate alınması gereken kalıcı kuralları, sınırları ve yasakları içerir.

## Zorunlu kurallar

- **Ayrı uygulama klasörü düzeni:** Proje kök dizininde yalnızca hafıza ve talimat yapısı (`CLAUDE.md`, `AGENTS.md`, `context/`) tutulmalı; ödevle ilgili tüm kodlama, test, veri, görsel çıktı ve rapor dosyaları `goruntu_isleme_odev3/` klasörü içinde yer almalıdır.
- **Docker konteyner zorunluluğu ve çakışma kontrolü:** Yerel (host) makineye hiçbir paket, kütüphane veya araç kurulmamalıdır. Gereken tüm kurulumlar ve çalıştırma işlemleri **Docker üzerinden konteyner içinde** yapılmalıdır. Konteyner oluşturmadan, başlatmadan veya kullanmadan önce mevcut konteynerler kontrol edilerek isim, port veya yapılandırma çakışması olmadığından emin olunmalıdır.
- **Dil ve izin verilen kütüphaneler:** Tüm implementasyonlar Python kullanılarak yapılmalıdır. Yalnızca `numpy`, `matplotlib.pyplot`, `PIL` (`Pillow`), `cv2` (`opencv-python`) ve `math` kütüphaneleri kullanılabilir (kurulum yalnızca Docker konteyneri içinde: `pip install numpy matplotlib pillow opencv-python`).
- **Modüler fonksiyon yapısı ve dokümantasyon:** Her soru ve alt işlem için ayrı fonksiyon yazılmalı, tüm fonksiyonlara açıklayıcı `docstring` eklenmeli ve kod anlaşılır yorumlarla desteklenmelidir.
- **Vektörize hesaplama:** Görüntü matrisi işlemlerinde `NumPy` dizi (`array`) işlemleri kullanılmalı, piksel düzeyinde `for` döngülerinden kaçınılmalıdır.
- **Taşma (overflow) kontrolü:** Parlaklık ve kontrast ayarlama gibi nokta işlemlerinde piksel değerlerinin `0-255` aralığında kalması için taşma kontrolü yapılmalıdır.
- **Görselleştirme ve raporlama:** Tüm görselleştirmelerde başlık ve eksen etiketleri bulunmalı; hesaplanan görüntü istatistikleri (ortalama, standart sapma, entropi, min-max) ile gamma analizi açıklamaları hem ekrana yazdırılmalı hem de rapora/README dokümantasyonuna eklenmelidir.

## Yapılmaması gerekenler

- **Yerel makineye kurulum yasağı:** Yerel sisteme doğrudan `pip`, `apt`, `conda` veya başka bir paket yöneticisiyle herhangi bir kurulum yapmak kesinlikle yasaktır.
- **Kontrolsüz konteyner işlemi yasağı:** Mevcut Docker konteynerlerini kontrol etmeden (çakışma analizi yapmadan) yeni konteyner oluşturmak veya çalıştırmak yasaktır.
- **Hazır histogram fonksiyonu yasağı:** Histogram hesaplama ve histogram eşitleme için `cv2.calcHist()`, `cv2.equalizeHist()` veya benzeri hazır kütüphane fonksiyonları kullanılamaz; sıfırdan implement edilmelidir.
- **Klasik döngü yasağı:** Piksel işlemlerinde `NumPy` vektörizasyonu yerine standart `for` döngüleri kullanılmamalıdır.

## Bütçe, süre ve kaynak sınırları

- **Teslim süresi:** Ödev teslim tarihi `28.11.2026` (3 hafta).
- **Çalışma ortamı sınırı:** Tüm bağımlılıklar ve çalışma zamanı işlemleri Docker konteyneri ile sınırlandırılmıştır.

## Hukuki, güvenlik ve gizlilik sınırları

- Test görüntülerinde yalnızca açık/ücretsiz veri setleri (`USC-SIPI`, `ECE533 Sample Images`, `Unsplash`), Python ile üretilen sentetik görüntüler veya gizlilik ihlali içermeyen kullanıcı çekimi görüntüler kullanılmalıdır.
- Proje bağlamına ve kod dosyalarına parola, erişim anahtarı veya gereksiz kişisel veri eklenmemelidir.

## Kullanıcı onayı gerektiren işlemler

- Mevcut kaynakların veya kullanıcı dosyalarının silinmesi ya da üzerine yazılması.
- Mevcut çalışan bir Docker konteynerini durdurma, silme veya değiştirme gibi çakışma çözümü gerektiren müdahaleler.
- Proje hedeflerini, kurallarını veya kapsamını değiştirecek kararlar.

