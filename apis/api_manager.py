#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API Manager - Gerencia Integração com APIs Externas
"""

import logging
import json
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class APIManager:
    """
    Gerencia requisições para APIs externas
    """
    
    def __init__(self):
        """Inicializa o gerenciador de APIs"""
        logger.info("Inicializando API Manager...")
        self.available_apis = {
            'weather': 'https://api.open-meteo.com/v1/forecast',
            'news': 'https://newsapi.org/v2',
            'github': 'https://api.github.com',
        }
        self.request_history = []
    
    def query(self, api_name: str, query_params: Dict = None) -> str:
        """
        Realiza uma consulta a uma API
        
        Args:
            api_name: Nome da API
            query_params: Parâmetros da consulta
            
        Returns:
            Resultado da consulta
        """
        logger.info(f"Consultando API: {api_name}")
        
        if api_name not in self.available_apis:
            return f"❌ API '{api_name}' não configurada. APIs disponíveis: {list(self.available_apis.keys())}"
        
        try:
            # Simulação de consulta
            result = {
                'api': api_name,
                'timestamp': datetime.now().isoformat(),
                'params': query_params or {},
                'status': 'success',
                'data': f"Dados da API {api_name} retornados com sucesso"
            }
            
            self.request_history.append(result)
            return json.dumps(result, indent=2, ensure_ascii=False)
            
        except Exception as e:
            logger.error(f"Erro ao consultar API: {e}")
            return f"❌ Erro ao consultar API: {str(e)}"
    
    def list_apis(self) -> str:
        """
        Lista APIs disponíveis
        """
        apis_text = "\n".join([f"- {name}: {url}" for name, url in self.available_apis.items()])
        return f"APIs Disponíveis:\n{apis_text}"
    
    def register_api(self, name: str, endpoint: str):
        """
        Registra uma nova API
        """
        self.available_apis[name] = endpoint
        logger.info(f"API '{name}' registrada: {endpoint}")
    
    def get_request_history(self) -> list:
        """
        Retorna histórico de requisições
        """
        return self.request_history
