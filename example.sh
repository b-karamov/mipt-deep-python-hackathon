#!/usr/bin/env bash
set -euo pipefail

API_ROOT="http://localhost:8000"

echo "Создаём пользователей..."
curl -L -X POST "$API_ROOT/users/" -H "Content-Type: application/json" -d '{"username":"ivan"}'
curl -L -X POST "$API_ROOT/users/" -H "Content-Type: application/json" -d '{"username":"maria"}'
curl -L -X POST "$API_ROOT/users/" -H "Content-Type: application/json" -d '{"username":"sergey"}'
curl -L -X POST "$API_ROOT/users/" -H "Content-Type: application/json" -d '{"username":"olga"}'
curl -L -X POST "$API_ROOT/users/" -H "Content-Type: application/json" -d '{"username":"dmitry"}'
echo

echo "Создаём посты..."
curl -L -X POST "$API_ROOT/posts?username=ivan"   -H "Content-Type: application/json" -d '{"title":"Привет, мир","content":"Запустил проект, тестирую API."}'
curl -L -X POST "$API_ROOT/posts?username=maria"  -H "Content-Type: application/json" -d '{"title":"Доброе утро","content":"Хочу выпить кофе."}'
curl -L -X POST "$API_ROOT/posts?username=sergey" -H "Content-Type: application/json" -d '{"title":"Обеденная пауза","content":"Вышел на улицу, солнце жарит."}'
echo

echo "Добавляем комментарии к постам..."
curl -L -X POST "$API_ROOT/comments/post/1?username=sergey" -H "Content-Type: application/json" -d '{"text":"Вижу, проект ожил! Круто."}'
curl -L -X POST "$API_ROOT/comments/post/1?username=olga"   -H "Content-Type: application/json" -d '{"text":"Жду первые фичи :)" }'
curl -L -X POST "$API_ROOT/comments/post/2?username=ivan"   -H "Content-Type: application/json" -d '{"text":"Уже сделал второй стакан."}'
curl -L -X POST "$API_ROOT/comments/post/3?username=maria"  -H "Content-Type: application/json" -d '{"text":"Солнечно у вас, завидую!"}'
echo

echo "Отвечаем на комментарии..."
curl -L -X POST "$API_ROOT/comments/1/reply?username=ivan"   -H "Content-Type: application/json" -d '{"text":"Спасибо, впереди ещё много работы!"}'
curl -L -X POST "$API_ROOT/comments/2/reply?username=dmitry" -H "Content-Type: application/json" -d '{"text":"Фичи в пути, stay tuned!"}'
echo
