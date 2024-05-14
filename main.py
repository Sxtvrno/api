import pymysql
import pymysql.cursors
from app import app
from config import mysql
from flask import jsonify
from flask import request


@app.route('/create/<id_producto>/<nombre_producto>/<valor_producto>/', methods=['POST'])
def create_producto(id_producto, nombre_producto, valor_producto):
    try:
        conn = mysql.connect
        cursor = conn.cursor()
        sqlQuery = "INSERT INTO producto(id_producto, nombre_producto, valor_producto) VALUES(DEFAULT, %s, %s, %s)"
        bindData = (id_producto, nombre_producto, valor_producto)
        cursor.execute(sqlQuery, bindData)
        conn.commit()
        response = jsonify('Producto agregado exitosamente')
        response.status_code = 200
        cursor.close()
        conn.close()
        return response
    except Exception as e:
        print(e)



@app.route('/', methods=['GET'])
def info_prod():
        try:
              
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT id_producto, nombre_producto, valor_producto FROM producto")
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



        
@app.route('/update', methods=['PUT'])
def actualizar_prod():
    try:
        _json = request.json
        _id = _json['id_producto']
        _name = _json['nombre_producto']
        _price = _json['valor_producto']
        if _name and _price and _id and request.method == 'PUT':			
            sqlQuery = "UPDATE producto SET nombre_producto=%s, precio=%s WHERE id_producto=%s"
            bindData = (_name, _price, _id,)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            response = jsonify('producto updated successfully!')
            response.status_code = 200
            return response
        else:
            return showMessage()
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close() 
        


@app.route('/delete/<int:id_producto>', methods=['DELETE'])
def eliminar_prod(idProducto):
    try:
        conn = mysql.connect
        cursor = conn.cursor()
        cursor.execute("DELETE FROM producto WHERE id_producto =%s", {idProducto})
        conn.commit()
        response = jsonify("Producto de código %s borrado" % idProducto)
        response.status_code = 200
        cursor.close()
        conn.close()
        return response
    except Exception as e:
        print(e)






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