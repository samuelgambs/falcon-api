from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import read_db_config
import datetime


def ultimo_registro():
    sql_id_ultimo_registro = """
        SELECT ID_REGISTRO_DE_RASTREAMENTO
        FROM registros_de_rastreamento
        WHERE ID_REGISTRO_DE_RASTREAMENTO > 1
        ORDER BY ID_REGISTRO_DE_RASTREAMENTO DESC
        LIMIT 1;"""

    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute(sql_id_ultimo_registro)
        row = cursor.fetchone()

        if not row:
            e = "Sem registros para registros_de_rastreamento"
            print(e)
            log_erros(item, e, 'registros_de_rastreamento')

        return row[0] 

    except Error as e:
        log_erros(item, e, 'registros_de_rastreamento')
    finally:
        cursor.close()
        conn.close()