from decimal import Decimal, ROUND_HALF_UP

UNITS = [
    "zéro","un","deux","trois","quatre","cinq","six","sept","huit","neuf",
    "dix","onze","douze","treize","quatorze","quinze","seize","dix-sept","dix-huit","dix-neuf"
]
TENS = ["","", "vingt","trente","quarante","cinquante","soixante","soixante","quatre-vingt","quatre-vingt"]

def _under_100(n: int) -> str:
    if n < 20:
        return UNITS[n]
    d, r = divmod(n, 10)
    if d in (7, 9):  # 70-79, 90-99
        return TENS[d] + "-" + UNITS[10 + r]
    if r == 0:
        return TENS[d]
    return TENS[d] + "-" + UNITS[r]

def _under_1000(n: int) -> str:
    c, r = divmod(n, 100)
    if c == 0:
        return _under_100(r)
    if c == 1:
        return "cent" + ("" if r == 0 else " " + _under_100(r))
    return UNITS[c] + " cent" + ("" if r == 0 else " " + _under_100(r))

def nombre_en_lettres(n: int) -> str:
    if n < 1000:
        return _under_1000(n)
    milliers, reste = divmod(n, 1000)
    if milliers == 1:
        texte = "mille"
    else:
        texte = _under_1000(milliers) + " mille"
    if reste:
        texte += " " + _under_1000(reste)
    return texte

def montant_en_lettres_fr(amount) -> str:
    """Montant en toutes lettres (FR) — dinars + centimes."""
    if amount is None:
        return "zéro dinars"
    amt = Decimal(str(amount)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    dinars = int(amt)
    centimes = int((amt - Decimal(dinars)) * 100)
    parts = [f"{nombre_en_lettres(dinars)} dinars"]
    if centimes:
        parts.append(f"{nombre_en_lettres(centimes)} centimes")
    return " et ".join(parts)
