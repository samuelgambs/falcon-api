from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import read_db_config

#### A FAZER : IMPLEMENTAR ORM
def modulo_rastreador(modulo, fabricante, gateway):
    import ipdb; ipdb.set_trace()
        
    sql_modulo_rastreador = """
        SELECT MODULO_RASTREADOR.ID_MODULO_RASTREADOR, 
            MODULO_RASTREADOR.ID_MODELO_RASTREADOR, 
            GATEWAY.ID_GATEWAY 
        FROM   MODULO_RASTREADOR, 
            GATEWAY 
        WHERE  MODULO_RASTREADOR.ID_ORIGINAL = {MODULO} 
            AND MODULO_RASTREADOR.ID_FABRICANTE =  {FABRICANTE}
            AND GATEWAY.ID_MODELO_MODULO_RASTREAMENTO = 
                MODULO_RASTREADOR.ID_MODELO_RASTREADOR 
            AND GATEWAY.CODIGO_GATEWAY_FISICO = {GATEWAY}""".format(
                MODULO = modulo, 
                FABRICANTE = fabricante, 
                GATEWAY = gateway )
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute(sql_modulo_rastreador)
        rows = cursor.fetchall()

        if not rows:
            e = "Sem registros para este item no módulo rastreador"
            #log_erros(item, e, 'MODULO_RASTREADOR')
            print(e)

        for row in rows:
            id_modulo_rastreador = row[0]
            return id_modulo_rastreador
        
    except Error as e:            
        #log_erros(item, e, 'MODULO_RASTREADOR')
        print(e)

    finally:
        cursor.close()
        conn.close()