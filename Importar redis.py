import redis
import json

r = redis.Redis(
    host=
    port=
    password=
    decode_responses=True
)

r.flushdb()

usuario = {
    "id_usuario": "user001", 
    "nome": "Ana Silva", 
    "idade": "28", 
    "cpf": "111.222.333-44", 
    "endereco": json.dumps({"bairro": "Centro", "cep": "11111-111", "rua": "Rua A"}), 
    "email": "ana@email.com", 
    "telefone": "+55 11 91111-1111"
}
r.hmset("usuario:user001", usuario)


evento = {
    "id_evento": "ev001", 
    "tipo": "Chuva Intensa", 
    "data": "2024-01-10", 
    "localizacao": json.dumps({"bairro": "Centro", "cep": "11111-111", "rua": "Rua A"}), 
    "descricao": "Alerta de chuva intensa.", 
    "autoridade_responsavel": "Defesa Civil", 
    "severidade": "Alta", 
    "cadastrado_por": "Cidadão"
}
r.hmset("evento:ev001", evento)


r.lpush("notificacoes:recentes", "notif003", "notif002", "notif001")


notificacoes = [
    {"id_notificacao": "notif001", "mensagem": "Alerta: Chuva intensa prevista.", "data": "2024-01-10T08:00:00Z"},
    {"id_notificacao": "notif002", "mensagem": "Alerta: Vendaval na região.", "data": "2024-01-11T09:00:00Z"},
    {"id_notificacao": "notif003", "mensagem": "Alerta: Risco de alagamento.", "data": "2024-01-12T10:00:00Z"}
]

for notif in notificacoes:
    r.hmset(f"notificacao:{notif['id_notificacao']}", notif)


r.sadd("usuario:user001:notificacoes", "notif001", "notif002")


r.sadd("tipos:eventos", "Chuva Intensa", "Vendaval", "Alagamento", "Deslizamento")


servicos = {
    "servico:301": {"nome": "Corpo de Bombeiros", "contato": "193"},
    "servico:302": {"nome": "Defesa Civil", "contato": "199"},
    "servico:303": {"nome": "SAMU", "contato": "192"}
}

for key, value in servicos.items():
    r.hmset(key, value)


r.sadd("evento:ev001:servicos", "301", "302")


print("=== Key-Value (Hash) ===")
print("Usuário user001:", r.hgetall("usuario:user001"))
print("\nEvento ev001:", r.hgetall("evento:ev001"))

print("\n=== Listas (LPUSH/LRANGE) ===")
print("Notificações recentes (LRANGE 0 -1):", r.lrange("notificacoes:recentes", 0, -1))
print("Detalhes da última notificação:", r.hgetall(f"notificacao:{r.lindex('notificacoes:recentes', 0)}"))

print("\n=== Sets (Conjuntos) ===")
print("Tipos de eventos disponíveis:", r.smembers("tipos:eventos"))
print("Serviços relacionados ao evento ev001:", r.smembers("evento:ev001:servicos"))
print("Detalhes do serviço 301:", r.hgetall("servico:301"))

print("\n=== Relacionamentos ===")
print("Notificações do usuário user001:", r.smembers("usuario:user001:notificacoes"))
for notif_id in r.smembers("usuario:user001:notificacoes"):
    print(f"- {notif_id}:", r.hgetall(f"notificacao:{notif_id}"))

print("\nOperações concluídas com sucesso!")
