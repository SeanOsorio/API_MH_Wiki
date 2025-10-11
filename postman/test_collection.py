#!/usr/bin/env python3
"""
Script de prueba para validar la colección de Postman
Simula los endpoints principales del sistema de autenticación
"""

import sys
import json
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.append(str(Path(__file__).parent.parent))

import requests
from datetime import datetime
import time


class AuthAPITester:
    """Tester para la API de autenticación"""
    
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url.rstrip('/')
        self.access_token = None
        self.refresh_token = None
        self.test_email = "test@example.com"
        self.test_password = "TestPassword123"
        
        print(f"🔧 Configurando tester para: {self.base_url}")
        print(f"📧 Email de prueba: {self.test_email}")
        print("=" * 50)
    
    def test_api_health(self):
        """Verificar que la API esté funcionando"""
        print("🏥 Verificando salud de la API...")
        try:
            response = requests.get(f"{self.base_url}/", timeout=5)
            print(f"✅ API respondiendo - Status: {response.status_code}")
            return True
        except requests.exceptions.ConnectionError:
            print("❌ API no responde. Asegúrate de que esté ejecutándose:")
            print("   python app.py")
            return False
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            return False
    
    def test_register(self):
        """Test de registro de usuario"""
        print("\n📝 Probando registro de usuario...")
        
        url = f"{self.base_url}/auth/register"
        data = {
            "email": self.test_email,
            "password": self.test_password
        }
        
        try:
            response = requests.post(url, json=data)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 201:
                result = response.json()
                print("✅ Registro exitoso")
                print(f"   Usuario ID: {result.get('user', {}).get('id')}")
                print(f"   Email: {result.get('user', {}).get('email')}")
                return True
            elif response.status_code == 400:
                error = response.json().get('error', 'Error desconocido')
                if 'ya está registrado' in error:
                    print("⚠️  Usuario ya existe (esperado en re-ejecuciones)")
                    return True
                else:
                    print(f"❌ Error de validación: {error}")
                    return False
            else:
                print(f"❌ Error inesperado: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Excepción: {e}")
            return False
    
    def test_login(self):
        """Test de login"""
        print("\n🚪 Probando login...")
        
        url = f"{self.base_url}/auth/login"
        data = {
            "email": self.test_email,
            "password": self.test_password
        }
        
        try:
            response = requests.post(url, json=data)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                self.access_token = result.get('access_token')
                self.refresh_token = result.get('refresh_token')
                
                print("✅ Login exitoso")
                print(f"   Access token: {self.access_token[:20]}...")
                print(f"   Refresh token: {self.refresh_token[:20]}...")
                print(f"   Expira en: {result.get('expires_in')} segundos")
                return True
            else:
                error = response.json().get('error', 'Error desconocido')
                print(f"❌ Error de login: {error}")
                return False
                
        except Exception as e:
            print(f"❌ Excepción: {e}")
            return False
    
    def test_get_me(self):
        """Test de obtener información del usuario actual"""
        print("\n👤 Probando obtener usuario actual...")
        
        if not self.access_token:
            print("❌ No hay access token. Ejecuta login primero.")
            return False
        
        url = f"{self.base_url}/auth/me"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        try:
            response = requests.get(url, headers=headers)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                user = result.get('user', {})
                print("✅ Usuario obtenido exitosamente")
                print(f"   ID: {user.get('id')}")
                print(f"   Email: {user.get('email')}")
                print(f"   Activo: {user.get('is_active')}")
                return True
            else:
                error = response.json().get('error', response.text)
                print(f"❌ Error: {error}")
                return False
                
        except Exception as e:
            print(f"❌ Excepción: {e}")
            return False
    
    def test_refresh(self):
        """Test de refresh token"""
        print("\n🔄 Probando refresh token...")
        
        if not self.refresh_token:
            print("❌ No hay refresh token. Ejecuta login primero.")
            return False
        
        url = f"{self.base_url}/auth/refresh"
        data = {"refresh_token": self.refresh_token}
        
        try:
            response = requests.post(url, json=data)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                old_token = self.access_token[:20] if self.access_token else "None"
                self.access_token = result.get('access_token')
                new_token = self.access_token[:20] if self.access_token else "None"
                
                print("✅ Refresh exitoso")
                print(f"   Token anterior: {old_token}...")
                print(f"   Token nuevo: {new_token}...")
                print(f"   Expira en: {result.get('expires_in')} segundos")
                return True
            else:
                error = response.json().get('error', response.text)
                print(f"❌ Error: {error}")
                return False
                
        except Exception as e:
            print(f"❌ Excepción: {e}")
            return False
    
    def test_logout_specific(self):
        """Test de logout específico"""
        print("\n🚫 Probando logout específico...")
        
        if not self.access_token or not self.refresh_token:
            print("❌ No hay tokens. Ejecuta login primero.")
            return False
        
        url = f"{self.base_url}/auth/logout"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        data = {"refresh_token": self.refresh_token}
        
        try:
            response = requests.post(url, json=data, headers=headers)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Logout específico exitoso")
                print(f"   Mensaje: {result.get('message')}")
                return True
            else:
                error = response.json().get('error', response.text)
                print(f"❌ Error: {error}")
                return False
                
        except Exception as e:
            print(f"❌ Excepción: {e}")
            return False
    
    def test_logout_all(self):
        """Test de logout total"""
        print("\n🚫 Probando logout total...")
        
        if not self.access_token:
            print("❌ No hay access token. Ejecuta login primero.")
            return False
        
        url = f"{self.base_url}/auth/logout"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        # Sin refresh_token en body = logout total
        
        try:
            response = requests.post(url, headers=headers)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Logout total exitoso")
                print(f"   Mensaje: {result.get('message')}")
                
                # Limpiar tokens
                self.access_token = None
                self.refresh_token = None
                return True
            else:
                error = response.json().get('error', response.text)
                print(f"❌ Error: {error}")
                return False
                
        except Exception as e:
            print(f"❌ Excepción: {e}")
            return False
    
    def run_full_test_suite(self):
        """Ejecuta la suite completa de pruebas"""
        print("🧪 INICIANDO SUITE DE PRUEBAS COMPLETA")
        print("=" * 50)
        
        tests = [
            ("API Health", self.test_api_health),
            ("Register", self.test_register),
            ("Login", self.test_login),
            ("Get Me", self.test_get_me),
            ("Refresh Token", self.test_refresh),
            ("Get Me (con nuevo token)", self.test_get_me),
            ("Logout Total", self.test_logout_all),
        ]
        
        results = {}
        
        for test_name, test_func in tests:
            try:
                results[test_name] = test_func()
            except Exception as e:
                print(f"💥 Excepción en {test_name}: {e}")
                results[test_name] = False
            
            time.sleep(0.5)  # Pequeña pausa entre tests
        
        # Resumen
        print("\n" + "=" * 50)
        print("📊 RESUMEN DE PRUEBAS")
        print("=" * 50)
        
        passed = 0
        total = len(results)
        
        for test_name, success in results.items():
            icon = "✅" if success else "❌"
            status = "PASS" if success else "FAIL"
            print(f"{icon} {test_name}: {status}")
            if success:
                passed += 1
        
        print(f"\n🎯 Resultado: {passed}/{total} pruebas pasaron")
        
        if passed == total:
            print("🎉 ¡Todas las pruebas pasaron! La colección de Postman debería funcionar perfectamente.")
        else:
            print("⚠️  Algunas pruebas fallaron. Revisa la configuración de la API.")
        
        return passed == total


def main():
    """Función principal"""
    print("🚀 VALIDADOR DE COLECCIÓN POSTMAN")
    print("Sistema de Autenticación - Parcial1Web")
    print("=" * 50)
    
    # Crear tester
    tester = AuthAPITester()
    
    # Ejecutar suite completa
    success = tester.run_full_test_suite()
    
    if success:
        print("\n🎊 ¡PERFECTO! Tu colección de Postman está lista para usar.")
        print("\n📋 Próximos pasos:")
        print("1. Importar Parcial1Web_Auth_Collection.json en Postman")
        print("2. Importar Parcial1Web_Auth_Environment.json como environment")
        print("3. Seleccionar el environment 'Parcial1Web - Autenticación (Local)'")
        print("4. ¡Comenzar a probar los endpoints!")
    else:
        print("\n🔧 Se encontraron problemas. Revisa:")
        print("1. Que la API esté ejecutándose: python app.py")
        print("2. Que la base de datos esté configurada correctamente")
        print("3. Que las dependencias estén instaladas: pip install -r requirements.txt")
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())