# Para iniciar:
#   Linux: ./run.sh
#   Windows: run.bat
# Ou manualmente: cd src && python __init__.py

import db
import auth 
from main import jogo
import os
import sys
from flask import Flask, render_template, request
import pygame
try:
    import cv2
except ImportError:
    cv2 = None
#from db import get_db # se der merda apaga <---
import sqlite3
import threading
import time
import requests
import werkzeug
from werkzeug.serving import run_simple

def create_app(test_config=None):
    _root = os.path.dirname(os.path.abspath(__file__))
    app = Flask(__name__,
        instance_path=os.path.join(_root, '..', 'data', 'instance'),
        template_folder=os.path.join(_root, '..', 'web', 'templates'),
        static_folder=os.path.join(_root, '..', 'web', 'static'))
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(_root, '..', 'data', 'instance', 'flaskr.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    @app.route('/shutdown', methods=['POST'])
    def shutdown():

        server_type = os.environ.get('SERVER_SOFTWARE', 'Desconhecido')
        print(f"Servidor Flask está rodando com: {server_type}")
        os._exit(0)

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    
    @app.route('/easterEgg,wow!:o')
    def easteregg():
        if cv2 is None:
            return "OpenCV não disponível neste sistema."
        def play_video(video_path, audio_path):
            pygame.init()
            pygame.mixer.init()
            cap = cv2.VideoCapture(video_path)

            if not cap.isOpened():
                print("Não foi possível abrir o vídeo.")
                return

            pygame.mixer.music.load(audio_path)
            pygame.mixer.music.play()

            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                cv2.imshow("Vídeo", frame)

                if cv2.waitKey(25) & 0xFF == 27:
                    break

            cap.release()
            pygame.mixer.music.stop()
            pygame.quit()
            cv2.destroyAllWindows()

        def main():
            video_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'sounds', "WTFhorse.mp4")
            audio_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'sounds', "WTFhorse.mp3")
            if not os.path.exists(video_path) or not os.path.exists(audio_path):
                return "Vídeo não encontrado."
            play_video(video_path, audio_path)
        
        main()
        return "Como você encontrou isso? Eu te mostrei kkkkkkkkkk"
    

    @app.route('/Tudopronto,podejogar!')
    def Tudoprontopodejogar():
        
        return "Cadastro concluído! Confira aba do jogo recém aberta logo abaixo ;^)"


    #@app.route('/dados') # se der merda apaga <---
    #def mostrar_dados():
    #    db = get_db()
    #    dados = db.execute('SELECT * FROM user').fetchall()  # Substitua 'nome_da_tabela' pelo nome da sua tabela
    #    print(dados)
    #    return render_template('dados.html', dados=dados)


    def get_db():
        db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'instance', 'flaskr.sqlite')
        conn = sqlite3.connect(db_path, check_same_thread=True)
        conn.row_factory = sqlite3.Row
        return conn

    @app.route('/bd')
    def bd():
        db = get_db()
        # Obtém todos os registros da tabela 'users'
        cursor = db.execute('SELECT username, password FROM user')
        registros = cursor.fetchall()  # Armazena todos os registros
        db.close()  # Fecha a conexão com o banco de dados

        return render_template('dados.html', registros=registros)



    db.init_app(app)
    
    app.register_blueprint(auth.bp)

    return app

def run_flask():
    app = create_app()
    #run_simple('127.0.0.1', 5000, app, use_reloader=False, threaded=True)
    app.run(debug=True, use_reloader=False, threaded=True)


# Create a thread for Flask to run separately
flask_thread = threading.Thread(target=run_flask)

# Start the Flask thread
flask_thread.start()

# Run the Pygame game in the main thread
jogo()

time.sleep(1)
try:
    requests.post('http://127.0.0.1:5000/shutdown', timeout=2)
except requests.exceptions.RequestException:
    pass

flask_thread.join(timeout=3)
sys.exit(0)
