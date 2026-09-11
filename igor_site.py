import os
import socket
import threading
import webbrowser
from flask import Flask, render_template_string

# пути и папки
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'static')
os.makedirs(os.path.join(STATIC_DIR, 'music'), exist_ok=True)

app = Flask(__name__, static_folder=STATIC_DIR)

HTML = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Игорь Киселёв | Официальный сайт</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --primary: #3b82f6;
            --dark: #1e40af;
            --accent: #f59e0b;
            --text: #1f2937;
            --muted: #6b7280;
            --bg-light: #f8fafc;
            --bg-dark: #0f172a;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        }

        html {
            scroll-behavior: smooth;
        }

        body {
            color: var(--text);
            line-height: 1.6;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }

        .container {
            width: 100%;
            max-width: 1140px;
            margin: 0 auto;
            padding: 0 20px;
        }

        /* навигация */
        header {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(8px);
            z-index: 100;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08);
            transition: background 0.3s;
        }

        nav {
            display: flex;
            justify-content: space-between;
            align-items: center;
            height: 70px;
        }

        .logo {
            font-size: 1.4rem;
            font-weight: 700;
            color: var(--dark);
            text-decoration: none;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .menu {
            display: flex;
            gap: 1.5rem;
            list-style: none;
        }

        .menu a {
            text-decoration: none;
            color: var(--text);
            font-weight: 600;
            font-size: 0.95rem;
            padding: 6px 14px;
            border-radius: 20px;
            transition: 0.2s ease;
        }

        .menu a:hover {
            background: var(--primary);
            color: #fff;
        }

        .burger {
            display: none;
            background: none;
            border: none;
            font-size: 1.5rem;
            cursor: pointer;
            color: var(--text);
        }

        /* hero */
        .hero {
            min-height: 80vh;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            color: #fff;
            padding: 120px 0 60px;
        }

        .hero h1 {
            font-size: clamp(2.2rem, 6vw, 3.8rem);
            margin-bottom: 1rem;
            line-height: 1.15;
            font-weight: 800;
        }

        .hero p {
            font-size: 1.2rem;
            margin-bottom: 2rem;
            opacity: 0.95;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
        }

        .btn {
            display: inline-block;
            background: var(--accent);
            color: #111;
            font-weight: 700;
            padding: 12px 32px;
            border-radius: 30px;
            text-decoration: none;
            transition: 0.2s transform;
            border: none;
            cursor: pointer;
        }

        .btn:hover {
            transform: translateY(-2px);
        }

        /* секции */
        section {
            padding: 80px 0;
        }

        .sec-light {
            background: #fff;
        }

        .sec-gray {
            background: var(--bg-light);
        }

        .sec-dark {
            background: var(--bg-dark);
            color: #fff;
        }

        .title {
            text-align: center;
            font-size: 2.2rem;
            margin-bottom: 40px;
            position: relative;
        }

        .title::after {
            content: '';
            display: block;
            width: 60px;
            height: 4px;
            background: var(--accent);
            margin: 12px auto 0;
            border-radius: 2px;
        }

        /* обо мне */
        .about-wrap {
            display: grid;
            grid-template-columns: 280px 1fr;
            gap: 40px;
            align-items: center;
        }

        .avatar-placeholder {
            height: 280px;
            background: #e2e8f0;
            border-radius: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--primary);
            font-size: 5rem;
        }

        .about-text p {
            margin-bottom: 15px;
            font-size: 1.05rem;
        }

        .tags {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 20px;
        }

        .tag {
            background: #e0e7ff;
            color: #3730a3;
            padding: 8px 16px;
            border-radius: 8px;
            font-size: 0.9rem;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }

        /* плашка скрытых данных */
        .privacy-card {
            border: 2px dashed rgba(255, 255, 255, 0.25);
            background: rgba(255, 255, 255, 0.04);
            border-radius: 16px;
            padding: 50px 20px;
            text-align: center;
            max-width: 650px;
            margin: 0 auto;
        }

        .privacy-card i {
            font-size: 2.8rem;
            color: var(--accent);
            margin-bottom: 15px;
        }

        .privacy-card h3 {
            margin-bottom: 10px;
            font-size: 1.3rem;
        }

        .privacy-card p {
            color: #cbd5e1;
            font-size: 0.95rem;
        }

        /* карточки */
        .grid-3 {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 25px;
        }

        .card {
            background: #fff;
            padding: 30px 25px;
            border-radius: 14px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
            text-align: center;
        }

        .card i {
            font-size: 2.5rem;
            color: var(--primary);
            margin-bottom: 15px;
        }

        .card h3 {
            margin-bottom: 10px;
        }

        .card p {
            color: var(--muted);
            font-size: 0.95rem;
        }

        /* плееры */
        .track-card {
            background: #fff;
            border-radius: 12px;
            padding: 22px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        .track-head {
            display: flex;
            align-items: center;
            gap: 14px;
        }

        .track-icon {
            width: 44px;
            height: 44px;
            background: #eff6ff;
            color: var(--primary);
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.2rem;
            flex-shrink: 0;
        }

        audio {
            width: 100%;
            height: 40px;
        }

        .track-desc {
            font-size: 0.9rem;
            color: var(--muted);
        }

        /* контакты и форма */
        .contact-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
        }

        .contact-links {
            display: flex;
            flex-direction: column;
            gap: 15px;
        }

        .c-box {
            display: flex;
            align-items: center;
            gap: 15px;
            padding: 18px;
            background: #fff;
            border-radius: 12px;
            text-decoration: none;
            color: var(--text);
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
            transition: 0.2s;
        }

        .c-box:hover {
            transform: translateY(-2px);
            color: var(--primary);
        }

        .c-box i {
            font-size: 1.8rem;
            color: var(--primary);
        }

        .form-card {
            background: #fff;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        }

        .form-group {
            margin-bottom: 15px;
        }

        .form-group label {
            display: block;
            font-size: 0.85rem;
            font-weight: 600;
            margin-bottom: 6px;
        }

        input, textarea {
            width: 100%;
            padding: 10px 12px;
            border: 1px solid #cbd5e1;
            border-radius: 8px;
            font-size: 0.95rem;
            outline: none;
        }

        input:focus, textarea:focus {
            border-color: var(--primary);
        }

        footer {
            background: #0b1120;
            color: #94a3b8;
            padding: 40px 0 20px;
            text-align: center;
            font-size: 0.9rem;
        }

        /* мобилки */
        @media (max-width: 800px) {
            .about-wrap, .contact-grid {
                grid-template-columns: 1fr;
            }

            .burger {
                display: block;
            }

            .menu {
                display: none;
                position: absolute;
                top: 70px;
                left: 0;
                width: 100%;
                background: #fff;
                flex-direction: column;
                padding: 20px;
                box-shadow: 0 8px 15px rgba(0,0,0,0.05);
            }

            .menu.show {
                display: flex;
            }
        }
    </style>
</head>
<body>
    <header>
        <div class="container">
            <nav>
                <a href="#" class="logo"><i class="fas fa-bolt"></i> Игорь Киселёв</a>
                <button class="burger" id="burgerBtn"><i class="fas fa-bars"></i></button>
                <ul class="menu" id="navMenu">
                    <li><a href="#about">Обо мне</a></li>
                    <li><a href="#gallery">Галерея</a></li>
                    <li><a href="#achievements">Достижения</a></li>
                    <li><a href="#video">Видео</a></li>
                    <li><a href="#music">Музыка</a></li>
                    <li><a href="#contact">Контакты</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <div class="hero">
        <div class="container">
            <h1>Игорь Киселёв</h1>
            <p>Терминатор в мире достижений. Всегда на шаг впереди!</p>
            <a href="#about" class="btn">Узнать больше</a>
        </div>
    </div>

    <section id="about" class="sec-light">
        <div class="container">
            <h2 class="title">Обо мне</h2>
            <div class="about-wrap">
                <div class="avatar-placeholder">
                    <i class="fas fa-user-astronaut"></i>
                </div>
                <div class="about-text">
                    <h3>Привет! Я Игорь Киселёв</h3>
                    <p>Известен как «Депутат» за свои невероятные пиджаки и способность достигать любых поставленных целей благодаря своим классным бархатным тягам.</p>
                    <p>Моя энергия и чувство стиля заряжают окружающих, а чувство юмора делает любую компанию ярче. Всегда готов прийти на помощь и поддержать в трудную минуту, ведь к вам я не равнодушен.</p>
                    <div class="tags">
                        <span class="tag"><i class="fas fa-brain"></i> Ум</span>
                        <span class="tag"><i class="fas fa-users"></i> Люблю людей</span>
                        <span class="tag"><i class="fas fa-handshake"></i> Неравнодушие</span>
                        <span class="tag"><i class="fas fa-vest"></i> Пиджачок</span>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <section id="gallery" class="sec-dark">
        <div class="container">
            <h2 class="title">Фотогалерея</h2>
            <div class="privacy-card">
                <i class="fas fa-shield-alt"></i>
                <h3>Материалы скрыты</h3>
                <p>Все персональные фотографии удалены из репозитория в целях соблюдения конфиденциальности.</p>
            </div>
        </div>
    </section>

    <section id="achievements" class="sec-light">
        <div class="container">
            <h2 class="title">Мои достижения</h2>
            <div class="grid-3">
                <div class="card">
                    <i class="fas fa-star"></i>
                    <h3>Школьная популярность</h3>
                    <p>Был душой компании, пользовался всеобщей любовью и имел кучу друзей в коллективе.</p>
                </div>
                <div class="card">
                    <i class="fas fa-graduation-cap"></i>
                    <h3>Красный аттестат</h3>
                    <p>Окончил колледж метростроя с отличием, доказав топовый уровень знаний на практике.</p>
                </div>
                <div class="card">
                    <i class="fas fa-award"></i>
                    <h3>Армейские будни</h3>
                    <p>Достойно прошёл службу, поддерживая боевой дух товарищей и железный настрой.</p>
                </div>
            </div>
        </div>
    </section>

    <section id="video" class="sec-dark">
        <div class="container">
            <h2 class="title">Видеоматериалы</h2>
            <div class="privacy-card">
                <i class="fas fa-lock"></i>
                <h3>Доступ ограничен</h3>
                <p>Видеозаписи изъяты из публичной ветки ради защиты персональных данных.</p>
            </div>
        </div>
    </section>

    <section id="music" class="sec-light">
        <div class="container">
            <h2 class="title">Музыка</h2>
            <div class="grid-3">
                <div class="track-card">
                    <div class="track-head">
                        <div class="track-icon"><i class="fas fa-music"></i></div>
                        <div>
                            <strong>Свободный крановщик</strong>
                            <div style="font-size: 0.8rem; color: #64748b;">Игорь Киселёв</div>
                        </div>
                    </div>
                    <audio controls preload="metadata">
                        <source src="/static/music/Свободный крановщик.mp3" type="audio/mpeg">
                    </audio>
                    <div class="track-desc">Короткое вступление о человеке, чья профессия делает его хозяином высоты.</div>
                </div>

                <div class="track-card">
                    <div class="track-head">
                        <div class="track-icon"><i class="fas fa-headphones"></i></div>
                        <div>
                            <strong>Депутат на кране</strong>
                            <div style="font-size: 0.8rem; color: #64748b;">Игорь Киселёв</div>
                        </div>
                    </div>
                    <audio controls preload="metadata">
                        <source src="/static/music/Депутат работающий на кране.mp3" type="audio/mpeg">
                    </audio>
                    <div class="track-desc">Ироничный трек о герое, совмещающем стиль, статус и работу на стройке.</div>
                </div>

                <div class="track-card">
                    <div class="track-head">
                        <div class="track-icon"><i class="fas fa-play"></i></div>
                        <div>
                            <strong>На закате дорог</strong>
                            <div style="font-size: 0.8rem; color: #64748b;">Игорь Киселёв</div>
                        </div>
                    </div>
                    <audio controls preload="metadata">
                        <source src="/static/music/На закате дорог, в путь вновь отправляет.mp3" type="audio/mpeg">
                    </audio>
                    <div class="track-desc">Баллада о бесконечном движении вперёд сквозь любые обстоятельства.</div>
                </div>
            </div>
        </div>
    </section>

    <section id="contact" class="sec-gray">
        <div class="container">
            <h2 class="title">Контакты</h2>
            <div class="contact-grid">
                <div class="contact-links">
                    <a href="https://vk.com" target="_blank" class="c-box">
                        <i class="fab fa-vk"></i>
                        <div>
                            <strong>Штаб ВКонтакте</strong>
                            <div style="font-size: 0.85rem; color: #64748b;">Фан-приемная депутата</div>
                        </div>
                    </a>
                    <a href="https://vk.com" target="_blank" class="c-box">
                        <i class="fas fa-shoe-prints"></i>
                        <div>
                            <strong>Бархатные тяги</strong>
                            <div style="font-size: 0.85rem; color: #64748b;">Линия стиля и консультаций</div>
                        </div>
                    </a>
                    <a href="https://t.me" target="_blank" class="c-box">
                        <i class="fab fa-telegram"></i>
                        <div>
                            <strong>Telegram приёмная</strong>
                            <div style="font-size: 0.85rem; color: #64748b;">@terminator_kiselev_bot</div>
                        </div>
                    </a>
                </div>

                <div class="form-card">
                    <form onsubmit="event.preventDefault(); alert('Сообщение отправлено!'); this.reset();">
                        <div class="form-group">
                            <label>Ваше имя</label>
                            <input type="text" required placeholder="Иван">
                        </div>
                        <div class="form-group">
                            <label>Email</label>
                            <input type="email" required placeholder="user@mail.ru">
                        </div>
                        <div class="form-group">
                            <label>Сообщение</label>
                            <textarea rows="4" required placeholder="Пару слов о проекте..."></textarea>
                        </div>
                        <button type="submit" class="btn" style="width: 100%;">Отправить</button>
                    </form>
                </div>
            </div>
        </div>
    </section>

    <footer>
        <div class="container">
            <p>© 2026 Игорь Киселёв. Все права защищены.</p>
        </div>
    </footer>

    <script>
        const burger = document.getElementById('burgerBtn');
        const menu = document.getElementById('navMenu');

        burger.addEventListener('click', () => {
            menu.classList.toggle('show');
        });

        menu.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                menu.classList.remove('show');
            });
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML)

def get_lan_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return '127.0.0.1'

if __name__ == '__main__':
    ip = get_lan_ip()
    print(f">> Dev server started: http://localhost:8080 (LAN: http://{ip}:8080)")
    
    # открываем вкладку через полсекунды после старта
    threading.Timer(0.6, lambda: webbrowser.open('http://localhost:8080')).start()
    
    try:
        app.run(host='0.0.0.0', port=8080, debug=True)
    except OSError:
        print(">> Port 8080 is busy, trying 5000...")
        app.run(host='0.0.0.0', port=5000, debug=True)
