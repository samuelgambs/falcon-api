from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import read_db_config
import datetime
import json


def insert_historico_rastreamento(tabela_historico_rastreamento, idcliente, idclassecoisa, idcoisa, data_recebimento, id_layout_reg_rastreamento, id_tipo_reg_rastreamento, idgateway, id_modulo_rastreador, dh_equipamento, item )
    sql_show_columns = "SHOW columns FROM {TABLE}".format(TABLE = tabela_historico_rastreamento)  
    
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute(sql_show_columns)
        columns = cursor.fetchall()

        if not columns:
            e = "Sem registros para nome tabela histórico "
            print(e)
            log_erros(item, e, 'tabela_historico')
            continue
        
        
    except Error as e:
        print(e)
        
    finally:
        cursor.close()
        conn.close()

    values = []
    row_values = []

    if ind_tp_campo == 'DE':
        divisor = 10 ** qtd_bytes_decimais
    ################# Requisito passado hoje
    """
    if item['tiporegistro'] == 3:

        SELECT 
        select_acesseorios  = SELECT * FROM ACESSORIOS 
                                WHERE ID_SUB_CONTA  = subconta.MODULO_RASTREADOR and
        num_serial = {hexa} and
        id_tipo_acessorio = 5 and
        status_acessorio = 1 

    
    if not: 
        break


    """


    for column in columns:
        for field, possible_values in item.items():
            field = field.upper()
            if (field == column[0]):
                row_values.append(column[0])
                if field[:5] == 'DT_HR':
                    possible_values = datetime.datetime.strptime(str(possible_values),  '%Y/%m/%d %H:%M:%S')
                    possible_values= str(possible_values)
                    possible_values = '"' + possible_values + '"' 
                if ind_tp_campo == 'DE':
                    possible_values = possible_values / divisor                       
                values.append(str(possible_values))


    """Take dictionary object dict and produce sql for 
    inserting it into the named table"""
    sql = 'INSERT INTO ' + nome_tab_hst_rastreamento
    sql += ' (  ID_CLIENTE, ID_CLASSE_COISA, ID_COISA, DT_HR_PROCESSAMENTO, '
    sql+=  ' ID_LAYOUT_REG_RASTREAMENTO, ID_TIPO_REG_RASTREAMENTO, ID_GATEWAY, ID_MODULO_RASTREADOR, DT_HR_MODULO, '
    sql += ', '.join(row_values)
    sql += ') VALUES (' + str(idcliente) + ',' + str(idclassecoisa) + ',' + str(idcoisa) + ', "' 
    sql += str(DT_HR_PROCESSAMENTO) +  '",' + str(id_layout_reg_rastreamento) + ',' + str(id_tipo_reg_rastreamento) + ',' 
    sql += str(item['idgateway']) + ',' + str(id_conjunto_rastreado) + ',"' +  str(dh_equipamento) + '",'
    sql += ', '.join(values)
    sql += ');'

    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute(sql)

    except Error as e:
        print(e)
        log_erros(item,e, nome_tab_hst_rastreamento)
    finally:
        cursor.close()
        conn.close()