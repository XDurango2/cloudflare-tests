from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# Cargar el token desde un archivo
def load_api_token(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip()  # Elimina espacios en blanco no deseados

# Definir la URL base de la API
API_BASE_URL = "https://api.cloudflare.com/client/v4/accounts/a71faaf431a55b28fbf7c2bfbe9c1fba/ai/run/"

# Cargar el token de la API desde el archivo
api_token = load_api_token('api_token.txt')

# Función para ejecutar el modelo
def run_model(model, inputs, timeout=1200):
    headers = {"Authorization": f"Bearer {api_token}"}
    input_data = { "messages": inputs }
    try:
        response = requests.post(f"{API_BASE_URL}{model}", headers=headers, json=input_data, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        return {"error": f"La solicitud ha superado el tiempo máximo de {timeout} segundos"}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

# Ruta para procesar la solicitud del formulario
@app.route('/submit', methods=['POST'])
def submit():
    essay_text = request.form['essay']  # Obtenemos el texto enviado por el formulario

    # Definir los inputs para la API
    inputs = [
        { "role": "system", "content": "You are a friendly teaching assistant who proofreads essays" },
        { "role": "user", "content": essay_text }
    ]

    # Ejecutar el modelo para revisar el ensayo
    result = run_model("@cf/meta/llama-3-8b-instruct", inputs, timeout=1200)
    print("Resultado de la IA:", result)  # Verifica lo que devuelve la API

    # Revisar el resultado
    if 'error' in result:
        return jsonify({"message": "Error al procesar la solicitud: " + result['error']})
    
    # Extraer el contenido revisado de la IA
    try:
        ai_response = result['content']  # Ajusta según la estructura de la respuesta
    except KeyError:
        return jsonify({"message": "Error al procesar la respuesta de la IA."})

    # Devolver el contenido revisado al usuario
    return jsonify({"message": "Revisión completada con éxito", "response": ai_response})

# Ruta para servir la página principal
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
