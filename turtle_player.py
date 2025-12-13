import pygame
import math
from utils import BLACK, RED, TURTLE_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT


class TurtlePlayer:
    def __init__(self, x, y):
        self.start_x = x
        self.start_y = y
        self.x = x
        self.y = y
        self.color = BLACK
        self.trail = [(x, y)]  # 그려진 경로
        self.speed = TURTLE_SPEED
        self.size = 15  # 터틀 크기

    def move(self, dx, dy):
        """터틀 이동 (dx, dy 방향으로)"""
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed

        # 화면 경계 체크
        new_x = max(self.size, min(SCREEN_WIDTH - self.size, new_x))
        new_y = max(self.size, min(SCREEN_HEIGHT - self.size, new_y))

        self.x = new_x
        self.y = new_y
        self.trail.append((self.x, self.y))

    def move_to(self, x, y):
        """특정 위치로 직접 이동 (자동 그리기용)"""
        self.x = x
        self.y = y
        self.trail.append((self.x, self.y))

    def get_position(self):
        """현재 위치 반환"""
        return (self.x, self.y)

    def get_trail(self):
        """그려진 경로 반환"""
        return self.trail.copy()

    def reset(self, x=None, y=None):
        """위치 및 경로 초기화"""
        if x is not None:
            self.start_x = x
        if y is not None:
            self.start_y = y
        self.x = self.start_x
        self.y = self.start_y
        self.trail = [(self.x, self.y)]
        self.color = BLACK

    def set_color(self, color):
        """터틀 및 선 색상 변경"""
        self.color = color

    def draw(self, screen):
        """터틀과 경로 그리기"""
        # 경로 그리기 (선)
        if len(self.trail) >= 2:
            pygame.draw.lines(screen, self.color, False, self.trail, 3)

        # 터틀 그리기 (삼각형)
        self._draw_turtle(screen)

    def _draw_turtle(self, screen):
        """터틀 아이콘 그리기 (삼각형 모양)"""
        # 간단한 삼각형 터틀
        size = self.size
        points = [
            (self.x, self.y - size),      # 위쪽 꼭지점
            (self.x - size * 0.7, self.y + size * 0.7),  # 왼쪽 아래
            (self.x + size * 0.7, self.y + size * 0.7),  # 오른쪽 아래
        ]
        pygame.draw.polygon(screen, self.color, points)
        pygame.draw.polygon(screen, (255, 255, 255), points, 2)  # 테두리


class AutoDrawer:
    """자동 그리기를 위한 클래스 (특수 스테이지용)"""

    def __init__(self, turtle, path):
        self.turtle = turtle
        self.path = path
        self.current_index = 0
        self.progress = 0.0  # 현재 세그먼트에서의 진행도 (0~1)
        self.speed = 2  # 자동 그리기 속도
        self.finished = False

    def update(self):
        """자동 그리기 업데이트 (매 프레임 호출)"""
        if self.finished or len(self.path) < 2:
            self.finished = True
            return

        if self.current_index >= len(self.path) - 1:
            self.finished = True
            return

        # 현재 세그먼트의 시작과 끝
        start = self.path[self.current_index]
        end = self.path[self.current_index + 1]

        # 세그먼트 길이
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        segment_len = math.sqrt(dx * dx + dy * dy)

        if segment_len == 0:
            self.current_index += 1
            self.progress = 0.0
            return

        # 진행도 업데이트
        self.progress += self.speed / segment_len

        if self.progress >= 1.0:
            # 다음 세그먼트로
            self.turtle.move_to(end[0], end[1])
            self.current_index += 1
            self.progress = 0.0
        else:
            # 보간된 위치로 이동
            new_x = start[0] + dx * self.progress
            new_y = start[1] + dy * self.progress
            self.turtle.move_to(new_x, new_y)

    def is_finished(self):
        return self.finished
