#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NLP Processor - Processamento de Linguagem Natural em Português
"""

import logging
import re
from typing import Tuple, Dict, Any, List

logger = logging.getLogger(__name__)

class NLPProcessor:
    """
    Processa linguagem natural em português
    """
    
    # Dicionários de palavras-chave
    GREETING_KEYWORDS = ['oi', 'olá', 'opa', 'e aí', 'hey', 'bom dia', 'boa tarde', 'boa noite']
    TASK_KEYWORDS = ['execute', 'faça', 'realize', 'crie', 'delete', 'modifique']
    API_KEYWORDS = ['consulte', 'busque', 'pesquise', 'api', 'busca']
    LEARN_KEYWORDS = ['aprenda', 'aprender', 'ensine', 'estude']
    HELP_KEYWORDS = ['ajuda', 'help', 'como', 'explique', 'o que']
    
    def __init__(self):
        """Inicializa o processador NLP"""
        logger.info("Inicializando NLP Processor...")
    
    def parse_command(self, user_input: str) -> Tuple[str, Dict[str, Any], float]:
        """
        Analisa um comando do usuário e identifica intenção
        
        Args:
            user_input: Entrada do usuário
            
        Returns:
            Tupla (intent, entities, confidence)
        """
        user_input_lower = user_input.lower().strip()
        
        # Remove pontuação
        cleaned_input = re.sub(r'[^\w\s]', '', user_input_lower)
        tokens = cleaned_input.split()
        
        intent, confidence = self._detect_intent(tokens, user_input_lower)
        entities = self._extract_entities(tokens, user_input_lower)
        
        logger.debug(f"Parsed - Intent: {intent}, Confidence: {confidence}, Entities: {entities}")
        
        return intent, entities, confidence
    
    def _detect_intent(self, tokens: List[str], user_input: str) -> Tuple[str, float]:
        """
        Detecta a intenção do usuário
        
        Args:
            tokens: Tokens da entrada
            user_input: Entrada original em minúsculas
            
        Returns:
            Tupla (intent, confidence)
        """
        # Saudação
        if any(keyword in tokens for keyword in self.GREETING_KEYWORDS):
            return 'greeting', 0.95
        
        # Tarefa
        if any(keyword in tokens for keyword in self.TASK_KEYWORDS):
            return 'execute_task', 0.85
        
        # API
        if any(keyword in tokens for keyword in self.API_KEYWORDS):
            return 'api_query', 0.85
        
        # Aprendizado
        if any(keyword in tokens for keyword in self.LEARN_KEYWORDS):
            return 'learn', 0.80
        
        # Ajuda
        if any(keyword in tokens for keyword in self.HELP_KEYWORDS):
            return 'help', 0.85
        
        # Padrão
        return 'unknown', 0.5
    
    def _extract_entities(self, tokens: List[str], user_input: str) -> Dict[str, Any]:
        """
        Extrai entidades da entrada
        
        Args:
            tokens: Tokens da entrada
            user_input: Entrada original
            
        Returns:
            Dicionário de entidades
        """
        entities = {
            'tokens': tokens,
            'raw_input': user_input,
            'length': len(tokens)
        }
        
        # Extrai números
        numbers = re.findall(r'\d+', user_input)
        if numbers:
            entities['numbers'] = [int(n) for n in numbers]
        
        # Extrai URLs
        urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', user_input)
        if urls:
            entities['urls'] = urls
        
        return entities
    
    def tokenize(self, text: str) -> List[str]:
        """
        Tokeniza texto
        """
        return text.lower().split()
    
    def remove_stopwords(self, tokens: List[str]) -> List[str]:
        """
        Remove stopwords em português
        """
        portuguese_stopwords = {
            'o', 'a', 'os', 'as', 'um', 'uma', 'uns', 'umas',
            'de', 'do', 'da', 'dos', 'das',
            'e', 'ou', 'mas', 'porém',
            'em', 'no', 'na', 'nos', 'nas',
            'por', 'para', 'com', 'sem',
            'é', 'são', 'foi', 'foram', 'ser', 'estar',
            'que', 'qual', 'quais', 'quando', 'onde',
            'este', 'esse', 'aquele', 'isto', 'isso', 'aquilo'
        }
        return [token for token in tokens if token not in portuguese_stopwords]
