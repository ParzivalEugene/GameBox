GameBox by Parzival
Made for YandexLyceum

Что это?

GameBox - это сборник из игр (на данной версии присутствуют: Крестики-Нолики, Тетрис), которых может дополнить каждый. GameBox создает базу данных и ведет статистику всех сыгранных вами игр, которую вы также можете редактировать под себя. Это очень гибкий лаунчер и вы буквально можете добавить в него свои модули, использовав pyqtSlot().


Какие игры есть на ванильной версии?

В GameBox присутствуют две игры:
  1.Крестики нолики:
    Известная всем игра, где нолики противостоят крестикам и наоборот. Цель игры выстроить три элемента одного типа в ряд (по диагонали, горизонтали или вертикали)

  2.Тетрис:
    Популярная игра конца 80х. Правила игры: Случайные фигурки тетрамино падают сверху в прямоугольный стакан шириной 10 и высотой 22 клетки. В полёте игрок может поворачивать         фигурку на 90° и двигать её по горизонтали. Также можно «сбрасывать» фигурку, то есть ускорять её падение, когда уже решено, куда фигурка должна упасть. Фигурка летит до тех       пор, пока не наткнётся на другую фигурку либо на дно стакана. Если при этом заполнился горизонтальный ряд из 10 клеток, он пропадает и всё, что выше него, опускается на одну       клетку. Темп игры постепенно ускоряется. Игра заканчивается, когда новая фигурка не может поместиться в стакан. Игрок получает очки за каждый заполненный ряд, поэтому его         задача — заполнять ряды, не заполняя сам стакан (по вертикали) как можно дольше, чтобы таким образом получить как можно больше очков.
    Источник: https://en.wikipedia.org/wiki/Tetris


Чем примечательна GameBox?

Помимо возможности играть в игры, GameBox предоставляет статистику всех матчей.
Исходный код написан по стандартам PEP8 (где не присутствуют атрибуты модуля PyQT) что делает его читабельным и удобным для понимания. Автор оставил комментарии для объяснения каждого шага программы.


Какие технологии были использованы при создании?

Весь проект реализован на языке python с графической оболочкой PyQT. Также были использованы модули: random - для случайной генерации тетрамино и sqlite для создания баз данных.
