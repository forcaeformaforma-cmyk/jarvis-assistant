#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flask Web Application - Interface Web do JARVIS
"""

import logging
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from datetime import datetime

from core.jarvis import JARVIS

logger = logging.getLogger(__name__)

def create_app():
    """
    Cria e configura a aplicação Flask
    """
    app = Flask(__name__, template_folder='templates', static_folder='static')
    CORS(app)
    
    # Inicializa JARVIS
    jarvis_instance = JARVIS()
    
    # ==================== ROUTES ====================
    
    @app.route('/')
    def index():
        """Página principal"""
        return jsonify({
            'name': 'JARVIS-Assistant Web Dashboard',
            'version': '1.0.0',
            'status': 'online',
            'endpoints': {
                'chat': '/api/chat',
                'status': '/api/status',
                'tasks': '/api/tasks',
                'apis': '/api/apis'
            }
        })
    
    @app.route('/api/chat', methods=['POST'])
    def chat():
        """Endpoint de chat com JARVIS"""
        try:
            data = request.get_json()
            user_input = data.get('message', '').strip()
            
            if not user_input:
                return jsonify({'error': 'Mensagem vazia'}), 400
            
            response = jarvis_instance.process_command(user_input)
            
            return jsonify({
                'success': True,
                'user_message': user_input,
                'jarvis_response': response,
                'timestamp': datetime.now().isoformat()
            })
        
        except Exception as e:
            logger.error(f"Erro no endpoint /chat: {e}")
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/status')
    def status():
        """Retorna status do JARVIS"""
        return jsonify(jarvis_instance.get_status())
    
    @app.route('/api/tasks')
    def tasks():
        """Lista tarefas disponíveis"""
        return jsonify({
            'available_tasks': list(jarvis_instance.task_executor.available_tasks.keys()),
            'execution_history': jarvis_instance.task_executor.get_execution_history()[-10:]
        })
    
    @app.route('/api/tasks/execute', methods=['POST'])
    def execute_task():
        """Executa uma tarefa"""
        try:
            data = request.get_json()
            task_name = data.get('task_name', '')
            params = data.get('params', {})
            
            if not task_name:
                return jsonify({'error': 'Task name não fornecido'}), 400
            
            result = jarvis_instance.execute_task_async(task_name, params)
            
            return jsonify({
                'success': True,
                'task': task_name,
                'result': result
            })
        
        except Exception as e:
            logger.error(f"Erro ao executar tarefa: {e}")
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/apis')
    def apis():
        """Lista APIs disponíveis"""
        return jsonify({
            'available_apis': list(jarvis_instance.api_manager.available_apis.keys()),
            'request_history': jarvis_instance.api_manager.get_request_history()[-10:]
        })
    
    @app.route('/api/memory')
    def memory():
        """Retorna dados da memória"""
        return jsonify({
            'interaction_count': jarvis_instance.memory.get_interaction_count(),
            'recent_interactions': jarvis_instance.memory._get_recent_history(10),
            'learned_patterns': jarvis_instance.memory.learned_patterns
        })
    
    # ==================== ERROR HANDLERS ====================
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Recurso não encontrado'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Erro interno do servidor'}), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
