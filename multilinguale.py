from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
from flask_babel import Babel, gettext as _
from flask_cors import CORS
import os
import json
import sh

app = Flask(__name__)
CORS(app)

# Настройка Babel
app.config['BABEL_DEFAULT_LOCALE'] = 'ru'
app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'
app.config['LANGUAGES'] = ['en', 'ru', 'pl']

babel = Babel(app)

# Определяем язык из параметра URL или cookies
def get_locale():
    lang = request.args.get('lang')
    if lang in app.config['LANGUAGES']:
        return lang
    return request.cookies.get('language') or request.accept_languages.best_match(app.config['LANGUAGES'])

babel.locale_selector_func = get_locale

# Делаем get_locale() доступной в шаблонах
@app.context_processor
def inject_locale():
    return {'get_locale': get_locale}

# Главная страница
@app.route('/')
def home():
    return render_template('project.html', title=_('Faith Project'), welcome_message=_('Welcome to Faith Project'))

# Страница Библии
@app.route('/bible')
def bible():
    return render_template('bible.html', title=_('Библия'))

# Загрузка содержимого Библии
@app.route('/bible/content')
def bible_content():
    lang = get_locale()
    bible_file = os.path.join('static', 'bible', f'Biblia_{lang}.json')

    if os.path.exists(bible_file):
        with open(bible_file, 'r', encoding='utf-8') as f:
            bible_data = json.load(f)
        return jsonify(bible_data)
    else:
        return jsonify({"error": "Файл не найден"}), 404

# Другие страницы
@app.route('/groups')
def groups():
    return render_template('groups.html', title=_('Группы'))

@app.route('/events')
def events():
    return render_template('events.html', title=_('Мероприятия'))

@app.route('/about')
def about():
    return render_template('about.html', title=_('О нас'))

# Устанавливаем язык через cookies
@app.route('/set_language/<lang>')
def set_language(lang):
    if lang not in app.config['LANGUAGES']:
        lang = 'ru'
    resp = make_response(redirect(request.referrer or url_for('home')))
    resp.set_cookie('language', lang)
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)