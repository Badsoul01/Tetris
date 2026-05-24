import sqlite3


class DatabaseManager:

    def __init__(self):
        self.connection = sqlite3.connect("highscores.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS high_score(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, score INTEGER, level INTEGER,pieces INTEGER)")
        self.connection.commit()


    def save_score(self,name,score,level,pieces):
        sql_query= "INSERT INTO high_score(name,score,level,pieces) VALUES (?,?,?,?)"

        values = (name, score, level, pieces)

        self.cursor.execute(sql_query, values)


        self.connection.commit()


    def top_ten(self):
        sql_query = "SELECT name,score,level,pieces FROM high_score ORDER BY score DESC LIMIT 10"
        self.cursor.execute(sql_query)

        return self.cursor.fetchall()
hra = DatabaseManager()
