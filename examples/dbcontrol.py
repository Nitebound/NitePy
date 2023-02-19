import mariadb


DBROOT = {
    'user': 'root',
    'password': 'crYpt1q?',
    'host': '192.168.0.102',
    'port': 3306,
    'database': 'netgame'
}


def create_user(username, user_pass):
    try:
        if username_available(username):
            conn = mariadb.connect(**DBROOT)
            cur = conn.cursor()
            cur.execute(f"INSERT INTO user (username, password) VALUES ('{username}', '{user_pass}')")
            print(f"{cur.rowcount} rows added to user table")
            conn.commit()
            conn.close()
            return True
    except mariadb.Error as e:
        print(f"An error occurred while trying to add user. Error: {e}")

    return False


def username_available(username):
    try:
        conn = mariadb.connect(**DBROOT)
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM user WHERE username = '{username}'")

        if cur.rowcount > 0:
            print("This username is already taken! Please try another.")
            conn.close()
            return False
        else:
            print("This username is available!")
            conn.close()
            return True

    except mariadb.Error as e:
        print(f"An error occurred querying the database. Error: {e}")


def login(username, password):
    try:
        conn = mariadb.connect(**DBROOT)
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM user WHERE username = '{username}'")

        if cur.rowcount > 0:
            true_pass = cur.fetchall()[0][2]
            if password == true_pass:
                return True
            conn.close()
            return True
        else:
            conn.close()
            return False

    except mariadb.Error as e:
        print(f"An error occurred querying the database. Error: {e}")


