# Pre-Entrega: Automatización QA - SauceDemo

## 1. Propósito del proyecto

El objetivo del proyecto es automatizar pruebas funcionales básicas sobre [SauceDemo](https://www.saucedemo.com/)

Las pruebas verifican el inicio de sesión, la visualización del catálogo de productos y las principales interacciones con el carrito de compras.

## 2. Tecnologías utilizadas

- **Python:** 
- **Pytest:** 
- **Selenium WebDriver:** 
- **Google Chrome:** 
- **Git y GitHub:** 

## 3. Requisitos previos

Antes de ejecutar el proyecto, es necesario contar con:

- Python instalado.
- Google Chrome instalado.
- Git instalado.
- Un entorno virtual de Python para aislar las dependencias del proyecto.

## 4. Instalación

### Clonar el repositorio

```bash
git clone git@github.com:Ariel1021/pre-entrega-automation-testing-ariel-rodrigo-salazar-lopez.git
```

### Crear y activar un entorno virtual

En Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

En Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### Instalar las dependencias

```bash
python -m pip install pytest selenium pytest-html
```

Selenium Manager puede gestionar automáticamente el controlador del navegador en versiones modernas de Selenium.

## 5. Ejecución de las pruebas

Para ejecutar todos los tests:

```bash
pytest tests/test_saucedemo.py -v
```

Para ejecutar los tests y generar un reporte HTML:

```bash
pytest tests/test_saucedemo.py -v --html=reports/reporte.html 
```

El reporte generado permite consultar los resultados de la ejecución, incluyendo las pruebas aprobadas y fallidas.

## 6. Casos de prueba implementados

1. **Login exitoso:** verifica el inicio de sesión con credenciales válidas.
2. **Verificación del inventario:** comprueba los títulos de la página y de la sección.
3. **Productos visibles:** verifica la presencia de productos en el catálogo.
4. **Validación de interfaz:** comprueba la visibilidad del menú y del selector de ordenamiento.
5. **Agregar producto al carrito:** verifica que el botón cambie su estado después de agregar un producto.
6. **Contador del carrito:** comprueba que el contador refleje la cantidad de productos agregados.
7. **Navegación al carrito:** verifica el acceso a la página del carrito.
8. **Producto en el carrito:** comprueba que el producto agregado coincida con el seleccionado en el catálogo.

Cada test prepara su propio estado inicial para poder ejecutarse de forma independiente.

## 7. Estructura del proyecto

```text

pre-entrega-automation-testing-ariel-rodrigo-salazar-lopez/

├── tests/
│   └── test_saucedemo.py
├── utils/
│   └── helpers.py
├── reports/
│   ├── assets
│   │   └── style.css
│   └── reporte.html
├── README.md
└── .gitignore
```

## 8. Sitio bajo prueba

https://www.saucedemo.com/
