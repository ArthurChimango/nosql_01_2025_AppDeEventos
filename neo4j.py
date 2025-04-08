from neo4j import GraphDatabase

class Neo4jDriver:
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def criar_estrutura_inicial(self):
        with self._driver.session() as session:
            session.execute_write(self._criar_grafo_exemplo)

    def _criar_grafo_exemplo(self, tx):
        tx.run("""
            MERGE (u:Usuario {
                id_usuario: 'u1',
                nome: 'João Silva',
                idade: 30,
                cpf: '12345678900',
                email: 'joao@email.com',
                telefone: '99999-0000',
                endereco_rua: 'Rua A',
                endereco_cidade: 'Cidade X',
                endereco_estado: 'MG'
            })

            MERGE (e:Evento {
                id_evento: 'ev1',
                tipo: 'Incêndio',
                data: '2025-04-01',
                descricao: 'Incêndio em zona urbana',
                severidade: 'Alta',
                autoridade_responsavel: 'Bombeiros',
                cadastrado_por: 'u1',
                localizacao_latitude: -18.9,
                localizacao_longitude: -48.3
            })

            MERGE (n:Notificacao {
                id_notificacao: 'n1',
                destinatario: 'u1',
                mensagem: 'Evacuar a área imediatamente',
                data_hora: '2025-04-01T12:00:00'
            })

            MERGE (r:Relatorio {
                id_relatorio: 'r1',
                id_evento: 'ev1',
                impacto: 'Alto',
                numero_alertas: 5,
                avaliacao_usuarios: 4.5
            })

            MERGE (h:HistoricoOcorrencia {
                id_ocorrencia: 'h1',
                id_evento: 'ev1',
                data_registro: '2025-03-30',
                descricao: 'Ocorrência anterior semelhante',
                autoridade_responsavel: 'Defesa Civil'
            })

            MERGE (s:ServicoEmergencia {
                servico_id: 101,
                nome_servico: 'SAMU',
                contato: '192',
                evento_id: 'ev1',
                data_hora_contato: '2025-04-01T12:30:00',
                status: 'Atendido'
            })

            MERGE (u)-[:REPORTOU]->(e)
            MERGE (u)-[:RECEBEU]->(n)
            MERGE (e)-[:GEROU]->(r)
            MERGE (e)-[:TEM_HISTORICO]->(h)
            MERGE (e)-[:ACIONOU]->(s)
        """)
neo4j_uri = "bolt://localhost:7687"
neo4j_user = "neo4j"
neo4j_password = ""

driver = Neo4jDriver(neo4j_uri, neo4j_user, neo4j_password)
driver.criar_estrutura_inicial()
driver.close()

# MATCH (n) RETURN n LIMIT 100

