
import sqlite3


conex=sqlite3.connect("BD")
puntero=conex.cursor()

puntero.execute("DROP TABLE IF EXISTS PRODUCTOS")

puntero.execute("""
    CREATE TABLE IF NOT EXISTS PRODUCTOS (
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        Nombre VARCHAR(50), 
        Precio INTEGER, 
        Seccion VARCHAR(20)
    )
""")

puntero.execute("INSERT INTO PRODUCTOS VALUES(NULL,'Balon',15,'DEPORTES')")

puntero.execute("DELETE FROM PRODUCTOS")#limpia la tabla

datos=[
    ('Balon',1,'DEPORTES'),
    ('Balon',152,'DEPORTES'),
    ('Balon',3,'DEPORTES')
]

puntero.executemany("INSERT INTO PRODUCTOS VALUES (NULL,?,?,?)",datos)

puntero.execute("SELECT * FROM "+"PRODUCTOS WHERE Seccion='DEPORTES'")#consulta filtrada
print(puntero.fetchall())

puntero.execute("UPDATE PRODUCTOS SET Precio=100 WHERE Id=2")#consulta filtrada
puntero.execute("DELETE FROM PRODUCTOS WHERE Id=4")

conex.commit()
conex.close()






