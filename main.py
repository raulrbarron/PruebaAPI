from flask import Flask, jsonify, request
import random

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
    },
    4: {
        "titulo": "Harry Potter y la cámara secreta",
        "autor": "J.K. Rowling",
        "anio": 1998,
        "genero": "aventura fantástica",
        "disponible": False,
        "calificacion": 9.7
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

# ejercicios de David


@app.route('/libros/eliminar-autor', methods=['DELETE'])
def eliminar_autor():
    autor = request.args.get('autor')

    global libros
    nuevo_diccionario = {}

    for id_lib, datos in libros.items():
        # Si el autor NO es el que quiero borrar, lo guardo
        if datos['autor'].lower() != autor.lower():
            nuevo_diccionario[id_lib] = datos

    libros = nuevo_diccionario

    return jsonify({
        "mensaje": f"Operación exitosa",
        "autor_eliminado": autor

    }), 200


@app.route('/libros/actualizar-libros', methods=['POST'])
def actualizar_libros():

    data = request.json
    # validamos los datos que necesitamos
    nombre = data.get('nombre')
    nuevo_genero = data.get('genero')
    nueva_disponibilidad = data.get('disponible')

    if not nombre:
        return jsonify({"error": "Falta el nombre para buscar el titulo"}), 400

    actualizados = 0
    libros_modificados = []

    for id_lib, datos in libros.items():
        if nombre.lower() in datos['titulo'].lower():
            # Actualizamos los campos del JSON
            if nuevo_genero:
                datos['genero'] = nuevo_genero
            # Usamos is not None porque False es un valor válido
            if nueva_disponibilidad is not None:
                datos['disponible'] = nueva_disponibilidad

            actualizados += 1
            libros_modificados.append({
                "id": id_lib,
                "titulo": datos['titulo'],
                "nuevo_genero": datos['genero'],
                "nueva_disponibilidad": datos['disponible']
            })

    return jsonify({
        "status": "success",
        "total_afectados": actualizados,
        "detalles": libros_modificados
    }), 200


@app.route('/libros/calificar-por-epoca', methods=['PUT'])
def calificar_por_epoca():
    actualizados = 0
    cambios = []

    # recorremos la lista
    for id_lib, datos in libros.items():

        if datos['anio'] >= 1900 and datos['anio'] <= 2000:
            calificacion_anterior = datos['calificacion']

            nueva_calificacion = round(random.uniform(8.0, 9.7), 1)

            datos['calificacion'] = nueva_calificacion

            actualizados += 1

            cambios.append({
                "titulo": datos['titulo'],
                "anio": datos['anio'],
                "calificacion_anterior": calificacion_anterior,
                "nueva_calificacion": nueva_calificacion
            })

    if actualizados == 0:
        return jsonify({"mensaje": "No se encontraron libros en ese rango de años"}), 404

    return jsonify({
        "status": "success",
        "total_libros_afectados": actualizados,
        "cambios": cambios
    }), 200


@app.route('/libros/agregar-categoria', methods=['POST'])
def agregar_categoria():
    actualizados = 0
    resumen = []

    for id_lib, datos in libros.items():

        nota = datos.get('calificacion', 0.0)

        if nota >= 9.6:
            categoria = "S+"
        elif nota >= 9.1:
            categoria = "S"
        elif nota >= 8.5:
            categoria = "A"
        elif nota >= 7.0:
            categoria = "B"
        else:
            categoria = "C"

        # agregamos el nuevo campo diccionario

        datos['categoria'] = categoria

        actualizados += 1
        resumen.append({
            "titulo": datos['titulo'],
            "calificacion": nota,
            "categoria_asignada": categoria
        })

    return jsonify({
        "status": "success",
        "mensaje": "Categorías calculadas y agregadas exitosamente",
        "total_actualizados": actualizados,
        "libros": resumen
    }), 200


if __name__ == "__main__":
    app.run(debug=True)
