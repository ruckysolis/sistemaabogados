from flask import Flask, render_template, request, redirect, url_for, Response
import io
import csv
import os
import urllib.parse

app = Flask(__name__)
ARCHIVO = "expedientes.csv"

if not os.path.exists(ARCHIVO):
    with open(ARCHIVO, mode="w", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        escritor.writerow(["Numero", "Cliente", "Materia", "Estado", "Fecha", "Notas"])

@app.route("/", methods=["GET", "POST"])
def index():
    expedientes = []
    filtro_estado = request.args.get("estado")

    with open(ARCHIVO, mode="r", encoding="utf-8") as f:
        lector = csv.reader(f)
        next(lector)  # Saltar el encabezado
        for fila in lector:
            if not filtro_estado or fila[3].lower() == filtro_estado.lower():
                expedientes.append(fila)

    return render_template("index.html", expedientes=expedientes, filtro_estado=filtro_estado)

@app.route("/agregar", methods=["GET", "POST"])
def agregar():
    if request.method == "POST":
        numero = request.form["numero"]
        cliente = request.form["cliente"]
        materia = request.form["materia"]
        estado = request.form["estado"]
        fecha = request.form["fecha"]
        notas = request.form["notas"]

        with open(ARCHIVO, mode="a", newline="", encoding="utf-8") as f:
            escritor = csv.writer(f)
            escritor.writerow([numero, cliente, materia, estado, fecha, notas])

        return redirect(url_for("index"))
    return render_template("agregar.html")

@app.route("/editar", methods=["GET", "POST"])
def editar():
    numero = request.args.get("numero")
    numero = urllib.parse.unquote(numero)
    expediente_encontrado = None
    expedientes = []

    with open(ARCHIVO, mode="r", encoding="utf-8") as f:
        lector = csv.reader(f)
        encabezado = next(lector)
        for fila in lector:
            if fila[0] == numero:
                expediente_encontrado = fila
            else:
                expedientes.append(fila)

    if not expediente_encontrado:
        return "Expediente no encontrado", 404

    if request.method == "POST":
        cliente = request.form["cliente"]
        materia = request.form["materia"]
        estado = request.form["estado"]
        fecha = request.form["fecha"]
        notas = request.form["notas"]

        expediente_editado = [numero, cliente, materia, estado, fecha, notas]
        expedientes.append(expediente_editado)

        with open(ARCHIVO, mode="w", newline="", encoding="utf-8") as f:
            escritor = csv.writer(f)
            escritor.writerow(["Numero", "Cliente", "Materia", "Estado", "Fecha", "Notas"])
            for fila in expedientes:
                escritor.writerow(fila)

        return redirect(url_for("index"))

    return render_template("editar.html", expediente=expediente_encontrado)

@app.route("/eliminar")
def eliminar():
    numero = request.args.get("numero")
    numero = urllib.parse.unquote(numero)
    expedientes_nuevos = []
    eliminado = False

    with open(ARCHIVO, mode="r", encoding="utf-8") as f:
        lector = csv.reader(f)
        encabezado = next(lector)
        for fila in lector:
            if fila[0] != numero:
                expedientes_nuevos.append(fila)
            else:
                eliminado = True

    if not eliminado:
        return "Expediente no encontrado", 404

    with open(ARCHIVO, mode="w", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        escritor.writerow(["Numero", "Cliente", "Materia", "Estado", "Fecha", "Notas"])
        for fila in expedientes_nuevos:
            escritor.writerow(fila)

    return redirect(url_for("index"))

# Página de búsqueda
@app.route("/buscar", methods=["GET", "POST"])
def buscar():
    expedientes = []
    query = request.args.get("query")

    with open(ARCHIVO, mode="r", encoding="utf-8") as f:
        lector = csv.reader(f)
        next(lector)  # Saltar el encabezado
        for fila in lector:
            if query.lower() in fila[0].lower() or query.lower() in fila[1].lower() or query.lower() in fila[2].lower():
                expedientes.append(fila)

    return render_template("index.html", expedientes=expedientes, query=query)

# Exportar a CSV
@app.route("/exportar")
def exportar():
    output = io.StringIO()
    escritor = csv.writer(output)
    # Escribir encabezado
    escritor.writerow(["Numero", "Cliente", "Materia", "Estado", "Fecha", "Notas"])

    # Escribir datos de expedientes
    with open(ARCHIVO, mode="r", encoding="utf-8") as f:
        lector = csv.reader(f)
        next(lector)  # Saltar el encabezado
        for fila in lector:
            escritor.writerow(fila)

    output.seek(0)
    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=expedientes.csv"}
    )

if __name__ == "__main__":
    app.run(debug=True)
