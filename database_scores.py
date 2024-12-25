import sqlite3

def initialize_database():
    connection = sqlite3.connect("game_times.db")
    cursor = connection.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS PlayerTimes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        player_name TEXT NOT NULL,
        finish_time REAL NOT NULL
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS GlobalTopTimes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        player_name TEXT NOT NULL,
        finish_time REAL NOT NULL
    )''')

    connection.commit()
    connection.close()

def store_player_time(player_name, finish_time):
    connection = sqlite3.connect("game_times.db")
    cursor = connection.cursor()

    cursor.execute("INSERT INTO PlayerTimes (player_name, finish_time) VALUES (?, ?)",
                   (player_name, finish_time))

    connection.commit()
    connection.close()

def update_global_top(player_name, finish_time):
    connection = sqlite3.connect("game_times.db")
    cursor = connection.cursor()


    cursor.execute("SELECT * FROM GlobalTopTimes ORDER BY finish_time ASC")
    top_times = cursor.fetchall()

    if len(top_times) < 10 or finish_time < top_times[-1][2]:

        cursor.execute("INSERT INTO GlobalTopTimes (player_name, finish_time) VALUES (?, ?)",
                       (player_name, finish_time))
        cursor.execute("DELETE FROM GlobalTopTimes WHERE id NOT IN (SELECT id FROM GlobalTopTimes ORDER BY finish_time ASC LIMIT 10)")

    connection.commit()
    connection.close()

def get_player_times(player_name):
    connection = sqlite3.connect("game_times.db")
    cursor = connection.cursor()

    cursor.execute("SELECT finish_time FROM PlayerTimes WHERE player_name = ?", (player_name,))
    times = cursor.fetchall()

    connection.close()
    return times

def get_global_top():
    connection = sqlite3.connect("game_times.db")
    cursor = connection.cursor()

    cursor.execute("SELECT player_name, finish_time FROM GlobalTopTimes ORDER BY finish_time ASC")
    top_times = cursor.fetchall()

    connection.close()
    return top_times