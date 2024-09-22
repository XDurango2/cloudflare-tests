import requests


API_BASE_URL = "https://api.cloudflare.com/client/v4/accounts/a71faaf431a55b28fbf7c2bfbe9c1fba/ai/run/"
headers = {"Authorization": "Bearer U2z-hQPH0ZY80xKsPgFpuQ_haaTksaai10MzU8jh"}


def run(model, inputs):
    input = { "messages": inputs }
    response = requests.post(f"{API_BASE_URL}{model}", headers=headers, json=input)
    return response.json()


inputs = [
    { "role": "system", "content": "You are a friendly teaching assistant who proofreads essays" },
    { "role": "user", "content": "Write suggestions about essays about motorsport history  "}
];
output = run("@cf/meta/llama-3-8b-instruct", inputs)
print(output)