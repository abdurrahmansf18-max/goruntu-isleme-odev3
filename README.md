# Görüntü İşleme 3. Ödevi — Nokta İşlemleri ve Histogram İşleme

**Ders:** Yapay Zeka Mühendisliği — Görüntü İşleme  
**Öğretim Üyesi:** Dr. Öğr. Üyesi Ramin Abbaszadi  
**Ödev Konusu:** Temel Nokta İşlemleri, Manuel Histogram Analizi, İstatistikler, Kontrast Germe, Sıfırdan Histogram Eşitleme ve Gamma Düzeltmesi

---

## 📌 Depo İçeriği

Bu depo, Görüntü İşleme 3. Ödevi'nin tüm kaynak kodlarını, testlerini, raporlarını, çıktı grafiklerini ve proje bağlam hafızasını içerir:

- **[`goruntu_isleme_odev3/`](goruntu_isleme_odev3/)**: Ödeve ait tüm Python kaynak kodları, testler, çıktılar ve rapor dosyaları:
  - **[`main.py`](goruntu_isleme_odev3/main.py)**: Soru 1–5'i sırasıyla çalıştıran ana betik (CLI ve interaktif mod).
  - **[`src/`](goruntu_isleme_odev3/src/)**: Soru 1–5 için geliştirilen vektörize NumPy modülleri.
  - **[`Rapor.pdf`](goruntu_isleme_odev3/Rapor.pdf)**: İstatistik tabloları, formüller ve karşılaştırma grafiklerini içeren PDF teslim raporu.
  - **[`RAPOR.md`](goruntu_isleme_odev3/RAPOR.md)** & **[`README.md`](goruntu_isleme_odev3/README.md)**: Detaylı markdown dokümantasyonu.
  - **[`tests/test_odev3.py`](goruntu_isleme_odev3/tests/test_odev3.py)**: Birim ve AST kural denetim testleri (10/10 test başarılı).
  - **[`outputs/figures/`](goruntu_isleme_odev3/outputs/figures/)**: 11 adet karşılaştırmalı grafik ve histogram analizi görseli.
- **`goruntu_isleme_odev3.zip`**: Teslim edilmeye hazır, optimize edilmiş (13.06 MB) teslim paketi.
- **`context/`**: Proje bağlamı, kurallar ve kaynaklar indeksi.
- **`CLAUDE.md` & `AGENTS.md`**: Çalışma talimatları ve uyumluluk katmanı.

---

## 🚀 Hızlı Başlangıç

```bash
cd goruntu_isleme_odev3
pip install -r requirements.txt
python3 main.py
```

Birim testlerini çalıştırmak için:
```bash
python3 -m unittest discover -s tests -v
```
