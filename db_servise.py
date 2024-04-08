import sqlite3
# необходим метод позволяющий доставать информацию о калорийности по названию определенного объекта

def get_calorie_by_description(description):


    connection = sqlite3.connect('db_products.db')
    cursor = connection.cursor()

    cursor.execute('SELECT product_calorie from product WHERE product_name = ?', (description,))
    results = cursor.fetchall()
    calorie = 0
    for row in results:
        calorie = float(row[0])
        break
    connection.close()
    return calorie
