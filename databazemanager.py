import sqlite3


class DatabaseManager:

    def __init__(self):
        self.connection = sqlite3.connect("highscores.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS high_score(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, score INTEGER, level INTEGER,pieces INTEGER,rows INTEGER)")
        self.connection.commit()


    def save_score(self,name,score,level,pieces,rows):
        sql_query= "INSERT INTO high_score(name,score,level,pieces,rows) VALUES (?,?,?,?,?)"

        values = (name, score, level, pieces,rows)

        self.cursor.execute(sql_query, values)


        self.connection.commit()


    def top_ten(self):
        sql_query = "SELECT name,score,level,pieces,rows FROM high_score ORDER BY score DESC LIMIT 10"
        self.cursor.execute(sql_query)

        return self.cursor.fetchall()


    def get_highest_score(self):
        sql_query = "SELECT name,score FROM high_score ORDER BY score DESC LIMIT 1"
        self.cursor.execute(sql_query)
        return self.cursor.fetchone()
    