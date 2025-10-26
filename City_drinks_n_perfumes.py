import sys
import textwrap
from hashlib import md5

CITIES = [
    "Diomira", "Isidora", "Dorothea", "Zaira", "Anastasia",
    "Tamara", "Zora", "Despina", "Zirma", "Isaura",
    "Maurilia", "Fedora", "Zoe", "Zenobia", "Euphemia",
    "Zobeide", "Hypatia", "Armilla", "Chloe", "Valdrada",
    "Olivia", "Sophronia", "Eutropia", "Zemrude", "Aglaura",
    "Octavia", "Ersilia", "Baucis", "Leandra", "Melania",
    "Esmeralda", "Phyllis", "Pyrrha", "Adelma", "Eudoxia",
    "Moriana", "Clarice", "Eusapia", "Beersheba", "Leonia",
    "Irene", "Argia", "Thekla", "Trude", "Olinda",
    "Laudomia", "Perinthia", "Procopia", "Raissa", "Andria",
    "Cecilia", "Marozia", "Penthesilea", "Theodora", "Berenice"
]

# Curated lists of drinks and perfumes (examples; change as you like)
DRINKS = [
    "Negroni", "Old Fashioned", "Manhattan", "Martini", "Aperol Spritz",
    "Sazerac", "Mojito", "Daiquiri", "French 75", "Whiskey Sour",
    "Espresso Martini", "Paloma", "Gimlet", "Sidecar", "Tom Collins"
]

COLOGNES_AND_PERFUMES = [
    "Chanel No.5 (classic aldehydic floral)",
    "Dior Sauvage (fresh aromatic)",
    "Jo Malone English Pear & Freesia (fruity floral)",
    "Tom Ford Oud Wood (warm woody)",
    "Le Labo Santal 33 (smoky woody)",
    "Guerlain Shalimar (oriental vanilla)",
    "Maison Francis Kurkdjian Baccarat Rouge 540 (amber floral)",
    "Byredo Gypsy Water (fresh woody)",
    "Creed Aventus (fruity chypre)",
    "Hermès Eau de Rhubarbe Écarlate (tart fruity)"
]

def deterministic_choice(key: str, options: list):
    """Return a deterministic choice from options based on key."""
    h = md5(key.encode("utf-8")).hexdigest()
    idx = int(h, 16) % len(options)
    return options[idx]

def recommend_drink(city: str) -> str:
    """Return a drink recommendation for a city."""
    # We'll make the recommendation feel 'poetic' by combining a base drink
    # with a short flavor-note derived from city name length / characters.
    base = deterministic_choice(city + "_drink", DRINKS)
    flavor_note = ""
    if any(ch in city.lower() for ch in "z"):
        flavor_note = "—an exotic, slightly bitter twist"
    elif len(city) <= 5:
        flavor_note = "—a bright, citrus-forward sip"
    elif len(city) >= 8:
        flavor_note = "—a deep, contemplative pour"
    else:
        flavor_note = "—a balanced, elegant choice"
    return f"{base} {flavor_note}"

def recommend_perfume(city: str) -> str:
    """Return a perfume recommendation for a city."""
    perfume = deterministic_choice(city + "_perfume", COLOGNES_AND_PERFUMES)
    # Add a short phrase that links scent to the city's 'mood'
    if city.endswith("a") or city.endswith("e"):
        mood = "soft, feminine elegance"
    elif city[0].lower() in "aeiou":
        mood = "airy, luminous presence"
    else:
        mood = "bold presence with warm undertones"
    return f"{perfume} — evokes {mood}."

def show_cities():
    print("Italo Calvino — Invisible Cities (55 cities)\n")
    for i, c in enumerate(CITIES, start=1):
        print(f"{i:2d}. {c}")
    print()

def find_city_by_input(user_input: str):
    # allow number or name (case-insensitive)
    user_input = user_input.strip()
    if user_input.isdigit():
        idx = int(user_input) - 1
        if 0 <= idx < len(CITIES):
            return CITIES[idx]
        else:
            return None
    # match by name (case-insensitive)
    for c in CITIES:
        if c.lower() == user_input.lower():
            return c
    # partial match: startswith or contains
    lowered = user_input.lower()
    matches = [c for c in CITIES if lowered in c.lower()]
    return matches[0] if len(matches) == 1 else None

def main():
    show_cities()
    prompt = textwrap.dedent("""\
        Pick a city by number or name (e.g. '7' or 'Zora').
        Type 'q' to quit.
    """)
    while True:
        choice = input(prompt + "Your choice: ").strip()
        if choice.lower() in ('q', 'quit', 'exit'):
            print("Goodbye — may your journeys be imaginary and fragrant.")
            sys.exit(0)
        city = find_city_by_input(choice)
        if not city:
            print("Couldn't find that city. Try a number or the exact name (or part of it).")
            continue
        drink = recommend_drink(city)
        print(f"\nFor {city}, I recommend: {drink}\n")
        # Next phase: perfume
        next_phase = input("Would you like a perfume recommendation for this city? (y/n): ").strip().lower()
        if next_phase in ('y', 'yes'):
            perfume = recommend_perfume(city)
            print(f"Perfume suggestion for {city}: {perfume}\n")
        else:
            print("No perfume this time — enjoy your drink.\n")
        another = input("Pick another city? (y/n): ").strip().lower()
        if another not in ('y', 'yes'):
            print("Farewell. If you'd like, run the script again to explore more pairings.")
            break

if __name__ == "__main__":
    main()
