import sqlite3
from datetime import datetime

def create_db():
    conn = sqlite3.connect('database.db')
    curr = conn.cursor()
    curr.execute('''
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            username UNIQUE,
            fullname VARCHAR(35)
        )
    ''')
    curr.execute('''
        CREATE TABLE IF NOT EXISTS plans(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id VARCHAR(35),
            plan VARCHAR(1000),
            date DATETIME,
            status INTEGER
        )
    ''')
    curr.execute('''
    CREATE TABLE IF NOT EXISTS saveup(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id VARCHAR(35) UNIQUE,
        money INTEGER
    )
    ''')
    conn.commit()
    conn.close()

def add_user(user_id, username, fullname):
    conn = sqlite3.connect('database.db')
    curr = conn.cursor()
    money = '0'
    # curr.execute('INSERT INTO saveup(money) VALUES(?, ?) WHERE user_id = ?', (money, user_id))
    try:
        money = '0'
        curr.execute('INSERT INTO saveup(user_id, money) VALUES(?, ?)', (user_id, money))
    except:
        pass
    try:
        curr.execute('INSERT INTO users(user_id, username, fullname) VALUES(?, ?, ?)', (user_id, username, fullname))
    except:
        pass
    conn.commit()
    conn.close()

# add_user(123456, 'sdcfvg', 'test')


def add_plan(user_id, plan, status):
    date = datetime.today()
    conn = sqlite3.connect('database.db')
    curr = conn.cursor()
    curr.execute('INSERT INTO plans(user_id, plan, date, status) VALUES(?, ?, ?, ?)', (user_id, plan, date, status))
    conn.commit()
    conn.close()



def get_plans(user_id):
    conn = sqlite3.connect('database.db')
    curr = conn.cursor()
    curr.execute('SELECT * FROM plans WHERE user_id = ?', (user_id,))
    plans = curr.fetchall()
    conn.close()
    return plans

def check_one_plan(user_id, pk):
    conn = sqlite3.connect('database.db')
    curr = conn.cursor()
    curr.execute('SELECT * FROM plans WHERE user_id = ? AND id = ?', (user_id, pk))
    plan = curr.fetchall()
    conn.close()
    return plan

    def change_status(user_id, pk, status):
        conn = sqlite3.connect('database.db')
        curr = conn.cursor()
        curr.execute('UPDATE plans SET status = ? WHERE user_id = ? AND id = ?', (status, user_id, pk))
        conn.commit()
        conn.close()


def edit_plan(user_id, plan_id):
    conn = sqlite3.connect('database.db')
    curr = conn.cursor()
    curr.execute('UPDATE plans SET plan = ? WHERE id = ?', (plan_id, user_id))
    conn.commit()
    conn.close()

def delete_plan(id, user_id):
    conn = sqlite3.connect('database.db')
    curr = conn.cursor()
    query = "DELETE FROM plans WHERE id = ? and user_id = ?"
    curr.execute(query, (id, user_id))
    conn.commit()
    conn.close()

def edit_plan(user_id, new_plan, plan_id):
    conn = sqlite3.connect('database.db')
    curr = conn.cursor()
    curr.execute('UPDATE plans SET plan = ? WHERE user_id = ? AND id = ?', (new_plan, user_id, plan_id))
    conn.commit()
    conn.close()


def check_plan_id(user_id, pk):
    conn = sqlite3.connect('database.db')
    curr = conn.cursor()
    query = "SELECT id FROM plans where user_id = ?"
    data = curr.execute(query, (user_id, )).fetchall()
    for i in enumerate(data):
        if i[0] + 1 == pk:
            return i[1][0]

        # print(check_plan_id(3, 7049119939))



        # a = 45
        # # def delete_plan(user_id, plan):
        # for i in enumerate(get_plans(7049119939)):
        #     if i[0] == a:
        #         print(i[1][0])
        #         break


def save_up_add_money(user_id, money):
    conn = sqlite3.connect('database.db')
    curr = conn.cursor()
    money_pk = curr.execute('SELECT money FROM saveup WHERE user_id = ?', (user_id,)).fetchone()
    if money_pk[0] is not None:
        curr.execute('UPDATE saveup SET money = ? WHERE user_id = ?', (money + money_pk[0], user_id))
    else:
        print('error')
    conn.commit()
    conn.close()

save_up_add_money(123456, 100)

def saved_money(user_id):
    conn = sqlite3.connect('database.db')
    curr = conn.cursor()
    money = curr.execute('SELECT money FROM saveup WHERE user_id = ?', (user_id,)).fetchone()
    conn.close()
    return money

# save_up_add_money(7049119939, 100)

# print(saved_money(7049119939))