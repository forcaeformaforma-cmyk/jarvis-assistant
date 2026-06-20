#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JARVIS-Assistant Main Entry Point

Assistente de IA autônomo inspirado no JARVIS do Homem de Ferro
"""

import sys
import argparse
import logging
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from core.jarvis import JARVIS
from web.app import create_app

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(
        description='JARVIS-Assistant: Assistente de IA Autônomo',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python main.py                  # Inicia modo CLI
  python main.py --web            # Inicia interface web
  python main.py --web --port 5000  # Interface web na porta 5000
        """
    )
    
    parser.add_argument('--web', action='store_true', 
                       help='Inicia interface web em vez de CLI')
    parser.add_argument('--port', type=int, default=5000,
                       help='Porta para a interface web (padrão: 5000)')
    parser.add_argument('--host', default='localhost',
                       help='Host para a interface web (padrão: localhost)')
    parser.add_argument('--debug', action='store_true',
                       help='Modo debug')
    
    args = parser.parse_args()
    
    try:
        if args.web:
            logger.info("Iniciando JARVIS-Assistant em modo Web...")
            app = create_app()
            app.run(host=args.host, port=args.port, debug=args.debug)
        else:
            logger.info("Iniciando JARVIS-Assistant em modo CLI...")
            jarvis = JARVIS()
            jarvis.start_cli()
    except KeyboardInterrupt:
        logger.info("\nJARVIS-Assistant desligado pelo usuário.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Erro ao iniciar JARVIS-Assistant: {e}", exc_info=True)
        sys.exit(1)

if __name__ == '__main__':
    main()
