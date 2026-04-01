# Задание 1
Сделаем скрипт __wikipedia_articles.py__
Принимает на вход 
- --depth: максимальная глубина посика
- --url: ссылка на стартовую статью в вики
- -l: максимальное количество ссылок которые скрипт берет из статьи для дальнейшего поиска. Надо ставить поменьше, а то будет работать очень долго

запускаем так

`python wikipedia_articles.py -u https://en.wikipedia.org/wiki/Roman_Empire -d 5 -l 7`

Я не дождался конца работы этого запуска, потому что на depth 5 считает очень долго :(. Нооо я в итоге дождался!

Результат визуализировали в виде графа с помощью __draw_wiki.py__

`python draw_wiki.py -i Roman_Empire.json -o Roman_Empire_graph`

<img width="2250" height="2250" alt="image" src="https://github.com/user-attachments/assets/f0a34930-aa2a-4be9-b8ac-854e1f785aef" />


# Задание 5
Создал телеграм бота и добавил нужные штуки в .githiub/workflows. Жду PR и прикреплю скрин (ну надеюсь сообщение придет ахах)
