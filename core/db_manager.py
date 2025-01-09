import sqlite3
from datetime import datetime


class DBManager:
    def __init__(self, db_path="game_data.db"):
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                total_coins INTEGER DEFAULT 0,
                total_time TEXT DEFAULT "00:00:00"
            )
        """)

        if not self.get_stats():
            self.cursor.execute("INSERT INTO stats (total_coins, total_time) VALUES (0, '00:00:00')")
            self.connection.commit()

    def get_stats(self):
        self.cursor.execute("SELECT total_coins, total_time FROM stats WHERE id = 1")
        return self.cursor.fetchone()

    def update_coins(self, coins):
        self.cursor.execute("UPDATE stats SET total_coins = total_coins + ? WHERE id = 1", (coins,))
        self.connection.commit()

    def update_time(self, time_played):
        current_time = self.get_stats()[1]
        total_time = self.add_times(current_time, time_played)
        self.cursor.execute("UPDATE stats SET total_time = ? WHERE id = 1", (total_time,))
        self.connection.commit()

    def add_times(self, time1, time2):
        t1 = datetime.strptime(time1, "%H:%M:%S")
        t2 = datetime.strptime(time2, "%H:%M:%S")
        total_seconds = (t1.hour * 3600 + t1.minute * 60 + t1.second) + (t2.hour * 3600 + t2.minute * 60 + t2.second)
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"

    def close(self):
        self.connection.close()
