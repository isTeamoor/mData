import pandas as pd
import re


main = pd.read_excel('AS.xlsx', sheet_name='main')
info = pd.read_excel('AS.xlsx', sheet_name='info')



### 1. В info оставляем только casing
info = info.loc[info['Part Name'].str.contains('casing', case=False, na=False)]
info.reset_index(drop=True, inplace=True)


### 2. Функция для нахождения индексов совпадающих строк
all_matched = []
def find_matches(tag, part_names):
    matches = [str(i) for i,name in enumerate(part_names) if re.search(rf'\b{tag}\b', name)]
    all_matched.extend(matches)
    return ', '.join(matches)

main['matches'] = main['Equipment Tag Number'].apply(lambda tag: find_matches(tag, info['Part Name']))


### 3. Список индексов строк из info, в которых были найдены тэги
used_indexes = []
for index in all_matched:
    used_indexes.append(int(index))


### 4. Поиск строк из info, в которых не были найдены тэги
unused_info = info.copy().loc[~info.index.isin(used_indexes)]
unused_main = main.copy().loc[ main['matches']=='' ]

unused_info.to_excel('unused_info.xlsx')
unused_main.to_excel('unused_main.xlsx')


# Разделим значения в столбце 'matches' на отдельные индексы
main_expanded = []
for idx, row in main.iterrows():
    # Получаем индексы из поля 'matches'
    matches = row['matches'].split(', ') if row['matches'] else []
    
    for match in matches:
        # Получаем строку из info по индексу
        info_row = info.loc[int(match)].to_dict()  # Преобразуем строку в словарь
        # Создаем новую строку, которая будет содержать данные из main и из info
        new_row = row.to_dict()
        new_row.update(info_row)  # Добавляем данные из info в строку main
        main_expanded.append(new_row)

# Создаем итоговый DataFrame
final_df = pd.DataFrame(main_expanded)

# Если нужно, сохраняем итоговый DataFrame в новый файл
final_df.to_excel('final_output.xlsx', index=False)
