import pandas as pd
import re

# Таблица соответствий латиницы и кириллицы
latin_to_cyrillic_map = {
    'Ya': 'Я', 'ya': 'я',
    'Yu': 'Ю', 'yu': 'ю', 
    'Sh': 'Ш', 'sh': 'ш',
    'Ch': 'Ч', 'ch': 'ч',
    'O‘': 'Ў', 'o‘': 'ў',
    'G‘': 'Ғ', 'g‘': 'ғ',
    'A': 'А', 'a': 'а',
    'B': 'Б', 'b': 'б',
    'C': 'К', 'c': 'к',
    'D': 'Д', 'd': 'д',
    'E': 'Е', 'e': 'е',
    'F': 'Ф', 'f': 'ф',
    'G': 'Г', 'g': 'г',
    'H': 'Ҳ', 'h': 'ҳ',
    'I': 'И', 'i': 'и',
    'J': 'Ж', 'j': 'ж',
    'K': 'К', 'k': 'к',
    'L': 'Л', 'l': 'л',
    'M': 'М', 'm': 'м',
    'N': 'Н', 'n': 'н',
    'O': 'О', 'o': 'о',
    'P': 'П', 'p': 'п',
    'Q': 'Қ', 'q': 'қ',
    'R': 'Р', 'r': 'р',
    'S': 'С', 's': 'с',
    'T': 'Т', 't': 'т',
    'U': 'У', 'u': 'у',
    'V': 'В', 'v': 'в',
    'X': 'Х', 'x': 'х',
    'Y': 'Й', 'y': 'й',
    'Z': 'З', 'z': 'з',
    'W':'В','w':'в',
    "'": 'ʼ', 
    '‘': 'ʼ', 
    '’': 'ʼ'
}

# Функция для извлечения 'tag' из текста
def extract_tag(work):
    match = re.search(r'\b\d{3}-[A-Za-z0-9]{1,6}-[A-Za-z0-9]{1,4}\b', work)
    return match.group(0) if match else None

# Функция для перевода текста
def translate_to_cyrillic(text):
    for latin, cyrillic in latin_to_cyrillic_map.items():
        text = text.replace(latin, cyrillic)
    return text

# Функция для перевода текста, исключая теги оборудования
def translate_works_excluding_tags(works):
    # Шаблон для поиска всех тегов (например, 150-VD-010)
    tag_pattern = r'\b\d{3}-[A-Za-z0-9]{1,6}-[A-Za-z0-9]{1,4}\b'
    
    # Поиск всех тегов и замена их на уникальные маркеры
    tags = re.findall(tag_pattern, works)
    markers = {}
    for i, tag in enumerate(tags):
        marker = f'{i}'
        markers[marker] = tag
        works = works.replace(tag, marker)

    # Перевод всего текста (без маркеров)
    works_translated = translate_to_cyrillic(works)

    # Восстановление тегов на свои места
    for marker, tag in markers.items():
        works_translated = works_translated.replace(marker, tag)

    return works_translated



### 1. Импорт SRC
src_PWU = pd.read_excel('TAR.xlsx', sheet_name='PWU')
src_UNO = pd.read_excel('TAR.xlsx', sheet_name='U&O')

def process(df):
    ### 2. Форматирование
    df['works'] = df['works'].str.strip()


    ### 3. Поле "tag",
    df['tag'] = df['works'].apply(extract_tag)
    df['tag'].fillna('undefined', inplace=True)


    ### 4. Поле "unit"
    df['unit'] = df['tag'].str[1:3]



    ### 5. Перевод с латинской на кирилицу
    df['works_cyrillic'] = df['works'].str.strip().apply(translate_works_excluding_tags)



    ### 6. Создание итоговой строки
    df['formatted_field'] = "- Unit " + df['unit'] + ": " + df['works_cyrillic'] + ";"



    df = df[['unit', 'tag','works','formatted_field' ]]

    return df


process(src_PWU).to_excel('translated PWU.xlsx')
process(src_UNO).to_excel('translated UNO.xlsx')
