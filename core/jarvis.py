#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JARVIS Core - Núcleo do Assistente Autônomo
"""

import logging
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

from nlp.processor import NLPProcessor
from apis.api_manager import APIManager
from tasks.task_executor import TaskExecutor
from learning.memory_system import MemorySystem

logger = logging.getLogger(__name__)

class JARVIS:
    """
    JARVIS - Just A Rather Very Intelligent System
    
    Assistente de IA autônomo com:
    - Processamento de linguagem natural em português
    - Integração com APIs externas
    - Execução automática de tarefas
    - Sistema de aprendizado contínuo
    """
    
    def __init__(self):
        """Inicializa o JARVIS"""
        logger.info("🤖 Inicializando JARVIS-Assistant...")
        
        self.name = "JARVIS"
        self.version = "1.0.0"
        self.initialized_at = datetime.now()
        
        # Componentes principais
        self.nlp = NLPProcessor()
        self.api_manager = APIManager()
        self.task_executor = TaskExecutor()
        self.memory = MemorySystem()
        
        # Status
        self.is_active = True
        self.conversation_history = []
        
        logger.info(f"✅ {self.name} v{self.version} pronto para servir!")
    
    def process_command(self, user_input: str) -> str:
        """
        Processa um comando do usuário e retorna resposta
        
        Args:
            user_input: Comando do usuário em português
            
        Returns:
            Resposta do JARVIS
        """
        logger.info(f"📝 Processando comando: {user_input}")
        
        # Análise de linguagem natural
        intent, entities, confidence = self.nlp.parse_command(user_input)
        logger.debug(f"Intent: {intent}, Confidence: {confidence}")
        
        # Consulta memória para contexto
        context = self.memory.get_context(intent, entities)
        
        # Determina ação
        response = self._handle_intent(intent, entities, context)
        
        # Armazena na memória
        self.conversation_history.append({
            'timestamp': datetime.now().isoformat(),
            'user_input': user_input,
            'intent': intent,
            'response': response
        })
        self.memory.add_interaction(user_input, intent, response)
        
        return response
    
    def _handle_intent(self, intent: str, entities: Dict[str, Any], context: Dict) -> str:
        """
        Trata uma intenção detectada
        
        Args:
            intent: Intenção detectada
            entities: Entidades extraídas
            context: Contexto da conversa
            
        Returns:
            Resposta apropriada
        """
        intent_lower = intent.lower()
        
        # Saudação
        if intent_lower in ['greeting', 'hello', 'oi']:
            return f"Olá! Sou o {self.name}, seu assistente de IA. Como posso ajudá-lo?"
        
        # Consultar API
        elif intent_lower == 'api_query':
            api_name = entities.get('api', 'default')
            query = entities.get('query', '')
            result = self.api_manager.query(api_name, query)
            return result
        
        # Executar tarefa
        elif intent_lower == 'execute_task':
            task_name = entities.get('task', '')
            result = self.task_executor.execute(task_name, entities)
            return result
        
        # Aprender
        elif intent_lower == 'learn':
            subject = entities.get('subject', '')
            return f"Estou aprendendo sobre {subject}. Obrigado por me ensinar!"
        
        # Desconhecer
        else:
            return f"Desculpe, não entendi completamente. Poderia reformular sua solicitação? (Intent detectado: {intent})"
    
    def execute_task_async(self, task_name: str, params: Dict = None) -> Dict:
        """
        Executa uma tarefa de forma assíncrona
        
        Args:
            task_name: Nome da tarefa
            params: Parâmetros da tarefa
            
        Returns:
            Resultado da tarefa
        """
        logger.info(f"⚙️ Executando tarefa: {task_name}")
        return self.task_executor.execute_async(task_name, params or {})
    
    def start_cli(self):
        """
        Inicia interface de linha de comando interativa
        """
        print(f"\n🤖 {self.name} v{self.version} - CLI Mode")
        print("="*50)
        print("Digite 'sair' para encerrar ou 'ajuda' para comandos")
        print("="*50 + "\n")
        
        while self.is_active:
            try:
                user_input = input("Você: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() == 'sair':
                    print("\n👋 Até logo!\n")
                    break
                
                if user_input.lower() == 'ajuda':
                    self._print_help()
                    continue
                
                response = self.process_command(user_input)
                print(f"\n{self.name}: {response}\n")
                
            except KeyboardInterrupt:
                print("\n\n👋 Até logo!\n")
                break
            except Exception as e:
                logger.error(f"Erro ao processar comando: {e}")
                print(f"❌ Erro: {str(e)}\n")
    
    def _print_help(self):
        """
        Exibe ajuda de comandos
        """
        help_text = """
        📋 Comandos disponíveis:
        
        Gerais:
        - "Olá" ou "Oi" - Saudação
        - "Ajuda" - Mostra esta mensagem
        - "Sair" - Encerra o programa
        
        Tarefas:
        - "Execute [tarefa_name]" - Executa uma tarefa específica
        - "Liste tarefas" - Lista tarefas disponíveis
        
        APIs:
        - "Consulte [api_name]" - Consulta uma API
        - "Liste APIs" - Lista APIs disponíveis
        
        Aprendizado:
        - "Aprenda sobre [tópico]" - JARVIS aprende sobre um tópico
        - "O que você sabe sobre [tópico]" - Consulta conhecimento
        """
        print(help_text)
    
    def get_status(self) -> Dict:
        """
        Retorna status do JARVIS
        """
        return {
            'name': self.name,
            'version': self.version,
            'active': self.is_active,
            'initialized_at': self.initialized_at.isoformat(),
            'conversation_count': len(self.conversation_history),
            'memory_interactions': self.memory.get_interaction_count()
        }
