import re


def parse_salary(salary_str):
    """
    Parse salary string menjadi (salary_min, salary_max) dalam satuan Rupiah.
    Return (None, None) kalau tidak bisa di-parse.
    """
    if not salary_str or salary_str.strip().lower() in ("none", "negotiable", "-"):
        return None, None

    s = salary_str.upper()

    # Cek apakah ada satuan "JUTA" atau "JT"
    is_juta = "JUTA" in s or "JT" in s

    # Ekstrak semua angka dari string (abaikan non-digit)
    numbers = re.findall(r"[\d.,]+", s)
    if not numbers:
        return None, None

    def to_int(n):
        # Buang titik dan koma, convert ke int
        cleaned = re.sub(r"[.,]", "", n)
        return int(cleaned)

    values = [to_int(n) for n in numbers]

    salary_min = values[0]
    salary_max = values[1] if len(values) > 1 else values[0]

    if is_juta:
        salary_min *= 1_000_000
        salary_max *= 1_000_000

    return salary_min, salary_max
