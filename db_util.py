import sqlite3
def create_table():
    # Устанавливаем соединение с базой данных
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()

    # Создаем таблицу Users
    cursor.execute('''
    CREATE TABLE "product" (
	"product_name"	TEXT,
	"product_calorie"	REAL
);
    ''')

    # Сохраняем изменения и закрываем соединение
    connection.commit()
    connection.close()
# CREATE TABLE "product" (
# 	"product_name"	TEXT,
# 	"product_calorie"	REAL
# );
# INSERT INTO product (product_name, product_calorie) VALUES ('apple',47);
# INSERT INTO product (product_name, product_calorie) VALUES ('orange',43);
# INSERT INTO product (product_name, product_calorie) VALUES ('banana', 88);
# INSERT INTO product (product_name, product_calorie) VALUES ('pizza', 250);

# SELECT product_calorie from product WHERE product_name = 'pizza'
def get_calorie_by_name(product_name):
    select = 'SELECT product_calorie from product WHERE product_name = '+ product_name
    print(select)
print(get_calorie_by_name('banana'))