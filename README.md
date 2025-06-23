# Доска объявлений
## Возможности:
- **Создание и просмотр объявлений**
- **Возможность оставлять отзывы к объявлениям**



### 1. Установка и настройка:
1. #### Обновление системных пакетов
   ```bash
    sudo apt update
    sudo apt upgrade
    ```
2. #### Утановка Docker и Docker Compose
   ```bash
    sudo apt update && sudo apt install -y docker.io docker-compose
    sudo systemctl enable docker
    sudo usermod -aG docker $USER && newgrp docker
    ```
3. #### Установка репозитория  
     ```bash
     git clone https://github.com/MyX007/Selling_board.git /var/www/selling_board
     ```
4. #### Настройка переменных окружения
   1. **Создайте в корневой папке проекта файл .env**
   2. **Заполните его в соответствии с образцом, находящимся в репозитории под названием .env.example**


5. #### Основные команды управления проектом
   - **Сборка и запуск**
      ```bash
      docker compose up -d --build
      ```
   - **Просмотр логов**
     ```bash
     docker compose logs
     ```
   - **Остановка**
     ```bash
     docker compose down
     ```


6. #### Примечания
   - **Миграции применяются автоматически**
   - **Локально роект запускается на локальном порту 8880**
   - **Celery и Celery Beat запускаются автоматически**
