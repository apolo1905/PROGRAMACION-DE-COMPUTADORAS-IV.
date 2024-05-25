import sqlite3

# Conexión a la base de datos SQLite
def conectar_db():
    return sqlite3.connect('recetas.db')

# Crear las tablas si no existen
def crear_tablas(): 
    with conectar_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS recetas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ingredientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                receta_id INTEGER,
                ingrediente TEXT NOT NULL,
                FOREIGN KEY (receta_id) REFERENCES recetas(id)
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pasos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                receta_id INTEGER,
                paso TEXT NOT NULL,
                FOREIGN KEY (receta_id) REFERENCES recetas(id)
            )
        ''')
        conn.commit()

# Agregar nueva receta
def agregar_receta():
    nombre = input("Nombre de la receta: ")
    with conectar_db() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO recetas (nombre) VALUES (?)", (nombre,))
        receta_id = cursor.lastrowid

        print("Agregar ingredientes (deje vacío para terminar):")
        while True:
            ingrediente = input("Ingrediente: ")
            if ingrediente == "":
                break
            cursor.execute("INSERT INTO ingredientes (receta_id, ingrediente) VALUES (?, ?)", (receta_id, ingrediente))

        print("Agregar pasos (deje vacío para terminar):")
        while True:
            paso = input("Paso: ")
            if paso == "":
                break
            cursor.execute("INSERT INTO pasos (receta_id, paso) VALUES (?, ?)", (receta_id, paso))
        conn.commit()

# Actualizar receta existente
def actualizar_receta():
    receta_id = int(input("ID de la receta a actualizar: "))
    with conectar_db() as conn:
        cursor = conn.cursor()
        nombre = input("Nuevo nombre de la receta (deje vacío para mantener): ")
        if nombre:
            cursor.execute("UPDATE recetas SET nombre = ? WHERE id = ?", (nombre, receta_id))
        
        print("Actualizar ingredientes (deje vacío para terminar):")
        cursor.execute("DELETE FROM ingredientes WHERE receta_id = ?", (receta_id,))
        while True:
            ingrediente = input("Ingrediente: ")
            if ingrediente == "":
                break
            cursor.execute("INSERT INTO ingredientes (receta_id, ingrediente) VALUES (?, ?)", (receta_id, ingrediente))
        
        print("Actualizar pasos (deje vacío para terminar):")
        cursor.execute("DELETE FROM pasos WHERE receta_id = ?", (receta_id,))
        while True:
            paso = input("Paso: ")
            if paso == "":
                break
            cursor.execute("INSERT INTO pasos (receta_id, paso) VALUES (?, ?)", (receta_id, paso))
        conn.commit()

# Eliminar receta existente
def eliminar_receta():
    receta_id = int(input("ID de la receta a eliminar: "))
    with conectar_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM recetas WHERE id = ?", (receta_id,))
        cursor.execute("DELETE FROM ingredientes WHERE receta_id = ?", (receta_id,))
        cursor.execute("DELETE FROM pasos WHERE receta_id = ?", (receta_id,))
        conn.commit()

# Ver listado de recetas
def ver_recetas():
    with conectar_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre FROM recetas")
        recetas = cursor.fetchall()
        for receta in recetas:
            print(f"{receta[0]}. {receta[1]}")

# Buscar ingredientes y pasos de receta
def buscar_receta():
    receta_id = int(input("ID de la receta a buscar: "))
    with conectar_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT nombre FROM recetas WHERE id = ?", (receta_id,))
        receta = cursor.fetchone()
        if receta:
            print(f"Receta: {receta[0]}")
            cursor.execute("SELECT ingrediente FROM ingredientes WHERE receta_id = ?", (receta_id,))
            ingredientes = cursor.fetchall()
            print("Ingredientes:")
            for ingrediente in ingredientes:
                print(f"- {ingrediente[0]}")
            cursor.execute("SELECT paso FROM pasos WHERE receta_id = ?", (receta_id,))
            pasos = cursor.fetchall()
            print("Pasos:")
            for paso in pasos:
                print(f"- {paso[0]}")
        else:
            print("Receta no encontrada")

# Menú principal
def menu():
    crear_tablas()
    while True:
        print("\n--- Libro de Recetas ---")
        print("1) Agregar nueva receta")
        print("2) Actualizar receta existente")
        print("3) Eliminar receta existente")
        print("4) Ver listado de recetas")
        print("5) Buscar ingredientes y pasos de receta")
        print("6) Salir")
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            agregar_receta()
        elif opcion == "2":
            actualizar_receta()
        elif opcion == "3":
            eliminar_receta()
        elif opcion == "4":
            ver_recetas()
        elif opcion == "5":
            buscar_receta()
        elif opcion == "6":
            print("Saliendo...")
            print("gracias por su visita")
            print("vuelva pronto.")
            break
        else:
            print("Opción no válida, imgrese de nuevo.")

if __name__ == "__main__":
    menu()
