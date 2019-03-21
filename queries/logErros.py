def log_erros(self, item, erro, tabela):
    data_gravacao = datetime.datetime.strptime(item['dhrecebimento'], "%Y-%m-%d %H:%M:%S")

    if type(erro) is str:
        payload  = {
        "ID_CLIENTE" : 0,
        "ID_SUB_CONTA" : 0,
        "ID_USUARIO" : 0,
        "ID_WEBSERVICES_RC" : 'PROCESSA_GATEWAY',	
        "DT_HR_ERRO" : DT_HR_PROCESSAMENTO,
        "CODIGO_ERRO_BD" : 0,
        "MSG_ERRO_BD" : erro,
        "TABELA_VIEW_RELACIONADA" : tabela,
        "COMANDO_UTILIZADO" : 0,
        "JSON" : item
        }
    else:
        payload  = {
            "ID_CLIENTE" : 0,
            "ID_USUARIO" : 0,
            "ID_WEBSERVICES_RC" : 'PROCESSA_GATEWAY',	
            "DT_HR_ERRO" : DT_HR_PROCESSAMENTO,
            "CODIGO_ERRO_BD" : erro.errno,
            "MSG_ERRO_BD" : erro.msg,
            "TABELA_VIEW_RELACIONADA" : erro,
            "COMANDO_UTILIZADO" : erro.sqlstate,
            "JSON" : item
        }

    url = "http://brasiltrack.com/APP001_ERROS_IO"

    r = requests.get(url, params=payload)
    print(r.url)

    sql_insert_registro_rastreamento = """
            INSERT INTO rc.registros_de_rastreamento
            (
            ID_GATEWAY,
            DT_HR_RECEBIMENTO,
            DT_HR_PROCESSAMENTO,
            JSON_REGISTRO_DE_RASTREAMENTO)
            VALUES(
            {ID_GATEWAY},
            "{DT_HR_RECEBIMENTO}",
            "{DT_HR_PROCESSAMENTO}",
            '{JSON_REGISTRO_DE_RASTREAMENTO}')
            """.format(
            ID_GATEWAY = item['IDGATEWAY'],
            DT_HR_RECEBIMENTO = data_gravacao,
            DT_HR_PROCESSAMENTO = DT_HR_PROCESSAMENTO,
            JSON_REGISTRO_DE_RASTREAMENTO = json.dumps(item))

    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute(sql_insert_registro_rastreamento)
        
    except Error as e:
        print(e)
        print("Erro ao salvar na tabela registros_de_rastreamento")
    finally:
        cursor.close()
        conn.close()