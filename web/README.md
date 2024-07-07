# WEB

### Эта часть кода развернута на сервере и доступна по адресу, указанному в корневом ReadMe

## Локальная установка и развертывание

1. **Установка Docker Desktop**
    - Установите Docker Desktop на ваше устройство.

2. **Клонирование директории или использование Docker Hub**

    **Клонирование репозитория с GitHub:**
    ```sh
    git clone https://github.com/afarut/RuStoreRAG.git
    cd RuStoreRAG/web
    ```

    **Или использование Docker Hub:**
    ```sh
    docker pull betmyex/rustore_chatbot-web:1.1
    ```

3. **Сборка и развертывание контейнера**

    **Если вы клонировали репозиторий с GitHub:**
    ```sh
    docker-compose build
    docker-compose up -d
    ```

    **Если вы загружали контейнер с Docker Hub:**
    ```sh
    docker run -d \
        --name flask_app \
        -p 5000:5000 \
        betmyex/rustore_chatbot-web:1.1
    ```

4. **Проверка работы**
    - Сайт теперь доступен по адресу: [http://127.0.0.1:5000](http://127.0.0.1:5000)
