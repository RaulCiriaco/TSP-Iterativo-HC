from flask import Flask, request, jsonify, render_template
import math
import random

app = Flask(__name__)

# Diccionario inicial de ciudades con coordenadas
coord = {
    'Jiloyork': (19.916012, -99.580580),
    'Toluca': (19.289165, -99.655697),
    'Atlacomulco': (19.799520, -99.873844),
    'Guadalajara': (20.677754472859146, -103.34625354877137),
    'Monterrey': (25.69161110159454, -100.321838480256),
    'QuintanaRoo': (21.163111924844458, -86.80231502121464),
    'Michoacan': (19.701400113725654, -101.20829680213464),
    'Aguascalientes': (21.87641043660486, -102.26438663286967),
    'CDMX': (19.432713075976878, -99.13318344772986),
    'QRO': (20.59719437542255, -100.38667040246602)
}

def distancia(coord1, coord2):
    return math.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)

def evalua_ruta(ruta, coord):
    total = sum(distancia(coord[ruta[i]], coord[ruta[i+1]]) for i in range(len(ruta)-1))
    total += distancia(coord[ruta[-1]], coord[ruta[0]])  # Distancia final
    return total

def i_hill_climbing(coord):
    ruta = list(coord.keys())
    random.shuffle(ruta)
    mejor_ruta = ruta[:]
    mejora = True

    while mejora:
        mejora = False
        dist_actual = evalua_ruta(ruta, coord)
        for i in range(len(ruta)):
            for j in range(i+1, len(ruta)):
                ruta_tmp = ruta[:]
                ruta_tmp[i], ruta_tmp[j] = ruta_tmp[j], ruta_tmp[i]
                dist = evalua_ruta(ruta_tmp, coord)
                if dist < dist_actual:
                    mejora = True
                    ruta = ruta_tmp[:]
                    break
    return {"ruta": ruta, "distancia_total": evalua_ruta(ruta, coord)}

@app.route('/')
def index():
    return render_template("index.html", coord=coord)

@app.route('/solve', methods=['POST'])
def solve_tsp():
    ruta_optima = i_hill_climbing(coord)
    return jsonify(ruta_optima)

@app.route('/add_city', methods=['POST'])
def add_city():
    data = request.json
    city_name = data.get("name")
    lat = data.get("lat")
    lon = data.get("lon")
    
    if city_name and lat and lon:
        coord[city_name] = (lat, lon)
    
    return jsonify({"success": True, "cities": coord})

@app.route('/delete_city', methods=['POST'])
def delete_city():
    data = request.json
    city_name = data.get("name")
    
    if city_name in coord:
        del coord[city_name]
    
    return jsonify({"success": True, "cities": coord})

if __name__ == "__main__":
    app.run(debug=True)
