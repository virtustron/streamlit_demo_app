# Example origin:
# https://habr.com/ru/post/664076/

# Source code:
# https://github.com/sozykin/streamlit_demo_app

# to run use ".\" before filename: 
# streamlit run .\recognize_app.py

import io
import streamlit as st
from PIL import Image
import numpy as np
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.efficientnet import preprocess_input, decode_predictions
import keras


def load_image():
    """Создание формы для загрузки изображения"""
    # Форма для загрузки изображения средствами Streamlit
    uploaded_file = st.file_uploader(
        label='Выберите изображение для распознавания')
    if uploaded_file is not None:
        # Получение загруженного изображения
        image_data = uploaded_file.getvalue()
        # Показ загруженного изображения на Web-странице средствами Streamlit
        st.image(image_data)
        # Возврат изображения в формате PIL
        return Image.open(io.BytesIO(image_data))
    else:
        return None

# загружает нейронную сеть
def load_model():
    #model = EfficientNetB0(weights='imagenet')
    model = keras.models.load_model('ml_model.pkl')
    return model

# выполняет предварительную обработку изображения для подготовки к распознаванию
def preprocess_image(img):
    img = img.resize((224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    return x

# печатает названия и вероятность для ТОП 3 классов, выданных моделью
def print_predictions(preds):
    classes = decode_predictions(preds, top=3)[0]
    for cl in classes:
        st.write(cl[1], cl[2])


###########################################################################

# Загружаем предварительно обученную модель
model = load_model()

# Выводим заголовок страницы
st.title('Классификация изображений')

# Выводим форму загрузки изображения и получаем изображение
img = load_image()

# Показывам кнопку для запуска распознавания изображения
result = st.button('Распознать изображение')

# Если кнопка нажата, то запускаем распознавание изображения
if result:
    # Предварительная обработка изображения
    x = preprocess_image(img)

    # Распознавание изображения
    preds = model.predict(x)

    # Выводим заголовок результатов распознавания жирным шрифтом
    # используя форматирование Markdown
    st.write('**Результаты распознавания:**')

    # Выводим результаты распознавания
    print_predictions(preds)
