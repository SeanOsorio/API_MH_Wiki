"""
Script de prueba para el sistema de autenticación completo.
Prueba: registro, login, tokens, roles, CAPTCHA y visualización de código fuente.
"""

import requests
import json
from io import BytesIO
from PIL import Image

BASE_URL = "http://127.0.0.1:5000/api/auth"

def print_section(title):
    """Imprime un separador de sección."""
    print(f"\n{'='*70}")
    print(f"🧪 {title}")
    print('='*70)

def test_login_admin():
    """Prueba 1: Login con el admin creado."""
    print_section("TEST 1: Login de Administrador")
    
    response = requests.post(f"{BASE_URL}/login", json={
        "username": "admin",
        "password": "qwertyuiop+"
    })
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        return response.json()['token']
    return None

def test_register_user():
    """Prueba 2: Registrar un usuario normal."""
    print_section("TEST 2: Registro de Usuario Normal")
    
    response = requests.post(f"{BASE_URL}/register", json={
        "username": "hunter_player",
        "email": "hunter@example.com",
        "password": "password123"
    })
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_login_user():
    """Prueba 3: Login con el usuario normal."""
    print_section("TEST 3: Login de Usuario Normal")
    
    response = requests.post(f"{BASE_URL}/login", json={
        "username": "hunter_player",
        "password": "password123"
    })
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        return response.json()['token']
    return None

def test_get_profile(token, user_type):
    """Prueba 4: Obtener perfil del usuario autenticado."""
    print_section(f"TEST 4: Obtener Perfil ({user_type})")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/me", headers=headers)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_get_all_users(admin_token, user_token):
    """Prueba 5: Listar usuarios (solo admin)."""
    print_section("TEST 5: Listar Todos los Usuarios")
    
    print("\n👑 Con token de ADMIN:")
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = requests.get(f"{BASE_URL}/users", headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    print("\n👤 Con token de USER (debería fallar):")
    headers = {"Authorization": f"Bearer {user_token}"}
    response = requests.get(f"{BASE_URL}/users", headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_captcha_generation():
    """Prueba 6: Generar un CAPTCHA."""
    print_section("TEST 6: Generar CAPTCHA")
    
    response = requests.post(f"{BASE_URL}/captcha")
    
    print(f"Status Code: {response.status_code}")
    print(f"Content-Type: {response.headers.get('Content-Type')}")
    print(f"X-Captcha-ID: {response.headers.get('X-Captcha-ID')}")
    
    if response.status_code == 200:
        # Guardar imagen de CAPTCHA para inspección
        captcha_id = response.headers.get('X-Captcha-ID')
        with open(f'captcha_{captcha_id}.png', 'wb') as f:
            f.write(response.content)
        print(f"✅ Imagen guardada como: captcha_{captcha_id}.png")
        return captcha_id
    return None

def test_captcha_verification(captcha_id):
    """Prueba 7: Verificar CAPTCHA (con entrada del usuario)."""
    print_section("TEST 7: Verificar CAPTCHA")
    
    print(f"\n📋 Abre la imagen: captcha_{captcha_id}.png")
    captcha_text = input("🔤 Ingresa el texto del CAPTCHA: ").strip()
    
    response = requests.post(f"{BASE_URL}/captcha/verify", json={
        "captcha_id": captcha_id,
        "captcha_text": captcha_text
    })
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    return response.status_code == 200

def test_view_source_code(admin_token, captcha_id):
    """Prueba 8: Ver código fuente (admin + captcha)."""
    print_section("TEST 8: Ver Código Fuente")
    
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = requests.post(f"{BASE_URL}/source", 
                           headers=headers,
                           json={
                               "captcha_id": captcha_id,
                               "file_path": "app.py"
                           })
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Archivo: {data['file']}")
        print(f"Líneas: {data['lines']}")
        print(f"\n📄 Primeras 20 líneas del código:")
        print("-" * 70)
        lines = data['content'].split('\n')[:20]
        for line in lines:
            print(line)
        print("-" * 70)
    else:
        print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_list_source_files(admin_token):
    """Prueba 9: Listar archivos disponibles."""
    print_section("TEST 9: Listar Archivos Disponibles")
    
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = requests.get(f"{BASE_URL}/source/files", headers=headers)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def run_all_tests():
    """Ejecuta todas las pruebas en secuencia."""
    print("\n" + "="*70)
    print("🚀 INICIANDO TESTS DEL SISTEMA DE AUTENTICACIÓN")
    print("="*70)
    
    # Test 1: Login admin
    admin_token = test_login_admin()
    if not admin_token:
        print("❌ Error: No se pudo obtener token de admin")
        return
    
    # Test 2: Registrar usuario normal
    test_register_user()
    
    # Test 3: Login usuario normal
    user_token = test_login_user()
    if not user_token:
        print("❌ Error: No se pudo obtener token de usuario")
        return
    
    # Test 4: Obtener perfiles
    test_get_profile(admin_token, "ADMIN")
    test_get_profile(user_token, "USER")
    
    # Test 5: Listar usuarios (admin vs user)
    test_get_all_users(admin_token, user_token)
    
    # Test 6: Generar CAPTCHA
    captcha_id = test_captcha_generation()
    if not captcha_id:
        print("❌ Error: No se pudo generar CAPTCHA")
        return
    
    # Test 7: Verificar CAPTCHA
    captcha_verified = test_captcha_verification(captcha_id)
    if not captcha_verified:
        print("⚠️  CAPTCHA no verificado, generando uno nuevo...")
        captcha_id = test_captcha_generation()
        if captcha_id:
            captcha_verified = test_captcha_verification(captcha_id)
    
    # Test 8: Ver código fuente (si CAPTCHA fue verificado)
    if captcha_verified:
        test_view_source_code(admin_token, captcha_id)
    
    # Test 9: Listar archivos disponibles
    test_list_source_files(admin_token)
    
    print("\n" + "="*70)
    print("✅ TESTS COMPLETADOS")
    print("="*70)

if __name__ == "__main__":
    try:
        run_all_tests()
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrumpidos por el usuario")
    except Exception as e:
        print(f"\n\n❌ Error durante los tests: {e}")
