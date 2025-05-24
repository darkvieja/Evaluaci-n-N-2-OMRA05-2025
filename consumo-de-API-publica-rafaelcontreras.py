import requests
import urllib.parse

key = "8ea4a752-e1fd-4834-a735-7b6b50347b1c"
route_url = "https://graphhopper.com/api/1/route?"

def geocodificar(ubicacion, key):
    while ubicacion == "":
        ubicacion = input("Ingrese la ubicación nuevamente: ")

    geocode_url = "https://graphhopper.com/api/1/geocode?"
    url = geocode_url + urllib.parse.urlencode({"q": ubicacion, "limit": "1", "key": key})
    respuesta = requests.get(url)
    datos = respuesta.json()
    estado = respuesta.status_code

    if estado == 200 and len(datos["hits"]) != 0:
        lat = datos["hits"][0]["point"]["lat"]
        lng = datos["hits"][0]["point"]["lng"]
        nombre = datos["hits"][0]["name"]
        pais = datos["hits"][0].get("country", "")
        region = datos["hits"][0].get("state", "")
        if region and pais:
            ubicacion_completa = f"{nombre}, {region}, {pais}"
        elif pais:
            ubicacion_completa = f"{nombre}, {pais}"
        else:
            ubicacion_completa = nombre
        print(f"\nUbicación encontrada: {ubicacion_completa}")
        print(f"URL de geocodificación:\n{url}\n")
    else:
        lat = "null"
        lng = "null"
        ubicacion_completa = ubicacion
        if estado != 200:
            print("Error en la geocodificación:")
            print("Código de estado:", estado)
            print("Mensaje:", datos.get("message", "Error desconocido"))

    return estado, lat, lng, ubicacion_completa

while True:
    print("\nTipos de vehículo disponibles: car, bike, foot")

    perfiles = ["car", "bike", "foot"]
    vehiculo = input("Ingrese un tipo de vehículo (o 'q' para salir): ")
    if vehiculo.lower() in ["q", "quit"]:
        break
    elif vehiculo not in perfiles:
        print("Tipo no válido. Se usará 'car' por defecto.")
        vehiculo = "car"

    origen_input = input("Ciudad de origen: ")
    if origen_input.lower() in ["q", "quit"]:
        break
    origen = geocodificar(origen_input, key)

    destino_input = input("Ciudad de destino: ")
    if destino_input.lower() in ["q", "quit"]:
        break
    destino = geocodificar(destino_input, key)

    rendimiento = float(input("Ingrese el rendimiento del vehículo (km por litro): "))

    print("\nCalculando ruta...")
    if origen[0] == 200 and destino[0] == 200:
        op = f"&point={origen[1]}%2C{origen[2]}"
        dp = f"&point={destino[1]}%2C{destino[2]}"
        url_ruta = route_url + urllib.parse.urlencode({"key": key, "vehicle": vehiculo}) + op + dp
        respuesta_ruta = requests.get(url_ruta)
        datos_ruta = respuesta_ruta.json()
        estado_ruta = respuesta_ruta.status_code

        if estado_ruta == 200:
            print("\nRuta obtenida con éxito:")
            print(f"URL de la ruta:\n{url_ruta}\n")
            print(f"Desde: {origen[3]}")
            print(f"Hasta: {destino[3]}")
            print(f"Vehículo: {vehiculo}\n")

            distancia_km = datos_ruta["paths"][0]["distance"] / 1000
            tiempo_ms = datos_ruta["paths"][0]["time"]
            horas = int(tiempo_ms / 1000 / 60 / 60)
            minutos = int((tiempo_ms / 1000 / 60) % 60)
            segundos = int((tiempo_ms / 1000) % 60)
            combustible = distancia_km / rendimiento

            print(f"Distancia total: {distancia_km:.2f} km")
            print(f"Duración del viaje: {horas:02d}:{minutos:02d}:{segundos:02d}")
            print(f"Combustible requerido para el viaje: {combustible:.2f} litros\n")

            print("Instrucciones del viaje:")
            for paso in datos_ruta["paths"][0]["instructions"]:
                texto = paso["text"]
                distancia_paso = paso["distance"] / 1000
                print(f"- {texto} ({distancia_paso:.2f} km)")

            print("\nFin del viaje.\n")
        else:
            print("Error al calcular la ruta.")
            print("Código de estado:", estado_ruta)
            print("Mensaje:", datos_ruta.get("message", "Error desconocido"))
    else:
        print("No se pudieron obtener los datos de origen o destino.")
