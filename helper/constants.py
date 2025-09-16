import pycountry

EMAIL = r"^[^@]+@[^@]+\.[^@]+$"
ISO_CURRENCIES = {c.alpha_3 for c in pycountry.currencies}
ISO_COUNTRIES = {c.alpha_3 for c in pycountry.countries} | {c.alpha_2 for c in pycountry.countries}
