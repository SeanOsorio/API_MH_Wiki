"""
Script para subir las imágenes REALES desde la carpeta Imeges/Icons/ a Railway.
Estas son las imágenes PNG originales de Monster Hunter, no los placeholders.
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.database import SessionLocal
from models.weapons_model import WeaponCategory

# Mapeo de nombres de archivo a nombres en la base de datos
CATEGORY_MAPPING = {
    'Great_Sword.png': 'Great Sword',
    'Long_Sword.png': 'Long Sword',
    'Sword_and_Shield.png': 'Sword and Shield',
    'Dual_Blades.png': 'Dual Blades',
    'Hammer.png': 'Hammer',
    'Hunting_Horn.png': 'Hunting Horn',
    'Lance.png': 'Lance',
    'Gunlance.png': 'Gunlance',
    'Switch_Axe.png': 'Switch Axe',
    'Charge_Blade.png': 'Charge Blade',
    'Insect_Glaive.png': 'Insect Glaive',
    'Bow.png': 'Bow',
    'Light_Bowgun.png': 'Light Bowgun',
    'Heavy_Bowgun.png': 'Heavy Bowgun'
}

def upload_real_images():
    """Sube las imágenes reales de Monster Hunter a Railway."""
    
    images_dir = os.path.join(os.path.dirname(__file__), 'images', 'Icons')
    
    if not os.path.exists(images_dir):
        print(f"❌ Error: No se encuentra la carpeta {images_dir}")
        return
    
    print("=" * 70)
    print("🎮 SUBIENDO IMÁGENES REALES DE MONSTER HUNTER A RAILWAY")
    print("=" * 70)
    print()
    print(f"📁 Directorio: {images_dir}")
    print()
    
    db = SessionLocal()
    
    try:
        uploaded_count = 0
        not_found_count = 0
        error_count = 0
        
        # Obtener todas las categorías
        categories = {cat.name: cat for cat in db.query(WeaponCategory).all()}
        
        # Procesar cada archivo
        for filename, category_name in CATEGORY_MAPPING.items():
            filepath = os.path.join(images_dir, filename)
            
            # Verificar si el archivo existe
            if not os.path.exists(filepath):
                print(f"   ⏭️  {category_name}: Archivo no encontrado ({filename})")
                not_found_count += 1
                continue
            
            # Verificar si la categoría existe en la DB
            if category_name not in categories:
                print(f"   ❌ {category_name}: Categoría no existe en la base de datos")
                error_count += 1
                continue
            
            try:
                # Leer la imagen
                with open(filepath, 'rb') as f:
                    image_data = f.read()
                
                image_size_kb = len(image_data) / 1024
                
                # Actualizar la categoría en Railway
                category = categories[category_name]
                category.icon_data = image_data
                category.icon_mime_type = 'image/png'
                
                print(f"   ✅ {category_name}: {image_size_kb:.1f} KB subido")
                uploaded_count += 1
                
            except Exception as e:
                print(f"   ❌ {category_name}: Error - {e}")
                error_count += 1
        
        # Commit todos los cambios
        db.commit()
        
        print()
        print("=" * 70)
        print("📊 RESUMEN")
        print("=" * 70)
        print(f"✅ Imágenes subidas: {uploaded_count}")
        print(f"⏭️  Archivos no encontrados: {not_found_count}")
        print(f"❌ Errores: {error_count}")
        print(f"📦 Total categorías: {len(categories)}")
        print()
        
        if uploaded_count > 0:
            print("🎉 ¡IMÁGENES REALES SUBIDAS A RAILWAY!")
            print()
            print("💡 Próximos pasos:")
            print("   1. El servidor ya está corriendo")
            print("   2. Refresca tu navegador: http://127.0.0.1:5000/weapons")
            print("   3. ¡Ahora deberías ver los iconos REALES de Monster Hunter!")
            print()
        else:
            print("⚠️  No se subieron imágenes. Verifica que los archivos existan.")
        
    except Exception as e:
        print(f"\n❌ Error fatal: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == '__main__':
    try:
        upload_real_images()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
