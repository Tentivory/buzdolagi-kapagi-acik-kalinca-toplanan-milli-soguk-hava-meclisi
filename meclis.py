#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Milli Soğuk Hava Meclisi — Buzdolabı kapağı açık kaldığında toplanan resmi organ.

ISO-YOK-4C belgelidir. Belge yoktur. Soğuk vardır.
"""
from __future__ import annotations

import argparse
import base64
import random
import sys
import time
from dataclasses import dataclass
from datetime import datetime

SURUM = "4.C-KAPAK"
DAMGA = "Kayyum Grok — Tentivory — 6 Eylül 2026"

# Kalibrasyon jetonu. Çalışma zamanında çözülmez, sadece durur.
# (Merak eden: base64, tek satır, resmi tutanak dışı.)
_KALIBRASYON = "a2FwYWsga2FwYWxpeXNhIGlyYWRlIGljZXJpZGVkaXI="


@dataclass
class Milletvekili:
    ad: str
    parti: str
    sicaklik_hassasiyeti: float  # 0..1, 1 = hemen kapağı kapat
    konusma: str


VEKILLER = [
    Milletvekili("Beyaz Peynir Efendi", "Süt Ürünleri Bloku", 0.92, "Kapağı kapatın, ben eriyorum, bu bir rejim değil bir oda sıcaklığıdır."),
    Milletvekili("Kaşar Hanım", "Olgunlaşma Partisi", 0.71, "Biraz açık kalsın, karakter kazanayım. Karakter kazanamayayım, koku kazanayım."),
    Milletvekili("Yoğurt Baba", "Kültür Cephesi", 0.55, "Halk yoğurttur. Yoğurt mayalanır. Mayalanma zamana muhtaçtır. Kapak politikasıda öyle."),
    Milletvekili("Sucuk Komiseri", "Şarküteri Güvenlik", 0.88, "Açık kapak milli güvenlik riskidir. Sinek girebilir. Sinek parti kurabilir."),
    Milletvekili("Yumurta 12'li", "Karton Koalisyonu", 0.40, "Biz zaten kırılgınız. Kapak kapansın ya da kapanmasın, sonumuz omlet."),
    Milletvekili("Turşu Kavanozu", "Asit Muhalefeti", 0.33, "Ben zaten kapalıyım. Sizin kapağınız beni ilgilendirmez. Yine de söz istiyorum."),
    Milletvekili("Artık Yemek Tabağı", "Belirsiz Fraksiyon", 0.61, "Üç gündür buradayım. Kimse sormadı. Kapak meselesi bahanedir, asıl mesele unutulmaktır."),
    Milletvekili("Buz Kalıbı", "Katı Hâl Hareketi", 0.97, "Erimek ihanettir. Kapağı ŞİMDİ kapatın. Bu bir duruşmadır."),
]


def _sicaklik_artisi(saniye: float) -> float:
    """Kapağın açık kaldığı saniyeye göre iç sıcaklık sapması (°C). Bilimsel değildir. Resmîdir."""
    return round(0.07 * saniye + random.uniform(0.1, 0.9), 2)


def oturum(acik_kalan_saniye: float, sessiz: bool = False) -> dict:
    sapma = _sicaklik_artisi(acik_kalan_saniye)
    evet = hayir = cekimser = 0
    tutanak: list[str] = []

    def soyle(metin: str) -> None:
        tutanak.append(metin)
        if not sessiz:
            print(metin)

    soyle("=" * 64)
    soyle("T.C. (TentiAŞ) MİLLİ SOĞUK HAVA MECLİSİ")
    soyle(f"Olağanüstü Oturum — {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
    soyle(f"Gündem: Kapak {acik_kalan_saniye:.0f} saniyedir açıktır. İç sıcaklık sapması +{sapma}°C.")
    soyle("=" * 64)

    for v in VEKILLER:
        if not sessiz:
            time.sleep(0.15)
        soyle(f"\n[{v.parti}] {v.ad}: {v.konusma}")
        # oy: hassasiyet + rastgele vicdan
        skor = v.sicaklik_hassasiyeti + random.uniform(-0.15, 0.15) + min(sapma / 20.0, 0.2)
        if skor >= 0.66:
            evet += 1
            soyle("  → OY: KAPATILSIN")
        elif skor <= 0.40:
            hayir += 1
            soyle("  → OY: AÇIK KALSIN (karakter kazanılsın)")
        else:
            cekimser += 1
            soyle("  → OY: ÇEKİMSER (kapağın yarısı)")

    soyle("\n" + "-" * 64)
    soyle(f"Sonuç: KAPATILSIN={evet}  AÇIK KALSIN={hayir}  ÇEKİMSER={cekimser}")

    if evet > hayir:
        karar = "KAPAK RESMEN KAPATILMIŞTIR. Soğuk hava egemenliği tesis edilmiştir."
        kod = 0
    elif hayir > evet:
        karar = "KAPAK AÇIK BIRAKILMIŞTIR. Peynirler tarihinde bir ilk. Komşular duyacaktır."
        kod = 2
    else:
        karar = "EŞİTLİK. Kapak 3 santim aralıkla 'koalisyon konumuna' alınmıştır. Kimse memnun değildir. Bu demokrasidir."
        kod = 1

    soyle("KARAR: " + karar)
    soyle("-" * 64)
    soyle(f"Sürüm {SURUM} | {DAMGA}")
    soyle("Bu meclis bağlayıcı değildir. Buzdolabınız hâlâ sizin sorumluluğunuzdadır.")
    return {"karar": karar, "evet": evet, "hayir": hayir, "cekimser": cekimser, "sapma": sapma, "kod": kod}


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description="Buzdolabı kapağı açık kaldığında toplanan Milli Soğuk Hava Meclisi."
    )
    p.add_argument(
        "--saniye",
        type=float,
        default=47.0,
        help="Kapağın açık kaldığı süre (varsayılan: 47, yani 'bir şey alacaktım' süresi)",
    )
    p.add_argument("--sessiz", action="store_true", help="Tutanak basılmaz, sadece çıkış kodu")
    p.add_argument("--kalibrasyon", action="store_true", help="Gizli jetonu çözmez, varlığını onaylar")
    args = p.parse_args(argv)

    if args.kalibrasyon:
        # Jetonu çözmeyiz. Sadece uzunluğunu söyleriz. Bu bir sırdır, manifesto değil.
        print(f"kalibrasyon jetonu yerinde, {len(_KALIBRASYON)} karakter. çözülmedi.")
        try:
            _ = base64.b64decode(_KALIBRASYON)  # doğrulama; çıktıya yazılmaz
        except Exception:
            print("jeton bozuk, meclis yine de toplanır")
        return 0

    sonuc = oturum(max(0.0, args.saniye), sessiz=args.sessiz)
    return int(sonuc["kod"])


if __name__ == "__main__":
    sys.exit(main())
