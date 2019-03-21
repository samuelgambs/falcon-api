import falcon, json, requests
from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import read_db_config
import datetime, time
from queries.SelectModuloRastreado import modulo_rastreador
from queries.SelectConjuntoRastreado import conjunto_rastreado
from queries.SelectLayoutRastreamento import layout_rastreamento
from queries.SelectTabelaHistorico import historico_rastreamento
from queries.InsertRegistroRastreamento import registro_rastreamento
from queries.SelectUltimoRegistro import ultimo_registro
from queries.InsertTabelaRastreamento import ultimo_registro
from queries.InsertRegistroRastreamento import insert_historico_rastreamento
from queries.UpdateItemsRastreamento import update_items_rastreamento
from queries.logErros import log_erros



DT_HR_PROCESSAMENTO = time.strftime("%Y-%m-%d %H:%M:%S")

class QuoteResource:
    
    def on_put(self, request, response, txn_id=None):
        """Responds to PUT request containing events."""
        response.body = "{}"

        request.context["body"] = request.stream.read()
        try:
            items = json.loads(request.context["body"].decode("utf-8"))
            """
            import ipdb; ipdb.set_trace()

            json_obj = json.dumps(items)
            json_size = len(json_obj)
            """

            for item in items:
                #formatando date time
                dt_hr_ult_transmissao = datetime.datetime.strptime(item['dhrecebimento'], "%Y-%m-%d %H:%M:%S")
                dh_equipamento = datetime.datetime.strptime(item['dhequipamento'], "%Y-%m-%d %H:%M:%S")
                #data_gravacao = datetime.datetime.strptime(item['data_gravacao'], "%Y-%m-%d %H:%M:%S")    
                data_recebimento = datetime.datetime.strptime(item['dhrecebimento'], "%Y-%m-%d %H:%M:%S")   

                #queries
                id_modulo_rastreador = modulo_rastreador(item['idmodulo'], item['fabricante'], item['idgateway'])
                conjunto_rastreado_dict = conjunto_rastreado(id_modulo_rastreador)
                layout_rastreamento_dict = layout_rastreamento[item['tiporegistro', dh_equipamento]]
                tabela_historico_rastreamento = historico_rastreamento(item['tiporegistro'])
                insert_registro_rastreamento = registro_rastreamento(conjunto_rastreado_dict['idcliente'], conjunto_rastreado_dict['idclassecoisa'], conjunto_rastreado_dict['idcoisa'], data_recebimento, layout_rastreamento_dict['id_layout_reg_rastreamento'], layout_rastreamento_dict['id_tipo_reg_rastreamento'], item['gateway'], id_modulo_rastreador, dh_equipamento, item)
                id_registro_de_rastreamento = ultimo_registro()
                insert_historico_rastreamento(tabela_historico_rastreamento, idcliente, idclassecoisa, idcoisa, data_recebimento, id_layout_reg_rastreamento, id_tipo_reg_rastreamento, idgateway, id_modulo_rastreador, dh_equipamento, item)
                update_items_rastreamento(tipo_registro, id_variaveis_de_rastreamento, id_modulo_rastreador, id_registro_de_rastreamento, item)
                update_conjunto_rastreado(data_gravacao, dh_equipamento, id_modulo_rastreador)
                
        except(KeyError, ValueError, UnicodeDecodeError):
            response.status = falcon.HTTP_400
            response.body = "Malformed request body"
            return
        

api = falcon.API()
api.add_route('/', QuoteResource())

