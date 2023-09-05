
import sqlite3

db = sqlite3.connect('users.db')

username = 'test_user'
password = 'test_password'

db.execute(
    'INSERT INTO gebruikers (username, password) VALUES (?, ?)',
    (username, password)
)

db.commit()