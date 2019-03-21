from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import read_db_config
import datetime
import json


def registro_rastreamento(
    idcliente, idclassecoisa, idcoisa, data_recebimento, id_layout_reg_rastreamento, id_tipo_reg_rastreamento, idgateway, id_modulo_rastreador, dh_equipamento, item ):

    import ipdb; ipdb.set_trace()
        
    sql_insert_registro_rastreamento = """
        INSERT INTO registros_de_rastreamento
        (ID_CLIENTE,
        ID_COISA,
        ID_TIPO_REG_RASTREAMENTO,
        ID_GATEWAY,
        ID_LAYOUT_REG_RASTREAMENTO,
        ID_MODULO_RASTREADOR,
        DT_HR_RECEBIMENTO,
        DT_HR_PROCESSAMENTO,
        JSON_REGISTRO_DE_RASTREAMENTO)
        VALUES(
        {ID_CLIENTE},
        {ID_COISA},
        {ID_TIPO_REG_RASTREAMENTO},
        {ID_GATEWAY},
        {ID_LAYOUT_REG_RASTREAMENTO},
        {ID_MODULO_RASTREADOR},
        "{DT_HR_RECEBIMENTO}",
        "{DT_HR_PROCESSAMENTO}",
        '{JSON_REGISTRO_DE_RASTREAMENTO}')""".format(ID_CLIENTE = idcliente,
        ID_CLASSE_COISA = idclassecoisa, 
        ID_COISA = idcoisa,
        DT_HR_RECEBIMENTO = data_recebimento,
        DT_HR_PROCESSAMENTO = data_recebimento,
        ID_LAYOUT_REG_RASTREAMENTO = id_layout_reg_rastreamento,
        ID_TIPO_REG_RASTREAMENTO = id_tipo_reg_rastreamento,
        ID_GATEWAY = item['idgateway'],
        ID_MODULO_RASTREADOR = id_modulo_rastreador,
        DT_HR_MODULO = dh_equipamento,
        JSON_REGISTRO_DE_RASTREAMENTO = json.dumps(item))

    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute(sql_insert_registro_rastreamento)
    except Error as e:
        print(e)
        log_erros(item,e,'registros_de_rastreamento')
    finally:
        cursor.close()
        conn.close()