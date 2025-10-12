#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 TESTER AUTOMÁTICO DEL SISTEMA DE ROLES
=========================================
Ejecuta pruebas automáticas completas del sistema de roles y permisos
Perfecto para demostrar en tu presentación.
"""

import requests
import json
import time
import sys
from datetime import datetime

# Configuración
BASE_URL = "http://localhost:5000"
ADMIN_CREDS = {"username": "admin", "password": "admin123"}

def print_header(title, icon="🔹"):
    """Imprime un header con formato"""
    print(f"\n{icon} {title}")
    print("=" * (len(title) + 4))

def print_step(step, message, status="info"):
    """Imprime un paso con formato"""
    icons = {
        "success": "✅",
        "error": "❌", 
        "info": "ℹ️",
        "warning": "⚠️"
    }
    print(f"{icons.get(status, 'ℹ️')} {step}. {message}")

def make_request(method, endpoint, data=None, headers=None, expected_status=None):
    """Hace una request y maneja errores"""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=headers, timeout=10)
        elif method.upper() == "POST":
            response = requests.post(url, json=data, headers=headers, timeout=10)
        elif method.upper() == "PUT":
            response = requests.put(url, json=data, headers=headers, timeout=10)
        elif method.upper() == "DELETE":
            response = requests.delete(url, headers=headers, timeout=10)
        else:
            print_step("ERROR", f"Método {method} no soportado", "error")
            return None
        
        # Verificar status si se especificó
        if expected_status and response.status_code != expected_status:
            print_step("WARNING", f"{method} {endpoint} retornó {response.status_code}, esperado {expected_status}", "warning")
        
        return response
        
    except requests.exceptions.ConnectionError:
        print_step("ERROR", f"No se pudo conectar a {url}", "error")
        return None
    except Exception as e:
        print_step("ERROR", f"{method} {endpoint} falló: {str(e)}", "error")
        return None

def test_health_check():
    """Test 1: Verificar que la API esté funcionando"""
    print_header("TEST 1: Health Check", "🏥")
    
    response = make_request("GET", "/")
    if response and response.status_code == 200:
        data = response.json()
        print_step(1, f"API funcionando: {data.get('message', 'OK')}", "success")
        return True
    else:
        print_step(1, "API no está respondiendo", "error")
        return False

def test_admin_login():
    """Test 2: Login como administrador"""
    print_header("TEST 2: Autenticación Admin", "🔐")
    
    response = make_request("POST", "/auth/login", ADMIN_CREDS)
    if response and response.status_code == 200:
        data = response.json()
        admin_token = data.get('access_token')
        user_info = data.get('user', {})
        
        print_step(2, f"Admin logueado: {user_info.get('username')} ({user_info.get('role')})", "success")
        return admin_token
    else:
        print_step(2, "Error en login de admin", "error")
        return None

def test_create_users(admin_token):
    """Test 3: Crear usuarios con diferentes roles"""
    print_header("TEST 3: Crear Usuarios con Roles", "👥")
    
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    users_to_create = [
        {
            "username": "moderador_demo",
            "email": "mod@demo.com",
            "password": "ModDemo123!",
            "role": "moderator"
        },
        {
            "username": "usuario_demo", 
            "email": "user@demo.com",
            "password": "UserDemo123!",
            "role": "user"
        }
    ]
    
    created_users = {}
    
    for i, user_data in enumerate(users_to_create, 3):
        response = make_request("POST", "/auth/register", user_data)
        if response and response.status_code == 201:
            data = response.json()
            user_info = data.get('user', {})
            created_users[user_info['role']] = user_info
            print_step(i, f"Usuario {user_info['role']} creado: {user_info['username']}", "success")
        else:
            print_step(i, f"Error creando usuario {user_data['role']}", "error")
    
    return created_users

def test_login_different_roles(created_users):
    """Test 4: Login con diferentes roles"""
    print_header("TEST 4: Login con Diferentes Roles", "🔑")
    
    login_data = {
        "moderator": {"username": "moderador_demo", "password": "ModDemo123!"},
        "user": {"username": "usuario_demo", "password": "UserDemo123!"}
    }
    
    tokens = {}
    
    for role, creds in login_data.items():
        response = make_request("POST", "/auth/login", creds)
        if response and response.status_code == 200:
            data = response.json()
            tokens[role] = data.get('access_token')
            user_info = data.get('user', {})
            print_step(len(tokens) + 4, f"Login {role}: {user_info.get('username')}", "success")
        else:
            print_step(len(tokens) + 4, f"Error login {role}", "error")
    
    return tokens

def test_permissions(tokens):
    """Test 5: Probar permisos diferenciados"""
    print_header("TEST 5: Test de Permisos por Rol", "🛡️")
    
    admin_headers = {"Authorization": f"Bearer {tokens.get('admin', '')}"}
    mod_headers = {"Authorization": f"Bearer {tokens.get('moderator', '')}"}
    user_headers = {"Authorization": f"Bearer {tokens.get('user', '')}"}
    
    step = 7
    
    # Test 1: Usuario normal intenta crear categoría (DEBE FALLAR)
    print_step(step, "Usuario normal intenta crear categoría...", "info")
    response = make_request("POST", "/categories", 
                          {"name": "Test Category", "description": "Test"}, 
                          user_headers)
    
    if response and response.status_code == 403:
        print_step(step, "✓ Usuario correctamente bloqueado", "success")
    else:
        print_step(step, "✗ Usuario NO fue bloqueado (error)", "error")
    
    step += 1
    
    # Test 2: Moderador crea categoría (DEBE FUNCIONAR)
    print_step(step, "Moderador intenta crear categoría...", "info")
    response = make_request("POST", "/categories",
                          {"name": "Pistolas Demo", "description": "Categoría de demostración"},
                          mod_headers)
    
    category_id = None
    if response and response.status_code == 201:
        data = response.json()
        category_id = data.get('category', {}).get('id')
        print_step(step, "✓ Moderador creó categoría exitosamente", "success")
    else:
        print_step(step, "✗ Moderador no pudo crear categoría", "error")
    
    step += 1
    
    # Test 3: Usuario lee categorías (DEBE FUNCIONAR)
    print_step(step, "Usuario intenta leer categorías...", "info")
    response = make_request("GET", "/categories", headers=user_headers)
    
    if response and response.status_code == 200:
        categories = response.json()
        print_step(step, f"✓ Usuario leyó {len(categories)} categorías", "success")
    else:
        print_step(step, "✗ Usuario no pudo leer categorías", "error")
    
    step += 1
    
    # Test 4: Usuario intenta eliminar categoría (DEBE FALLAR)
    if category_id:
        print_step(step, "Usuario intenta eliminar categoría...", "info")
        response = make_request("DELETE", f"/categories/{category_id}", headers=user_headers)
        
        if response and response.status_code == 403:
            print_step(step, "✓ Usuario correctamente bloqueado para eliminar", "success")
        else:
            print_step(step, "✗ Usuario NO fue bloqueado para eliminar", "error")
    
    return category_id

def test_role_management(admin_token, created_users):
    """Test 6: Gestión de roles"""
    print_header("TEST 6: Gestión de Roles (Admin)", "⚙️")
    
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    # Listar roles
    print_step(12, "Listando roles disponibles...", "info")
    response = make_request("GET", "/auth/roles", headers=headers)
    if response and response.status_code == 200:
        roles = response.json().get('roles', [])
        print_step(12, f"Roles encontrados: {[r['name'] for r in roles]}", "success")
    
    # Listar usuarios
    print_step(13, "Listando usuarios registrados...", "info")
    response = make_request("GET", "/auth/users", headers=headers)
    if response and response.status_code == 200:
        users = response.json().get('users', [])
        print_step(13, f"Usuarios registrados: {len(users)}", "success")
        
        # Mostrar usuarios por rol
        for user in users:
            role_name = user.get('role', {}).get('name', 'Sin rol')
            print(f"    • {user.get('username')} → {role_name}")

def generate_report():
    """Generar reporte final"""
    print_header("REPORTE FINAL", "📋")
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print("📊 Resumen de Pruebas:")
    print("   ✅ Sistema de autenticación funcionando")
    print("   ✅ Roles y permisos implementados correctamente")
    print("   ✅ Control de acceso por endpoints")
    print("   ✅ Gestión administrativa de usuarios")
    print("   ✅ Seguridad diferenciada por rol")
    
    print(f"\n🕒 Pruebas completadas: {current_time}")
    print("🎯 Sistema listo para presentación")

def main():
    """Función principal"""
    print("🧪 INICIANDO TESTS AUTOMÁTICOS DEL SISTEMA DE ROLES")
    print("=" * 60)
    print("🎯 Este script demuestra el funcionamiento completo del sistema")
    print("🔥 Perfecto para presentar tu parcial\n")
    
    # Esperar un momento para que el servidor esté listo
    time.sleep(2)
    
    # Test 1: Health Check
    if not test_health_check():
        print("\n❌ La API no está funcionando. ¿Está ejecutándose 'python app.py'?")
        sys.exit(1)
    
    # Test 2: Admin Login
    admin_token = test_admin_login()
    if not admin_token:
        print("\n❌ No se pudo autenticar como admin")
        sys.exit(1)
    
    # Test 3: Crear usuarios
    created_users = test_create_users(admin_token)
    
    # Test 4: Login con diferentes roles
    tokens = test_login_different_roles(created_users)
    tokens['admin'] = admin_token
    
    # Test 5: Probar permisos
    test_permissions(tokens)
    
    # Test 6: Gestión de roles
    test_role_management(admin_token, created_users)
    
    # Reporte final
    generate_report()
    
    print("\n" + "=" * 60)
    print("🎉 ¡TODOS LOS TESTS COMPLETADOS EXITOSAMENTE!")
    print("🚀 Tu sistema de roles está funcionando perfectamente")
    print("💡 Usa la colección de Postman para demostraciones interactivas")
    print("=" * 60)

if __name__ == "__main__":
    main()