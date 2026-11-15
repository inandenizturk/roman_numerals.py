def roman_to_int(s: str) -> int:
    s = s.strip().upper()
    if not s:
        raise ValueError("Boş giriş yapılamaz.")

    values = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    
    # Geçersiz karakter kontrolü
    if any(ch not in values for ch in s):
        raise ValueError("Geçersiz Roma rakamı karakteri!")

    # 1. Adım: Roma rakamını sayıya çevir
    total = 0
    for i in range(len(s)):
        curr = values[s[i]]
        if i + 1 < len(s) and curr < values[s[i + 1]]:
            total -= curr
        else:
            total += curr

    # 2. Adım: Aralık kontrolü (1 - 4999)
    if not (1 <= total <= 4999):
        raise ValueError("Sayı 1 ile 4999 arasında olmalıdır!")

    # 3. Adım: Kurallı yazılış doğrulaması (IIII, VIIII, IC vb. yakalar)
    if int_to_roman(total) != s:
        raise ValueError(f"Geçersiz Roma rakamı dizilimi: {s}")

    return total


def int_to_roman(num: int) -> str:
    # 4999'a kadar desteklemek için M'ler başta döner
    mapping = [
        (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
        (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
        (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")
    ]
    res = []
    for val, sym in mapping:
        while num >= val:
            res.append(sym)
            num -= val
    return "".join(res)


# --- Test ---
if __name__ == "__main__":
    girdi = input("Roma rakamı girin (1-4999): ")
    try:
        sonuc = roman_to_int(girdi)
        print(f"Sonuç: {sonuc}")
    except ValueError as e:
        print(f"Hata: {e}")
