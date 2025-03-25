import sqlite3

DB_PATH = "actions/restaurant.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS daily_menu")
    cursor.execute("DROP TABLE IF EXISTS allergens")

    # Table des réservations
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reservations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            guests INTEGER NOT NULL,
            date_time TEXT NOT NULL,
            comment TEXT,
            booking_number TEXT UNIQUE
        )
    """)

    # Table du menu du jour sans la contrainte UNIQUE sur 'date'
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS daily_menu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            menu TEXT NOT NULL
        )
    """)

    # Table des allergènes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS allergens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ingredient TEXT UNIQUE NOT NULL
        )
    """)

    # Table du restaurant (une seule ligne avec le nombre max de places)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS restaurant (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            max_seats INTEGER NOT NULL
        )
    """)

    # Ajouter un menu pour le 25 mars 2025
    menu_data = [
        ('2025-03-25', 'Lasagnes végétariennes'),
        ('2025-03-26', 'Poulet rôti et pommes de terre'),
        ('2025-03-27', 'Salade César'),
        ('2025-03-28', 'Tarte aux pommes')
    ]

    cursor.executemany("INSERT INTO daily_menu (date, menu) VALUES (?, ?)", menu_data)

    # Ajouter des allergènes fictifs
    allergenes_data = [
        ('Gluten',),
        ('Lactose',),
        ('Fruits à coque',),
        ('Soja',),
        ('Œufs',)
    ]

    cursor.executemany("INSERT INTO allergens (ingredient) VALUES (?)", allergenes_data)

    # Vérifier si une entrée pour le restaurant existe, sinon en ajouter une par défaut
    cursor.execute("SELECT COUNT(*) FROM restaurant")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO restaurant (max_seats) VALUES (?)", (50,))  # Exemple : 50 places

    conn.commit()
    conn.close()

init_db()
