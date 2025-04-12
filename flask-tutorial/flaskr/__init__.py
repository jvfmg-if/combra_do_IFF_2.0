#Rode esse arquivo normalmente, apenas o main.py é em terminal dedicado.
#Instale as bibliotecas.
#Para iniciar:

#   - Abra o cmd e digite: flask --app flaskr init-db; depois digite: flask --app flaskr run --debug

#Se não funcionou, sinto-lhe informar, mas boa sorte.

import db
import auth 
from main import jogo
import os
from flask import Flask, render_template
import pygame
import cv2
#from db import get_db # se der merda apaga <---
import sqlite3
import threading
import time

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config['DATABASE'] = 'instance/flaskr.sqlite'  # Substitua pelo caminho correto# se der merda apaga <---
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    
    @app.route('/easterEgg,wow!:o')
    def easteregg():
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

                if cv2.waitKey(25) & 0xFF == 27:  # Pressione ESC para sair
                    break

            cap.release()
            pygame.mixer.music.stop()
            pygame.quit()
            cv2.destroyAllWindows()

        def main():
            video_path = "C:/Users/ferre/OneDrive/Área de Trabalho/WTFhorse.mp4"
            audio_path = "C:/Users/ferre/OneDrive/Área de Trabalho/WTFhorse.mp3"
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
    # Conecta ao banco de dados SQLite
        conn = sqlite3.connect('instance/flaskr.sqlite')
        conn.row_factory = sqlite3.Row  # Para acessar os dados como dicionários
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
    app.run(debug=True, use_reloader=False, threaded=True)


# Create a thread for Flask to run separately
flask_thread = threading.Thread(target=run_flask)

# Start the Flask thread
flask_thread.start()

# Run the Pygame game in the main thread
jogo()

time.sleep(2)  # Give Flask a second to fully initialize
os.system('curl -X POST http://127.0.0.1:5000/shutdown')

# Ensure the Flask thread stops after the game ends
flask_thread.join()
os.system("exit")
