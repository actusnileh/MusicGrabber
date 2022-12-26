import sqlite3 as sq


async def sql_start():
    global db, cur
    db = sq.connect('userinfo.db')
    cur = db.cursor()

    cur.execute(
        'CREATE TABLE IF NOT EXISTS userinfo(user_id TEXT PRIMARY KEY, user_name TEXT)')

    db.commit()


# добавляем юзера
async def sql_add_user(user_id):
    user = cur.execute("SELECT 1 FROM userinfo WHERE user_id = '{key}'".format(key=user_id)).fetchone()
    if not user:
        cur.execute("INSERT INTO userinfo VALUES(?, ?)", (user_id, ''))
        db.commit()


# добавляем сущ. юзеру имя из тг
async def sql_add_user_name(user_name, user_id):
    cur.execute("UPDATE userinfo SET user_name = '{}' WHERE user_id = '{}'".format(user_name, user_id))
    db.commit()
