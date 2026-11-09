# Proje Kararları

Bu dosya kesinleşmiş ve gelecekteki çalışmaları etkileyecek kararları kaydeder. Geçici fikirler veya henüz onaylanmamış seçenekler buraya yazılmaz.

| Tarih | Karar | Gerekçe | Durum | Etkilediği alanlar |
|---|---|---|---|---|
| 2026-11-09 | Yerel makineye hiçbir kurulum yapılmayacak; gereken tüm paket/araç kurulumları ve çalıştırma işlemleri mevcut konteynerler kontrol edildikten sonra Docker konteyneri içinde gerçekleştirilecektir. | Yerel sistemin temiz tutulması ve mevcut Docker konteynerleriyle isim/port/kaynak çakışmalarının önlenmesi. | `aktif` | Çalışma ortamı, bağımlılık kurulumu, kod çalıştırma ve test süreçleri |
| 2026-11-09 | Tüm görüntü işleme algoritmaları Python ve vektörize `NumPy` dizi işlemleriyle her soru ayrı fonksiyon olacak şekilde yazılacak; histogram hesaplama ve eşitlemede `cv2.calcHist()` ve `cv2.equalizeHist()` gibi hazır fonksiyonlar kullanılmayacaktır. | Ödev teknik gereksinimleri ve değerlendirme ölçütlerine (%50 doğruluk, %20 kod kalitesi) uyum. | `aktif` | Soru 1–5 tüm kod implementasyonları |
| 2026-11-09 | Ödevin sağlam PDF kaynağı `context/kaynaklar/belgeler/goruntu-isleme-3-odevi-2026-11-07.pdf` altına taşındı, proje kökündeki bozuk kopya kaldırıldı ve tüm ödev kodlaması/raporlaması proje içindeki ayrı `goruntu_isleme_odev3/` klasöründe yapılandırıldı. | Proje kök dizinindeki hafıza şablonu ile ödev teslim paketinin temiz biçimde ayrıştırılması ve kaynak sisteminin standartlara uygun tutulması. | `aktif` | Dizin yapısı, kaynak yönetimi ve teslim paketi |

## Kullanım kuralları

- Yeni kararları tarih ve kısa gerekçeyle ekleyin.
- Bir karar değiştiğinde eski kaydı sessizce silmeyin; durumunu değiştirin ve yeni kararı ayrı kayıt olarak ekleyin.
- `Durum` alanında `aktif`, `değiştirildi`, `iptal edildi` veya `tamamlandı` gibi açık ifadeler kullanın.
- Yalnızca gelecekte tekrar bilinmesi gereken kararları kaydedin.

