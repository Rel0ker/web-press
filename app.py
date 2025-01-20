from flask import Flask, render_template, request, jsonify
import pyautogui
import json
import logging
import comtypes
from gui import set_volume, toggle_mute, get_audio_interface, set_device_volume, get_device_volume, is_muted

# Инициализация COM-объектов

comtypes.CoInitialize()  # Инициализация COM-объектов

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

# Загрузка выбранных устройств
def load_selected_devices():
    try:
        with open("selected_devices.json", "r") as file:
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
    
    # Загружаем выбранные устройства
    selected_devices = load_selected_devices()
    return render_template('index.html', grouped_combinations=grouped, selected_devices=selected_devices)

# Обработка нажатий кнопок
@app.route('/press', methods=['POST'])
def press_key():
    try:
        key_combination = request.form.get('key')
        if not key_combination:
            return jsonify({'success': False, 'message': 'No key combination provided'}), 400

        keys = key_combination.split('+')
        pyautogui.hotkey(*keys)
        return jsonify({'success': True, 'message': f'Key pressed: {key_combination}'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 400

# Управление громкостью
@app.route('/set_volume', methods=['POST'])
def set_volume_endpoint():
    volume = request.form.get('volume')
    if volume:
        set_volume(float(volume))
        return jsonify({'success': True, 'message': f'Volume set to {volume}'})
    return jsonify({'success': False, 'message': 'No volume provided'}), 400

# Включение/выключение звука
@app.route('/toggle_mute', methods=['POST'])
def toggle_mute_endpoint():
    toggle_mute()  # Переключаем состояние звука
    is_muted_state = is_muted()  # Получаем текущее состояние
    return jsonify({'success': True, 'muted': is_muted_state})
@app.route('/is_muted', methods=['GET'])
def is_muted_endpoint():
    try:
        is_muted_state = is_muted()
        return jsonify({'success': True, 'muted': is_muted_state})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 400
# Получение текущей громкости
@app.route('/get_volume', methods=['GET'])
def get_volume_endpoint():
    comtypes.CoInitialize()
    try:
        audio_interface = get_audio_interface()
        volume = audio_interface.GetMasterVolumeLevelScalar() * 100
        return jsonify({'success': True, 'volume': volume})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 400

# Управление громкостью устройства
@app.route('/set_device_volume', methods=['POST'])
def set_device_volume_endpoint():
    device_id = request.form.get('device_id')
    volume = request.form.get('volume')
    if device_id and volume:
        set_device_volume(device_id, float(volume))
        return jsonify({'success': True, 'message': f'Device volume set to {volume}'})
    return jsonify({'success': False, 'message': 'No device ID or volume provided'}), 400

# Получение текущей громкости устройства
@app.route('/get_device_volume', methods=['GET'])
def get_device_volume_endpoint():
    device_id = request.args.get('device_id')
    if device_id:
        try:
            volume = get_device_volume(device_id)
            return jsonify({'success': True, 'volume': volume})
        except Exception as e:
            return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 400
    return jsonify({'success': False, 'message': 'No device ID provided'}), 400

# Получение выбранных устройств
@app.route('/get_selected_devices', methods=['GET'])
def get_selected_devices():
    try:
        selected_devices = load_selected_devices()
        return jsonify({'success': True, 'devices': selected_devices})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)