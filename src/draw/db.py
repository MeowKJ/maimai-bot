import sqlite3

# 连接到数据库（如果不存在，则会创建一个新的数据库）
conn = sqlite3.connect('local_database.db')

# 创建一个游标对象，用于执行 SQL 语句
cursor = conn.cursor()

# 创建表格（如果不存在）
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        score INTEGER NOT NULL DEFAULT 0
    )
''')

# 提交更改
conn.commit()


def insert_user(user_id, user_name):
    # 插入数据
    cursor.execute('INSERT INTO users (id, name) VALUES (?, ?)', (user_id, user_name))
    conn.commit()


def delete_user(user_id):
    # 删除数据
    cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()


def get_all_users():
    # 获取所有用户数据
    cursor.execute('SELECT * FROM users')
    return cursor.fetchall()


def update_user_name(user_id, new_name):
    # 更新用户姓名
    cursor.execute('UPDATE users SET name = ? WHERE id = ?', (new_name, user_id))
    conn.commit()


def update_or_insert_user(user_id, new_name):
    # 使用 INSERT OR REPLACE 语句，如果用户存在则更新，不存在则插入新记录
    cursor.execute('INSERT OR REPLACE INTO users (id, name) VALUES (?, ?)', (user_id, new_name))
    conn.commit()


def updata_user_score(user_id, score):
    # 更新用户分数
    cursor.execute('UPDATE users SET score = ? WHERE id = ?', (score, user_id))
    conn.commit()


def get_user_score(user_id):
    cursor.execute('SELECT score FROM users WHERE id = ?', (user_id,))
    result = cursor.fetchone()  # 获取查询结果的第一行数据
    return result[0] if result else None  # 返回姓名或 None


def get_user_name_by_id(user_id):
    # 使用 SELECT 语句查询用户姓名
    cursor.execute('SELECT name FROM users WHERE id = ?', (user_id,))
    result = cursor.fetchone()  # 获取查询结果的第一行数据
    return result[0] if result else None  # 返回姓名或 None
