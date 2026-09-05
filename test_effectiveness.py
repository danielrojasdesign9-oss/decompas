import requests
import json
import time
import sys
import io

# Configurar codificación
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

WEBHOOK_URL = "http://localhost:8765"

# Test cases más complejos
test_cases = [
    {
        "input": "Cuál es el estado actual del proyecto Decompas?",
        "expected_keywords": ["landing", "bot", "webhook", "discord"]
    },
    {
        "input": "Necesito que me ayudes a crear una propuesta para un restaurante en Cali que se llama El Buen Sabor",
        "expected_keywords": ["propuesta", "restaurante", "Cali", "El Buen Sabor"]
    },
    {
        "input": "Cuánto costaría automatizar el WhatsApp de un negocio con 50 clientes diarios?",
        "expected_keywords": ["costo", "automatizar", "WhatsApp", "clientes"]
    },
    {
        "input": "Quiero integrar mi tienda Shopify con un chatbot que responda preguntas frecuentes",
        "expected_keywords": ["Shopify", "chatbot", "integrar", "preguntas"]
    },
    {
        "input": "Dame un resumen de todos los proyectos que tenemos en el portafolio",
        "expected_keywords": ["TIR", "E-Signer", "Silin", "Linklight", "Innu", "Paycool"]
    }
]

def send_test(message):
    """Envía un mensaje de prueba"""
    response = requests.post(WEBHOOK_URL, json={
        "source": "hermes",
        "message": message
    })
    return response.json()

def wait_for_response(timeout=10):
    """Espera una respuesta de OpenCode"""
    start = time.time()
    while time.time() - start < timeout:
        try:
            response = requests.get(WEBHOOK_URL)
            data = response.json()
            messages = data.get("messages", [])
            
            for msg in messages:
                if msg["source"] == "opencode":
                    return msg["message"]
        except:
            pass
        time.sleep(1)
    return None

def validate_response(response, keywords):
    """Valida si la respuesta contiene las palabras clave"""
    if not response:
        return False, "No se recibió respuesta"
    
    response_lower = response.lower()
    found = [kw for kw in keywords if kw.lower() in response_lower]
    missing = [kw for kw in keywords if kw.lower() not in response_lower]
    
    return len(found) > 0, f"Encontradas: {found}, Faltantes: {missing}"

print("=== PRUEBA DE EFECTIVIDAD ===\n")

results = []
for i, test in enumerate(test_cases, 1):
    print(f"Test {i}: {test['input'][:50]}...")
    
    # Enviar mensaje
    send_result = send_test(test["input"])
    print(f"  Enviado: {send_result}")
    
    # Esperar respuesta
    response = wait_for_response(timeout=15)
    
    # Validar
    is_valid, details = validate_response(response, test["expected_keywords"])
    
    print(f"  Respuesta: {response[:100] if response else 'None'}...")
    print(f"  Válido: {is_valid} - {details}")
    print()
    
    results.append({
        "test": i,
        "input": test["input"],
        "response": response,
        "valid": is_valid,
        "details": details
    })
    
    time.sleep(2)

# Resumen
print("=== RESUMEN ===")
valid_count = sum(1 for r in results if r["valid"])
print(f"Tests pasados: {valid_count}/{len(results)}")
print(f"Tasa de éxito: {(valid_count/len(results)*100):.1f}%")

for r in results:
    status = "V" if r["valid"] else "X"
    print(f"  {status} Test {r['test']}: {r['input'][:40]}...")