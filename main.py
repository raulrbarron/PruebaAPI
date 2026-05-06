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


@app.route("/libros")
def get_libros():
    libro = libros
    return jsonify(libro), 200

# Obtener un libro por ID


@app.route("/libros/1")
def get_librosID():
    return jsonify(libros[1]), 200

# POST -> Crear Informacion

# Crear un libro


@app.route('/libros', methods=['POST'])
def create_user():
    data = request.get_json()
    # data = {
    #     "titulo": "Nuevo libro",
    #     "autor": "Autor",
    #     "anio": 2020,
    #     "genero": "novela",
    #     "disponible": True,
    #     "calificacion": 8.5
    # }

    # data['status'] = "libro creado"
    return jsonify(data), 201


# Reemplazar un libro completo


@app.route('/libros', methods=['PUT'])
def replace_user():
    data = request.get_json()
    global libros
    libros = data
    return jsonify({"message": "Libro fully replaced", "libro": libros})

# Actualizar parcialmente


@app.route('/libros', methods=['PATCH'])
def update_user():
    data = request.get_json()
    global libros
    libros.update(data)
    return jsonify({"message": "Libro partially updated", "libro": libros})

# Eliminar un libro


if __name__ == "__main__":
    app.run(debug=True)
