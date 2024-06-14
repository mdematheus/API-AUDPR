from dotenv import load_dotenv
import os
from app import create_app

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

app = create_app()

if __name__ == '__main__':
    # Configuração para habilitar o modo de depuração baseado em variáveis de ambiente
    debug_mode = os.getenv('FLASK_DEBUG', 'true').lower() in ['true', '1', 't']
    app.run(debug=debug_mode)
