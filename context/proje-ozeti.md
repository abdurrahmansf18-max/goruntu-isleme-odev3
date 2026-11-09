# Proje Özeti

Bu dosya projenin ne olduğunu, neden var olduğunu, kapsamını ve mevcut durumunu açıklar.

## Projenin adı

Görüntü İşleme 3. Ödevi — Nokta İşlemleri ve Histogram İşleme

## Kısa tanım

Yapay Zeka Mühendisliği Görüntü İşleme dersi (Dr. Öğr. Üyesi Ramin Abbaszadi) kapsamında verilen 3. ödev projesidir. Temel nokta işlemleri ve histogram işleme algoritmalarının Python ve `NumPy` kullanılarak sıfırdan gerçeklenmesini, karşılaştırmalı olarak görselleştirilmesini ve raporlanmasını kapsar.

## Ana amaç

Hazır histogram hesaplama ve eşitleme fonksiyonları (`cv2.calcHist`, `cv2.equalizeHist` vb.) kullanmadan; parlaklık/kontrast ayarlama, negatif alma, eşikleme, manuel histogram ve görüntü istatistikleri hesaplama, kontrast germe, sıfırdan histogram eşitleme ve gamma düzeltmesi algoritmalarını vektörize `NumPy` işlemleriyle doğru biçimde geliştirmek, görselleştirmek ve analiz etmektir.

## Kapsama dahil olanlar

- **Soru 1 — Temel Nokta İşlemleri (25 Puan):** Parlaklık ayarlama (7p), kontrast ayarlama (8p), görüntü negatif alma (5p) ve eşikleme (5p) fonksiyonları ile yan yana karşılaştırmalı görselleştirme.
- **Soru 2 — Histogram Analizi ve Görselleştirme (20 Puan):** Gri seviye görüntünün manuel histogram hesaplaması/çizimi (8p) ve görüntü istatistiklerinin (ortalama, standart sapma, entropi, min-max) hesaplanarak ekrana ve rapora yazdırılması (12p).
- **Soru 3 — Kontrast Germe (15 Puan):** Manuel kontrast germe implementasyonu (10p) ve orijinal/işlenmiş görüntüler ile histogramlarının `2x2` subplot'ta gösterilmesi (5p).
- **Soru 4 — Histogram Eşitleme (25 Puan):** Sıfırdan histogram eşitleme algoritması (20p) ve orijinal/eşitlenmiş görüntüler ile histogramlarının `2x2` subplot'ta karşılaştırılması (5p).
- **Soru 5 — Gamma Düzeltmesi (15 Puan):** Farklı gamma değerleri (`0.5, 1.0, 1.5, 2.0, 2.5`) için gamma düzeltme fonksiyonu (10p) ve her değerin görüntü üzerindeki etkisinin analizi (5p).
- **Dokümantasyon ve Çalışma Ortamı:** Açıklayıcı `docstring` ve kod içi yorumlar, `README`/rapor dokümantasyonu ve yerel makineye hiçbir kurulum yapılmadan Docker konteyneri üzerinde izole çalıştırma yapısı.

## Kapsam dışında kalanlar

- Histogram hesaplama ve histogram eşitleme için `cv2.calcHist()`, `cv2.equalizeHist()` gibi hazır kütüphane fonksiyonlarının kullanımı.
- Yerel (host) makineye doğrudan paket, kütüphane veya araç kurulumu yapılması.

## Mevcut durum

- Proje ana çalışma talimatları (`CLAUDE.md`) ve proje bağlam hafızası (`context/`) ödev belgesine, Docker izolasyon kuralına ve ayrı klasör düzenine göre yapılandırıldı.
- Ödevin sağlam PDF kaynağı `context/kaynaklar/belgeler/goruntu-isleme-3-odevi-2026-11-07.pdf` konumuna taşındı ve kökteki bozuk kopya kaldırıldı.
- Tüm ödev kodlaması (`goruntu_isleme_odev3/src/`), ana çalıştırma betiği (`goruntu_isleme_odev3/main.py`), birim ve AST kural testleri (`goruntu_isleme_odev3/tests/test_odev3.py`), test görüntüleri (`goruntu_isleme_odev3/data/test_images/`), 11 adet yüksek çözünürlüklü görselleştirme (`goruntu_isleme_odev3/outputs/figures/`) ve dokümantasyon (`goruntu_isleme_odev3/README.md`, `goruntu_isleme_odev3/RAPOR.md`) tamamlanıp Docker konteyneri içinde doğrulandı.

## Önemli konumlar

- `CLAUDE.md` ve `AGENTS.md`: Projenin ana çalışma talimatları ve Codex uyumluluk katmanı.
- `context/`: Proje bağlam haritası (`context/README.md`), hedefler, kurallar, kararlar ve kaynak envanteri.
- `context/kaynaklar/belgeler/goruntu-isleme-3-odevi-2026-11-07.pdf`: Ödevin resmi yönerge belgesi.
- `goruntu_isleme_odev3/`: Ödeve ait tüm Python kodlarının, testlerin, veri setlerinin, üretilen grafiklerin ve raporların yer aldığı bağımsız uygulama klasörü.

