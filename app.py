from flask import Flask, render_template, request, jsonify
import pyautogui
import json
import logging

app = Flask(__name__)

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)

# Загрузка сочетаний из файла
def load_combinations():
    try:
        with open("combinations.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

@app.route('/')
def index():
    combinations = load_combinations()
    grouped = { "blue": [],"green": [], "cyan": [], "purple": [], "yellow": [], "none": []}
    for combo in combinations:
        color = combo.get('color', 'none')  # По умолчанию зеленый
        grouped[color].append(combo)
    return render_template('index.html', grouped_combinations=grouped)



# Обработка нажатий кнопок
@app.route('/press', methods=['POST'])
def press_key():
    try:
        # Логируем полученные данные
        app.logger.debug(f"Received form data: {request.form}")

        # Получаем данные из формы
        key_combination = request.form.get('key')
        if not key_combination:
            return jsonify({'success': False, 'message': 'No key combination provided'}), 400

        # Логируем сочетание клавиш
        app.logger.debug(f"Key combination: {key_combination}")

        # Разделяем сочетание на отдельные клавиши
        keys = key_combination.split('+')

        # Логируем клавиши
        app.logger.debug(f"Keys: {keys}")

        # Имитируем нажатие сочетания клавиш
        pyautogui.hotkey(*keys)
        return jsonify({'success': True, 'message': f'Key pressed: {key_combination}'})
    except Exception as e:
        app.logger.error(f"Error: {str(e)}")
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)