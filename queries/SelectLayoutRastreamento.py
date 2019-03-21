from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import read_db_config


def layout_rastreamento(tipo_registro, dh_equipamento):
    import ipdb; ipdb.set_trace()
        
    sql_layout_rastreamento = """
            SELECT   id_variaveis_de_rastreamento, 
            id_tipo_reg_rastreamento, 
            id_layout_reg_rastreamento, 
            status_variavel_de_rastreamento, 
            desc_variavel_de_rastreamento, 
            desc_coluna_tab_historico, 
            seq_apresentacao, 
            posicao_inicial, 
            posicao_final, 
            ind_tp_campo, 
            comando_conversao_campo, 
            qtd_bytes_inteiros, 
            qtd_bytes_decimais, 
            qtd_bytes_alfanumericos 
    FROM     variaveis_de_rastreamento 
    WHERE    variaveis_de_rastreamento.id_tipo_reg_rastreamento = {TIPO_REGISTRO}
    AND      status_variavel_de_rastreamento = 1 
    AND      id_layout_reg_rastreamento IN 
            ( 
                    SELECT 
                        MAX(id_layout_reg_rastreamento) 
                    FROM   layout_reg_rastreamento 
                    WHERE  layout_reg_rastreamento.id_tipo_reg_rastreamento = {TIPO_REGISTRO}
                    AND    layout_reg_rastreamento.dt_hr_ini_validade <= '{DH_EQUIPAMENTO}' 
                    AND    layout_reg_rastreamento.dt_hr_fim_validade >= '{DH_EQUIPAMENTO}' )
    ORDER BY variaveis_de_rastreamento.seq_apresentacao LIMIT 1""".format(
        TIPO_REGISTRO = tipo_registro,
        DH_EQUIPAMENTO = dh_equipamento)


    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute(sql_layout_rastreamento)
        rows = cursor.fetchone()

        if not rows:
            e = "Sem registros para nome tabela variaveis rastreamento"
            log_erros(item, e, 'variaveis_de_rastreamento')

        d = dict() 
        d['id_variaveis_de_rastreamento'] = row[0]
        d['id_tipo_reg_rastreamento'] = row[1]
        d['id_layout_reg_rastreamento'] = row[2]
        d['ind_tp_campo'] = row[9]
        d['qtd_bytes_decimais'] = row[12] 
           
        return d
        

    except Error as e:
        log_erros(item, e, 'variaveis_de_rastreamento')

    finally:
        cursor.close()
        conn.close()    