from flask import Flask, jsonify, send_file, request
from werkzeug.middleware.proxy_fix import ProxyFix
import os
import mimetypes
from pathlib import Path
from werkzeug.utils import secure_filename
import random
from PIL import Image
import uuid
import io

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

IMAGES_FOLDER = 'images'
UPLOADS_FOLDER = 'uploads'

# Создаем папку для загруженных фото если её нет
os.makedirs(UPLOADS_FOLDER, exist_ok=True)

mimetypes.add_type('image/webp', '.webp')
ALLOWED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.webp'}

@app.route('/uploads', methods=['GET', 'POST'])
def handle_uploads():
    if request.method == 'POST':
        try:
            if 'file' not in request.files:
                return jsonify({'status': 'error', 'message': 'Файл не найден'}), 400
            
            file = request.files['file']
            if file.filename == '':
                return jsonify({'status': 'error', 'message': 'Файл не выбран'}), 400
            
            # Получаем расширение файла
            file_extension = os.path.splitext(secure_filename(file.filename))[1].lower()
            
            if file_extension not in ALLOWED_EXTENSIONS:
                return jsonify({'status': 'error', 'message': 'Недопустимый формат файла'}), 400
            
            # Генерируем уникальное имя файла
            filename = f"{uuid.uuid4()}{file_extension}"
            
            # Открываем изображение с помощью PIL
            image = Image.open(file)
            
            # Конвертируем в RGB если изображение в RGBA
            if image.mode == 'RGBA':
                image = image.convert('RGB')
            
            # Изменяем размер с сохранением пропорций
            image.thumbnail((300, 300))
            
            # Сохраняем обработанное изображение
            output = io.BytesIO()
            image.save(output, format=image.format or 'JPEG', quality=85, optimize=True)
            output.seek(0)
            
            # Сохраняем файл
            image_path = os.path.join(UPLOADS_FOLDER, filename)
            with open(image_path, 'wb') as f:
                f.write(output.getvalue())
            
            return jsonify({'status': 'success', 'message': 'Файл успешно загружен'})
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500
    else:
        try:
            images = []
            for filename in os.listdir(UPLOADS_FOLDER):
                if filename.lower().endswith(tuple(ALLOWED_EXTENSIONS)):
                    images.append(filename)
            random.shuffle(images)
            return jsonify({'status': 'success', 'images': images})
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/uploads/<filename>')
def get_uploaded_image(filename):
    try:
        filename = secure_filename(filename)
        file_extension = os.path.splitext(filename)[1].lower()
        if file_extension not in ALLOWED_EXTENSIONS:
            return jsonify({'status': 'error', 'message': 'Недопустимый формат файла'}), 400

        image_path = Path(UPLOADS_FOLDER) / filename
        
        try:
            image_path = image_path.resolve()
            if not str(image_path).startswith(str(Path(UPLOADS_FOLDER).resolve())):
                return jsonify({'status': 'error', 'message': 'Доступ запрещен'}), 403
        except Exception:
            return jsonify({'status': 'error', 'message': 'Недопустимый путь'}), 400

        if not image_path.is_file():
            return jsonify({'status': 'error', 'message': 'Изображение не найдено'}), 404
        
        mimetype = mimetypes.guess_type(str(image_path))[0] or 'application/octet-stream'
        return send_file(str(image_path), mimetype=mimetype)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/')
def index():
    return jsonify({
        'message': 'it works'
    })

@app.route('/images')
def get_all_images():
    try:
        images = []
        for filename in os.listdir(IMAGES_FOLDER):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
                images.append(filename)
        
        # Перемешиваем список изображений
        random.shuffle(images)
        
        return jsonify({
            'status': 'success',
            'images': images
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/images/<filename>')
def get_image(filename):
    try:
        # Очищаем имя файла от потенциально опасных символов
        filename = secure_filename(filename)
        
        # Проверяем расширение файла
        file_extension = os.path.splitext(filename)[1].lower()
        if file_extension not in ALLOWED_EXTENSIONS:
            return jsonify({
                'status': 'error',
                'message': 'Недопустимый формат файла'
            }), 400

        # Используем Path для безопасной работы с путями
        image_path = Path(IMAGES_FOLDER) / filename
        
        # Проверяем, что путь не выходит за пределы разрешенной директории
        try:
            image_path = image_path.resolve()
            if not str(image_path).startswith(str(Path(IMAGES_FOLDER).resolve())):
                return jsonify({
                    'status': 'error',
                    'message': 'Доступ запрещен'
                }), 403
        except Exception:
            return jsonify({
                'status': 'error',
                'message': 'Недопустимый путь'
            }), 400

        if not image_path.is_file():
            return jsonify({
                'status': 'error',
                'message': 'Изображение не найдено'
            }), 404
        
        mimetype = mimetypes.guess_type(str(image_path))[0]
        if not mimetype:
            mimetype = 'application/octet-stream'
            
        return send_file(str(image_path), mimetype=mimetype)
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.after_request
def add_header(response):
    if 'Cache-Control' not in response.headers:
        response.headers['Cache-Control'] = 'public, max-age=86400'
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7002, debug=True)
