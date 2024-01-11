import sqlite3


try:
    #init sql
    sqlite_connection = sqlite3.connect('tatarlit.db')
    cursor = sqlite_connection.cursor()
    print("Подключен к SQLite")
   
    #open file
    with open('newdata_book.txt') as file:
        lines = [line.rstrip() for line in file]
    print(len(lines))
    #insert data
    for line in lines:
        print(line)
        data=line.split('|')
        data_=(int(data[0]),data[1],'/home/ips/projects/bd/Tatarby/books/'+data[2],'/home/ips/projects/bd/Tatarby/books/'+data[3],int(data[4]),int(data[5]))
        cursor.execute("DELETE FROM Book WHERE BookName=?",(data[1],))
        sqlite_insert_query = f"""INSERT INTO Book
                          VALUES (?, ?, ?, ?, ?, ?);"""
        cursor.execute(sqlite_insert_query, data_)
        print(sqlite_insert_query)
        sqlite_connection.commit()
        print("Запись успешно вставлена ​​таблицу sqlitedb_developers ", cursor.rowcount)
    cursor.execute("SELECT * FROM Book")
    result = cursor.fetchall()
    print(result) 
    cursor.close()

except sqlite3.Error as error:
    print("Ошибка при работе с SQLite", error)
finally:
    if sqlite_connection:
        sqlite_connection.commit()
        sqlite_connection.close()
        print("Соединение с SQLite закрыто")

