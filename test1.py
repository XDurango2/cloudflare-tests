import requests

# Cargar el token desde un archivo
def load_api_token(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip()  # Elimina espacios en blanco no deseados

# Definir la URL base de la API
API_BASE_URL = "https://api.cloudflare.com/client/v4/accounts/a71faaf431a55b28fbf7c2bfbe9c1fba/ai/run/"

# Cargar el token de la API desde el archivo
api_token = load_api_token('api_token.txt')

# Función para ejecutar el modelo
def run(model, inputs):
    headers = {"Authorization": f"Bearer {api_token}"}
    input_data = { "messages": inputs }
    response = requests.post(f"{API_BASE_URL}{model}", headers=headers, json=input_data)
    return response.json()

# Definir los inputs
inputs = [
    { "role": "system", "content": "You are a friendly teaching assistant who proofreads essays" },
    { "role": "user", "content": "Write suggestions about essays about motorsport history" }
]

# Ejecutar el modelo y obtener el resultado
output = run("@cf/meta/llama-3-8b-instruct", inputs)

# Guardar el resultado en un archivo de texto
with open('output.txt', 'w') as file:
    file.write(str(output))  # Convertimos a string para asegurarnos de que todo se pueda guardar

print("El output ha sido guardado en 'output.txt'")
