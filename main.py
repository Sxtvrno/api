import pymysql
from app import app
from config import mysql
from flask import jsonify, request, redirect



@app.route('/')
def inicio():
    return("HOLA MUNDO")



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
    finally:
        cursor.close() 
        conn.close() 



@app.route('/productos', methods=['GET'])
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



        
@app.route('/update', methods=['PUT'])
def actualizar_prod():
    try:
        _json = request.json
        _id_producto = _json['id_producto']
        _nombre_producto = _json['nombre_producto']
        _valor_producto = _json['valor_producto']
        if _id_producto and _nombre_producto and _valor_producto and request.method == 'PUT':			
            sqlQuery = "UPDATE producto SET nombre_producto=%s, valor_producto=%s WHERE id_producto=%s"
            bindData = (_nombre_producto, _valor_producto, _id_producto,)
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