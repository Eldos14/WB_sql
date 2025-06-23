import requests
import sqlite3 as sql
import random
import time

proxies = {
    "http": "http://5435d268bba805db9446__cr.kz:1ce35e8a9661e50b@gw.dataimpulse.com:10009",
    "https": "http://5435d268bba805db9446__cr.kz:1ce35e8a9661e50b@gw.dataimpulse.com:10019"
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
}

conn = sql.connect("cotalog.db")
c = conn.cursor()


c.execute("""
CREATE TABLE IF NOT EXISTS WB ( 
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    characteristics TEXT,
    price INT,
    article INT
)
""")


random_articles = [random.randint(1000000, 99999999) for _ in range(100)]


for article in random_articles:
    try:
        part = str(article)
        url = f"https://alm-basket-cdn-02.geobasket.ru/vol{part[0:3]}/part{part[0:5]}/{part}/info/ru/card.json"

        response = requests.get(url, headers=headers, proxies=proxies, timeout=10)
        if response.status_code != 200:
            print(f"[{article}] Нет url: {response.status_code}")
            continue

        try:
            data = response.json()
        except ValueError:
            print(f"[{article}] Ошибка при декодировании JSON")
            continue

        name = data.get('imt_name', 'Нет данных')
        description = data.get('description', 'Нет описания')
        price = data.get('priceU')
        

        print(f"Товар {article} — {name}, цена: {price} руб.")

     
        c.execute("""
            INSERT INTO WB (name, characteristics, price, article)
            VALUES (?, ?, ?, ?)
        """, (name, description, price, article))

        time.sleep(1)

    except Exception as e:
        print(f"[{article}] Ошибка: {e}")
        continue


c.execute('SELECT * FROM WB WHERE price < 10000')
results = c.fetchall()
for row in results:
    print(row)

conn.commit()
conn.close()
