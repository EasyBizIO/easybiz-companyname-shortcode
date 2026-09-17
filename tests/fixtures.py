"""Shared test data — not collected by pytest (no test_ prefix)."""

# Golden examples from the ENG-1192 ticket body — every row of its example table
# (excluding the last "3 Delhaize in one company" row, which is about step 4
# uniqueness/suffixing and out of scope for the pure packer).
TICKET_EXAMPLES = [
    ("Delhaize", "DELHAIZE"),
    ("Delhaize Belgique SA", "DELHAIZEBE"),
    ("Delhaize Luxembourg S.A.", "DELHAIZELU"),
    ("ArcelorMittal", "ARCELORMIT"),
    ("Arcelor Mittal Luxembourg S.A.", "ARCELORMIL"),
    ("Banque Internationale à Luxembourg S.A.", "BANQUEINLU"),
    ("L'Oréal Paris", "LOREALPARI"),
    ("Café Müller GmbH & Co. KG", "CAFEMULLER"),
    ("Amazon EU S.à r.l.", "AMAZONEU"),
    ("Ørsted A/S", "ORSTED"),
    ("Straßenbau und Tiefbau GmbH", "STRASSENBT"),
    ("Łukasiewicz Sp. z o.o.", "LUKASIEWIC"),
    ("De Nederlandsche Bank N.V.", "NEDERLANDB"),
    ("Æthelred Holdings Ltd", "AETHELREDH"),
    ("The Group SA", "GROUP"),
    ("Jean-Claude Van Damme", "JEANCLADAM"),
    ("POST Luxembourg", "POSTLUXEMB"),
    ("SE Banken", "SEBANKEN"),
    ("La Se Rena", "SERENA"),
]
