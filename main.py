import pymysql
from app import app
from config import mysql
from flask import jsonify, request, redirect, render_template, url_for
from transbank.webpay.webpay_plus.transaction import Transaction, WebpayOptions
from transbank.common.integration_type import IntegrationType


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/create/<id_producto2>/<nombre_producto2>/<valor_producto2>/<tipo_producto2>', methods=['POST'])
def create_producto(id_producto2, nombre_producto2, valor_producto2, tipo_producto2):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sqlQuery = "INSERT INTO producto(id_producto, nombre_producto, valor_producto, tipo_producto) VALUES(%s, %s, %s,%s)"
        bindData = (id_producto2, nombre_producto2, valor_producto2, tipo_producto2)
        cursor.execute(sqlQuery, bindData)
        conn.commit()
        response = jsonify('Producto agregado exitosamente')
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
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
            cursor.execute("SELECT id_producto, tipo_producto, nombre_producto, valor_producto  FROM producto")
            empRows = cursor.fetchall()
            response = jsonify(empRows)
            response.status_code = 200
            return response
        except Exception as e:
            print(e)
        finally:
            cursor.close() 
            conn.close()  
@app.route('/producto/<int:id_producto>')
def detalle_prod(id_producto):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id_producto, nombre_producto, valor_producto FROM producto WHERE id_producto =%s", id_producto)
        empRow = cursor.fetchone()
        response = jsonify(empRow)
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()
@app.route('/update/<int:id_producto>/<valor_producto>', methods=['PUT', 'PATCH'])
def actualizar_producto(id_producto, valor_producto):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sqlQuery = "UPDATE producto SET valor_producto=%s WHERE id_producto=%s"
        bindData = (valor_producto, id_producto)
        cursor.execute(sqlQuery, bindData)
        conn.commit()
        response = jsonify("Producto actualizado correctamente")
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
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
        print(e)
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
        return f"Estado de la transacción: {response['status']}, Monto: {response['amount']}, Orden de compra: {response['buy_order']}, Codigo de autorización: {response['authorization_code']}"
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