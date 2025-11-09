"""
Script para poblar la base de datos con datos de ejemplo de Monster Hunter
Este script inserta directamente en la base de datos usando SQLAlchemy
"""

from config.database import get_db
from models.weapons_model import WeaponCategory, Weapon

print("=" * 70)
print("🎮 POBLANDO BASE DE DATOS CON DATOS DE MONSTER HUNTER")
print("=" * 70)

# Categorías de armas de Monster Hunter
categories_data = [
    {"name": "Great Sword", "description": "Arma pesada de gran daño. Lenta pero devastadora con ataques cargados."},
    {"name": "Long Sword", "description": "Espada larga con gran alcance. Se fortalece con el sistema de gauge."},
    {"name": "Sword and Shield", "description": "Arma versátil y ágil. Permite usar objetos sin guardar el arma."},
    {"name": "Dual Blades", "description": "Dos espadas rápidas. Modo demonio para ataques frenéticos."},
    {"name": "Hammer", "description": "Arma contundente pesada. Especializada en aturdir monstruos."},
    {"name": "Hunting Horn", "description": "Martillo musical. Otorga buffs al equipo mientras combate."},
    {"name": "Lance", "description": "Lanza y escudo. Excelente defensa y ataques precisos."},
    {"name": "Gunlance", "description": "Lanza con cañón. Combina ataques cuerpo a cuerpo con explosiones."},
    {"name": "Switch Axe", "description": "Transforma entre hacha y espada. Modo espada desata elemento."},
    {"name": "Charge Blade", "description": "Espada y escudo que se combina en un hacha. Guarda energía para ataques."},
    {"name": "Insect Glaive", "description": "Alabarda con insecto. Permite combate aéreo y buffs de kinsect."},
    {"name": "Bow", "description": "Arco a distancia. Dispara flechas cargadas y revestidas."},
    {"name": "Light Bowgun", "description": "Ballesta ligera y móvil. Gran variedad de municiones."},
    {"name": "Heavy Bowgun", "description": "Ballesta pesada. Alto daño pero menor movilidad. Tiene escudo."}
]

db = next(get_db())

try:
    print("\n📦 Creando categorías de armas...")
    category_map = {}
    
    for cat_data in categories_data:
        # Verificar si ya existe
        existing = db.query(WeaponCategory).filter(WeaponCategory.name == cat_data["name"]).first()
        if existing:
            print(f"   ⚠️  {cat_data['name']} - Ya existe (ID: {existing.id})")
            category_map[cat_data["name"]] = existing.id
        else:
            category = WeaponCategory(**cat_data)
            db.add(category)
            db.flush()  # Para obtener el ID
            category_map[cat_data["name"]] = category.id
            print(f"   ✅ {cat_data['name']} - ID: {category.id}")
    
    db.commit()
    
    # Armas específicas de Monster Hunter
    weapons_data = [
        {"name": "Rathalos Glinsword", "category": "Great Sword", "description": "Gran espada forjada con materiales del Rathalos. Alta afinidad de fuego."},
        {"name": "Wyvern Blade 'Fall'", "category": "Great Sword", "description": "Espada gigante hecha de huesos de Wyvern. Gran daño bruto."},
        {"name": "Buster Sword", "category": "Great Sword", "description": "Espada básica pero confiable. Perfecta para principiantes."},
        
        {"name": "Divine Slasher", "category": "Long Sword", "description": "Katana sagrada con alto daño blanco. Requiere habilidad excepcional."},
        {"name": "Nargacuga Blade", "category": "Long Sword", "description": "Espada ágil del Nargacuga. Alta afinidad crítica natural."},
        {"name": "Iron Katana", "category": "Long Sword", "description": "Katana de hierro tradicional. Base sólida para mejoras."},
        
        {"name": "Rathalos Edge", "category": "Sword and Shield", "description": "Espada y escudo de Rathalos. Balance perfecto de ataque y defensa."},
        {"name": "Corona", "category": "Sword and Shield", "description": "Espada elegante con escudo dorado. Apariencia real."},
        
        {"name": "Fire and Ice", "category": "Dual Blades", "description": "Espadas gemelas con elementos opuestos. Fuego y hielo en armonía."},
        {"name": "Twin Nails", "category": "Dual Blades", "description": "Garras gemelas de Tigrex. Fuerza bruta sin elemento."},
        {"name": "Suzuka Twins", "category": "Dual Blades", "description": "Espadas gemelas legendarias. Perfectamente balanceadas."},
        
        {"name": "Diablos Hammer", "category": "Hammer", "description": "Martillo masivo de Diablos. El más alto daño bruto sin elemento."},
        {"name": "Iron Hammer", "category": "Hammer", "description": "Martillo de hierro pesado. Herramienta fundamental del cazador."},
        
        {"name": "Fortissimo II", "category": "Hunting Horn", "description": "Cuerno con melodías de ataque. Fortalece todo el grupo."},
        {"name": "Bone Horn", "category": "Hunting Horn", "description": "Cuerno hecho de hueso de monstruo. Sonido profundo y resonante."},
        
        {"name": "Chrome Lance", "category": "Lance", "description": "Lanza brillante de acero cromado. Excelente defensa."},
        {"name": "Iron Lance", "category": "Lance", "description": "Lanza básica pero efectiva. Alcance confiable."},
        
        {"name": "Royal Burst", "category": "Gunlance", "description": "Gunlance real con gran capacidad de explosión."},
        {"name": "Iron Gunlance", "category": "Gunlance", "description": "Gunlance de hierro estándar. Balance de poder y control."},
        
        {"name": "Power Smasher", "category": "Switch Axe", "description": "Switch Axe con gran potencia en modo espada."},
        {"name": "Proto Iron Axe", "category": "Switch Axe", "description": "Hacha transformable básica. Introducción al estilo."},
        
        {"name": "Diablos Tyrannis", "category": "Charge Blade", "description": "Charge Blade de Diablos. Devastadores ataques SAED."},
        {"name": "Defender Charge Blade", "category": "Charge Blade", "description": "Espada cargada del defensor. Equilibrio perfecto."},
        
        {"name": "True Gae Bolg", "category": "Insect Glaive", "description": "Glaive legendario con insecto veloz. Dominio aéreo supremo."},
        {"name": "Iron Blade", "category": "Insect Glaive", "description": "Glaive de hierro con kinsect básico. Gran movilidad."},
        
        {"name": "Hazak Velos II", "category": "Bow", "description": "Arco del Vaal Hazak. Elemento dragón con veneno."},
        {"name": "Flying Kadachi Strikebow", "category": "Bow", "description": "Arco eléctrico de Tobi-Kadachi. Rápido y paralizante."},
        {"name": "Iron Bow", "category": "Bow", "description": "Arco de hierro confiable. Buena base para comenzar."},
        
        {"name": "Karma", "category": "Light Bowgun", "description": "Ballesta ligera de Nergigante. Munición perforante especializada."},
        {"name": "Aqua Assault", "category": "Light Bowgun", "description": "Ballesta acuática ligera. Disparo rápido de agua."},
        
        {"name": "Dark Devourer", "category": "Heavy Bowgun", "description": "Ballesta pesada de Deviljho. Tremendo poder de fuego."},
        {"name": "Iron Assault", "category": "Heavy Bowgun", "description": "Ballesta pesada de hierro. Gran capacidad de munición."}
    ]
    
    print("\n🗡️ Creando armas específicas...")
    weapons_created = 0
    
    for weapon_data in weapons_data:
        category_name = weapon_data.pop("category")
        category_id = category_map.get(category_name)
        
        if not category_id:
            print(f"   ⚠️ Categoría no encontrada para: {weapon_data['name']}")
            continue
        
        # Verificar si ya existe
        existing = db.query(Weapon).filter(Weapon.name == weapon_data["name"]).first()
        if existing:
            print(f"   ⚠️  {weapon_data['name']} - Ya existe")
            continue
        
        weapon = Weapon(category_id=category_id, **weapon_data)
        db.add(weapon)
        weapons_created += 1
        print(f"   ✅ {weapon_data['name']}")
    
    db.commit()
    
    # Resumen
    print("\n" + "=" * 70)
    print("📊 RESUMEN DE LA BASE DE DATOS")
    print("=" * 70)
    
    categories_count = db.query(WeaponCategory).count()
    weapons_count = db.query(Weapon).count()
    
    print(f"✅ Total de categorías: {categories_count}")
    print(f"✅ Total de armas: {weapons_count}")
    print(f"✅ Nuevas armas creadas: {weapons_created}")
    
    print("\n🎮 Base de datos poblada exitosamente!")
    print("🌐 Accede a la wiki en: http://127.0.0.1:5000")
    
except Exception as e:
    db.rollback()
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()
