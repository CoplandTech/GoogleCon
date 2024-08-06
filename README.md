# Импорт контактов из сервиса [GOOGLE CONTACTS](https://contacts.google.com/)

Этот проект предназначен для импорта из сервиса [GOOGLE CONTACTS](https://contacts.google.com/) и создания телефонной книги в форматах .XML и .JSON

## Оглавление

- [Описание](#описание)
- [Требования](#требования)
- [Установка](#установка)
- [Использование](#использование)

## Описание

Проект состоит из следующих основных компонентов:

1. **Чтение контактов**: Чтение контактов из [GOOGLE CONTACTS](https://contacts.google.com/)
2. **Генерация .xml файла**: Сохранение данных в XML файл в соответствии со структурой телефонных кних YEALINK.
3. **Генерация .json файла**: Сделано для внутренних нужд.
4. **Поднятие FLASK для HTTP(S) GET**: Получение ФИО контакта с помощью HTTP(S) GET по номеру телефона. Требуется для интеграции телефонной книги и телефонии FreePBX
   
## Требования

- Разработка и тестирование проводилось только на Python 3.10
- Библиотеки: Указаны в файле [requirements.txt](https://github.com/CoplandTech/GoogleCon/blob/main/requirements.txt)
- Файл [Credentials.json](https://console.cloud.google.com/apis/credentials). В моём случае подошло получение файла с типом "Web application".

## Установка

1. Получите файл [credentials.json](https://console.cloud.google.com/apis/credentials) и замените содержимое файла [credentials.json](https://github.com/CoplandTech/GoogleCon/blob/main/bot/auth/credentials.json).
В моём случае подошло получение файла с типом "Web application".

2. Клонируйте/скачайте репозиторий:

    ```sh
    git clone https://github.com/CoplandTech/GoogleCon.git
    ```

3. (ОПЦИОНАЛЬНО) Воспользуйтесь [небольшой инструкцией](https://github.com/CoplandTech/python_bots_service) для установки ботов в качестве сервиса. [Инструкция](https://github.com/CoplandTech/python_bots_service) так же будет полезна для установки нескольких ботов на одной машине. 

4. Установите необходимые зависимости и запустите скрипт:
    ```sh
    pip install -r requirements.txt
    ```
    ```sh
    python3 main.py
    ```

5. После запуска скрипта, вас попросят перейти по ссылке для подтверждения прав доступа к аккаунту. Файл **token.json** перезапишется самостоятельно.
   
## Использование

Из главных примечаний для корректной работы скрипта и формирования [contacts.xml](https://github.com/CoplandTech/GoogleCon/blob/main/contacts.xml) в требуемом формате, нужно заполнять:
| Поле в GOOGLE  | Значение в XML |
| ------------- | ------------- |
| Имя | Unit - Name |
| Среднее имя | Unit - Middle |
| Фамилия | Unit - Name |
| Должность | Unit - JobTitle |
| Отдел | Menu - Name |
| Эл. почта | Unit - Email |
| Телефон с ярлыком "Короткий" | Unit - Phone1 |
| Телефон с ярлыком "Корпоративный" | Unit - Phone2 |
| - | Unit - Phone3 |
| - | Unit - default_photo |

В файл XML попадают только те контакты которые соответствуют ярлыку. Поэтому контакты требуется помещать в специальный ЯРЛЫК в GOOGLE.
ID Ярлыка можно получуть в URL при сортировке контактов по URL например "https://contacts.google.com/u/0/label/356e7c498b8c85b3" - после /label/ идёт ID ярлыка.
ID требуется вписать в файле [Google_api.py](https://github.com/CoplandTech/GoogleCon/blob/main/bot/google_api.py)
```python
for contact in all_contacts:
  memberships = contact.get("memberships", [])
  group_ids = [membership.get("contactGroupMembership", {}).get("contactGroupId") for membership in memberships]
  if "4742592e8b960a62" in group_ids:  # ID ГРУППЫ из GOOGLE CONTACT
    xml_book_contacts.append(contact)
  if "f1351030eedda16" in group_ids: # ID ГРУППЫ из GOOGLE CONTACT
    https_book_contacts.append(contact)
  if not any(group_id in ["4742592e8b960a62", "f1351030eedda16"] for group_id in group_ids): # ID ГРУПП из GOOGLE CONTACT
    other_contacts.append(contact)
```

