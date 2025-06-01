## Установка

1.  **Клонируйте репозиторий (если применимо):**
    ```bash
    git clone <your_repository_url>
    cd <your_project_directory>
    ```

2.  **Создайте и активируйте виртуальное окружение:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate  # для Windows
    # source venv/bin/activate  # для Linux/macOS
    ```

3.  **Установите зависимости:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Настройте подключение к базе данных MS SQL Server:**
    *   Убедитесь, что у вас установлен MS SQL Server и настроен ODBC драйвер.
    *   Создайте файл `.env` в корневой папке проекта и укажите переменные окружения для подключения к базе данных (см. пример ниже).

    ```
    DATABASE_NAME=YourDatabaseName
    DATABASE_USER=YourDatabaseUser
    DATABASE_PASSWORD=YourDatabasePassword
    DATABASE_HOST=YourDatabaseHost
    DATABASE_PORT=YourDatabasePort (обычно 1433)
    ```

5.  **Создайте базу данных:**
    ```bash
    python database_utils.py
    ```
    *   Этот скрипт создаст базу данных "YourDatabaseName" (или другую, указанную в `.env`) на вашем сервере MS SQL Server.

6.  **Примените миграции:**
    ```bash
    python manage.py migrate
    ```

7.  **Создайте суперпользователя:**
    ```bash
    python manage.py createsuperuser
    ```

8.  **Загрузите данные викторины (опционально):**

    Если вы хотите загрузить предустановленные данные викторины, выполните следующую команду:

    ```bash
    python manage.py load_quiz_data
    ```

    *   Убедитесь, что файл `quiz_data.json` находится в корне проекта (или измените путь в команде `load_quiz_data`, если он расположен в другом месте).

9.  **Запустите тесты:**

    Чтобы запустить все тесты в проекте, выполните следующую команду:

    ```bash
    python manage.py test tests
    ```

10. **Запустите сервер разработки:**
    ```bash
    python manage.py runserver
    ```

||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||


# API Викторина - Инструкция по тестированию

## Загрузка данных викторины

Перед тестированием API необходимо загрузить данные викторины в базу данных.

1.  Убедитесь, что файл `quiz_data.json` находится в корневой директории проекта.

2.  Запустите команду:

    ```bash
    python manage.py load_quiz_data
    ```

3.  Убедитесь, что данные загружены, проверив таблицы `QuestionCategory`, `Question` и `Answer` в Django Admin или через Django shell.

## Тестирование `check_answer` endpoint

Endpoint `/api/quiz/check_answer/` используется для проверки, является ли ответ пользователя правильным. Требуется аутентификация.

### Настройка Postman

1.  **Аутентификация:** Получите токен аутентификации для пользователя (любого аутентифицированного пользователя, не обязательно суперпользователя). Добавьте токен в заголовок `Authorization` с типом `Bearer Token`.

### Тестовые случаи

#### 1. Правильный ответ

*   **Метод:** `POST`
*   **URL:** `/api/quiz/check_answer/`
*   **Заголовок:** `Authorization: Bearer YOUR_AUTH_TOKEN`
*   **Body (raw, JSON):**

    ```json
    {
        "question_id": 1,  // Замените на ID существующего вопроса
        "answer_id": 2     // Замените на ID правильного ответа для этого вопроса
    }
    ```

*   **Ожидаемый результат:**

    *   Status Code: `200 OK`
    *   Body:

        ```json
        {
            "question_text": "Какое животное является самым крупным млекопитающим на Земле?", // текст вопроса
            "is_correct": true
        }
        ```

#### 2. Неправильный ответ

*   **Метод:** `POST`
*   **URL:** `/api/quiz/check_answer/`
*   **Заголовок:** `Authorization: Bearer YOUR_AUTH_TOKEN`
*   **Body (raw, JSON):**

    ```json
    {
        "question_id": 1,  // Замените на ID существующего вопроса
        "answer_id": 3     // Замените на ID *неправильного* ответа для этого вопроса
    }
    ```

*   **Ожидаемый результат:**

    *   Status Code: `200 OK`
    *   Body:

        ```json
        {
            "question_text": "Какое животное является самым крупным млекопитающим на Земле?", // текст вопроса
            "is_correct": false
        }
        ```

#### 3. Несуществующий вопрос

*   **Метод:** `POST`
*   **URL:** `/api/quiz/check_answer/`
*   **Заголовок:** `Authorization: Bearer YOUR_AUTH_TOKEN`
*   **Body (raw, JSON):**

    ```json
    {
        "question_id": 999,  // Несуществующий ID вопроса
        "answer_id": 1       // Любой ID ответа
    }
    ```

*   **Ожидаемый результат:**

    *   Status Code: `404 Not Found`
    *   Body:

        ```json
        {
            "error": "Вопрос не найден"
        }
        ```

#### 4. Несуществующий ответ

*   **Метод:** `POST`
*   **URL:** `/api/quiz/check_answer/`
*   **Заголовок:** `Authorization: Bearer YOUR_AUTH_TOKEN`
*   **Body (raw, JSON):**

    ```json
    {
        "question_id": 1,  // ID существующего вопроса
        "answer_id": 999    // Несуществующий ID ответа
    }
    ```

*   **Ожидаемый результат:**

    *   Status Code: `404 Not Found`
    *   Body:

        ```json
        {
            "error": "Ответ не найден"
        }
        ```

#### 5. Ответ не принадлежит вопросу

*   **Метод:** `POST`
*   **URL:** `/api/quiz/check_answer/`
*   **Заголовок:** `Authorization: Bearer YOUR_AUTH_TOKEN`
*   **Body (raw, JSON):**

    ```json
    {
        "question_id": 1,  // ID вопроса
        "answer_id": 5     // ID ответа, который *не* относится к этому вопросу
    }
    ```

*   **Ожидаемый результат:**

    *   Status Code: `400 Bad Request`
    *   Body:

        ```json
        {
            "error": "Этот ответ не принадлежит данному вопросу."
        }
        ```

#### 6. Без аутентификации

*   **Метод:** `POST`
*   **URL:** `/api/quiz/check_answer/`
*   **Body (raw, JSON):**

    ```json
    {
        "question_id": 1,
        "answer_id": 2
    }
    ```

*   **Ожидаемый результат:**

    *   Status Code: `401 Unauthorized`

## Дополнительные замечания

*   Перед тестированием убедитесь, что сервер Django запущен.
*   Замените `YOUR_AUTH_TOKEN` на фактический токен аутентификации.
*   Проверяйте логи Django для получения дополнительной информации об ошибках.
