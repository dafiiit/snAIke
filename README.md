# snAIke Idee
Die Idee wäre es hier erst ein Snake Spiel zu programmieren, dann die Inputs und outputs richtig ausgeben zu lassen, und abschließend damit eine KI zu trainieren. Dabei will ich erstmal mit dem einfachst möglichen Szenario anfangen(Python und kleine KI) und dann kompliziertere Konzepte ausprobieren (limitierte Wahrnehmung), Weltsimulation seperieren und dabei Vorhersage mit einbinden. 
# ToDo 1
- Klassendiagram_01 erstellen
- Spiel programmieren
- Inputfunktion und Outputfunktion global machen
    - mit 2. dokument testen
- Videos und Papers zu Reinforcement learning schauen
- KI_01 programmieren
- KI_01 trainieren
- KI_01 testen
# Klassendiagram_01
```mermaid
classDiagram
    class SnakeGame{
        - int width
        - int height
        - int delay
        - int cell_size
        + game_loop(): void
        + move_snake(): void
        + check_collision(): void
        + update_score(): void
        + draw(): void
        + create_food(): void
        + on_key_press(): void
        + play_again(): void
        + run(): void                        
    }
```
# Ablauf
move_snake() --> check_collision() --> update_score() --> draw()
## Änderungen
move_snake(vektor) --> check_collision() --> update_score() --> draw() --> return_score() --> return_matrix() -->inference(matrix) --> repeat
### move_snake()
Muss mithilfe von einem 3x1 Vektor bedienbar werden.
### return_score()
Soll den aktuellen Score ausgeben.
### return_matrix
Soll das Spielfeld als Matrix ausgeben.
