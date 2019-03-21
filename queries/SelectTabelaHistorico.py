from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import read_db_config

def historico_rastreamento(tipo_registro):
    
    sql_historico_rastreamento = """
    SELECT A.nome_tab_hst_rastreamento 
    FROM   classe_tipo_reg_rastreamento AS A, 
        conjunto_rastreado AS B 
    WHERE  A.id_classe_coisa = B.id_classe_coisa 
        AND A.id_tipo_reg_rastreamento = {registro} 
        AND A.ind_setup_ok = 1 LIMIT 1""".format(registro = tipo_registro)

    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute(sql_historico_rastreamento)
        row = cursor.fetchone()

        if not row:
            e = "Sem registros para nome tabela histórico rastreamento"
            print(e)
            log_erros(item, e, 'conjunto_rastreado')
        
        
        nome_tab_hst_rastreamento = row[0]
        return nome_tab_hst_rastreamento[2:-2] 

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()