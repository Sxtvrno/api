import pymysql
import requests
import datetime
from app import app
from config import mysql
from flask import jsonify, request, redirect, render_template, url_for
from transbank.webpay.webpay_plus.transaction import Transaction, WebpayOptions
from transbank.common.integration_type import IntegrationType

# Obtener la fecha actual
fecha_actual = datetime.datetime.now().strftime('%Y-%m-%d')

# Construir la URL con la fecha actual
url_base = "https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx"
user = "fr.vergarah@duocuc.cl"
password = "Francisco7711"
timeseries = "F073.TCO.PRE.Z.D"

# Crear la URL final
API_BCENTRAL = f"{url_base}?user={user}&pass={password}&firstdate={fecha_actual}&timeseries={timeseries}"


def get_exchange_rate():
    response = requests.get(API_BCENTRAL)
    if response.status_code == 200:
        data = response.json()
        # Acceder a la tasa de cambio en la estructura JSON proporcionada
        exchange_rate = data['Series']['Obs'][0]['value']
        return float(exchange_rate)
    else:
        raise Exception("Error al obtener la tasa de cambio.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/create/<nombre_producto2>/<valor_producto2>/<tipo_producto2>/<stock2>', methods=['POST'])
def create_producto(nombre_producto2, valor_producto2, tipo_producto2, stock2):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sqlQuery = "INSERT INTO producto(nombre_producto, valor_producto, tipo_producto, stock) VALUES(%s, %s,%s,%s)"
        bindData = (nombre_producto2, valor_producto2, tipo_producto2, stock2)
        cursor.execute(sqlQuery, bindData)
        conn.commit()
        response = jsonify('Producto agregado exitosamente')
        response.status_code = 200
        return response
    except Exception as e:
        print("Error al crear producto:", e)
        response = jsonify({"error": "No se pudo crear el producto"})
        response.status_code = 500
        return response
    finally:
        cursor.close() 
        conn.close()

@app.route('/producto', methods=['GET'])
def info_prod():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id_producto, tipo_producto, nombre_producto, valor_producto, stock FROM producto")
        empRows = cursor.fetchall()
        
        # Obtener la tasa de cambio
        try:
            exchange_rate = get_exchange_rate()
        except Exception as e:
            print("Error al obtener la tasa de cambio:", e)
            return jsonify({"error": str(e)}), 500
        
        # Convertir los precios a USD
        for row in empRows:
            row['valor_producto_usd'] = round(row['valor_producto'] / exchange_rate, 2)
        
        response = jsonify(empRows)
        response.status_code = 200
        return response
    except Exception as e:
        print("Error al obtener productos:", e)
        response = jsonify({"error": "No se pudieron obtener los productos"})
        response.status_code = 500
        return response
    finally:
        cursor.close() 
        conn.close()

@app.route('/producto/<int:id_producto>')
def detalle_prod(id_producto):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id_producto, nombre_producto, valor_producto, stock FROM producto WHERE id_producto =%s", id_producto)
        empRow = cursor.fetchone()
        
        # Obtener la tasa de cambio
        try:
            exchange_rate = get_exchange_rate()
        except Exception as e:
            print("Error al obtener la tasa de cambio:", e)
            return jsonify({"error": str(e)}), 500
        
        # Convertir el precio a USD
        if empRow:
            empRow['valor_producto_usd'] = round(empRow['valor_producto'] / exchange_rate, 2)
        
        response = jsonify(empRow)
        response.status_code = 200
        return response
    except Exception as e:
        print("Error al obtener detalle del producto:", e)
        response = jsonify({"error": "No se pudo obtener el detalle del producto"})
        response.status_code = 500
        return response
    finally:
        cursor.close() 
        conn.close()

@app.route('/update/<int:id_producto>/<valor_producto>/<stock>', methods=['PUT', 'PATCH'])
def actualizar_producto(id_producto, valor_producto, stock):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sqlQuery = "UPDATE producto SET valor_producto=%s , stock =%s WHERE id_producto=%s"
        bindData = (valor_producto, stock, id_producto)
        cursor.execute(sqlQuery, bindData)
        conn.commit()
        response = jsonify("Producto actualizado correctamente")
        response.status_code = 200
        return response
    except Exception as e:
        print("Error al actualizar producto:", e)
        response = jsonify({"error": "No se pudo actualizar el producto"})
        response.status_code = 500
        return response
    finally:
        cursor.close()
        conn.close()

@app.route('/delete/<int:id_producto>', methods=['DELETE'])
def eliminar_prod(id_producto):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM producto WHERE id_producto =%s", (id_producto,))
        conn.commit()
        response = jsonify("Producto de código %s borrado" % id_producto)
        response.status_code = 200
        return response
    except Exception as e:
        print("Error al eliminar producto:", e)
        response = jsonify({"error": "No se pudo eliminar el producto"})
        response.status_code = 500
        return response
    finally:
        cursor.close()
        conn.close()




# Configuración de las credenciales de prueba de Transbank
api_key_id = "597055555532"
api_key_secret = "579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C"
options = WebpayOptions(api_key_id, api_key_secret, IntegrationType.TEST)
transaction = Transaction(options)


@app.route('/create_transaction', methods=['GET'])
def create_transaction():
    buy_order = "ordenCompra12345678"
    session_id = "sesion1234557545"
    amount = request.args.get('amount')
    if not amount:
        return "Debe proporcionar un monto.", 400
    amount = int(amount)
    return_url = "http://localhost:5000/commit_transaction"
    response = transaction.create(buy_order, session_id, amount, return_url)
    return redirect(response['url'] + '?token_ws=' + response['token'])

@app.route('/commit_transaction', methods=['GET', 'POST'])
def commit_transaction():
    token = request.args.get('token_ws') if request.method == 'GET' else request.form.get('token_ws')
    try:
        response = transaction.commit(token)
        return render_template('commit.html',
                               status=response['status'],
                               amount=response['amount'],
                               buy_order=response['buy_order'],
                               authorization_code=response['authorization_code'])
    except Exception as e:
        return f"Error al confirmar la transacción: {e}"
    

@app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'Informacion no encontrada, Lorem Impsum: ' + request.url,
    }
    response = jsonify(message)
    response.status_code = 404
    return response




if __name__ == "__main__":
    app.run(debug=True)