import csv
import os

ARCHIVO = "expedientes.csv"

# Si el archivo no existe, lo creamos con encabezados
if not os.path.exists(ARCHIVO):
    with open(ARCHIVO, mode="w", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        escritor.writerow(["Numero", "Cliente", "Materia", "Estado", "Fecha", "Notas"])


def agregar_expediente():
    numero = input("Número de expediente: ")
    cliente = input("Nombre del cliente: ")
    materia = input("Materia (civil, familiar, etc.): ")
    estado = input("Estado del asunto (activo, concluido, en pausa): ")
    fecha = input("Fecha de inicio (YYYY-MM-DD): ")
    notas = input("Notas adicionales: ")

    with open(ARCHIVO, mode="a", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        escritor.writerow([numero, cliente, materia, estado, fecha, notas])

    print("✅ Expediente agregado con éxito.")


def listar_expedientes():
    print("\n📂 Lista de expedientes:\n")
    with open(ARCHIVO, mode="r", encoding="utf-8") as f:
        lector = csv.reader(f)
        encabezados = next(lector)
        print(" | ".join(encabezados))
        print("-" * 70)
        for fila in lector:
            print(" | ".join(fila))
    print()

def buscar_expediente():
    criterio = input("Buscar por (1) Número o (2) Nombre de cliente: ")

    if criterio not in ["1", "2"]:
        print("❌ Opción inválida.")
        return

    termino = input("Escribe el dato a buscar: ").lower()

    encontrado = False
    with open(ARCHIVO, mode="r", encoding="utf-8") as f:
        lector = csv.reader(f)
        encabezados = next(lector)
        print("\n🔍 Resultados encontrados:\n")
        print(" | ".join(encabezados))
        print("-" * 70)
        for fila in lector:
            if criterio == "1" and termino in fila[0].lower():
                print(" | ".join(fila))
                encontrado = True
            elif criterio == "2" and termino in fila[1].lower():
                print(" | ".join(fila))
                encontrado = True

    if not encontrado:
        print("❌ No se encontraron resultados.")

def editar_expediente():
    numero_buscar = input("Número del expediente a editar: ")

    expedientes = []
    encontrado = False

    with open(ARCHIVO, mode="r", encoding="utf-8") as f:
        lector = csv.reader(f)
        encabezados = next(lector)
        expedientes.append(encabezados)
        for fila in lector:
            if fila[0] == numero_buscar:
                print("Expediente encontrado. Déjalo en blanco si no quieres cambiar ese campo.")
                nuevo_cliente = input(f"Cliente ({fila[1]}): ") or fila[1]
                nueva_materia = input(f"Materia ({fila[2]}): ") or fila[2]
                nuevo_estado = input(f"Estado ({fila[3]}): ") or fila[3]
                nueva_fecha = input(f"Fecha ({fila[4]}): ") or fila[4]
                nuevas_notas = input(f"Notas ({fila[5]}): ") or fila[5]

                fila = [fila[0], nuevo_cliente, nueva_materia, nuevo_estado, nueva_fecha, nuevas_notas]
                encontrado = True
            expedientes.append(fila)

    if not encontrado:
        print("❌ No se encontró el expediente.")
        return

    with open(ARCHIVO, mode="w", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        escritor.writerows(expedientes)

    print("✅ Expediente actualizado.")

def eliminar_expediente():
    numero_buscar = input("Número del expediente a eliminar: ")

    expedientes = []
    eliminado = False

    with open(ARCHIVO, mode="r", encoding="utf-8") as f:
        lector = csv.reader(f)
        encabezados = next(lector)
        expedientes.append(encabezados)
        for fila in lector:
            if fila[0] != numero_buscar:
                expedientes.append(fila)
            else:
                eliminado = True

    if not eliminado:
        print("❌ No se encontró el expediente.")
        return

    with open(ARCHIVO, mode="w", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        escritor.writerows(expedientes)

    print("🗑️ Expediente eliminado.")




def menu():
    while True:
        print("\n---- Sistema de Expedientes ----")
        print("1. Agregar expediente")
        print("2. Ver todos los expedientes")
        print("3. Buscar expediente")
        print("4. Editar expediente")
        print("5. Eliminar expediente")
        print("6. Salir")

        opcion = input("Elige una opción: ")

        if opcion == "1":
            agregar_expediente()
        elif opcion == "2":
            listar_expedientes()
        elif opcion == "3":
            buscar_expediente()
        elif opcion == "4":
            editar_expediente()
        elif opcion == "5":
            eliminar_expediente()
        elif opcion == "6":
            print("¡Hasta luego!")
            break
        else:
            print("❌ Opción inválida. Intenta de nuevo.")



menu()
