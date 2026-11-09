"""
Görüntü İşleme 3. Ödevi — Nokta İşlemleri ve Histogram İşleme Ana Çalıştırma Betiği.

Bu betik, Soru 1'den Soru 5'e kadar tüm algoritmaları sırasıyla çalıştırır,
görüntü istatistiklerini ve gamma düzeltmesi analizini ekrana ve rapor dosyasına
yazdırır, tüm karşılaştırmalı görselleştirmeleri outputs/figures/ dizinine kaydeder.

Kullanım (Docker konteyneri içinde):
    python3 main.py
    python3 main.py --parlaklik 50 --kontrast 1.5 --esik 128
    python3 main.py --interaktif
"""

import argparse
import os
from typing import List

from src.test_goruntuleri import test_goruntulerini_hazirla
from src.soru1_nokta_islemleri import (
    parlaklik_ayarla,
    kontrast_ayarla,
    goruntu_negatifi_al,
    esikleme_uygula,
    soru1_tum_islemleri_uygula,
    soru1_gorsellestir,
)
from src.soru2_histogram_analizi import (
    manuel_histogram_hesapla,
    histogram_ciz,
    goruntu_istatistikleri_hesapla,
    istatistikleri_yazdir,
    soru2_gorsellestir,
)
from src.soru3_kontrast_germe import (
    manuel_kontrast_germe,
    soru3_gorsellestir,
)
from src.soru4_histogram_esitleme import (
    manuel_histogram_esitleme,
    soru4_gorsellestir,
)
from src.soru5_gamma_duzeltmesi import (
    VARSAYILAN_GAMMA_DEGERLERI,
    gamma_duzeltmesi,
    coklu_gamma_uygula,
    gamma_analizi_olustur,
    soru5_gorsellestir,
)

__all__ = [
    "parlaklik_ayarla",
    "kontrast_ayarla",
    "goruntu_negatifi_al",
    "esikleme_uygula",
    "soru1_tum_islemleri_uygula",
    "soru1_gorsellestir",
    "manuel_histogram_hesapla",
    "histogram_ciz",
    "goruntu_istatistikleri_hesapla",
    "istatistikleri_yazdir",
    "soru2_gorsellestir",
    "manuel_kontrast_germe",
    "soru3_gorsellestir",
    "manuel_histogram_esitleme",
    "soru4_gorsellestir",
    "gamma_duzeltmesi",
    "coklu_gamma_uygula",
    "gamma_analizi_olustur",
    "soru5_gorsellestir",
]


def argumanlari_cozumle() -> argparse.Namespace:
    """Komut satırı argümanlarını çözümler ve döndürür."""
    parser = argparse.ArgumentParser(
        description="Görüntü İşleme 3. Ödevi — Nokta İşlemleri ve Histogram İşleme"
    )
    parser.add_argument(
        "--parlaklik",
        type=float,
        default=50.0,
        help="Soru 1a parlaklık ayarlama sabiti (varsayılan: 50.0)",
    )
    parser.add_argument(
        "--kontrast",
        type=float,
        default=1.5,
        help="Soru 1b kontrast faktörü (varsayılan: 1.5)",
    )
    parser.add_argument(
        "--esik",
        type=int,
        default=128,
        help="Soru 1d eşikleme (threshold) değeri (varsayılan: 128)",
    )
    parser.add_argument(
        "--interaktif",
        action="store_true",
        help="Soru 1 parametrelerini kullanıcıdan interaktif olarak alır.",
    )
    parser.add_argument(
        "--test-klasoru",
        type=str,
        default="data/test_images",
        help="Test görüntülerinin bulunduğu/kaydedileceği klasör.",
    )
    parser.add_argument(
        "--cikti-klasoru",
        type=str,
        default="outputs/figures",
        help="Görselleştirme çıktılarının kaydedileceği klasör.",
    )
    return parser.parse_args()


def odevi_calistir(args: argparse.Namespace) -> None:
    """
    Tüm ödev sorularını sırasıyla çalıştırır, görselleri ve istatistik raporunu üretir.

    Parametreler:
        args (argparse.Namespace): Çalıştırma parametreleri.
    """
    os.makedirs(args.cikti_klasoru, exist_ok=True)
    rapor_bolumleri: List[str] = [
        "======================================================================",
        "GÖRÜNTÜ İŞLEME 3. ÖDEVİ — NOKTA İŞLEMLERİ VE HİSTOGRAM İŞLEME RAPORU",
        "======================================================================",
        "",
    ]

    print("\n[Adım 0] Test görüntüleri hazırlanıyor...")
    goruntuler = test_goruntulerini_hazirla(args.test_klasoru)
    normal_img = goruntuler["normal_goruntu"]
    dusuk_kontrast_img = goruntuler["dusuk_kontrast"]
    koyu_img = goruntuler["koyu_goruntu"]
    sentetik_dk_img = goruntuler["sentetik_dusuk_kontrast"]

    if args.interaktif:
        girilen_p = input("Soru 1a — Parlaklık sabiti girin (varsayılan 50): ").strip()
        parlaklik_degeri = float(girilen_p) if girilen_p else 50.0
        girilen_k = input("Soru 1b — Kontrast faktörü girin (varsayılan 1.5): ").strip()
        kontrast_faktoru = float(girilen_k) if girilen_k else 1.5
        girilen_t = input("Soru 1d — Eşik değeri girin (varsayılan 128): ").strip()
        esik_degeri = int(girilen_t) if girilen_t else 128
    else:
        parlaklik_degeri = args.parlaklik
        kontrast_faktoru = args.kontrast
        esik_degeri = args.esik

    # ------------------------------------------------------------------
    # SORU 1: Temel Nokta İşlemleri (25 Puan)
    # ------------------------------------------------------------------
    print("\n[Soru 1] Temel Nokta İşlemleri uygulanıyor ve görselleştiriliyor...")
    soru1_dosyalar = soru1_gorsellestir(
        normal_img,
        cikti_klasoru=args.cikti_klasoru,
        parlaklik_degeri=parlaklik_degeri,
        kontrast_faktoru=kontrast_faktoru,
        esik_degeri=esik_degeri,
    )
    soru1_sonuclar = soru1_tum_islemleri_uygula(
        normal_img,
        parlaklik_artir=parlaklik_degeri,
        parlaklik_azalt=-abs(parlaklik_degeri),
        kontrast_artir=kontrast_faktoru,
        kontrast_azalt=0.6,
        esik_degeri=esik_degeri,
    )
    rapor_bolumleri.append("--- SORU 1: TEMEL NOKTA İŞLEMLERİ İSTATİSTİKLERİ ---")
    for islem_adi, islem_img in soru1_sonuclar.items():
        ist = goruntu_istatistikleri_hesapla(islem_img)
        metin = istatistikleri_yazdir(f"Soru 1 - {islem_adi}", ist)
        rapor_bolumleri.append(metin)
    rapor_bolumleri.append("")

    # ------------------------------------------------------------------
    # SORU 2: Histogram Analizi ve Görselleştirme (20 Puan)
    # ------------------------------------------------------------------
    print("\n[Soru 2] Manuel Histogram Analizi ve Görüntü İstatistikleri hesaplanıyor...")
    soru2_dosyalar = soru2_gorsellestir(goruntuler, cikti_klasoru=args.cikti_klasoru)
    rapor_bolumleri.append("--- SORU 2: TEST GÖRÜNTÜLERİ HİSTOGRAM VE İSTATİSTİK ANALİZİ ---")
    for ad, img in goruntuler.items():
        ist = goruntu_istatistikleri_hesapla(img)
        metin = istatistikleri_yazdir(f"Soru 2 - Test Görüntüsü ({ad})", ist)
        rapor_bolumleri.append(metin)
    rapor_bolumleri.append("")

    # ------------------------------------------------------------------
    # SORU 3: Kontrast Germe (Contrast Stretching) (15 Puan)
    # ------------------------------------------------------------------
    print("\n[Soru 3] Manuel Kontrast Germe uygulanıyor ve 2x2 subplot çiziliyor...")
    gerilmis_dogal, soru3_dogal_yol = soru3_gorsellestir(
        dusuk_kontrast_img,
        kayit_yolu=os.path.join(args.cikti_klasoru, "soru3_kontrast_germe_2x2.png"),
        baslik_eki="Düşük Kontrastlı Görüntü [95, 155]",
    )
    gerilmis_sentetik, soru3_sentetik_yol = soru3_gorsellestir(
        sentetik_dk_img,
        kayit_yolu=os.path.join(args.cikti_klasoru, "soru3_sentetik_kontrast_germe_2x2.png"),
        baslik_eki="Sentetik Düşük Kontrastlı Görüntü [100, 149]",
    )
    rapor_bolumleri.append("--- SORU 3: KONTRAST GERME ÖNCESİ VE SONRASI İSTATİSTİKLERİ ---")
    rapor_bolumleri.append(
        istatistikleri_yazdir(
            "Soru 3 - Düşük Kontrastlı Görüntü (Önce)",
            goruntu_istatistikleri_hesapla(dusuk_kontrast_img),
        )
    )
    rapor_bolumleri.append(
        istatistikleri_yazdir(
            "Soru 3 - Kontrast Germe Sonrası (Doğal)",
            goruntu_istatistikleri_hesapla(gerilmis_dogal),
        )
    )
    rapor_bolumleri.append(
        istatistikleri_yazdir(
            "Soru 3 - Sentetik Düşük Kontrast (Önce)",
            goruntu_istatistikleri_hesapla(sentetik_dk_img),
        )
    )
    rapor_bolumleri.append(
        istatistikleri_yazdir(
            "Soru 3 - Sentetik Kontrast Germe Sonrası",
            goruntu_istatistikleri_hesapla(gerilmis_sentetik),
        )
    )
    rapor_bolumleri.append("")

    # ------------------------------------------------------------------
    # SORU 4: Histogram Eşitleme (Histogram Equalization) (25 Puan)
    # ------------------------------------------------------------------
    print("\n[Soru 4] Sıfırdan Histogram Eşitleme uygulanıyor ve 2x2 subplot çiziliyor...")
    esitlenmis_koyu, soru4_koyu_dosyalar = soru4_gorsellestir(
        koyu_img,
        kayit_yolu=os.path.join(args.cikti_klasoru, "soru4_histogram_esitleme_2x2.png"),
        cdf_kayit_yolu=os.path.join(args.cikti_klasoru, "soru4_cdf_ve_donusum_egrisi.png"),
        baslik_eki="Koyu Görüntü",
    )
    esitlenmis_dk, soru4_dk_dosyalar = soru4_gorsellestir(
        dusuk_kontrast_img,
        kayit_yolu=os.path.join(
            args.cikti_klasoru, "soru4_dusuk_kontrast_histogram_esitleme_2x2.png"
        ),
        cdf_kayit_yolu=os.path.join(
            args.cikti_klasoru, "soru4_dusuk_kontrast_cdf_ve_donusum_egrisi.png"
        ),
        baslik_eki="Düşük Kontrastlı Görüntü",
    )
    rapor_bolumleri.append("--- SORU 4: HİSTOGRAM EŞİTLEME ÖNCESİ VE SONRASI İSTATİSTİKLERİ ---")
    rapor_bolumleri.append(
        istatistikleri_yazdir(
            "Soru 4 - Koyu Görüntü (Önce)",
            goruntu_istatistikleri_hesapla(koyu_img),
        )
    )
    rapor_bolumleri.append(
        istatistikleri_yazdir(
            "Soru 4 - Koyu Görüntü Histogram Eşitleme Sonrası",
            goruntu_istatistikleri_hesapla(esitlenmis_koyu),
        )
    )
    rapor_bolumleri.append(
        istatistikleri_yazdir(
            "Soru 4 - Düşük Kontrastlı Görüntü Histogram Eşitleme Sonrası",
            goruntu_istatistikleri_hesapla(esitlenmis_dk),
        )
    )
    rapor_bolumleri.append("")

    # ------------------------------------------------------------------
    # SORU 5: Gamma Düzeltmesi (15 Puan)
    # ------------------------------------------------------------------
    print("\n[Soru 5] Gamma Düzeltmesi (0.5, 1.0, 1.5, 2.0, 2.5) ve Analizi yapılıyor...")
    soru5_dosyalar = soru5_gorsellestir(
        normal_img,
        cikti_klasoru=args.cikti_klasoru,
        gamma_degerleri=VARSAYILAN_GAMMA_DEGERLERI,
    )
    gamma_analiz_metni = gamma_analizi_olustur(normal_img, VARSAYILAN_GAMMA_DEGERLERI)
    rapor_bolumleri.append(gamma_analiz_metni)
    rapor_bolumleri.append("")

    # İstatistik ve analiz raporunu diske kaydet
    rapor_dosya_yolu = os.path.join(os.path.dirname(args.cikti_klasoru), "istatistik_ve_analiz_raporu.txt")
    os.makedirs(os.path.dirname(os.path.abspath(rapor_dosya_yolu)), exist_ok=True)
    with open(rapor_dosya_yolu, "w", encoding="utf-8") as f:
        f.write("\n".join(rapor_bolumleri) + "\n")

    print("\n======================================================================")
    print("TÜM ÖDEV ADIMLARI BAŞARIYLA TAMAMLANDI!")
    print(f"• İstatistik ve Analiz Raporu : {rapor_dosya_yolu}")
    print("• Üretilen Görselleştirmeler  :")
    for yol in [
        soru1_dosyalar["yan_yana"],
        soru1_dosyalar["detayli"],
        soru2_dosyalar["tekil"],
        soru2_dosyalar["coklu"],
        soru3_dogal_yol,
        soru3_sentetik_yol,
        soru4_koyu_dosyalar["karsilastirma_2x2"],
        soru4_koyu_dosyalar["cdf_ve_donusum"],
        soru4_dk_dosyalar["karsilastirma_2x2"],
        soru5_dosyalar["karsilastirma"],
        soru5_dosyalar["donusum_egrileri"],
    ]:
        print(f"  - {yol}")
    print("======================================================================")


if __name__ == "__main__":
    odevi_calistir(argumanlari_cozumle())
