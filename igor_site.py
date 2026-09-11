import os
import socket
import threading
import webbrowser
from flask import Flask, render_template_string

# Базовые директории для локального ПК и PythonAnywhere
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'static')

# Автоматическое создание необходимых папок
for subfolder in ['images', 'videos', 'music']:
    os.makedirs(os.path.join(STATIC_DIR, subfolder), exist_ok=True)

app = Flask(__name__, static_folder=STATIC_DIR)

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
    <meta name="description" content="Официальный сайт Игоря Киселёва - Терминатора в мире достижений">
    <meta name="keywords" content="Игорь Киселёв, депутат, терминатор, достижения, музыка, видео">
    <meta name="author" content="Игорь Киселёв">
    <title>Игорь Киселёв | Официальный сайт</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --primary-blue: #3b82f6;
            --dark-blue: #1e40af;
            --light-blue: #dbeafe;
            --accent: #f59e0b;
            --text-dark: #1f2937;
            --text-light: #6b7280;
            --white: #ffffff;
            --bg-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            -webkit-tap-highlight-color: transparent;
        }

        html {
            scroll-behavior: smooth;
        }

        body {
            background: var(--bg-gradient);
            color: var(--text-dark);
            line-height: 1.6;
            min-height: 100vh;
            overflow-x: hidden;
            width: 100%;
        }

        .container {
            width: 100%;
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 clamp(15px, 4vw, 30px);
        }

        /* === ШАПКА === */
        .header {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
            position: fixed;
            width: 100%;
            top: 0;
            left: 0;
            z-index: 1000;
            transition: all 0.3s ease;
        }

        .header.scrolled {
            background: rgba(255, 255, 255, 0.98);
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
        }

        .nav {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0.9rem 0;
        }

        .logo {
            font-size: clamp(1.3rem, 3.5vw, 1.7rem);
            font-weight: 800;
            background: linear-gradient(45deg, var(--primary-blue), var(--dark-blue));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: flex;
            align-items: center;
            gap: 8px;
            text-decoration: none;
            z-index: 1002;
        }

        .nav-links {
            display: flex;
            gap: 1.5rem;
            list-style: none;
        }

        .nav-links a {
            text-decoration: none;
            color: var(--text-dark);
            font-weight: 600;
            padding: 0.5rem 1rem;
            border-radius: 25px;
            transition: all 0.3s ease;
            white-space: nowrap;
            display: inline-block;
        }

        .nav-links a:hover,
        .nav-links a.active {
            background: var(--primary-blue);
            color: var(--white);
        }

        .mobile-menu-btn {
            display: none;
            background: none;
            border: none;
            font-size: 1.6rem;
            color: var(--text-dark);
            cursor: pointer;
            padding: 0.4rem;
            z-index: 1002;
        }

        /* === ГЛАВНЫЙ ЭКРАН === */
        .hero {
            padding: clamp(120px, 18vh, 180px) 0 clamp(60px, 10vh, 100px);
            text-align: center;
            color: var(--white);
            min-height: 85vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .hero-content {
            width: 100%;
        }

        .hero h1 {
            font-size: clamp(2.2rem, 7vw, 4.2rem);
            font-weight: 800;
            margin-bottom: 1.2rem;
            text-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
            line-height: 1.15;
        }

        .hero p {
            font-size: clamp(1rem, 2.5vw, 1.35rem);
            margin-bottom: 2rem;
            opacity: 0.95;
            max-width: 620px;
            margin-left: auto;
            margin-right: auto;
        }

        .btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            padding: clamp(12px, 2.5vw, 15px) clamp(26px, 4vw, 36px);
            background: var(--accent);
            color: var(--text-dark);
            text-decoration: none;
            border-radius: 50px;
            font-weight: 700;
            transition: all 0.3s ease;
            border: none;
            cursor: pointer;
            font-size: clamp(0.95rem, 2vw, 1.05rem);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
        }

        .btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(245, 158, 11, 0.45);
        }

        .btn:active {
            transform: scale(0.98);
        }

        /* === СЕКЦИИ === */
        .section {
            padding: clamp(50px, 8vw, 90px) 0;
        }

        .section-light {
            background: var(--white);
        }

        .section-dark {
            background: #0f172a;
            color: var(--white);
        }

        .section-title {
            text-align: center;
            font-size: clamp(1.8rem, 5vw, 2.6rem);
            font-weight: 800;
            margin-bottom: clamp(2rem, 5vw, 3rem);
            color: inherit;
        }

        .section-title::after {
            content: '';
            display: block;
            width: 60px;
            height: 4px;
            background: var(--accent);
            margin: 12px auto 0;
            border-radius: 4px;
        }

        /* === ОБО МНЕ === */
        .about-grid {
            display: grid;
            grid-template-columns: 1fr 1.3fr;
            gap: clamp(1.8rem, 4vw, 3.5rem);
            align-items: center;
        }

        .photo-container {
            text-align: center;
            display: flex;
            justify-content: center;
        }

        .main-photo {
            width: 100%;
            max-width: 380px;
            border-radius: 20px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
            height: auto;
            aspect-ratio: 3/4;
            object-fit: cover;
        }

        .about-content h3 {
            font-size: clamp(1.4rem, 3.5vw, 2rem);
            color: var(--primary-blue);
            margin-bottom: 1.2rem;
        }

        .traits-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
            gap: 0.8rem;
            margin-top: 1.5rem;
        }

        .trait-badge {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 0.8rem 1rem;
            background: var(--light-blue);
            border-radius: 12px;
            font-weight: 600;
            font-size: 0.95rem;
            color: var(--text-dark);
        }

        /* === СЕТКИ И КАРТОЧКИ === */
        .gallery-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(min(240px, 100%), 1fr));
            gap: 1.2rem;
        }

        .gallery-item {
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.25);
            aspect-ratio: 1;
            background: #1e293b;
            position: relative;
        }

        .gallery-item img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.4s ease;
            display: block;
        }

        .gallery-item:hover img {
            transform: scale(1.05);
        }

        .achievements-grid,
        .video-grid,
        .music-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(min(300px, 100%), 1fr));
            gap: 1.5rem;
        }

        .achievement-card {
            background: var(--white);
            padding: clamp(1.5rem, 3vw, 2.2rem);
            border-radius: 16px;
            text-align: center;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.06);
            color: var(--text-dark);
            transition: transform 0.3s ease;
        }

        .achievement-card:hover {
            transform: translateY(-5px);
        }

        .achievement-icon {
            font-size: clamp(2.2rem, 5vw, 3rem);
            color: var(--primary-blue);
            margin-bottom: 1rem;
        }

        /* === ВИДЕО === */
        .video-item {
            background: var(--white);
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
            display: flex;
            flex-direction: column;
        }

        .video-player {
            width: 100%;
            aspect-ratio: 16/9;
            background: #000;
            position: relative;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .video-player video {
            width: 100%;
            height: 100%;
            object-fit: cover;
            display: block;
        }

        .video-content {
            padding: 1.2rem 1.4rem;
            color: var(--text-dark);
            flex-grow: 1;
        }

        .video-content h4 {
            color: var(--dark-blue);
            margin-bottom: 0.4rem;
            font-size: 1.15rem;
        }

        /* === МУЗЫКА === */
        .music-item {
            background: var(--white);
            border-radius: 16px;
            padding: clamp(1.2rem, 3vw, 1.6rem);
            box-shadow: 0 8px 25px rgba(0,0,0,0.06);
        }

        .music-header {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 1rem;
        }

        .music-icon {
            width: 48px;
            height: 48px;
            background: linear-gradient(45deg, var(--primary-blue), var(--dark-blue));
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 1.3rem;
            flex-shrink: 0;
        }

        audio {
            width: 100%;
            height: 40px;
            margin-bottom: 0.8rem;
        }

        /* === КОНТАКТЫ === */
        .contact-container {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: clamp(1.5rem, 4vw, 3rem);
        }

        .contact-info {
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }

        .contact-card {
            display: flex;
            align-items: center;
            gap: 1.2rem;
            padding: 1.2rem 1.4rem;
            background: var(--white);
            border-radius: 14px;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.06);
            text-decoration: none;
            color: var(--text-dark);
            transition: all 0.3s ease;
        }

        .contact-card:hover {
            background: var(--primary-blue);
            color: var(--white);
            transform: translateX(4px);
        }

        .contact-icon {
            font-size: 2rem;
            color: var(--primary-blue);
        }

        .contact-card:hover .contact-icon {
            color: var(--white);
        }

        .contact-form-box {
            background: var(--white);
            padding: clamp(1.5rem, 4vw, 2.2rem);
            border-radius: 18px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
        }

        .contact-form-box h3 {
            color: var(--dark-blue);
            margin-bottom: 1.2rem;
            font-size: 1.4rem;
        }

        .form-group {
            margin-bottom: 1rem;
        }

        .form-group label {
            display: block;
            margin-bottom: 0.4rem;
            font-weight: 600;
            font-size: 0.95rem;
        }

        input, textarea {
            width: 100%;
            padding: 0.85rem 1rem;
            border: 2px solid #e2e8f0;
            border-radius: 10px;
            font-size: 16px; /* Предотвращает зум на iOS */
            outline: none;
            transition: border-color 0.3s ease;
        }

        input:focus, textarea:focus {
            border-color: var(--primary-blue);
        }

        /* === ПОДВАЛ === */
        .footer {
            background: #090d16;
            color: var(--white);
            padding: clamp(2.5rem, 5vw, 3.5rem) 0 1.5rem;
        }

        .footer-content {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 2rem;
            margin-bottom: 2rem;
        }

        .copyright {
            text-align: center;
            padding-top: 1.5rem;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            font-size: 0.9rem;
            opacity: 0.8;
        }

        .placeholder {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 1.5rem;
            background: var(--light-blue);
            border-radius: 14px;
            color: var(--text-dark);
            width: 100%;
            height: 100%;
        }

        /* === АДАПТИВНОСТЬ ПОД ЭКРАНЫ === */
        @media (max-width: 900px) {
            .about-grid, .contact-container {
                grid-template-columns: 1fr;
            }
            .photo-container {
                margin-bottom: 1rem;
            }
        }

        @media (max-width: 768px) {
            .nav-links {
                position: fixed;
                top: 0;
                right: -100%;
                width: 80%;
                max-width: 320px;
                height: 100vh;
                background: var(--white);
                flex-direction: column;
                justify-content: flex-start;
                align-items: stretch;
                padding: 85px 1.5rem 2rem;
                gap: 0.4rem;
                transition: right 0.35s cubic-bezier(0.4, 0, 0.2, 1);
                box-shadow: -8px 0 25px rgba(0, 0, 0, 0.15);
                z-index: 1001;
            }

            .nav-links.active {
                right: 0;
            }

            .nav-links a {
                padding: 0.9rem 1.2rem;
                border-radius: 10px;
                font-size: 1.05rem;
            }

            .mobile-menu-btn {
                display: block;
            }

            .hero h1 {
                font-size: 2.3rem;
            }

            .gallery-grid {
                grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
                gap: 0.8rem;
            }
        }

        @media (max-width: 480px) {
            .gallery-grid {
                grid-template-columns: 1fr 1fr;
            }
            .traits-grid {
                grid-template-columns: 1fr 1fr;
            }
            .btn {
                width: 100%;
            }
        }
    </style>
</head>
<body>
    <header class="header" id="header">
        <div class="container">
            <nav class="nav">
                <a href="#" class="logo">
                    <i class="fas fa-fire"></i> Игорь Киселёв
                </a>
                <button class="mobile-menu-btn" id="mobileMenuBtn" aria-label="Открыть меню">
                    <i class="fas fa-bars"></i>
                </button>
                <ul class="nav-links" id="navLinks">
                    <li><a href="#about" class="active">Обо мне</a></li>
                    <li><a href="#gallery">Галерея</a></li>
                    <li><a href="#achievements">Достижения</a></li>
                    <li><a href="#video">Видео</a></li>
                    <li><a href="#music">Музыка</a></li>
                    <li><a href="#contact">Контакты</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <!-- Главный экран -->
    <section class="hero">
        <div class="container">
            <div class="hero-content">
                <h1>Игорь Киселёв</h1>
                <p>Терминатор в мире достижений. Всегда на шаг впереди!</p>
                <a href="#about" class="btn">
                    <i class="fas fa-user"></i> Узнать больше
                </a>
            </div>
        </div>
    </section>

    <!-- Обо мне -->
    <section id="about" class="section section-light">
        <div class="container">
            <h2 class="section-title">Обо мне</h2>
            <div class="about-grid">
                <div class="photo-container">
                    <img src="{{ url_for('static', filename='images/21qejkhtw.jpg') }}"
                         alt="Игорь Киселёв" class="main-photo"
                         onerror="this.style.display='none'; this.nextElementSibling.style.display='flex'">
                    <div class="placeholder" style="display: none;">
                        <i class="fas fa-camera" style="font-size: 2.5rem; margin-bottom: 0.5rem; color: var(--primary-blue);"></i>
                        <h3>Фото Игоря</h3>
                    </div>
                </div>
                <div class="about-content">
                    <h3>Привет! Я Игорь Киселёв</h3>
                    <p style="margin-bottom: 1rem; font-size: 1.05rem;">
                        Известен как «Депутат» за свои невероятные пиджаки и способность достигать любых поставленных целей благодаря своим классным бархатным тягам.
                        Моя энергия и чувство стиля заряжают окружающих, а чувство юмора делает любую компанию ярче.
                    </p>
                    <p style="margin-bottom: 1.2rem; font-size: 1.05rem;">
                        Всегда готов прийти на помощь и поддержать в трудную минуту, ведь к вам я не равнодушен. Верю, что настоящая сила — в доброте и любви к ближнему.
                    </p>
                    <div class="traits-grid">
                        <div class="trait-badge"><i class="fas fa-brain" style="color: var(--primary-blue);"></i> <span>Ум</span></div>
                        <div class="trait-badge"><i class="fas fa-users" style="color: var(--primary-blue);"></i> <span>Люблю людей</span></div>
                        <div class="trait-badge"><i class="fas fa-handshake" style="color: var(--primary-blue);"></i> <span>Неравнодушие</span></div>
                        <div class="trait-badge"><i class="fas fa-vest" style="color: var(--primary-blue);"></i> <span>Пиджачок</span></div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Галерея -->
    <section id="gallery" class="section section-dark">
        <div class="container">
            <h2 class="section-title">Фотогалерея</h2>
            <div class="gallery-grid">
                <div class="gallery-item">
                    <img src="{{ url_for('static', filename='images/2fh32J3OmHhebkZLy81PrrXVH7T50eSFv7OfjqOdJiual_hWFaIYgfUokUJ-875eGLC2U2JCvf9brT_ouPYVfkN8.jpg') }}"
                         alt="Игорь с курочкой" loading="lazy"
                         onerror="this.style.display='none'; this.nextElementSibling.style.display='flex'">
                    <div class="placeholder" style="display: none;"><i class="fas fa-image"></i></div>
                </div>
                <div class="gallery-item">
                    <img src="{{ url_for('static', filename='images/7R3ueRTqofE5W9xpzMgDpeV5h-yuQDnCIeJnBytjZoffZPvBh7mrUK2h8pGHIU_9FjpicKq1aw6U3tPlfbLUmnpe.jpg') }}"
                         alt="Игорь в кресле" loading="lazy"
                         onerror="this.style.display='none'; this.nextElementSibling.style.display='flex'">
                    <div class="placeholder" style="display: none;"><i class="fas fa-image"></i></div>
                </div>
                <div class="gallery-item">
                    <img src="{{ url_for('static', filename='images/p9sTkbvTbfzUsvzC0S-5sUYzWkU1THolCrEEGJ0AchQMPLKGkHj5jJWheQCwGj0QgENgz_f9ChnWKDPx0npr309K.jpg') }}"
                         alt="Игорь на Красной площади" loading="lazy"
                         onerror="this.style.display='none'; this.nextElementSibling.style.display='flex'">
                    <div class="placeholder" style="display: none;"><i class="fas fa-image"></i></div>
                </div>
                <div class="gallery-item">
                    <img src="{{ url_for('static', filename='images/Q1AU6KmOHdM5lSSAtt7Nrh9fTj4pHN6UtX_Hggl2HAh9GXbe98uKy9dO45k1b9YK_w6QVCPp81kyEbSzyNsENNhF.jpg') }}"
                         alt="Выпускной" loading="lazy"
                         onerror="this.style.display='none'; this.nextElementSibling.style.display='flex'">
                    <div class="placeholder" style="display: none;"><i class="fas fa-image"></i></div>
                </div>
                <div class="gallery-item">
                    <img src="{{ url_for('static', filename='images/photo_2025-09-23_21-28-17.jpg') }}"
                         alt="Игорь на службе" loading="lazy"
                         onerror="this.style.display='none'; this.nextElementSibling.style.display='flex'">
                    <div class="placeholder" style="display: none;"><i class="fas fa-image"></i></div>
                </div>
            </div>
        </div>
    </section>

    <!-- Достижения -->
    <section id="achievements" class="section section-light">
        <div class="container">
            <h2 class="section-title">Достижения</h2>
            <div class="achievements-grid">
                <div class="achievement-card">
                    <div class="achievement-icon"><i class="fas fa-star"></i></div>
                    <h3>Душа компании</h3>
                    <p>Пользовался всеобщей любовью и уважением, заряжая коллектив отличным настроением.</p>
                </div>
                <div class="achievement-card">
                    <div class="achievement-icon"><i class="fas fa-graduation-cap"></i></div>
                    <h3>Красный аттестат</h3>
                    <p>Закончил колледж метростроя с отличием, доказав выдающийся уровень знаний.</p>
                </div>
                <div class="achievement-card">
                    <div class="achievement-icon"><i class="fas fa-shield-alt"></i></div>
                    <h3>Армейские будни</h3>
                    <p>Достойно прошёл службу в вооруженных силах, сохраняя железный боевой дух.</p>
                </div>
            </div>
        </div>
    </section>

    <!-- Видеоматериалы -->
    <section id="video" class="section section-dark">
        <div class="container">
            <h2 class="section-title">Видеоматериалы</h2>
            <div class="video-grid">
                <!-- Видео 1 -->
                <div class="video-item">
                    <div class="video-player">
                        <video controls playsinline webkit-playsinline preload="metadata"
                               poster="{{ url_for('static', filename='images/video-preview1.jpg') }}"
                               onerror="this.style.display='none'; this.nextElementSibling.style.display='flex'">
                            <source src="{{ url_for('static', filename='videos/video_2025-11-28_21-47-04.mp4') }}" type="video/mp4">
                            <source src="{{ url_for('static', filename='videos/video_2025-11-28_21-47-04.webm') }}" type="video/webm">
                            Ваш браузер не поддерживает видео тег.
                        </video>
                        <div class="placeholder" style="display: none; background: #1e293b; color: white;">
                            <i class="fas fa-video" style="font-size: 2.5rem; margin-bottom: 0.5rem;"></i>
                            <span>Видео 1 в обработке</span>
                        </div>
                    </div>
                    <div class="video-content">
                        <h4>Мои достижения</h4>
                        <p style="color: var(--text-light); font-size: 0.9rem;">Видео о главных профессиональных успехах</p>
                    </div>
                </div>

                <!-- Видео 2 -->
                <div class="video-item">
                    <div class="video-player">
                        <video controls playsinline webkit-playsinline preload="metadata"
                               poster="{{ url_for('static', filename='images/video-preview2.jpg') }}"
                               onerror="this.style.display='none'; this.nextElementSibling.style.display='flex'">
                            <source src="{{ url_for('static', filename='videos/video_2025-11-28_21-33-30.mp4') }}" type="video/mp4">
                            <source src="{{ url_for('static', filename='videos/video_2025-11-28_21-33-30.webm') }}" type="video/webm">
                            Ваш браузер не поддерживает видео тег.
                        </video>
                        <div class="placeholder" style="display: none; background: #1e293b; color: white;">
                            <i class="fas fa-video" style="font-size: 2.5rem; margin-bottom: 0.5rem;"></i>
                            <span>Видео 2 в обработке</span>
                        </div>
                    </div>
                    <div class="video-content">
                        <h4>Моменты из жизни</h4>
                        <p style="color: var(--text-light); font-size: 0.9rem;">Яркие и памятные жизненные кадры</p>
                    </div>
                </div>

                <!-- Видео 3 -->
                <div class="video-item">
                    <div class="video-player">
                        <video controls playsinline webkit-playsinline preload="metadata"
                               poster="{{ url_for('static', filename='images/video_2025-12-07_20-37-47.jpg') }}"
                               onerror="this.style.display='none'; this.nextElementSibling.style.display='flex'">
                            <source src="{{ url_for('static', filename='videos/video_2025-12-07_20-37-47.mp4') }}" type="video/mp4">
                            <source src="{{ url_for('static', filename='videos/video_2025-12-07_20-37-47.webm') }}" type="video/webm">
                            Ваш браузер не поддерживает видео тег.
                        </video>
                        <div class="placeholder" style="display: none; background: #1e293b; color: white;">
                            <i class="fas fa-video" style="font-size: 2.5rem; margin-bottom: 0.5rem;"></i>
                            <span>Видео 3 в обработке</span>
                        </div>
                    </div>
                    <div class="video-content">
                        <h4>Широкий Игорь</h4>
                        <p style="color: var(--text-light); font-size: 0.9rem;">Неформальные встречи и общение с друзьями</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Музыка -->
    <section id="music" class="section section-light">
        <div class="container">
            <h2 class="section-title">Музыкальные треки</h2>
            <div class="music-grid">
                <div class="music-item">
                    <div class="music-header">
                        <div class="music-icon"><i class="fas fa-music"></i></div>
                        <div>
                            <h4>Свободный крановщик</h4>
                            <p style="color: var(--text-light); font-size: 0.85rem;">Игорь Киселёв</p>
                        </div>
                    </div>
                    <audio controls preload="none">
                        <source src="{{ url_for('static', filename='music/Свободный крановщик.mp3') }}" type="audio/mpeg">
                    </audio>
                    <p style="color: var(--text-light); font-size: 0.9rem;">Атмосферное вступление о хозяине высоты и времени.</p>
                </div>

                <div class="music-item">
                    <div class="music-header">
                        <div class="music-icon"><i class="fas fa-headphones"></i></div>
                        <div>
                            <h4>Депутат на кране</h4>
                            <p style="color: var(--text-light); font-size: 0.85rem;">Игорь Киселёв</p>
                        </div>
                    </div>
                    <audio controls preload="none">
                        <source src="{{ url_for('static', filename='music/Депутат работающий на кране.mp3') }}" type="audio/mpeg">
                    </audio>
                    <p style="color: var(--text-light); font-size: 0.9rem;">Ироничная песня о совмещении власти и физического труда.</p>
                </div>

                <div class="music-item">
                    <div class="music-header">
                        <div class="music-icon"><i class="fas fa-play"></i></div>
                        <div>
                            <h4>На закате дорог</h4>
                            <p style="color: var(--text-light); font-size: 0.85rem;">Игорь Киселёв</p>
                        </div>
                    </div>
                    <audio controls preload="none">
                        <source src="{{ url_for('static', filename='music/На закате дорог, в путь вновь отправляет.mp3') }}" type="audio/mpeg">
                    </audio>
                    <p style="color: var(--text-light); font-size: 0.9rem;">Баллада о движении вперёд машиниста сквозь огни столицы.</p>
                </div>
            </div>
        </div>
    </section>

    <!-- Контакты -->
    <section id="contact" class="section section-light" style="background: #f8fafc;">
        <div class="container">
            <h2 class="section-title">Контакты</h2>
            <div class="contact-container">
                <div class="contact-info">
                    <a href="https://vk.com/id324737660" class="contact-card" target="_blank" rel="noopener">
                        <div class="contact-icon"><i class="fab fa-vk"></i></div>
                        <div>
                            <h4>ВКонтакте</h4>
                            <p style="color: var(--text-light); font-size: 0.9rem;">Основная страница</p>
                        </div>
                    </a>
                    <a href="https://vk.com/kiselevterminator" class="contact-card" target="_blank" rel="noopener">
                        <div class="contact-icon"><i class="fab fa-vk"></i></div>
                        <div>
                            <h4>ВКонтакте</h4>
                            <p style="color: var(--text-light); font-size: 0.9rem;">Игорь Киселёв не умер?</p>
                        </div>
                    </a>
                    <a href="https://t.me/Igor_744" class="contact-card" target="_blank" rel="noopener">
                        <div class="contact-icon"><i class="fab fa-telegram"></i></div>
                        <div>
                            <h4>Telegram</h4>
                            <p style="color: var(--text-light); font-size: 0.9rem;">@Igor_744</p>
                        </div>
                    </a>
                </div>

                <div class="contact-form-box">
                    <h3>Напишите мне</h3>
                    <form id="contactForm" onsubmit="event.preventDefault(); alert('Сообщение отправлено!'); this.reset();">
                        <div class="form-group">
                            <label>Ваше имя</label>
                            <input type="text" placeholder="Введите имя" required>
                        </div>
                        <div class="form-group">
                            <label>Ваш Email</label>
                            <input type="email" placeholder="name@example.com" required>
                        </div>
                        <div class="form-group">
                            <label>Сообщение</label>
                            <textarea placeholder="Ваш текст..." rows="4" required></textarea>
                        </div>
                        <button type="submit" class="btn" style="width: 100%;">
                            <i class="fas fa-paper-plane"></i> Отправить сообщение
                        </button>
                    </form>
                </div>
            </div>
        </div>
    </section>

    <!-- Подвал -->
    <footer class="footer">
        <div class="container">
            <div class="footer-content">
                <div>
                    <h3 style="margin-bottom: 0.8rem;">Игорь Киселёв</h3>
                    <p style="opacity: 0.8; font-size: 0.95rem;">Человек с невероятной энергией. Всегда открыт для новых знакомств и сотрудничества.</p>
                </div>
                <div>
                    <h3 style="margin-bottom: 0.8rem;">Навигация</h3>
                    <p><a href="#about" style="color: white; text-decoration: none; opacity: 0.8;">Обо мне</a></p>
                    <p><a href="#gallery" style="color: white; text-decoration: none; opacity: 0.8;">Галерея</a></p>
                    <p><a href="#video" style="color: white; text-decoration: none; opacity: 0.8;">Видео</a></p>
                    <p><a href="#music" style="color: white; text-decoration: none; opacity: 0.8;">Музыка</a></p>
                </div>
            </div>
            <div class="copyright">
                <p>&copy; 2026 Игорь Киселёв. Все права защищены.</p>
            </div>
        </div>
    </footer>

    <script>
        const mobileMenuBtn = document.getElementById('mobileMenuBtn');
        const navLinks = document.getElementById('navLinks');
        const header = document.getElementById('header');

        // Открытие/закрытие мобильного меню
        mobileMenuBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            navLinks.classList.toggle('active');
            mobileMenuBtn.innerHTML = navLinks.classList.contains('active') ?
                '<i class="fas fa-times"></i>' : '<i class="fas fa-bars"></i>';
        });

        // Закрытие при клике по пунктам меню
        document.querySelectorAll('.nav-links a').forEach(link => {
            link.addEventListener('click', () => {
                navLinks.classList.remove('active');
                mobileMenuBtn.innerHTML = '<i class="fas fa-bars"></i>';
            });
        });

        // Закрытие меню при клике вне его области
        document.addEventListener('click', (e) => {
            if (!navLinks.contains(e.target) && !mobileMenuBtn.contains(e.target)) {
                navLinks.classList.remove('active');
                mobileMenuBtn.innerHTML = '<i class="fas fa-bars"></i>';
            }
        });

        // Эффект шапки при прокрутке
        window.addEventListener('scroll', () => {
            header.classList.toggle('scrolled', window.scrollY > 50);
        });
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

def get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

if __name__ == '__main__':
    local_ip = get_ip_address()
    print("=" * 60)
    print("🚀 САЙТ ИГОРЯ КИСЕЛЁВА ЗАПУЩЕН")
    print(f"💻 ПК (локально): http://localhost:8080")
    print(f"📱 С телефона (Wi-Fi): http://{local_ip}:8080")
    print("=" * 60)

    threading.Timer(1.0, lambda: webbrowser.open_new('http://localhost:8080')).start()

    try:
        app.run(host='0.0.0.0', port=8080, debug=True)
    except Exception:
        app.run(host='0.0.0.0', port=5000, debug=True)