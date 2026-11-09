"""
Görüntü İşleme 3. Ödevi — Kapsamlı Birim ve Kural Doğrulama Testleri.

Bu test modülü:
1. Soru 1–5 tüm matematiksel formüllerin doğruluğunu,
2. [0, 255] taşma (overflow) kontrollerini,
3. Entropi, ortalama, standart sapma, CDF ve s_k dönüşüm özelliklerini,
4. AST (Soyut Sözdizimi Ağacı) analizi ile hesaplama fonksiyonlarında for/while döngüsü
   kullanılmadığını, tüm fonksiyonlarda docstring bulunduğunu ve cv2.calcHist /
   cv2.equalizeHist gibi yasaklı hazır fonksiyonların çağrılmadığını doğrular.
"""

import ast
import inspect
import math
import os
import unittest
import numpy as np

from src.soru1_nokta_islemleri import (
    parlaklik_ayarla,
    kontrast_ayarla,
    goruntu_negatifi_al,
    esikleme_uygula,
)
from src.soru2_histogram_analizi import (
    manuel_histogram_hesapla,
    goruntu_istatistikleri_hesapla,
)
from src.soru3_kontrast_germe import manuel_kontrast_germe
from src.soru4_histogram_esitleme import manuel_histogram_esitleme
from src.soru5_gamma_duzeltmesi import (
    VARSAYILAN_GAMMA_DEGERLERI,
    gamma_duzeltmesi,
    coklu_gamma_uygula,
)


class TestGörüntüİşlemeÖdev3(unittest.TestCase):
    """Soru 1–5 algoritmalarını ve teknik kuralları doğrulayan test sınıfı."""

    def test_soru1a_parlaklik_ve_tasma_kontrolu(self) -> None:
        """Soru 1a: Parlaklık ekleme/çıkarma ve [0, 255] taşma kontrolünü doğrular."""
        giris = np.array([[10, 100, 240], [0, 128, 255]], dtype=np.uint8)
        artirilmis = parlaklik_ayarla(giris, 30)
        beklenen_artirilmis = np.array([[40, 130, 255], [30, 158, 255]], dtype=np.uint8)
        np.testing.assert_array_equal(artirilmis, beklenen_artirilmis)

        azaltilmis = parlaklik_ayarla(giris, -30)
        beklenen_azaltilmis = np.array([[0, 70, 210], [0, 98, 225]], dtype=np.uint8)
        np.testing.assert_array_equal(azaltilmis, beklenen_azaltilmis)
        self.assertEqual(artirilmis.dtype, np.uint8)
        self.assertEqual(azaltilmis.dtype, np.uint8)

    def test_soru1b_kontrast_ayarla(self) -> None:
        """Soru 1b: output = factor * (input - 128) + 128 formülünü ve taşmayı doğrular."""
        giris = np.array([[28, 128, 228]], dtype=np.uint8)
        sonuc = kontrast_ayarla(giris, 1.5)
        # 28 -> 1.5*(-100)+128 = -22 -> clip 0
        # 128 -> 1.5*(0)+128 = 128
        # 228 -> 1.5*(100)+128 = 278 -> clip 255
        beklenen = np.array([[0, 128, 255]], dtype=np.uint8)
        np.testing.assert_array_equal(sonuc, beklenen)

    def test_soru1c_negatif_alma(self) -> None:
        """Soru 1c: output = 255 - input formülünü doğrular."""
        giris = np.array([[0, 55, 128, 200, 255]], dtype=np.uint8)
        sonuc = goruntu_negatifi_al(giris)
        beklenen = np.array([[255, 200, 127, 55, 0]], dtype=np.uint8)
        np.testing.assert_array_equal(sonuc, beklenen)

    def test_soru1d_esikleme(self) -> None:
        """Soru 1d: Eşik değerinden büyüklerin 255, diğerlerinin 0 olmasını doğrular."""
        giris = np.array([[50, 127, 128, 129, 250]], dtype=np.uint8)
        sonuc = esikleme_uygula(giris, 128)
        beklenen = np.array([[0, 0, 0, 255, 255]], dtype=np.uint8)
        np.testing.assert_array_equal(sonuc, beklenen)

    def test_soru2a_manuel_histogram(self) -> None:
        """Soru 2a: Manuel histogramın frekans toplamını ve bin doğruluğunu test eder."""
        giris = np.array([[0, 0, 10, 255], [10, 10, 128, 255]], dtype=np.uint8)
        hist = manuel_histogram_hesapla(giris)
        self.assertEqual(hist.shape, (256,))
        self.assertEqual(int(np.sum(hist)), giris.size)
        self.assertEqual(int(hist[0]), 2)
        self.assertEqual(int(hist[10]), 3)
        self.assertEqual(int(hist[128]), 1)
        self.assertEqual(int(hist[255]), 2)
        self.assertEqual(int(hist[50]), 0)

    def test_soru2b_goruntu_istatistikleri(self) -> None:
        """Soru 2b: Ortalama, standart sapma, entropi ve min/max değerlerini doğrular."""
        ikili = np.array([[0, 255], [0, 255]], dtype=np.uint8)
        ist = goruntu_istatistikleri_hesapla(ikili)
        self.assertAlmostEqual(ist["ortalama"], 127.5, places=5)
        self.assertAlmostEqual(ist["standart_sapma"], 127.5, places=5)
        self.assertAlmostEqual(ist["entropi"], 1.0, places=5)
        self.assertEqual(ist["min_deger"], 0)
        self.assertEqual(ist["max_deger"], 255)

        duzgun = np.arange(256, dtype=np.uint8).reshape(16, 16)
        ist_duzgun = goruntu_istatistikleri_hesapla(duzgun)
        self.assertAlmostEqual(ist_duzgun["entropi"], 8.0, places=5)

    def test_soru3_manuel_kontrast_germe(self) -> None:
        """Soru 3a: Kontrast germe işleminin [min, max] aralığını [0, 255] yaptığını doğrular."""
        giris = np.array([[100, 125, 150], [110, 130, 140]], dtype=np.uint8)
        gerilmis, min_ilk, max_ilk = manuel_kontrast_germe(giris)
        self.assertEqual(min_ilk, 100)
        self.assertEqual(max_ilk, 150)
        self.assertEqual(int(np.min(gerilmis)), 0)
        self.assertEqual(int(np.max(gerilmis)), 255)
        self.assertIn(int(gerilmis[0, 1]), (127, 128))

    def test_soru4_manuel_histogram_esitleme(self) -> None:
        """Soru 4a: Sıfırdan histogram eşitleme adımlarını (PDF, CDF, s_k) doğrular."""
        koyu = np.array(
            [
                [10, 12, 15, 20],
                [12, 18, 22, 25],
                [14, 20, 28, 35],
                [16, 24, 32, 40],
            ],
            dtype=np.uint8,
        )
        esitlenmis, ara = manuel_histogram_esitleme(koyu)
        self.assertEqual(esitlenmis.shape, koyu.shape)
        self.assertEqual(esitlenmis.dtype, np.uint8)
        self.assertAlmostEqual(float(np.sum(ara["pdf"])), 1.0, places=6)
        self.assertAlmostEqual(float(ara["cdf"][-1]), 1.0, places=6)
        self.assertEqual(int(ara["donusum_fonksiyonu_sk"][-1]), 255)
        farklar = np.diff(ara["donusum_fonksiyonu_sk"].astype(np.int32))
        self.assertTrue(np.all(farklar >= 0))
        self.assertEqual(int(np.max(esitlenmis)), 255)

    def test_soru5_gamma_duzeltmesi(self) -> None:
        """Soru 5a: Gamma düzeltmesi formülünü ve gamma değerlerinin etkisini doğrular."""
        giris = np.array([[0, 64, 128, 192, 255]], dtype=np.uint8)
        birim = gamma_duzeltmesi(giris, 1.0)
        np.testing.assert_array_equal(birim, giris)

        coklu = coklu_gamma_uygula(giris, VARSAYILAN_GAMMA_DEGERLERI)
        self.assertGreater(float(np.mean(coklu[0.5])), float(np.mean(giris)))
        self.assertLess(float(np.mean(coklu[1.5])), float(np.mean(giris)))
        self.assertLess(float(np.mean(coklu[2.5])), float(np.mean(coklu[1.5])))

        beklenen_128 = round(255.0 * math.pow(128.0 / 255.0, 2.0))
        self.assertEqual(int(coklu[2.0][0, 2]), beklenen_128)

    def test_teknik_kurallar_docstring_ve_vektorizasyon(self) -> None:
        """Teknik Gereksinimler Denetimi."""
        hesaplama_fonksiyonlari = [
            parlaklik_ayarla,
            kontrast_ayarla,
            goruntu_negatifi_al,
            esikleme_uygula,
            manuel_histogram_hesapla,
            goruntu_istatistikleri_hesapla,
            manuel_kontrast_germe,
            manuel_histogram_esitleme,
            gamma_duzeltmesi,
        ]

        for fonk in hesaplama_fonksiyonlari:
            self.assertIsNotNone(fonk.__doc__, f"{fonk.__name__} docstring içermiyor!")
            self.assertGreater(len(fonk.__doc__.strip()), 30, f"{fonk.__name__} docstring çok kısa!")

            kaynak = inspect.getsource(fonk)
            agac = ast.parse(kaynak)
            donguler = [
                dugum for dugum in ast.walk(agac) if isinstance(dugum, (ast.For, ast.While))
            ]
            self.assertEqual(
                len(donguler),
                0,
                f"{fonk.__name__} içinde döngü tespit edildi (NumPy array işlemi kullanılmalı)!",
            )

        yasakli_cagrilar = {"calcHist", "equalizeHist", "histogram", "bincount"}
        src_dizini = os.path.join(os.path.dirname(os.path.dirname(__file__)), "src")
        for dosya in os.listdir(src_dizini):
            if not dosya.endswith(".py"):
                continue
            tam_yol = os.path.join(src_dizini, dosya)
            with open(tam_yol, "r", encoding="utf-8") as f:
                agac = ast.parse(f.read(), filename=dosya)
            for dugum in ast.walk(agac):
                if isinstance(dugum, ast.Call):
                    fonk_adi = None
                    if isinstance(dugum.func, ast.Name):
                        fonk_adi = dugum.func.id
                    elif isinstance(dugum.func, ast.Attribute):
                        fonk_adi = dugum.func.attr
                    self.assertNotIn(
                        fonk_adi,
                        yasakli_cagrilar,
                        f"{dosya} içinde yasaklı hazır fonksiyon ({fonk_adi}) çağrıldı!",
                    )


if __name__ == "__main__":
    unittest.main(verbosity=2)
