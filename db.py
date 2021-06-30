from debugger import debug

import sqlite3 as sql


class MyTelegramDB:
    """SQL DB for storing data from VK, Spotify, Telegram bot"""

    def __init__(
            self,
            db_name: str
    ):
        self.__db_name = db_name
        self.__con = None
        self.__cur = None
        debug("Created MyTelegramDB object")

    def __del__(self):
        debug("Deleted MyTelegramDB object")

    def connect_db(self):
        self.__con = sql.connect(self.__db_name)

    def cursor_db(self):
        self.__cur = self.__con.cursor()

    def commit_db(self):
        self.__con.commit()

    def close_cursor_db(self):
        self.__cur.close()

    def close_db(self):
        self.__con.close()

    def create_table_db(self):
        self.__cur.execute("""
            CREATE TABLE
            IF NOT EXISTS
            `main` (
                `telegram_user_id` STRING, 
                `vk_group_name` STRING, 
                `spotify_pid` STRING, 
                `last_vk_post_date_time`: STRING)
        """)

    def set_values_db(self, telegram_user_id, vk_group_name, spotify_pid):
        self.__cur.execute(f"""
            INSERT INTO `main`
            VALUES ('{telegram_user_id}', '{vk_group_name}', '{spotify_pid}')
        """)

    def get_values_db(self):
        pass

    def delete_values_db(self):
        pass


if __name__ == "__main__":
    name = "vk_to_spoti_telegram.db"


if __name__ == "__main__/":
    print("1 - добавление\n2 - получение")
    choice = int(input("> "))
    con = sql.connect('test.db')
    with con:
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS `test` (`name` STRING, `surname` STRING)")

        if choice == 1:
            name = input("Name\n> ")
            surname = input("Surname\n> ")
            cur.execute(f"INSERT INTO `test` VALUES ('{name}', '{surname}')")
        elif choice == 2:
            cur.execute("SELECT * FROM `test`")
            rows = cur.fetchall()
            for row in rows:
                print(row[0], row[1])
        else:
            print("Вы ошиблись")

        con.commit()
        cur.close()
