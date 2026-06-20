#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Memory System - Sistema de Memória e Aprendizado
"""

import logging
import json
from typing import Dict, List, Any
from datetime import datetime
from collections import defaultdict

logger = logging.getLogger(__name__)

class MemorySystem:
    """
    Sistema de memória que permite aprendizado contínuo
    """
    
    def __init__(self):
        """Inicializa o sistema de memória"""
        logger.info("Inicializando Memory System...")
        self.interactions = []
        self.knowledge_base = defaultdict(dict)
        self.user_preferences = {}
        self.learned_patterns = []
    
    def add_interaction(self, user_input: str, intent: str, response: str):
        """
        Armazena uma interação na memória
        
        Args:
            user_input: Entrada do usuário
            intent: Intenção detectada
            response: Resposta do JARVIS
        """
        interaction = {
            'timestamp': datetime.now().isoformat(),
            'user_input': user_input,
            'intent': intent,
            'response': response,
            'helpful': None  # Pode ser marcado depois
        }
        self.interactions.append(interaction)
        logger.debug(f"Interação armazenada: {intent}")
    
    def get_context(self, intent: str, entities: Dict = None) -> Dict:
        """
        Retorna contexto baseado em interações anteriores
        
        Args:
            intent: Intenção atual
            entities: Entidades atuais
            
        Returns:
            Dicionário com contexto
        """
        context = {
            'similar_intents': self._find_similar_intents(intent),
            'user_history': self._get_recent_history(5),
            'learned_patterns': self._get_relevant_patterns(intent)
        }
        return context
    
    def _find_similar_intents(self, intent: str, limit: int = 3) -> List[Dict]:
        """
        Encontra intenções semelhantes em histórico
        """
        similar = [i for i in self.interactions if i['intent'] == intent]
        return similar[-limit:]
    
    def _get_recent_history(self, limit: int = 5) -> List[Dict]:
        """
        Retorna histórico recente
        """
        return self.interactions[-limit:]
    
    def _get_relevant_patterns(self, intent: str) -> List[Dict]:
        """
        Retorna padrões relevantes
        """
        return [p for p in self.learned_patterns if intent in p.get('related_intents', [])]
    
    def learn_pattern(self, pattern_name: str, description: str, related_intents: List[str]):
        """
        Aprende um novo padrão
        
        Args:
            pattern_name: Nome do padrão
            description: Descrição
            related_intents: Intenções relacionadas
        """
        pattern = {
            'name': pattern_name,
            'description': description,
            'related_intents': related_intents,
            'learned_at': datetime.now().isoformat()
        }
        self.learned_patterns.append(pattern)
        logger.info(f"Novo padrão aprendido: {pattern_name}")
    
    def store_knowledge(self, topic: str, information: Dict):
        """
        Armazena conhecimento sobre um tópico
        
        Args:
            topic: Tópico
            information: Informações
        """
        self.knowledge_base[topic] = {
            'data': information,
            'stored_at': datetime.now().isoformat()
        }
        logger.info(f"Conhecimento armazenado sobre: {topic}")
    
    def retrieve_knowledge(self, topic: str) -> Dict:
        """
        Recupera conhecimento sobre um tópico
        
        Args:
            topic: Tópico
            
        Returns:
            Informações armazenadas
        """
        return self.knowledge_base.get(topic, {})
    
    def set_user_preference(self, key: str, value: Any):
        """
        Define preferência do usuário
        """
        self.user_preferences[key] = value
        logger.debug(f"Preferência definida: {key} = {value}")
    
    def get_user_preference(self, key: str, default: Any = None) -> Any:
        """
        Retorna preferência do usuário
        """
        return self.user_preferences.get(key, default)
    
    def get_interaction_count(self) -> int:
        """
        Retorna número total de interações
        """
        return len(self.interactions)
    
    def export_memory(self) -> Dict:
        """
        Exporta memória em formato JSON
        """
        return {
            'interactions': self.interactions,
            'knowledge_base': dict(self.knowledge_base),
            'user_preferences': self.user_preferences,
            'learned_patterns': self.learned_patterns,
            'export_timestamp': datetime.now().isoformat()
        }
