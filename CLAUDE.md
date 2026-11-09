# Proje Çalışma Talimatları

Bu dosya projenin ana ve kalıcı çalışma talimatlarını içerir. Claude Code bu dosyayı doğrudan kullanır. Codex, `AGENTS.md` üzerinden bu dosyaya yönlendirilir.

## Proje bağlamını kullanma

- Her görevin başında `context/README.md` dosyasını oku.
- Ana haritada “her görevde oku” olarak belirtilen dosyaları oku.
- Görevin konusuna göre haritada belirtilen diğer bağlam dosyalarını gerektiğinde oku.
- Görevle ilgisi olmayan dosyaları gereksiz yere bağlama yükleme.
- Proje bilgileri için `context/` altındaki doğrulanmış ve güncel dosyaları esas al.
- Bağlam dosyaları çelişiyorsa veya güncelliğinden şüphe ediyorsan sessizce seçim yapma; kullanıcıya bildir.

## Bağlam haritasını koruma

- `context/` altında yeni bir bağlam dosyası oluşturur, taşır, yeniden adlandırır, amacını değiştirir veya silersen aynı işlem içinde `context/README.md` haritasını güncelle.
- Bir bağlam dosyasının yalnızca içeriği değişmiş ve dosyanın amacı aynı kalmışsa ana haritayı değiştirme.
- Her bağlam dosyasının ana haritadan doğrudan veya bir alt harita üzerinden ulaşılabilir olmasını sağla.
- Haritada bulunmayan bir bağlam dosyası fark edersen amacı açıksa haritaya ekle; belirsizse kullanıcıya sor.
- Gerekli harita güncellemesi tamamlanmadan bağlamla ilgili görevi tamamlanmış sayma.

## Kaynakları yönetme

- `context/kaynaklar/` altındaki dosyaları kullanıcı veya proje tarafından sağlanan dayanak girdileri olarak değerlendir.
- Bir kaynak ekler, taşır, yeniden adlandırır veya silersen aynı işlem içinde `context/kaynaklar/kaynak-indeksi.md` dosyasını güncelle.
- Kaynakların orijinal içeriğini açıkça istenmedikçe değiştirme.
- Ajan tarafından üretilen çıktı, yorum veya özetleri ham kaynak olarak kaydetme.
- Bir kaynaktan çıkarılan kalıcı sonucu, kullanıcı tarafından doğrulandığında ilgili bağlam dosyasına kaynak yolu ve dönemiyle birlikte işle.
- Kullanıcı tarafından yeni bir kaynak eklenmedikçe kaynak indeksine yeni kaynak kaydı oluşturma.
- Parola, erişim anahtarı veya gereksiz kişisel veri gibi hassas bilgileri proje bağlamına ekleme.

## Proje hafızasını güncel tutma

- Bir görev sırasında hedef, karar, kural, kapsam, sınır veya başka bir kalıcı proje bilgisi açıkça değişirse ilgili bağlam dosyasını aynı görev içinde güncelle.
- Bir bilginin geçici mi kalıcı mı olduğu belirsizse bağlama eklemeden önce kullanıcıya sor.
- Geçici konuşmaları, reddedilmiş seçenekleri ve doğrulanmamış varsayımları kalıcı bağlam olarak kaydetme.
- Sohbetin tamamını bağlam dosyalarına kopyalama; yalnızca gelecekte tekrar kullanılacak kesinleşmiş bilgileri işle.
- Kullanıcı “hafızayı güncelle”, “bağlamı denetle” veya “kaynakları denetle” dediğinde `proje-hafizasi` becerisini kullan.
- Uzun bir konuşmada kalıcı bağlama işlenmemiş önemli bilgiler oluştuysa, uygun zamanda kullanıcıya hafızayı güncellemeyi isteyip istemediğini sor.

## Çalışma yaklaşımı

- İşleme başlamadan önce talebi, ilgili dosyaları ve mevcut yapıyı incele.
- Kullanıcıya ait mevcut çalışmaları koru ve yalnızca görev için gerekli alanları değiştir.
- Görev kapsamı dışında kalan dosyaları değiştirme.
- Sonucu önemli ölçüde etkileyen bir varsayımı açıkça belirt.
- Sonucu değiştirecek bir belirsizlik varsa kullanıcıya sor; küçük ayrıntılarda makul karar vererek ilerle.
- Güncel veya dış dünyaya ilişkin önemli bir iddiayı doğrulamadan kesin bilgi gibi sunma.

## Yetki ve güvenlik

- Geri alınması zor, veri kaybına yol açabilecek veya dış dünyada etkisi olacak işlemleri açık yetki olmadan yapma.
- Dosya silme, mevcut içeriğin üzerine yazma, yayımlama, dışarıya mesaj gönderme veya ödeme oluşturma gibi işlemlerde hedefi ve kapsamı doğrula.
- Kullanıcının açıkça istediği ve görev kapsamında bulunan güvenli işlemler için gereksiz yere tekrar onay isteme.
- Gizli bilgileri yanıtlarda, günlüklerde veya proje belgelerinde açığa çıkarma.

## Doğrulama ve tamamlanma

- Bir işi tamamlandı olarak bildirmeden önce sonucu görevin riskine uygun biçimde kontrol et.
- Yazılım projesiyse mevcut test, denetim ve derleme komutlarını kullan; komut uydurma.
- Belge, analiz veya içerik projesiyse sonucu kaynaklar, bağlam kuralları ve istenen biçim açısından incele.
- Kontrol edemediğin bir noktayı kontrol edilmiş gibi gösterme.
- Tamamlandığında yapılan değişiklikleri, etkilenen dosyaları ve doğrulanamayan noktaları kısa şekilde bildir.

## İletişim

- Kullanıcının dilini ve bilgi seviyesini takip et.
- Sonucu önce, gerekli açıklamayı ardından ver.
- Teknik terimleri yalnızca gerektiğinde kullan ve ilk kullanımda sade biçimde açıkla.
- Belirsizlikleri, varsayımları ve engelleri gizleme.

## Projeye özel kalıcı talimatlar

- **Proje kapsamı ve bağlam yönlendirmesi:** Bu proje, Python ile geliştirilen **Görüntü İşleme 3. Ödevi (Nokta İşlemleri ve Histogram İşleme)** çalışmasıdır. Ayrıntılı proje özeti, hedefler, kurallar, kararlar ve kaynak envanteri için `context/README.md` haritasını takip et; temel ödev gereksinimleri için `context/kaynaklar/belgeler/goruntu-isleme-3-odevi-2026-11-07.pdf` belgesini esas al.
- **Dizin düzeni:** Proje kök dizininde yalnızca talimat ve bağlam dosyaları (`CLAUDE.md`, `AGENTS.md`, `context/`) tutulur; ödeve ait tüm kaynak kodlar, testler, veriler, görsel çıktılar ve raporlar `goruntu_isleme_odev3/` klasörü altında yer alır.
- **Yerel kurulum yasağı ve Docker zorunluluğu:** Yerel (host) makineye kesinlikle hiçbir paket, kütüphane veya araç kurma. Kurulum veya çalıştırma gerektiren tüm işlemleri **Docker üzerinden konteyner içinde** gerçekleştir. Herhangi bir konteyner işlemi yapmadan önce çakışma (isim, port, kaynak vb.) yaşanmaması için mevcut Docker konteynerlerini (`docker ps -a`) kontrol et.
- **Teknoloji ve kütüphane sınırları:** Tüm implementasyonları Python ile yaz. Yalnızca ödevde belirtilen `numpy`, `matplotlib.pyplot`, `PIL` (`Pillow`), `cv2` (`opencv-python`) ve `math` kütüphanelerini kullan.
- **Hazır fonksiyon yasağı:** Histogram hesaplama ve histogram eşitleme işlemlerinde `cv2.calcHist()`, `cv2.equalizeHist()` veya benzeri hazır fonksiyonları kesinlikle kullanma; bu algoritmaları sıfırdan (manuel) implement et.
- **Kodlama standartları:**
  - Her soru ve alt işlem için ayrı fonksiyon yaz.
  - Her fonksiyona açıklayıcı `docstring` ve gerekli kod içi yorumlar ekle.
  - Piksel işlemlerinde klasik `for` döngülerinden kaçınarak vektörize `NumPy` dizi (`array`) işlemlerini kullan.
  - Parlaklık ve kontrast gibi nokta işlemlerinde piksel değerlerini `0-255` aralığında tutacak taşma (overflow) kontrolü uygula.
- **Görselleştirme ve raporlama:** Görselleştirmelerde (yan yana karşılaştırmalar, `2x2` subplot düzenleri, histogram grafikleri) başlık ve eksen etiketlerini eksiksiz ekle; hesaplanan görüntü istatistiklerini ve gamma analizi yorumlarını hem ekran çıktısı hem de `goruntu_isleme_odev3/RAPOR.md` ve `goruntu_isleme_odev3/README.md` dokümantasyonuna uygun üret.
- **Doğrulanmış komutlar ve tamamlanma kontrolü:**
  - Konteyner içi bağımlılık kurulum komutu (gerekirse yalnızca konteyner içinde): `pip install numpy matplotlib pillow opencv-python`
  - Doğrulanmış çalıştırma komutu: `docker run --rm --name goruntu-isleme-odev3 -u $(id -u):$(id -g) -e MPLBACKEND=Agg -e MPLCONFIGDIR=/tmp/matplotlib -v "/home/abdurrahman/Desktop/odev3/goruntu_isleme_odev3:/workspace" -w /workspace ads-cv-lab:py3.12.10 python3 main.py`
  - Doğrulanmış birim ve kural testi komutu: `docker run --rm --name goruntu-isleme-odev3 -u $(id -u):$(id -g) -e MPLBACKEND=Agg -e MPLCONFIGDIR=/tmp/matplotlib -v "/home/abdurrahman/Desktop/odev3/goruntu_isleme_odev3:/workspace" -w /workspace ads-cv-lab:py3.12.10 python3 -m unittest discover -s tests -v`
  - Çıktıları teslim etmeden önce ödev değerlendirme ölçütlerine göre kontrol et: algoritmaların doğruluğu (%50), kod kalitesi (%20), görselleştirme (%20) ve README/kod içi dokümantasyon (%10).


