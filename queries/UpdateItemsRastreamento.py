from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import read_db_config
import datetime
import json

def update_items_rastreamento(tipo_registro, id_variaveis_de_rastreamento, id_modulo_rastreador, id_registro_de_rastreamento, item):

    for key in item.keys():
        sql_update_itens_rastreamento = """
        UPDATE itens_de_rastreamento 
            SET    vlr_itens_de_rastreamento = "{CAMPO}", 
                id_ult_registros_de_rastreamento = 
                {ID_REGISTRO_RASTREAMENTO} 
            WHERE  itens_de_rastreamento.id_variaveis_de_rastreamento = 
                        {VARIAVEIS_DE_RASTREAMENTO} 
                AND itens_de_rastreamento.id_modulo_rastreador = 
                    {ID_MODULO_RASTREADOR} 
                AND itens_de_rastreamento.id_tipo_reg_rastreamento = {TIPO_REGISTRO}""".format(
                    CAMPO = key,
                    TIPO_REGISTRO = tipo_registro,
                    VARIAVEIS_DE_RASTREAMENTO = id_variaveis_de_rastreamento,
                    ID_MODULO_RASTREADOR = id_modulo_rastreador,
                    ID_REGISTRO_RASTREAMENTO = id_registro_de_rastreamento) 
    try:
        #print(sql_update_itens_rastreamento)
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute(sql_update_itens_rastreamento)
    except Error as e:
        print(e)
    finally:
        cursor.close()
        conn.close()