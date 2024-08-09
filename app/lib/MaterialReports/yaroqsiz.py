import pdfplumber
import pandas as pd
import os


def extract_data(pdf_path, filename):

    ### 1. Получение из pdf файла таблицы и номера документа (1-я строчка сверху)
    with pdfplumber.open(pdf_path) as pdf:

        ### 1.1. Извлечение заголовка для получения номера документа ('ORD')
        page = pdf.pages[0]
        text = page.extract_text()
        docNumber = text[ 0 : text.find('\n') ].split(':')[-1]


        ### 1.2. Извлечение таблицы из каждой страницы и добавление в список для дальнейшего объединения
        all_tables = []
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                all_tables.append( pd.DataFrame(table, columns=['№','Материал (из акта)','Код товара', 'Количество (из акта)', 'Ед.изм', 'Примечание']) )
    


    ### 2. Объединение dataFrames (таблиц из pdf) и добавление номера документа
    df = pd.concat(all_tables, ignore_index=True)
    df['Номер документа'] = docNumber
    df['Номер файла'] = filename


    ### 3. Форматирование данных
    df = df.loc[ df['№'] != "№" ]
    df['Материал (из акта)'] = df['Материал (из акта)'].apply(lambda x: x.replace('\n', ' ').replace('/n', ' '))
    df['Код товара'].fillna('undefined', inplace=True)
    df['Код товара'] = df['Код товара'].map(lambda x: x.strip()) # удаление пробелов и табуляции
    df['Количество (из акта)'] = pd.to_numeric(df['Количество (из акта)'], errors='coerce')
    df['Количество (из акта)'].fillna(0, inplace=True)

    df['На уничтожение'] = ""
    df['В повторное использование'] = ""
    df['На металл'] = ""
    df['Алюминий, кг'] = 0
    df['Нержавейка, кг'] = 0
    df['Черный металл, кг'] = 0
    df['Драг. металл, кг'] = 0

    return df[['№','Номер файла','Номер документа','Код товара','Материал (из акта)','Количество (из акта)',
               'На уничтожение','В повторное использование','На металл','Алюминий, кг','Нержавейка, кг','Черный металл, кг','Драг. металл, кг']]

def custom_exceptions(inputDF):
    df = inputDF.copy()

    df.loc[ df['Номер документа'] == 'ORD-048/713-2024',  'Код товара' ] = 'WIM0052598' #50

    return df

def execute(transacts):
    ### 1. Получает из директории список всех файлов
    directory_path = 'acts/'
    files = []
    for file in os.listdir(directory_path):
        if os.path.isfile(os.path.join(directory_path, file)):
            files.append(file)


    ### 2. Собирает в dataframe все файлы из директории
    tables = []
    for file in files:
        tables.append( extract_data( f'{directory_path}{file}', file ) )
    
    result = pd.concat(tables, ignore_index=True)
  


    ### 3. Если указан складской код вместо бухгалтерского
    transactions = transacts[['Catalogue Number', 'Код товара']] 

    result = custom_exceptions(result)

    result['Код товара'] = result['Код товара'].apply(lambda x: ( transactions.loc[ transactions['Catalogue Number']==x, 'Код товара' ].unique() )[0]     if x in  transactions['Catalogue Number'].unique() else x)
    result['Код товара'] = result['Код товара'].map(lambda x: '0000'+ x if len(x)==1 else '000'+ x if len(x)==2 else '00'+ x if len(x)==3 else '0' + x if len(x)==4 else x[-5:] )



    ### 4. Готовый dataFrame
    result.to_excel('yaroqsiz_aktlar.xlsx', index=False)
    return result