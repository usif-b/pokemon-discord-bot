import sqlite3

db = sqlite3.connect('pokemonbot')

cursor = db.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users(
        ID INTEGER PRIMARY KEY,
        lastDropTime DATETIME
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Pokemon(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        userID INTEGER,
        pokemonName TEXT,
        pokemonID INTEGER
    )
''')

db.commit()