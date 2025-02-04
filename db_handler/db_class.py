import datetime
import sqlite3

class DatabaseHandler(object):
    def __init__(self, file: str):
        self.file = file
        self.cursor = None
        self.conn = None
        self.conn = sqlite3.connect(self.file)
        self.cursor = self.conn.cursor()

    async def init(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS users (id BIGINT PRIMARY KEY, chosen_mode TINYINT DEFAULT 0);")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS user_finances (id BIGINT, money INT NOT NULL, "
                            "time_period DATE NOT NULL, primary key (id, time_period));")
        self.conn.commit()

    async def add_user(self, user_id: int) -> None:
        self.cursor.execute("INSERT INTO users (id) VALUES (?)", (user_id,))
        self.conn.commit()
        print("[DATABASE] Called 'add_user'")

    async def add_finances(self, user_id: int, money: int) -> None:
        date = datetime.date.today()
        qry = "SELECT 1 FROM user_finances WHERE id = ? AND time_period = ?"
        self.cursor.execute(qry, (user_id, date))
        result = self.cursor.fetchall()
        if result:
            self.cursor.execute("UPDATE user_finances SET money = money + ? WHERE id = ? AND time_period = ?", (money, user_id, date))
        else:
            self.cursor.execute("INSERT INTO user_finances VALUES (?, ?, ?)", (user_id, money, date))
        self.conn.commit()
        print("[DATABASE] Called 'add_finances'")

    async def set_finances(self, user_id: int, money: int) -> None:
        date = datetime.date.today()
        qry = "SELECT 1 FROM user_finances WHERE id = ? AND time_period = ?"
        self.cursor.execute(qry, (user_id, date))
        result = self.cursor.fetchall()
        if result is not None:
            self.cursor.execute("UPDATE user_finances SET money = ? WHERE id = ? AND time_period = ?", (money, user_id, date))
        else:
            self.cursor.execute("INSERT INTO user_finances VALUES (?, ?, ?)", (user_id, money, date))
        self.conn.commit()
        print("[DATABASE] Called 'set_finances'")

    async def get_total_finances_by_date(self, user_id: int, date: datetime.date = None) -> int | None:
        if date is None:
            date = datetime.date.today()
        qry = "SELECT money FROM user_finances WHERE id = ? AND time_period = ?"
        self.cursor.execute(qry, (user_id, date))
        self.conn.commit()
        result = self.cursor.fetchall()
        print("[DATABASE] Called 'get_total_finances'")
        return result[0][0]

    async def get_total_finances(self, user_id: int) -> int | None:
        qry = "SELECT SUM(money) FROM user_finances WHERE id = ?"
        self.cursor.execute(qry, (user_id,))
        self.conn.commit()
        result = self.cursor.fetchall()
        print("[DATABASE] Called 'get_total_finances'")
        return result[0][0]

    async def get_total_finances_period(self, user_id: int, date1: datetime.date, date2: datetime.date = None) -> int | None:
        qry = "SELECT SUM(money) FROM user_finances WHERE id = ? AND time_period between ? AND ?;"
        if date2 is None:
            date2 = datetime.date.today()
        self.cursor.execute(qry, (user_id, date1, date2))
        self.conn.commit()
        result = self.cursor.fetchall()
        print("[DATABASE] Called 'get_total_finances_period'")
        return result[0][0]

    async def get_finances(self, user_id: int) -> list | None:
        qry = "SELECT money, time_period FROM user_finances WHERE id = ?;"
        self.cursor.execute(qry, (user_id,))
        self.conn.commit()
        result = self.cursor.fetchall()
        print("[DATABASE] Called 'get_finances'")
        return result

    async def get_finances_period(self, user_id: int, date1: datetime.date, date2: datetime.date = None) -> list | None:
        qry = "SELECT money FROM user_finances WHERE id = ? AND time_period between ? AND ?;"
        if date2 is None:
            date2 = datetime.date.today()
        self.cursor.execute(qry, (user_id, date1, date2))
        self.conn.commit()
        result = self.cursor.fetchall()
        print("[DATABASE] Called 'get_finances_period'")
        return result[0]

    async def change_mode(self, user_id: int, mode: int) -> None:
        self.cursor.execute("UPDATE users SET chosen_mode = ? WHERE id = ?", (mode, user_id))
        self.conn.commit()
        print("[DATABASE] Called 'change_mode'")
