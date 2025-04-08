import redis
import json
from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from bson import ObjectId
from redisbloom.client import Client as RedisBloomClient

# Configuração do Redis
r = redis.Redis(
    host='redis-17999.c308.sa-east-1-1.ec2.redns.redis-cloud.com',
    port=17999,
    password='bojQoovMeJFullJPkSyDylOseHSUtz43',
    decode_responses=True
)

# Configuração do RedisBloom (para os filtros probabilísticos)
rb = RedisBloomClient(
    host='redis-17999.c308.sa-east-1-1.ec2.redns.redis-cloud.com',
    port=17999,
    password='bojQoovMeJFullJPkSyDylOseHSUtz43'
)

# Inicialização do FastAPI
app = FastAPI()

# Configuração do MongoDB
uri = "mongodb+srv://adm:@cluster0.puzceax.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)
db = client["AppEventos"]

# Coleções do MongoDB
usuarios = db["usuarios"]
eventos = db["eventos"]
notificacoes = db["notificacoes"]
relatorios = db["relatorios"]
historico_ocorrencias = db["historico_ocorrencias"]
servicos_emergencia = db["servicos_emergencia"]

# Modelos Pydantic
class Usuario(BaseModel):
    id_usuario: str
    nome: str
    idade: int
    cpf: str
    endereco: dict
    email: str
    telefone: str

class Evento(BaseModel):
    id_evento: str
    tipo: str
    data: str
    localizacao: dict
    descricao: str
    autoridade_responsavel: str
    severidade: str
    cadastrado_por: str

class Notificacao(BaseModel):
    id_notificacao: str
    destinatario: str
    mensagem: str
    data_hora: str

class Relatorio(BaseModel):
    id_relatorio: str
    id_evento: str
    impacto: str
    numero_alertas: int
    avaliacao_usuarios: float

class HistoricoOcorrencia(BaseModel):
    id_ocorrencia: str
    id_evento: str
    data_registro: str
    descricao: str
    autoridade_responsavel: str

class ServicoEmergencia(BaseModel):
    servico_id: int
    nome_servico: str
    contato: str
    evento_id: str
    data_hora_contato: str
    status: str

# Função para inicializar dados e filtros
def inicializar_sistema():
    # Inicializar Redis
    r.flushdb()
    
    # Criar Bloom Filter para eventos (taxa de erro de 1%, capacidade inicial de 10.000 itens)
    try:
        rb.bfCreate('eventos:bloomfilter', 0.01, 10000)
    except:
        pass  # Já existe
    
    # Dados de exemplo
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
    rb.bfAdd('eventos:bloomfilter', 'ev001')  # Adiciona ao Bloom Filter

    # Inicializa HyperLogLog para notificações
    r.pfadd("notificacoes:destinatarios_unicos", "user001")

# Função para criar índices no MongoDB
def criar_indices():
    usuarios.create_index([("id_usuario", 1)], unique=True)
    eventos.create_index([("id_evento", 1)], unique=True)
    eventos.create_index([("tipo", 1)])
    eventos.create_index([("severidade", 1)])
    notificacoes.create_index([("data_hora", 1)])
    relatorios.create_index([("id_evento", 1)])
    relatorios.create_index([("numero_alertas", -1)])
    historico_ocorrencias.create_index([("id_evento", 1)])
    servicos_emergencia.create_index([("evento_id", 1)])

# Endpoints da API
@app.post("/eventos/", response_model=Evento)
async def criar_evento(evento: Evento):
    # Verifica no Bloom Filter primeiro (rápido)
    if rb.bfExists('eventos:bloomfilter', evento.id_evento):
        # Pode ser um falso positivo, então verifica no MongoDB
        if eventos.find_one({"id_evento": evento.id_evento}):
            raise HTTPException(status_code=400, detail="Evento já existe")
    
    # Se não existe, adiciona ao Bloom Filter e ao MongoDB
    rb.bfAdd('eventos:bloomfilter', evento.id_evento)
    eventos.insert_one(evento.dict())
    
    # Armazena no Redis também
    evento_redis = evento.dict()
    evento_redis["localizacao"] = json.dumps(evento_redis["localizacao"])
    r.hmset(f"evento:{evento.id_evento}", evento_redis)
    
    return evento

@app.post("/notificacoes/", response_model=Notificacao)
async def criar_notificacao(notificacao: Notificacao):
    # Armazena no MongoDB
    notificacoes.insert_one(notificacao.dict())
    
    # Adiciona ao HyperLogLog para contagem de destinatários únicos
    r.pfadd("notificacoes:destinatarios_unicos", notificacao.destinatario)
    
    # Armazena no Redis
    notif_redis = notificacao.dict()
    r.hmset(f"notificacao:{notificacao.id_notificacao}", notif_redis)
    r.lpush("notificacoes:recentes", notificacao.id_notificacao)
    
    return notificacao

@app.get("/eventos/verificar/{evento_id}")
async def verificar_evento_existe(evento_id: str):
    """
    Verifica se um evento existe usando o Bloom Filter (rápido)
    Pode retornar falsos positivos, mas nunca falsos negativos
    """
    existe = rb.bfExists('eventos:bloomfilter', evento_id)
    return {
        "existe": existe,
        "observacao": "Pode ser um falso positivo (confirme no banco principal se necessário)"
    }

@app.get("/notificacoes/estatisticas")
async def estatisticas_notificacoes():
    """
    Retorna estatísticas de notificações, incluindo contagem aproximada
    de destinatários únicos usando HyperLogLog
    """
    total_notificacoes = notificacoes.count_documents({})
    destinatarios_unicos = r.pfcount("notificacoes:destinatarios_unicos")
    
    return {
        "total_notificacoes": total_notificacoes,
        "destinatarios_unicos_estimados": destinatarios_unicos,
        "observacao": "Contagem de destinatários únicos é aproximada (margem de erro ~0.8%)"
    }

# ... (mantenha todos os outros endpoints originais) ...

# Inicialização dos dados e filtros
@app.on_event("startup")
async def startup_event():
    inicializar_sistema()
    criar_indices()
    print("Sistema inicializado com:")
    print("- Bloom Filter para eventos")
    print("- HyperLogLog para notificações")
    print("- Índices MongoDB criados")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
