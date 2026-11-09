import json
import os

# Загрузка настроек пути к файлу
with open("data/config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

FILENAME = config["database_bike_path"]

# Загрузка базы данных велосипедов
if os.path.exists(FILENAME):
    with open(FILENAME, "r", encoding="utf-8") as f:
        bikes = json.load(f)
else:
    bikes = {}

while True:
    print("\n--- ГЛАВНОЕ МЕНЮ ---")
    print("1. Добавить новый велосипед")
    print("2. Посмотреть каталог с фильтрами")
    print("0. Выйти из программы")
    
    choice = input("Выберите пункт меню: ")
    
    # Добавление нового велосипеда
    if choice == "1":
        bike_id = input("Введите номер велосипеда: ")
        name = input("Введите название (модель): ")
        
        print("Выберите тип велосипеда:")
        print("1. Горный")
        print("2. Детский")
        print("3. Городской")
        type_choice = input("Введите номер типа (или свой вариант текстом): ")
        
        if type_choice == "1":
            bike_type = "горный"
        elif type_choice == "2":
            bike_type = "детский"
        elif type_choice == "3":
            bike_type = "городской"
        else:
            bike_type = type_choice.lower()
            
        price_str = input("Введите цену за сутки: ")
        
        # Проверка на пустые поля
        if bike_id == "" or name == "" or bike_type == "" or price_str == "":
            print("Ошибка: нельзя оставлять поля пустыми!")
            continue
            
        # Проверка уникальности номера
        if bike_id in bikes:
            print("Ошибка: велосипед с таким номером уже есть!")
            continue
            
        price = int(price_str)
        if price <= 0:
            print("Ошибка: цена должна быть больше нуля!")
            continue
            
        # Запись велосипеда в общую базу
        bikes[bike_id] = {
            "name": name,
            "type": bike_type,
            "price": price,
            "status": "доступен"
        }
        
        with open(FILENAME, "w", encoding="utf-8") as f:
            json.dump(bikes, f, ensure_ascii=False, indent=4)
            
        print("Велосипед успешно добавлен и сохранен!")
        
    # Просмотр каталога с фильтрацией
    elif choice == "2":
        print("\n--- НАСТРОЙКА ФИЛЬТРОВ (нажмите Enter, чтобы пропустить) ---")
        filter_name = input("Искать по названию: ")
        filter_type = input("Искать по типу (горный / детский / городской): ")
        filter_status = input("Статус (все / доступен / занят): ")
        filter_price_str = input("Максимальная цена: ")
        
        filtered_list = []
        
        # Фильтрация всех велосипедов из базы
        for b_id in bikes:
            info = bikes[b_id]
            
            if filter_name != "" and filter_name.lower() not in info["name"].lower():
                continue
                
            if filter_type != "" and filter_type.lower() not in info["type"].lower():
                continue
                
            if filter_status == "доступен" and info["status"] != "доступен":
                continue
            if filter_status == "занят" and info["status"] != "занят":
                continue
                
            if filter_price_str != "":
                max_price = int(filter_price_str)
                if info["price"] > max_price:
                    continue
            
            # Сбор данных для сортировки в формате: [цена, id, название, тип, статус]
            filtered_list.append([info["price"], int(b_id), info["name"], info["type"], info["status"]])
            
        # Автоматическая сортировка списка (сначала по цене, затем по ID)
        filtered_list.sort()
        
        # Вывод результатов на экран
        if len(filtered_list) == 0:
            print("Ничего не найдено по таким фильтрам.")
        else:
            print("\n--- РЕЗУЛЬТАТЫ ПОИСКА ---")
            for bike in filtered_list:
                print(f"ID: {bike[1]} | Тип: {bike[3]} | Название: {bike[2]} | Цена: {bike[0]} руб. | Статус: {bike[4]}")
                
    # Выход из программы
    elif choice == "0":
        print("Программа завершена. До свидания!")
        break
        
    else:
        print("Неверный ввод! Напишите 1, 2 или 0.")