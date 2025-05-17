# Ferremas - API de Gestión de Productos y Pagos

Proyecto backend desarrollado en Python con Flask para gestionar un inventario de productos (Ferretería) con conexión a base de datos MySQL. Además, integra procesamiento de pagos con Transbank Webpay Plus en modo prueba.

---

## Descripción

Ferremas es una API REST que permite:

- Crear, leer, actualizar y eliminar productos en un inventario.
- Consultar productos con su valor en pesos chilenos y su conversión aproximada a dólares estadounidenses (USD) usando la tasa de cambio actual del Banco Central de Chile.
- Gestionar transacciones de pago simuladas con Transbank Webpay Plus.
- Interfaz básica con páginas HTML para la administración y visualización.

---

## Tecnologías utilizadas

- Python 3.7+
- Flask
- Flask-MySQL
- Flask-CORS
- PyMySQL
- Requests
- Transbank SDK (Webpay Plus)
- Base de datos MariaDB / MySQL

---

## Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/tuusuario/ferremas.git

cd ferremas
```
Crea y activa un entorno virtual (opcional pero recomendado):

```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```
Instala las dependencias:

```bash
pip install -r requirements.txt
Configura la base de datos MySQL:
```
Crea una base de datos llamada ferremas.

Ejecuta el script ferremas.sql para crear la tabla producto y cargar datos iniciales

## Uso
Ejecuta la aplicación con:

```bash
python main.py
```
La API estará disponible en http://localhost:5000.

## Endpoints principales
| Ruta                                      | Método    | Descripción                                        |
| ----------------------------------------- | --------- | -------------------------------------------------- |
| `/`                                       | GET       | Página principal (index.html)                      |
| `/admin`                                  | GET       | Página de administración (admin.html)              |
| `/producto`                               | GET       | Listar todos los productos con precio en CLP y USD |
| `/producto/<id_producto>`                 | GET       | Detalle de un producto por ID                      |
| `/create/<nombre>/<valor>/<tipo>/<stock>` | POST      | Crear un nuevo producto                            |
| `/update/<id>/<valor>/<stock>`            | PUT/PATCH | Actualizar precio y stock de un producto           |
| `/delete/<id>`                            | DELETE    | Eliminar un producto por ID                        |
| `/create_transaction`                     | GET       | Crear transacción de pago en modo prueba (Webpay)  |
| `/commit_transaction`                     | GET/POST  | Confirmar transacción y mostrar estado             |


Notas:
La conversión de precios a USD se realiza usando la tasa de cambio diaria oficial obtenida del Banco Central de Chile mediante su API pública pero con mis credenciales, en caso de utilizarse para una evaluacion cambiar las credenciales.

La integración con Transbank Webpay Plus está configurada en modo TEST con credenciales de prueba.

Las credenciales de base de datos y Transbank están visibles en los archivos para facilitar pruebas; se recomienda proteger esta información en un entorno de producción.

Licencia
Este proyecto es de uso privado / académico. Puedes adaptarlo y usarlo según tus necesidades.

Si tienes dudas o quieres colaborar, abre un issue o contacta conmigo.

¡Gracias por usar Ferremas! 🚀
