# JARVIS-Assistant Documentation

## Guia de Início Rápido

### Instalação

```bash
git clone https://github.com/forcaeformaforma-cmyk/jarvis-assistant.git
cd jarvis-assistant
pip install -r requirements.txt
```

### Execução

#### CLI Mode
```bash
python main.py
```

#### Web Mode
```bash
python main.py --web
```

## Arquitetura

### Componentes Principais

1. **NLP Processor** - Processa linguagem natural em português
2. **API Manager** - Gerencia integrações com APIs externas
3. **Task Executor** - Executa tarefas automaticamente
4. **Memory System** - Aprende de interações anteriores
5. **Web Interface** - Dashboard web para interação

### Fluxo de Funcionamento

```
User Input
    ↓
NLP Processing (Intent Detection)
    ↓
Context Retrieval (Memory System)
    ↓
Intent Handler
    ↓
Response Generation
    ↓
Memory Storage
    ↓
User Output
```

## Usando a API Web

### Chat
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Olá JARVIS"}'
```

### Status
```bash
curl http://localhost:5000/api/status
```

### Execute Task
```bash
curl -X POST http://localhost:5000/api/tasks/execute \
  -H "Content-Type: application/json" \
  -d '{"task_name": "backup"}'
```

## Extensões Futuras

- [ ] Integração com LLMs (GPT, Llama)
- [ ] Reconhecimento de voz
- [ ] Integração com smart home
- [ ] Dashboard avançado com React
- [ ] Sistema de plugins
- [ ] Persistência de dados em banco de dados
