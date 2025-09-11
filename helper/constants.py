import pycountry

EMAIL = r"^[^@]+@[^@]+\.[^@]+$"
ISO_CURRENCIES = {c.alpha_3 for c in pycountry.currencies}
