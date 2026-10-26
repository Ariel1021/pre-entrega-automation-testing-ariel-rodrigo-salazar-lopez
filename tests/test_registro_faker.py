import pytest
from faker import Faker
from pages.registro_page import RegistroPage

def test_registro_usuario_aleatorio(driver):
    """Test que usa Faker para generar datos aleatorios"""
    fake = Faker('es_ES')
    
    # Generar datos únicos para cada ejecución
    email = fake.email()
    print(f"\n📧 Email generado: {email}")
    
    # Usar los datos en el test
    registro_page = RegistroPage(driver)
    registro_page.abrir()
    registro_page.completar_email(email)
    registro_page.enviar()
    
    # Verificar que la URL cambió (indicando que se procesó el form)
    assert "email_sent" in driver.current_url, "No se procesó el formulario correctamente"
    
    # Verificar que apareció el mensaje
    mensaje = registro_page.obtener_mensaje()
    print(f"📋 Mensaje recibido: {mensaje}")
    assert "sent" in mensaje.lower(), f"No se encontró confirmación en: {mensaje}"

@pytest.mark.parametrize("locale", ['es_ES', 'es_AR', 'es_MX', 'en_US'])
def test_emails_diferentes_locales(driver, locale):
    """Test que genera emails con diferentes configuraciones regionales"""
    fake = Faker(locale)
    
    email = fake.email()
    nombre = fake.name()
    print(f"\n🌍 Locale: {locale}")
    print(f"👤 Nombre: {nombre}")
    print(f"📧 Email: {email}")
    
    registro_page = RegistroPage(driver)
    registro_page.abrir()
    registro_page.completar_email(email)
    registro_page.enviar()
    
    # Verificar que se procesó el formulario
    assert "email_sent" in driver.current_url, f"Formulario no procesado para locale {locale}"

def test_datos_faker_completos():
    """Test que muestra todos los tipos de datos que puede generar Faker"""
    fake = Faker('es_ES')
    
    print(f"\n🧑 INFORMACIÓN PERSONAL:")
    print(f"   Nombre completo: {fake.name()}")
    print(f"   Nombre: {fake.first_name()}")
    print(f"   Apellido: {fake.last_name()}")
    print(f"   Email: {fake.email()}")
    print(f"   Teléfono: {fake.phone_number()}")
    
    print(f"\n🏠 DIRECCIONES:")
    print(f"   Dirección: {fake.address()}")
    print(f"   Ciudad: {fake.city()}")
    print(f"   País: {fake.country()}")
    print(f"   Código postal: {fake.postcode()}")
    
    print(f"\n🌐 INTERNET:")
    print(f"   URL: {fake.url()}")
    print(f"   Dominio: {fake.domain_name()}")
    print(f"   Usuario: {fake.user_name()}")
    print(f"   Contraseña: {fake.password()}")
    
    print(f"\n🔢 NÚMEROS Y FECHAS:")
    print(f"   Número aleatorio: {fake.random_int(1, 100)}")
    print(f"   Fecha: {fake.date()}")
    print(f"   Hora: {fake.time()}")
    
    print(f"\n📝 TEXTO:")
    print(f"   Palabra: {fake.word()}")
    print(f"   Oración: {fake.sentence()}")
    print(f"   Párrafo: {fake.text()[:100]}...")
    
    print(f"\n🏢 EMPRESA:")
    print(f"   Empresa: {fake.company()}")
    
    # Este test siempre pasa, solo es para mostrar datos
    assert True

def test_multiples_usuarios_faker(driver):
    """Test que crea múltiples usuarios con datos únicos"""
    fake = Faker('es_ES')
    
    print(f"\n👥 GENERANDO 5 USUARIOS ÚNICOS:")
    
    emails_generados = []
    
    for i in range(1, 6):
        nombre = fake.name()
        email = fake.email()
        telefono = fake.phone_number()
        
        print(f"   Usuario {i}:")
        print(f"     Nombre: {nombre}")
        print(f"     Email: {email}")
        print(f"     Teléfono: {telefono}")
        
        # Verificar que cada email es único
        assert email not in emails_generados, f"Email duplicado: {email}"
        emails_generados.append(email)
        
        assert "@" in email
        assert len(nombre) > 0
    
    print(f"\n✅ Todos los emails son únicos: {len(set(emails_generados)) == 5}")
    assert True