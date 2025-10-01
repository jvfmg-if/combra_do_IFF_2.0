import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

def _sync_jogadores_file_from_db():
    db = get_db()
    usuarios = db.execute("SELECT username, password FROM user").fetchall()
    with open("textos/jogadores.txt","w") as arquivo:
        for u in usuarios:
            arquivo.write(f"{u['username']},{u['password']},\n")

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif username == "WTF" and password == "horse!":
            return redirect(url_for("easteregg"))

        if error is None:
            try:
                db.execute("""

                    CREATE TABLE IF NOT EXISTS user (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                    );"""
                )
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, password),
                )
                db.commit()
                # Espelha o banco no arquivo
                _sync_jogadores_file_from_db()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                flash('Cadastro realizado com sucesso!', 'success')
                return redirect(url_for("auth.register"))

        flash(error, 'error')

    return render_template('auth/register.html')

@bp.route('/sync-file', methods=('POST',))
def sync_file():
    _sync_jogadores_file_from_db()
    flash('Arquivo jogadores.txt sincronizado com o banco.')
    return redirect(url_for('auth.register'))


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif user['password'] != password:  # Comparação direta da senha
            error = 'Incorrect password.'

        if error is None:
            
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('Tudoprontopodejogar'))

        flash(error)
    # Desabilita a página de login web; mantém somente POST para o jogo
    return redirect(url_for('auth.register'))


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
