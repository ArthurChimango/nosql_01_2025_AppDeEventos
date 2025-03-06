from pymongo import MongoClient

uri = "mongodb+srv://adm:3231@cluster0.puzceax.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)
db = client["AppEventos"]

usuarios = db["usuarios"]
eventos = db["eventos"]
notificacoes = db["notificacoes"]
relatorios = db["relatorios"]
historico_ocorrencias = db["historico_ocorrencias"]
servicos_emergencia = db["servicos_emergencia"]

usuario = {
    "id_usuario": "user123",
    "nome": "Fulano de Tal",
    "idade": 30,
    "cpf": "123.456.789-00",
    "endereco": {
        "bairro": "Centro",
        "cep": "12345-678",
        "rua": "Rua Principal"
    },
    "email": "fulano@email.com",
    "telefone": "+55 11 99999-9999"
}
usuarios.insert_one(usuario)

evento = {
    "id_evento": "ev123",
    "tipo": "Chuva Intensa",
    "data": "2024-09-15",
    "localizacao": {
        "bairro": "Centro",
        "cep": "12345-678",
        "rua": "Rua Principal"
    },
    "descricao": "Alerta de chuva intensa com risco de alagamentos.",
    "autoridade_responsavel": "Defesa Civil",
    "severidade": "Alta",
    "cadastrado_por": "Cidadão"
}
eventos.insert_one(evento)

notificacao = {
    "id_notificacao": "notif789",
    "destinatario": "user123",
    "mensagem": "Alerta: Tempestade prevista para as próximas horas. Evite áreas de risco.",
    "data_hora": "2024-09-10T10:00:00Z"
}
notificacoes.insert_one(notificacao)

relatorio = {
    "id_relatorio": "rep001",
    "id_evento": "ev123",
    "impacto": "Alagamento em vias principais",
    "numero_alertas": 150,
    "avaliacao_usuarios": 4.7
}
relatorios.insert_one(relatorio)

historico = {
    "id_ocorrencia": "hist202",
    "id_evento": "ev123",
    "data_registro": "2024-08-30",
    "descricao": "Relatório final sobre os impactos da tempestade.",
    "autoridade_responsavel": "Defesa Civil"
}
historico_ocorrencias.insert_one(historico)

servico = {
    "servico_id": 201,
    "nome_servico": "Corpo de Bombeiros",
    "contato": "193",
    "evento_id": "ev123",
    "data_hora_contato": "2023-10-15T14:40:00Z",
    "status": "Contatado"
}
servicos_emergencia.insert_one(servico)

eventos.delete_one({"id_evento": "ev123"})

usuarios_cadastrados = usuarios.find()
for usuario in usuarios_cadastrados:
    print(usuario)

print("Operações concluídas com sucesso!")
