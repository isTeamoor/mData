import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, classification_report

"""# -------------------------
# 1. Данные с пропусками (np.nan)
# -------------------------
# 10 домов, 5 признаков: [Площадь, Кол-во комнат, Этаж, Возраст дома, Расстояние до центра]
X = np.array([
    [50, 2, 1, 5, 3],
    [60, 3, 2, 10, 2],
    [80, 3, 3, 15, 5],
    [100, 4, 5, 20, 1],
    [70, 2, 4, 8, 4],
    [90, 3, 6, 12, 6],
    [120, 5, 10, 25, 2],
    [55, 2, 1, 3, 3],
    [65, 3, 2, 7, 4],
    [85, 4, 3, 18, np.nan]  # пропуск в последнем признаке
])

# Целевая переменная: цена
y = np.array([150, 180, 240, 300, 200, 260, 350, 160, 190, 280])

# -------------------------
# 2. Разделение на обучение и тест
# -------------------------
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

print("X_train shape:", X_train.shape)
print("X_test shape:", X_test.shape)

# -------------------------
# 3. Заполнение пропусков
# -------------------------
imputer = SimpleImputer(strategy='mean')  # заменяем пропуски на среднее по признаку
X_train_imputed = imputer.fit_transform(X_train)
X_test_imputed = imputer.transform(X_test)

# -------------------------
# 4. Масштабирование признаков
# -------------------------
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_imputed)
X_test_scaled = scaler.transform(X_test_imputed)

# -------------------------
# 5. Создаем модель линейной регрессии
# -------------------------
model = LinearRegression()

# -------------------------
# 6. Обучаем модель
# -------------------------
model.fit(X_train_scaled, y_train)

# -------------------------
# 7. Делаем предсказания
# -------------------------
y_pred = model.predict(X_test_scaled)

# -------------------------
# 8. Оцениваем качество модели
# -------------------------
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("\nПредсказанные цены:", y_pred)
print("Истинные цены:", y_test)
print("Mean Squared Error (MSE):", mse)
print("R² score:", r2)

# -------------------------
# 9. Предсказание для нового дома
# -------------------------
new_house = np.array([[75, 3, 4, 10, np.nan]])  # новый дом с пропуском
new_house_imputed = imputer.transform(new_house)  # заменяем пропуски на среднее
new_house_scaled = scaler.transform(new_house_imputed)
new_price = model.predict(new_house_scaled)
print("\nПредсказанная цена для нового дома:", new_price[0])"""

# 1. Загружаем данные
iris = load_iris()
X = iris.data  # признаки: длина/ширина лепестка и чашелистика
y = iris.target  # классы: 0=setosa, 1=versicolor, 2=virginica

# 2. Добавим пропуски для примера
import numpy as np
X[0, 0] = np.nan  # заменяем первый признак первого объекта на пропуск

# 3. Разделяем на обучение и тест
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# 4. Заполняем пропуски средним
imputer = SimpleImputer(strategy='mean')
X_train_imputed = imputer.fit_transform(X_train)
X_test_imputed = imputer.transform(X_test)

# 5. Масштабируем признаки
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_imputed)
X_test_scaled = scaler.transform(X_test_imputed)

# 6. Создаем классификатор
model = LogisticRegression(max_iter=200)

# 7. Обучаем модель
model.fit(X_train_scaled, y_train)

# 8. Делаем предсказания
y_pred = model.predict(X_test_scaled)

# 9. Оцениваем качество
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

print("\nПодробный отчёт по классам:")
print(classification_report(y_test, y_pred, target_names=iris.target_names))

# 10. Предсказание для нового объекта
new_flower = np.array([[5.0, 3.5, 1.4, 0.2]])  # пример нового цветка
new_flower_scaled = scaler.transform(new_flower)
predicted_class = model.predict(new_flower_scaled)
print("\nПредсказанный класс нового цветка:", iris.target_names[predicted_class[0]])