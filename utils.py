import re
import json
import sqlite3

from datetime import datetime, timedelta

class NotAdmin(Exception):
    {}

class Database:
    def __init__(self):
        self.connection = sqlite3.connect('member.db', check_same_thread=False)
        self.cur = self.connection.cursor()

        self.cur.execute('''
        CREATE TABLE IF NOT EXISTS Users (
        name TEXT PRIMARY KEY,
        id INTEGET NOT NULL,
        reason TEXT NOT NULL
        )
        ''')

        self.cur.execute('''
        CREATE TABLE IF NOT EXISTS Admin (
        name TEXT PRIMARY KEY
        )
        ''')

        self.connection.commit()
    
    def write_to(self, name, id, reason):
        try:
            self.cur.execute('INSERT INTO Users (name, id, reason) VALUES (?, ?, ?)', (name, id, reason))
            self.connection.commit()
        except sqlite3.IntegrityError:
            self.cur.execute('UPDATE USERS SET reason = ? WHERE id = ?',(reason, id))
            self.connection.commit()

    def read(self, name):
        self.cur.execute('SELECT id FROM Users WHERE name=?', (name))
        return self.cur.fetchall()
    
    def delete_from(self, name):
        self.cur.execute('DELETE FROM Users WHERE name=?', (name))
        self.connection.commit()

    def add_admin(self, name):
        try:
            self.cur.execute('INSERT INTO Admin (name) VALUES (?)', (name,))
            self.connection.commit()
        except:
            pass
    
    def check_admin(self, name):
        if self.cur.execute('SELECT * FROM Admin WHERE name = ?', (name,)).fetchall():
            return True
        return False
    
    def get_admin(self):
        return self.cur.execute('SELECT * FROM Admin').fetchall()
    
    def get_mute(self):
        return self.cur.execute('SELECT * FROM Users WHERE reason="mute"').fetchall()
    
    def get_ban(self):
        return self.cur.execute('SELECT * FROM Users WHERE reason="ban"').fetchall()


def calc_time(time: str | None):
    if not time:
        return None
    
    re_match = re.match(r"(\d+)([a-z])", time.lower().strip())
    now = datetime.now()

    if re_match:
        val = int(re_match.group(1))
        unit = re_match.group(2)

        match unit:
            case "h": delta = timedelta(hours = val)
            case "d": delta = timedelta(days = val)
            case "w": delta = timedelta(weeks = val)
            case _: return None
    else:
        return None
    
    return now + delta

def read_from_file(filename, name):
    with open(filename, 'r', encoding="utf-8") as file:
        data = json.load(file) 
        return data[name]

def write_to_log(filename, txt):
    with open(filename, 'a', encoding='utf-8') as f:
       f.write('\n' + txt)

