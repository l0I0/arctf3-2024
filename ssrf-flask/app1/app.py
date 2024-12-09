from flask import Flask, request, jsonify
import requests
import urllib.request
import os

app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <style>
        body {
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
            background: #f0f0f0;
        }
        .navbar {
            background: #333;
            padding: 15px 0;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .nav-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .logo {
            color: white;
            font-size: 24px;
            text-decoration: none;
            font-weight: bold;
        }
        .nav-links a {
            color: white;
            text-decoration: none;
            margin-left: 20px;
            padding: 8px 15px;
            border-radius: 4px;
            transition: background 0.3s;
        }
        .nav-links a:hover {
            background: #444;
        }
        .main-content {
            max-width: 800px;
            margin: 40px auto;
            padding: 20px;
            text-align: center;
        }
        .welcome-text {
            font-size: 2em;
            color: #333;
            margin-bottom: 20px;
            animation: fadeIn 1s ease;
        }
        .description {
            color: #666;
            line-height: 1.6;
            margin-bottom: 30px;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
    <nav class="navbar">
        <div class="nav-container">
            <a href="/" class="logo">PhotoGallery</a>
            <div class="nav-links">
                <a href="/">Главная</a>
                <a href="/photos">Фотографии</a>
                <a href="/uploaded-photos">Загруженные фото</a>
                <a href="/uploads">Загрузить фото</a>
            </div>
        </div>
    </nav>
    <div class="main-content">
        <h1 class="welcome-text">Добро пожаловать в PhotoGallery</h1>
        <p class="description">
            Здесь вы можете найти все фотографии. 
            Перейдите в раздел "Фотографии" чтобы посмотреть галерею.
        </p>
    </div>
    '''

@app.route('/photos')
def photos():
    return '''
    <style>
        /* Копируем существующие стили для navbar */
        body {
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
            background: #f0f0f0;
        }
        .navbar {
            background: #333;
            padding: 15px 0;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .nav-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .logo {
            color: white;
            font-size: 24px;
            text-decoration: none;
            font-weight: bold;
        }
        .nav-links a {
            color: white;
            text-decoration: none;
            margin-left: 20px;
            padding: 8px 15px;
            border-radius: 4px;
            transition: background 0.3s;
        }
        .nav-links a:hover {
            background: #444;
        }
        /* Существующие стили для галереи */
        .image-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 10px;
            padding: 20px;
            max-width: 1200px;
            margin: 0 auto;
        }
        .image-item {
            opacity: 0;
            transform: scale(0.6);
            animation: zoomIn 0.6s cubic-bezier(0.4, 0, 0.2, 1) forwards;
            overflow: hidden;
        }
        .image-item img {
            width: 100%;
            height: 200px;
            object-fit: cover;
            display: block;
            border-radius: 8px;
            transition: all 0.3s ease;
        }
        .image-item img:hover {
            transform: scale(1.1);
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        @keyframes zoomIn {
            0% { opacity: 0; transform: scale(0.6); }
            100% { opacity: 1; transform: scale(1); }
        }
    </style>
    <nav class="navbar">
        <div class="nav-container">
            <a href="/" class="logo">PhotoGallery</a>
            <div class="nav-links">
                <a href="/">Главная</a>
                <a href="/photos">Фотографии</a>
                <a href="/uploaded-photos">Загруженные фото</a>
                <a href="/uploads">Загрузить фото</a>
            </div>
        </div>
    </nav>
    <div id="images" class="image-grid"></div>
    <script>
        function loadImages(images) {
            const container = document.getElementById('images');
            const fragment = document.createDocumentFragment();
            
            images.forEach((image, index) => {
                const div = document.createElement('div');
                div.className = 'image-item';
                div.style.animationDelay = `${index * 100}ms`;
                
                const img = document.createElement('img');
                img.src = `/fetch?url=http://web-photo:7002/images/${image}`;
                img.loading = 'lazy';
                
                div.appendChild(img);
                fragment.appendChild(div);
            });
            
            container.appendChild(fragment);
        }

        window.onload = function() {
            fetch('/fetch?url=http://web-photo:7002/images')
                .then(response => response.json())
                .then(data => {
                    if (data.images) {
                        loadImages(data.images);
                    }
                })
                .catch(error => {
                    document.getElementById('images').innerHTML = 
                        `<p style="color: red;">Ошибка при загрузке изображений: ${error}</p>`;
                });
        }
    </script>
    '''

@app.route('/fetch', methods=['GET', 'POST'])
def fetch():
    url = request.args.get('url')
    
    if not url:
        return 'Укажите URL'
    
    try:
        if url.startswith('file://'):
            path = url.replace('file://', '')
            if os.path.isdir(path):
                files = os.listdir(path)
                return '\n'.join(files)
            if os.path.isfile(path):
                with open(path, 'r') as f:
                    return f.read()
            return 'Файл не найден'
        
        if request.method == 'POST':
            files = {
                'file': (
                    request.files['file'].filename,
                    request.files['file'].stream,
                    request.files['file'].content_type
                )
            }
            response = requests.post(url, files=files)
        else:
            response = requests.get(url)
            
        if url.endswith(('.webp', '.jpg', '.jpeg', '.png', '.gif')):
            return response.content, 200, {'Content-Type': response.headers.get('Content-Type', 'image/jpeg')}
            
        return response.json() if 'application/json' in response.headers.get('Content-Type', '') else response.text
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/uploads')
def uploads():
    return '''
    <style>
        body {
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
            background: #f0f0f0;
        }
        .navbar {
            background: #333;
            padding: 15px 0;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .nav-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .logo {
            color: white;
            font-size: 24px;
            text-decoration: none;
            font-weight: bold;
        }
        .nav-links a {
            color: white;
            text-decoration: none;
            margin-left: 20px;
            padding: 8px 15px;
            border-radius: 4px;
            transition: background 0.3s;
        }
        .nav-links a:hover {
            background: #444;
        }
        .upload-container {
            max-width: 600px;
            margin: 40px auto;
            padding: 30px;
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .upload-title {
            text-align: center;
            color: #333;
            margin-bottom: 30px;
            font-size: 24px;
        }
        .upload-form {
            display: flex;
            flex-direction: column;
            gap: 20px;
        }
        .file-input-container {
            border: 2px dashed #ccc;
            padding: 30px;
            text-align: center;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .file-input-container:hover {
            border-color: #666;
            background: #f8f8f8;
        }
        .file-input-container input[type="file"] {
            display: none;
        }
        .file-input-label {
            color: #666;
            font-size: 16px;
            cursor: pointer;
        }
        .upload-button {
            background: #4CAF50;
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .upload-button:hover {
            background: #45a049;
            transform: translateY(-2px);
        }
        .upload-button:active {
            transform: translateY(0);
        }
        #upload-status {
            margin-top: 20px;
            padding: 15px;
            border-radius: 8px;
            display: none;
            text-align: center;
            font-size: 16px;
        }
        .success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
    </style>
    <nav class="navbar">
        <div class="nav-container">
            <a href="/" class="logo">PhotoGallery</a>
            <div class="nav-links">
                <a href="/">Главная</a>
                <a href="/photos">Фотографии</a>
                <a href="/uploaded-photos">Загруженные фото</a>
                <a href="/uploads">Загрузить фото</a>
            </div>
        </div>
    </nav>
    <div class="upload-container">
        <h2 class="upload-title">Загрузить фотографию</h2>
        <form id="uploadForm" class="upload-form" enctype="multipart/form-data">
            <div class="file-input-container" onclick="document.getElementById('fileInput').click()">
                <input type="file" id="fileInput" name="file" accept="image/*" required>
                <label for="fileInput" class="file-input-label">
                    Нажмите или перетащите файл сюда
                </label>
            </div>
            <button type="submit" class="upload-button">Загрузить</button>
        </form>
        <div id="upload-status"></div>
    </div>
    <script>
        const form = document.getElementById('uploadForm');
        const status = document.getElementById('upload-status');
        const fileInput = document.getElementById('fileInput');
        const fileLabel = document.querySelector('.file-input-label');

        fileInput.addEventListener('change', function() {
            if (this.files && this.files[0]) {
                fileLabel.textContent = this.files[0].name;
            } else {
                fileLabel.textContent = 'Нажмите или перетащите файл сюда';
            }
        });

        form.onsubmit = async (e) => {
            e.preventDefault();
            const formData = new FormData(form);
            status.style.display = 'block';
            status.className = '';
            status.textContent = 'Загрузка...';

            try {
                const response = await fetch('/fetch?url=http://web-photo:7002/uploads', {
                    method: 'POST',
                    body: formData
                });
                const result = await response.json();
                
                if (result.status === 'success') {
                    status.className = 'success';
                    status.textContent = result.message;
                    form.reset();
                    fileLabel.textContent = 'Нажмите или перетащите файл сюда';
                } else {
                    status.className = 'error';
                    status.textContent = result.message;
                }
            } catch (error) {
                status.className = 'error';
                status.textContent = 'Ошибка при загрузке файла';
            }
        };
    </script>
    '''

@app.route('/uploaded-photos')
def uploaded_photos():
    return '''
    <style>
        /* Те же стили, что и в /photos */
        body {
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
            background: #f0f0f0;
        }
        .navbar {
            background: #333;
            padding: 15px 0;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .nav-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .logo {
            color: white;
            font-size: 24px;
            text-decoration: none;
            font-weight: bold;
        }
        .nav-links a {
            color: white;
            text-decoration: none;
            margin-left: 20px;
            padding: 8px 15px;
            border-radius: 4px;
            transition: background 0.3s;
        }
        .nav-links a:hover {
            background: #444;
        }
        .image-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 10px;
            padding: 20px;
            max-width: 1200px;
            margin: 0 auto;
        }
        .image-item {
            opacity: 0;
            transform: scale(0.6);
            animation: zoomIn 0.6s cubic-bezier(0.4, 0, 0.2, 1) forwards;
            overflow: hidden;
        }
        .image-item img {
            width: 100%;
            height: 200px;
            object-fit: cover;
            display: block;
            border-radius: 8px;
            transition: all 0.3s ease;
        }
        .image-item img:hover {
            transform: scale(1.1);
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        @keyframes zoomIn {
            0% { opacity: 0; transform: scale(0.6); }
            100% { opacity: 1; transform: scale(1); }
        }
    </style>
    <nav class="navbar">
        <div class="nav-container">
            <a href="/" class="logo">PhotoGallery</a>
            <div class="nav-links">
                <a href="/">Главная</a>
                <a href="/photos">Фотографии</a>
                <a href="/uploaded-photos">Загруженные фото</a>
                <a href="/uploads">Загрузить фото</a>
            </div>
        </div>
    </nav>
    <div id="images" class="image-grid"></div>
    <script>
        function loadImages() {
            fetch('/fetch?url=http://web-photo:7002/uploads')
                .then(response => response.json())
                .then(data => {
                    const container = document.getElementById('images');
                    container.innerHTML = '';
                    if (data.images && data.images.length > 0) {
                        data.images.forEach((image, index) => {
                            const div = document.createElement('div');
                            div.className = 'image-item';
                            div.style.animationDelay = `${index * 100}ms`;
                            
                            const img = document.createElement('img');
                            img.src = `/fetch?url=http://web-photo:7002/uploads/${image}`;
                            img.loading = 'lazy';
                            
                            div.appendChild(img);
                            container.appendChild(div);
                        });
                    } else {
                        container.innerHTML = '<p style="text-align: center; color: #666;">Нет загруженных фотографий</p>';
                    }
                })
                .catch(error => {
                    document.getElementById('images').innerHTML = 
                        `<p style="color: red;">Ошибка при загрузке изображений: ${error}</p>`;
                });
        }

        window.onload = loadImages;
    </script>
    '''