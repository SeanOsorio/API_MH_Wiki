# Changelog

## [2.0.0] - Monster Hunter Wilds Edition - 2025-11-08

### 🎨 Added - Monster Hunter Wilds Theme System
- **Dual Theme System**: Complete day/night mode toggle with Monster Hunter Wilds color palette
  - Day Mode: Warm earth tones (#b08e36, #97b78d) with cream backgrounds (#f7f5ef)
  - Night Mode: Dark atmospheric backgrounds (#1a1d17, #252822, #2f332b)
  - Orange accent colors (#c0821a, #e0b054) replacing old gold
  - Theme toggle button with smooth transitions and localStorage persistence

### 🎮 Added - WikiDex-Style Frontend
- **Three-Level Navigation System**:
  - `/weapons` - Category grid view with weapon counts
  - `/weapons/category/{id}` - WikiDex-style table listing weapons by category
  - `/weapons/{id}` - Detailed weapon view with stats and descriptions
- **Responsive Design**: Mobile-friendly layouts with CSS Grid
- **Interactive Elements**: Hover effects, smooth transitions, and dynamic loading
- **Breadcrumb Navigation**: Clear page hierarchy and navigation paths

### 🗃️ Database & Backend
- **PostgreSQL Migration**: Fully migrated from MongoDB to PostgreSQL on Railway
  - Host: tramway.proxy.rlwy.net:42753
  - Converted PyMongo to SQLAlchemy ORM
  - Maintained data integrity with proper relationships
- **Seeded Database**: 14 weapon categories and 32 Monster Hunter weapons
- **API Blueprint Separation**: All API routes now under `/api` prefix

### 🐛 Fixed
- Fixed AttributeError issues in controllers (dict vs object access)
- Fixed dark mode white boxes by implementing proper CSS variable system
- Fixed weapon list loading issue (API response structure mismatch)
- Corrected gradient directions and color applications across all templates

### 🎨 Styling Improvements
- Converted all hardcoded colors to CSS custom properties
- Implemented proper color contrast for accessibility
- Added themed shadows and borders using CSS variables
- Updated all component styles to support both themes seamlessly

### 📝 Templates Updated
- `base.html` - Added theme toggle button and script
- `weapons_categories.html` - Category cards with theme support
- `weapons_list.html` - WikiDex table with adaptive colors
- `weapon_detail.html` - Detailed view with themed sections
- `style.css` - Complete CSS variable system (626 lines)

## [1.0.0] - First Strike - 2025-11-05

### Added
- Initial Flask application structure
- MongoDB integration with PyMongo
- Basic CRUD API for weapons and categories
- Repository pattern implementation
- Service layer architecture
- Basic error handling and logging

---

**Legend:**
- 🎨 Design & UI
- 🎮 Features
- 🗃️ Database & Backend
- 🐛 Bug Fixes
- 📝 Documentation
- ⚡ Performance
- 🔒 Security
