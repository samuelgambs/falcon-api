from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import read_db_config
import datetime
import json

def update_conjunto_rastreado(data_gravacao, dh_equipamento, id_modulo_rastreador):

    sql_update_conjunto_rastreado = """
        UPDATE conjunto_rastreado 
        SET    dt_hr_penultima_transmissao = '{DH_AUXILIAR}', 
            dt_hr_ult_transmissao = '{DT_HR_ULT_TRANSMISSAO}', 
            ind_transmissao_ok = 1 
        WHERE  id_modulo_rastreador =  {ID_MODULO_RASTREADOR}
        AND    status_conjunto_rastreado = 1""".format(
        DH_AUXILIAR = data_gravacao,
        DT_HR_ULT_TRANSMISSAO = dh_equipamento,
        ID_MODULO_RASTREADOR=id_modulo_rastreador)

    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute(sql_update_conjunto_rastreado)

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()