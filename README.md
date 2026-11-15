# Roma Rakamı → Tam Sayı Dönüştürücü

Roma rakamlarıyla yazılmış bir sayıyı (1–4999 arası) tam sayıya çeviren ve hatalı yazılışları reddeden bir Python programı.

## Problem

Bir öğrenci, çocuğunun Roma rakamlarıyla ilgili ödevlerini kontrol etmek istiyor. Program, kullanıcının girdiği Roma rakamını gündelik hayatta kullandığımız sayı sistemine çevirmeli.

**Kabul kriterleri:**
- Yanlış girdiler ele alınmalı (örneğin `III` 3 demektir ama `IIII` diye bir Roma rakamı yoktur; `VII` 7 demektir ama `VIIII` diye bir Roma rakamı yoktur).
- 1 ile 4999 arasındaki tüm sayılar için çalışmalı.
- Komut satırı (CLI) ya da grafik arayüz fark etmez.

## Algoritma

**1. Çevirme:** Rakamlar soldan sağa okunur. Bir rakam sağındakinden küçükse çıkarılır, değilse toplanır.

```
XIV:  X (10) → sağındaki I'dan büyük  → +10
      I (1)  → sağındaki V'den küçük  → −1
      V (5)  → sağında rakam yok      → +5
                                  toplam = 14
```

**2. Aralık kontrolü:** Sonuç 1 ile 4999 arasında değilse hata verilir.

**3. Kurallı yazılış doğrulaması:** Çevirme kuralı tek başına `IIII` gibi hatalı girdileri de kabul eder (1+1+1+1 = 4). Bunu önlemek için bulunan sayı tekrar Roma rakamına çevrilir ve girdiyle karşılaştırılır. Aynı değilse girdi hatalıdır.

```
XIV  → 14 → tekrar çevir → "XIV"  ✓ kabul
IIII → 4  → tekrar çevir → "IV"   ✗ hata
IC   → 99 → tekrar çevir → "XCIX" ✗ hata
```

Bu yöntem sayesinde hatalı yazılışların kurallarını tek tek kodlamaya gerek kalmıyor.

## Kullanım

```bash
python roman_numerals.py
```

```
Roma rakamı girin (1-4999): MCMXCIV
Sonuç: 1994
```

Küçük harf ve baştaki/sondaki boşluklar kabul edilir (`iv` → 4, `" XII "` → 12).

## Test sonuçları

1'den 4999'a kadar bütün sayılar sayı → Roma rakamı → sayı şeklinde çevrildi, 4999 sayının hepsi doğru sonuç verdi.

| Girdi | Sonuç |
|---|---|
| `III` | 3 |
| `VII` | 7 |
| `XLII` | 42 |
| `MCMXCIV` | 1994 |
| `MMMMCMXCIX` | 4999 |
| `IIII` | Hata: geçersiz dizilim |
| `VIIII` | Hata: geçersiz dizilim |
| `IC` | Hata: geçersiz dizilim |
| `XXXX` | Hata: geçersiz dizilim |
| `MMMMM` | Hata: sayı 1–4999 arasında olmalı |
| `ABC` | Hata: geçersiz karakter |
| (boş) | Hata: boş giriş |

## Kullanılan teknolojiler

Python 3 (harici kütüphane gerekmez)
