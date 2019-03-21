from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import read_db_config
import datetime


def conjunto_rastreado(id_modulo_rastreador):
    import ipdb; ipdb.set_trace()
        
    sql_conjunto_rastreado = """
    SELECT ID_CONJUNTO_RASTREADO, 
        ID_CLASSE_COISA, 
        ID_COISA, 
        ID_CLIENTE,
        ID_SUB_CONTA
        DT_HR_ULT_TRANSMISSAO
        
    FROM   CONJUNTO_RASTREADO 
    WHERE  CONJUNTO_RASTREADO.ID_MODULO_RASTREADOR = {ID_MODULO_RASTREADOR}
        AND STATUS_CONJUNTO_RASTREADO = 1 LIMIT 1
            """.format(ID_MODULO_RASTREADOR = id_modulo_rastreador)

    try:          
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute(sql_conjunto_rastreado)
        row = cursor.fetchone()

        if not row:
            e = "Sem registros para este item no CONJUNTO_RASTREADO"
            log_erros(item, e, 'CONJUNTO_RASTREADO')
            
        d = dict() 
        d['idcliente'] = row[3]
        d['idcoisa'] = row[3]
        d['idclassecoisa'] = row[1]
        d['id_conjunto_rastreado'] = row[0]
        d['id_sub_conta'] = row[4]

        return d

    except Error as e:
        log_erros(item, e, 'CONJUNTO_RASTREADO')
    finally:
        cursor.close()
        conn.close()