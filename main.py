from flask import Flask, jsonify, request

app = Flask(__name__)

libros = {
    1: {
        "titulo": "Cien años de soledad",
        "autor": "Gabriel García Márquez",
        "anio": 1967,
        "genero": "realismo mágico",
        "disponible": True,
        "calificacion": 9.5
    },
    2: {
        "titulo": "1984",
        "autor": "George Orwell",
        "anio": 1949,
        "genero": "distopía",
        "disponible": True,
        "calificacion": 9.2
    },
    3: {
        "titulo": "El principito",
        "autor": "Antoine de Saint-Exupéry",
        "anio": 1943,
        "genero": "fábula",
        "disponible": False,
        "calificacion": 8.8
    }
}


@app.route('/')
def root():
    return "Hola"

# GET -> Obtener informacion

# Obtener todos los libros


@app.route("/libros",  methods=['GET'])
def get_libros():
    libro = libros
    return jsonify(libro), 200

# Obtener un libro por ID


@app.route('/libros/<int:libro_id>', methods=['GET'])
def get_libro(libro_id):
    libro = libros.get(libro_id)

    respuesta = libro.copy()
    respuesta['id'] = libro_id
    return jsonify(respuesta), 200

# POST -> Crear Informacion

# Crear un libro


@app.route('/libros', methods=['POST'])
def create_libro():
    data = request.json

    if not data or 'titulo' not in data or 'autor' not in data:
        return jsonify({"error": "Título y Autor son obligatorios"}), 400

    nuevo_id = 4

    nuevo_libro = {
        "titulo": data['titulo'],
        "autor": data['autor'],
        "anio": data.get('anio', 2020),
        "genero": data.get('genero', "novela"),
        "disponible": data.get('disponible', True),
        "calificacion": data.get('calificacion', 8.5)
    }

    libros[nuevo_id] = nuevo_libro
    return jsonify({"id": nuevo_id, **nuevo_libro}), 201


# Reemplazar un libro completo


@app.route('/libros/<int:libro_id>', methods=['PUT'])
def replace_libro(libro_id):
    data = request.get_json()

    libro = libros[libro_id]
    libro["titulo"] = data.get("titulo", "nuevo libro")
    libro["autor"] = data.get("autor", "autor")
    libro['anio'] = data.get("anio", 2020)
    libro['genero'] = data.get('genero', "novela")
    libro['disponible'] = data.get('disponible', True)
    libro['calificacion'] = data.get('calificacion', 8.5)
    return jsonify(libro), 200
    # return jsonify({"message": "Libro fully replaced"})

# Actualizar parcialmente


@app.route('/libros/<int:libro_id>', methods=['PATCH'])
def update_libro(libro_id):
    data = request.get_json()
    libro = libros[libro_id]
    libro["calificacion"] = data.get("calificacion", 8)
    return jsonify(libro), 200

# Eliminar un libro


@app.route('/libros/<int:libro_id>', methods=['DELETE'])
def delete_libro(libro_id):
    if libro_id not in libros:
        return jsonify({"error": "Libro no encontrado"}), 404
    else:
        del libros[libro_id]
        return jsonify({"mensaje": "Libro eliminado correctamente"}), 200


if __name__ == "__main__":
    app.run(debug=True)
