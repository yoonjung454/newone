"""
Snake Game
==========
파이썬 표준 라이브러리인 turtle 모듈만 사용하는 간단한 스네이크 게임입니다.
별도 라이브러리 설치 없이 바로 실행할 수 있습니다.

실행 방법:
    python snake_game.py

조작법:
    방향키 (↑ ↓ ← →) 로 이동
    스페이스바 : 일시정지 / 재개
    ESC : 종료

게임 규칙:
    - 빨간 먹이를 먹으면 점수가 오르고 뱀 길이가 늘어납니다.
    - 벽이나 자기 몸에 부딪히면 게임 오버됩니다.
    - 게임 오버 후 아무 키나 누르면 재시작됩니다.
"""

import turtle
import random
import time

# ---------------------------------------------------------------------------
# 기본 설정
# ---------------------------------------------------------------------------
WIDTH, HEIGHT = 600, 600
CELL_SIZE = 20
MOVE_DELAY = 0.10  # 초 단위, 작을수록 뱀이 빨리 움직임

BG_COLOR = "black"
SNAKE_COLOR = "lime green"
HEAD_COLOR = "green"
FOOD_COLOR = "red"
TEXT_COLOR = "white"


class SnakeGame:
    def __init__(self):
        # 화면 설정
        self.screen = turtle.Screen()
        self.screen.title("Snake Game")
        self.screen.bgcolor(BG_COLOR)
        self.screen.setup(width=WIDTH + 40, height=HEIGHT + 80)
        self.screen.tracer(0)  # 수동으로 화면 갱신 (부드러운 애니메이션)

        # 점수 표시용 펜
        self.pen = turtle.Turtle()
        self.pen.speed(0)
        self.pen.shape("square")
        self.pen.color(TEXT_COLOR)
        self.pen.penup()
        self.pen.hideturtle()
        self.pen.goto(0, HEIGHT / 2 + 20)

        self.score = 0
        self.high_score = 0
        self.paused = False
        self.running = True

        self.setup_controls()
        self.new_game()

    # -------------------------------------------------------------------
    # 초기화 / 재시작
    # -------------------------------------------------------------------
    def new_game(self):
        self.direction = "stop"
        self.next_direction = "stop"
        self.score = 0
        self.paused = False

        # 기존 세그먼트 지우기
        if hasattr(self, "segments"):
            for seg in self.segments:
                seg.hideturtle()
        if hasattr(self, "food") and self.food:
            self.food.hideturtle()

        # 머리
        self.head = turtle.Turtle()
        self.head.speed(0)
        self.head.shape("square")
        self.head.color(HEAD_COLOR)
        self.head.penup()
        self.head.goto(0, 0)

        self.segments = []

        # 먹이
        self.food = turtle.Turtle()
        self.food.speed(0)
        self.food.shape("square")
        self.food.color(FOOD_COLOR)
        self.food.penup()
        self.place_food()

        self.update_score()

    def place_food(self):
        x_range = range(-WIDTH // 2 + CELL_SIZE, WIDTH // 2, CELL_SIZE)
        y_range = range(-HEIGHT // 2 + CELL_SIZE, HEIGHT // 2, CELL_SIZE)
        while True:
            x = random.choice(list(x_range))
            y = random.choice(list(y_range))
            # 뱀 몸통과 겹치지 않도록
            if (x, y) != (self.head.xcor(), self.head.ycor()) and all(
                (x, y) != (s.xcor(), s.ycor()) for s in self.segments
            ):
                self.food.goto(x, y)
                break

    # -------------------------------------------------------------------
    # 컨트롤
    # -------------------------------------------------------------------
    def setup_controls(self):
        self.screen.listen()
        self.screen.onkeypress(lambda: self.set_direction("up"), "Up")
        self.screen.onkeypress(lambda: self.set_direction("down"), "Down")
        self.screen.onkeypress(lambda: self.set_direction("left"), "Left")
        self.screen.onkeypress(lambda: self.set_direction("right"), "Right")
        self.screen.onkeypress(self.toggle_pause, "space")
        self.screen.onkeypress(self.quit_game, "Escape")

    def set_direction(self, new_dir):
        opposite = {"up": "down", "down": "up", "left": "right", "right": "left"}
        if new_dir == opposite.get(self.direction):
            return  # 정반대 방향으로는 즉시 못 돌게 막음 (자기 자신과 충돌 방지)
        self.next_direction = new_dir

    def toggle_pause(self):
        self.paused = not self.paused

    def quit_game(self):
        self.running = False

    # -------------------------------------------------------------------
    # 점수판
    # -------------------------------------------------------------------
    def update_score(self):
        self.pen.clear()
        self.pen.write(
            f"Score: {self.score}   High Score: {self.high_score}",
            align="center",
            font=("Consolas", 16, "normal"),
        )

    def show_game_over(self):
        self.pen.goto(0, 0)
        self.pen.write(
            "GAME OVER\n아무 키나 누르면 재시작합니다",
            align="center",
            font=("Consolas", 20, "bold"),
        )
        self.pen.goto(0, HEIGHT / 2 + 20)

    # -------------------------------------------------------------------
    # 메인 루프
    # -------------------------------------------------------------------
    def move(self):
        self.direction = self.next_direction

        # 몸통 이동: 뒤 세그먼트가 앞 세그먼트 자리로 순차 이동
        for i in range(len(self.segments) - 1, 0, -1):
            x, y = self.segments[i - 1].xcor(), self.segments[i - 1].ycor()
            self.segments[i].goto(x, y)
        if self.segments:
            self.segments[0].goto(self.head.xcor(), self.head.ycor())

        # 머리 이동
        if self.direction == "up":
            self.head.sety(self.head.ycor() + CELL_SIZE)
        elif self.direction == "down":
            self.head.sety(self.head.ycor() - CELL_SIZE)
        elif self.direction == "left":
            self.head.setx(self.head.xcor() - CELL_SIZE)
        elif self.direction == "right":
            self.head.setx(self.head.xcor() + CELL_SIZE)

    def check_wall_collision(self):
        x, y = self.head.xcor(), self.head.ycor()
        return (
            x > WIDTH / 2 - CELL_SIZE / 2
            or x < -WIDTH / 2 + CELL_SIZE / 2
            or y > HEIGHT / 2 - CELL_SIZE / 2
            or y < -HEIGHT / 2 + CELL_SIZE / 2
        )

    def check_self_collision(self):
        for seg in self.segments:
            if seg.distance(self.head) < CELL_SIZE / 2:
                return True
        return False

    def check_food_collision(self):
        if self.head.distance(self.food) < CELL_SIZE:
            self.place_food()

            # 새 몸통 세그먼트 추가
            new_segment = turtle.Turtle()
            new_segment.speed(0)
            new_segment.shape("square")
            new_segment.color(SNAKE_COLOR)
            new_segment.penup()
            self.segments.append(new_segment)

            self.score += 10
            if self.score > self.high_score:
                self.high_score = self.score
            self.update_score()

    def run(self):
        while self.running:
            self.screen.update()

            if not self.paused and self.next_direction != "stop":
                self.move()

                if self.check_wall_collision() or self.check_self_collision():
                    time.sleep(1)
                    self.show_game_over()
                    self.screen.update()
                    self.wait_for_restart()
                    continue

                self.check_food_collision()

            time.sleep(MOVE_DELAY)

        turtle.bye()

    def wait_for_restart(self):
        """게임 오버 후 아무 키나 누르면 재시작."""
        self.restart_flag = False

        def trigger_restart():
            self.restart_flag = True

        for key in ("Up", "Down", "Left", "Right", "space", "Return"):
            self.screen.onkeypress(trigger_restart, key)

        while not self.restart_flag and self.running:
            self.screen.update()
            time.sleep(0.05)

        # 원래 키 바인딩 복원
        self.setup_controls()
        if self.running:
            self.new_game()


def main():
    game = SnakeGame()
    try:
        game.run()
    except turtle.Terminator:
        pass


if __name__ == "__main__":
    main()
