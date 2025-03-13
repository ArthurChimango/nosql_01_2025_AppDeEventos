from pymongo import MongoClient

uri = "mongodb+srv://adm:1430@cluster0.puzceax.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)
db = client["AppEventos"]

usuarios = db["usuarios"]
eventos = db["eventos"]
notificacoes = db["notificacoes"]
relatorios = db["relatorios"]
historico_ocorrencias = db["historico_ocorrencias"]
servicos_emergencia = db["servicos_emergencia"]


pipeline_eventos_por_tipo = [
    {
        "$group": {
            "_id": "$tipo", 
            "total": { "$sum": 1 }  
        }
    }
]
resultado_eventos_por_tipo = eventos.aggregate(pipeline_eventos_por_tipo)
print("Eventos por Tipo:")
for doc in resultado_eventos_por_tipo:
    print(f"Tipo: {doc['_id']}, Total: {doc['total']}")


pipeline_usuarios_mais_de_30 = [
    {
        "$match": {
            "idade": { "$gt": 30 }  
        }
    }
]
resultado_usuarios_mais_de_30 = usuarios.aggregate(pipeline_usuarios_mais_de_30)
print("\nUsuários com mais de 30 anos:")
for doc in resultado_usuarios_mais_de_30:
    print(doc)


pipeline_media_avaliacao = [
    {
        "$group": {
            "_id": "$id_evento", 
            "media_avaliacao": { "$avg": "$avaliacao_usuarios" } 
        }
    }
]
resultado_media_avaliacao = relatorios.aggregate(pipeline_media_avaliacao)
print("\nMédia de Avaliação por Evento:")
for doc in resultado_media_avaliacao:
    print(f"Evento ID: {doc['_id']}, Média de Avaliação: {doc['media_avaliacao']}")


pipeline_notificacoes_periodo = [
    {
        "$match": {
            "data_hora": {
                "$gte": "2024-09-10T00:00:00Z",  
                "$lt": "2024-09-11T00:00:00Z"   
            }
        }
    }
]
resultado_notificacoes_periodo = notificacoes.aggregate(pipeline_notificacoes_periodo)
print("\nNotificações Enviadas no Período (10/09/2024):")
for doc in resultado_notificacoes_periodo:
    print(doc)


pipeline_eventos_por_severidade = [
    {
        "$group": {
            "_id": "$severidade",
            "total": { "$sum": 1 }
        }
    }
]
resultado_eventos_por_severidade = eventos.aggregate(pipeline_eventos_por_severidade)
print("Eventos por Severidade:")
for doc in resultado_eventos_por_severidade:
    print(f"Severidade: {doc['_id']}, Total: {doc['total']}")

pipeline_evento_mais_alertas = [
    {
        "$sort": { "numero_alertas": -1 }
    },
    {
        "$limit": 1
    }
]
resultado_evento_mais_alertas = relatorios.aggregate(pipeline_evento_mais_alertas)
print("\nEvento com Maior Número de Alertas:")
for doc in resultado_evento_mais_alertas:
    print(doc)
print("\nOperações concluídas com sucesso!")