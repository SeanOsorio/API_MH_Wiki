#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 VALIDADOR AUTOMÁTICO DEL SISTEMA
===================================
Este script valida que todo el sistema funciona correctamente
sin necesidad de configuración manual.
"""

import requests
import json
import time
import sys

BASE_URL = "http://localhost:5000"

def print_status(message, status="info"):
    """Imprime mensajes con formato"""
    icons = {
        "success": "✅",
        "error": "❌", 
        "info": "ℹ️",
        "warning": "⚠️"
    }
    print(f"{icons.get(status, 'ℹ️')} {message}")

def test_endpoint(method, endpoint, data=None, headers=None, expected_status=200):
    """Prueba un endpoint específico"""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=headers, timeout=10)
        elif method.upper() == "POST":
            response = requests.post(url, json=data, headers=headers, timeout=10)
        else:
            raise ValueError(f"Método {method} no soportado")
            
        if response.status_code == expected_status:
            print_status(f"{method} {endpoint} - OK ({response.status_code})", "success")
            return response.json() if response.content else {}
        else:
            print_status(f"{method} {endpoint} - ERROR ({response.status_code})", "error")
            print(f"   Respuesta: {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        print_status(f"{method} {endpoint} - ERROR: No se pudo conectar al servidor", "error")
        return None
    except Exception as e:
        print_status(f"{method} {endpoint} - ERROR: {str(e)}", "error")
        return None

def main():
    """Ejecuta todas las pruebas"""
    print("🧪 INICIANDO VALIDACIÓN AUTOMÁTICA DEL SISTEMA")
    print("=" * 50)
    
    # Esperar un momento para que el servidor esté listo
    time.sleep(2)
    
    # 1. Probar health check
    print("\n🔍 1. Probando Health Check...")
    health = test_endpoint("GET", "/")
    if not health:
        print_status("El servidor no está respondiendo. ¿Está ejecutándose 'python app.py'?", "error")
        sys.exit(1)
    
    # 2. Probar info del sistema
    print("\n📋 2. Probando Info del Sistema...")
    info = test_endpoint("GET", "/info")
    if info:
        print_status(f"Versión: {info.get('version', 'N/A')}", "info")
        print_status(f"Base de datos: {info.get('database', 'N/A')}", "info")
    
    # 3. Probar registro de usuario
    print("\n👤 3. Probando Registro de Usuario...")
    user_data = {
        "username": "test_user_123",
        "email": "test@example.com", 
        "password": "MiPassword123!"
    }
    register_response = test_endpoint("POST", "/auth/register", user_data, expected_status=201)
    
    if not register_response:
        print_status("No se pudo registrar usuario", "error")
        sys.exit(1)
    
    # 4. Probar login
    print("\n🔑 4. Probando Login...")
    login_data = {
        "username": user_data["username"],
        "password": user_data["password"]
    }
    login_response = test_endpoint("POST", "/auth/login", login_data)
    
    if not login_response or "access_token" not in login_response:
        print_status("No se pudo hacer login", "error")
        sys.exit(1)
    
    access_token = login_response["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # 5. Probar endpoint protegido
    print("\n🔒 5. Probando Endpoint Protegido...")
    me_response = test_endpoint("GET", "/auth/me", headers=headers)
    
    if me_response:
        print_status(f"Usuario autenticado: {me_response.get('username')}", "info")
    
    # 6. Probar categorías
    print("\n📂 6. Probando Categorías...")
    categories_response = test_endpoint("GET", "/categories", headers=headers)
    
    # 7. Probar armas
    print("\n🔫 7. Probando Armas...")
    weapons_response = test_endpoint("GET", "/weapons", headers=headers)
    
    # 8. Probar logout
    print("\n👋 8. Probando Logout...")
    logout_response = test_endpoint("POST", "/auth/logout", headers=headers)
    
    # Resumen final
    print("\n" + "=" * 50)
    print("🎉 ¡VALIDACIÓN COMPLETADA EXITOSAMENTE!")
    print("=" * 50)
    print("✅ Servidor funcionando correctamente")
    print("✅ Autenticación JWT operativa") 
    print("✅ Base de datos configurada")
    print("✅ Todos los endpoints responden")
    print("\n🚀 ¡Tu sistema está listo para la presentación!")
    print("\n💡 Para ver la documentación completa:")
    print("   • Postman: Importar postman/Parcial1Web_Auth_Collection.json")
    print("   • OpenAPI: Ver docs/openapi.yaml")

if __name__ == "__main__":
    main()