from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from bson import ObjectId

app = FastAPI()

uri = "mongodb+srv://adm:.puzceax.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)
db = client["AppEventos"]

usuarios = db["usuarios"]
eventos = db["eventos"]
notificacoes = db["notificacoes"]
relatorios = db["relatorios"]
historico_ocorrencias = db["historico_ocorrencias"]
servicos_emergencia = db["servicos_emergencia"]

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

@app.post("/usuarios/", response_model=Usuario)
async def criar_usuario(usuario: Usuario):
    if usuarios.find_one({"id_usuario": usuario.id_usuario}):
        raise HTTPException(status_code=400, detail="Usuário já existe")
    usuarios.insert_one(usuario.dict())
    return usuario

@app.get("/usuarios/", response_model=List[Usuario])
async def listar_usuarios():
    return list(usuarios.find())

@app.post("/eventos/", response_model=Evento)
async def criar_evento(evento: Evento):
    if eventos.find_one({"id_evento": evento.id_evento}):
        raise HTTPException(status_code=400, detail="Evento já existe")
    eventos.insert_one(evento.dict())
    return evento

@app.get("/eventos/", response_model=List[Evento])
async def listar_eventos():
    return list(eventos.find())

@app.post("/notificacoes/", response_model=Notificacao)
async def criar_notificacao(notificacao: Notificacao):
    notificacoes.insert_one(notificacao.dict())
    return notificacao

@app.get("/notificacoes/", response_model=List[Notificacao])
async def listar_notificacoes():
    return list(notificacoes.find())

@app.post("/relatorios/", response_model=Relatorio)
async def criar_relatorio(relatorio: Relatorio):
    relatorios.insert_one(relatorio.dict())
    return relatorio

@app.get("/relatorios/", response_model=List[Relatorio])
async def listar_relatorios():
    return list(relatorios.find())

@app.post("/historico_ocorrencias/", response_model=HistoricoOcorrencia)
async def criar_historico(historico: HistoricoOcorrencia):
    historico_ocorrencias.insert_one(historico.dict())
    return historico

@app.get("/historico_ocorrencias/", response_model=List[HistoricoOcorrencia])
async def listar_historico():
    return list(historico_ocorrencias.find())

@app.post("/servicos_emergencia/", response_model=ServicoEmergencia)
async def criar_servico(servico: ServicoEmergencia):
    servicos_emergencia.insert_one(servico.dict())
    return servico

@app.get("/servicos_emergencia/", response_model=List[ServicoEmergencia])
async def listar_servicos():
    return list(servicos_emergencia.find())

@app.delete("/eventos/{evento_id}")
async def deletar_evento(evento_id: str):
    result = eventos.delete_one({"id_evento": evento_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Evento não encontrado")
    return {"message": "Evento deletado com sucesso"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
