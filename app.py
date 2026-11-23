from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

comedores = [
    {"id": 1, "nombre": "Comedor Virgen de Lourdes", "zona": "Sector 3", "necesita": ["Arroz", "Aceite", "Lentejas"]},
    {"id": 2, "nombre": "Comedor Unidos por la Vida", "zona": "Sector 5", "necesita": ["Leche", "Azúcar", "Avena"]},
    {"id": 3, "nombre": "Comedor Luz del Sur", "zona": "Sector 8", "necesita": ["Atún", "Fideos", "Legumbres"]},
]

donaciones = []


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/comedores")
def listar_comedores():
    return jsonify(comedores)


@app.get("/api/donaciones")
def listar_donaciones():
    return jsonify(donaciones)


@app.post("/api/donaciones")
def crear_donacion():
    datos = request.get_json(silent=True) or {}
    requeridos = ("donante", "comedorId", "alimento", "cantidad")
    if not all(datos.get(campo) for campo in requeridos):
        return jsonify({"error": "Completa todos los campos obligatorios"}), 400

    comedor = next((item for item in comedores if item["id"] == int(datos["comedorId"])), None)
    if comedor is None:
        return jsonify({"error": "Comedor no encontrado"}), 404

    donacion = {
        "id": len(donaciones) + 1,
        "donante": datos["donante"].strip(),
        "comedor": comedor["nombre"],
        "alimento": datos["alimento"].strip(),
        "cantidad": datos["cantidad"].strip(),
        "estado": "Pendiente de coordinación",
    }
    donaciones.insert(0, donacion)
    return jsonify(donacion), 201


if __name__ == "__main__":
    app.run(debug=True)
