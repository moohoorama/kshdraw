import pygame
import math
from utils import (
    SCREEN_WIDTH, SCREEN_HEIGHT, GRAY, GREEN, GOAL_SIZE,
    PATH_TOLERANCE, has_four, point_to_line_distance
)
from effects import generate_help_path


class Stage:
    """스테이지 관리 클래스"""

    def __init__(self, stage_num):
        self.stage_num = stage_num
        self.path = self._generate_path()
        self.start_pos = self.path[0] if self.path else (100, 300)
        self.goal_pos = self.path[-1] if self.path else (700, 300)

    def _generate_path(self):
        """스테이지 번호에 따른 경로 생성"""
        # 특수 스테이지는 빈 경로 반환 (자동 그리기)
        if self.is_special_stage():
            return []

        # 스테이지별 경로 데이터
        paths = self._get_stage_paths()

        if self.stage_num <= len(paths):
            return paths[self.stage_num - 1]
        else:
            # 45번 이후는 랜덤 생성
            return self._generate_random_path()

    def _get_stage_paths(self):
        """44개 스테이지의 경로 데이터"""
        cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2

        paths = [
            # Stage 1: 직선 (가로)
            [(100, 300), (700, 300)],

            # Stage 2: 직선 (세로)
            [(400, 100), (400, 500)],

            # Stage 3: L자
            [(100, 150), (100, 450), (400, 450)],

            # Stage 4: 특수 스테이지 (빈 경로)
            [],

            # Stage 5: 역 L자
            [(700, 150), (700, 450), (400, 450)],

            # Stage 6: ㄱ자
            [(100, 150), (500, 150), (500, 450)],

            # Stage 7: Z자
            [(150, 150), (650, 150), (150, 450), (650, 450)],

            # Stage 8: 사각형
            [(200, 150), (600, 150), (600, 450), (200, 450), (200, 150)],

            # Stage 9: 삼각형
            [(400, 100), (650, 450), (150, 450), (400, 100)],

            # Stage 10: 대각선
            [(100, 100), (700, 500)],

            # Stage 11: W자
            [(100, 150), (250, 450), (400, 200), (550, 450), (700, 150)],

            # Stage 12: M자
            [(100, 450), (100, 150), (400, 350), (700, 150), (700, 450)],

            # Stage 13: N자
            [(150, 450), (150, 150), (650, 450), (650, 150)],

            # Stage 14: 특수 스테이지
            [],

            # Stage 15: 번개
            [(200, 100), (400, 250), (250, 300), (500, 500)],

            # Stage 16: 계단 (상승)
            [(100, 500), (200, 500), (200, 400), (300, 400), (300, 300),
             (400, 300), (400, 200), (500, 200), (500, 100), (600, 100)],

            # Stage 17: 계단 (하강)
            [(100, 100), (200, 100), (200, 200), (300, 200), (300, 300),
             (400, 300), (400, 400), (500, 400), (500, 500), (600, 500)],

            # Stage 18: 지그재그 (수평)
            [(100, 200), (200, 400), (300, 200), (400, 400), (500, 200), (600, 400), (700, 200)],

            # Stage 19: 지그재그 (수직)
            [(200, 100), (400, 200), (200, 300), (400, 400), (200, 500)],

            # Stage 20: 오각형
            self._regular_polygon(cx, cy, 5, 180),

            # Stage 21: 육각형
            self._regular_polygon(cx, cy, 6, 150),

            # Stage 22: 팔각형
            self._regular_polygon(cx, cy, 8, 150),

            # Stage 23: 별 (5각)
            self._star(cx, cy, 5, 180, 80),

            # Stage 24: 특수 스테이지
            [],

            # Stage 25: 별 (6각)
            self._star(cx, cy, 6, 150, 70),

            # Stage 26: 나선형 (안으로)
            self._spiral(cx, cy, 200, 50, clockwise=True),

            # Stage 27: 나선형 (밖으로)
            self._spiral(cx, cy, 50, 200, clockwise=False),

            # Stage 28: 하트
            self._heart(cx, cy, 2.5),

            # Stage 29: 물결
            self._wave(100, 300, 600, 4, 100),

            # Stage 30: 이중 사각형
            [(200, 150), (600, 150), (600, 450), (200, 450), (200, 150),
             (300, 220), (500, 220), (500, 380), (300, 380), (300, 220)],

            # Stage 31: 십자가
            [(400, 100), (400, 250), (250, 250), (250, 350), (400, 350),
             (400, 500), (500, 500), (500, 350), (650, 350), (650, 250),
             (500, 250), (500, 100), (400, 100)],

            # Stage 32: 화살표
            [(100, 300), (500, 300), (500, 200), (700, 300), (500, 400), (500, 300)],

            # Stage 33: 집 모양
            [(200, 450), (200, 250), (400, 100), (600, 250), (600, 450),
             (200, 450), (200, 250), (600, 250)],

            # Stage 34: 특수 스테이지
            [],

            # Stage 35: 미로 1
            [(100, 100), (100, 500), (300, 500), (300, 200), (200, 200),
             (200, 400), (400, 400), (400, 100), (600, 100), (600, 500), (700, 500)],

            # Stage 36: 미로 2
            [(100, 300), (200, 300), (200, 100), (400, 100), (400, 300),
             (300, 300), (300, 500), (500, 500), (500, 200), (700, 200)],

            # Stage 37: 복잡한 지그재그
            [(100, 150)] + [(100 + i * 60, 150 if i % 2 == 0 else 450) for i in range(11)],

            # Stage 38: 8자
            self._figure_eight(cx, cy, 120),

            # Stage 39: 무한대
            self._infinity(cx, cy, 150),

            # Stage 40: 톱니바퀴
            self._gear(cx, cy, 180, 120, 12),

            # Stage 41: 다이아몬드
            [(400, 80), (650, 300), (400, 520), (150, 300), (400, 80)],

            # Stage 42: 나비 모양
            [(400, 300), (200, 100), (200, 500), (400, 300),
             (600, 500), (600, 100), (400, 300)],

            # Stage 43: 복잡한 별
            self._star(cx, cy, 8, 200, 100),

            # Stage 44: 특수 스테이지
            [],
        ]

        return paths

    def _regular_polygon(self, cx, cy, sides, radius):
        """정다각형 경로 생성"""
        points = []
        for i in range(sides + 1):
            angle = 2 * math.pi * i / sides - math.pi / 2
            x = cx + radius * math.cos(angle)
            y = cy + radius * math.sin(angle)
            points.append((x, y))
        return points

    def _star(self, cx, cy, points, outer_r, inner_r):
        """별 모양 경로 생성"""
        path = []
        for i in range(points * 2 + 1):
            angle = math.pi * i / points - math.pi / 2
            r = outer_r if i % 2 == 0 else inner_r
            x = cx + r * math.cos(angle)
            y = cy + r * math.sin(angle)
            path.append((x, y))
        return path

    def _spiral(self, cx, cy, start_r, end_r, clockwise=True):
        """나선형 경로 생성"""
        path = []
        steps = 40
        for i in range(steps + 1):
            t = i / steps
            r = start_r + (end_r - start_r) * t
            angle = 4 * math.pi * t * (1 if clockwise else -1) - math.pi / 2
            x = cx + r * math.cos(angle)
            y = cy + r * math.sin(angle)
            path.append((x, y))
        return path

    def _heart(self, cx, cy, scale):
        """하트 모양 경로 생성"""
        path = []
        for i in range(50):
            t = 2 * math.pi * i / 49
            x = cx + scale * 16 * math.sin(t) ** 3
            y = cy - scale * (13 * math.cos(t) - 5 * math.cos(2 * t)
                              - 2 * math.cos(3 * t) - math.cos(4 * t))
            path.append((x, y))
        path.append(path[0])
        return path

    def _wave(self, start_x, center_y, width, periods, amplitude):
        """물결 모양 경로 생성"""
        path = []
        steps = 40
        for i in range(steps + 1):
            t = i / steps
            x = start_x + width * t
            y = center_y + amplitude * math.sin(2 * math.pi * periods * t)
            path.append((x, y))
        return path

    def _figure_eight(self, cx, cy, size):
        """8자 모양 경로 생성"""
        path = []
        for i in range(50):
            t = 2 * math.pi * i / 49
            x = cx + size * math.sin(t)
            y = cy + size * math.sin(t) * math.cos(t)
            path.append((x, y))
        path.append(path[0])
        return path

    def _infinity(self, cx, cy, size):
        """무한대 모양 경로 생성"""
        path = []
        for i in range(50):
            t = 2 * math.pi * i / 49
            scale = 2 / (3 - math.cos(2 * t))
            x = cx + size * scale * math.cos(t)
            y = cy + size * scale * math.sin(2 * t) / 2
            path.append((x, y))
        path.append(path[0])
        return path

    def _gear(self, cx, cy, outer_r, inner_r, teeth):
        """톱니바퀴 모양 경로 생성"""
        path = []
        for i in range(teeth * 4 + 1):
            angle = 2 * math.pi * i / (teeth * 4) - math.pi / 2
            if (i // 2) % 2 == 0:
                r = outer_r
            else:
                r = inner_r
            x = cx + r * math.cos(angle)
            y = cy + r * math.sin(angle)
            path.append((x, y))
        return path

    def _generate_random_path(self):
        """랜덤 경로 생성 (45번 이후 스테이지)"""
        import random
        random.seed(self.stage_num)  # 일관된 랜덤

        path = [(100, 300)]
        for _ in range(random.randint(5, 10)):
            x = random.randint(100, 700)
            y = random.randint(100, 500)
            path.append((x, y))

        return path

    def is_special_stage(self):
        """4가 포함된 특수 스테이지인지 확인"""
        return has_four(self.stage_num)

    def get_path(self):
        """경로 반환"""
        return self.path

    def get_start_pos(self):
        """시작 위치 반환"""
        return self.start_pos

    def get_goal_pos(self):
        """골 위치 반환"""
        return self.goal_pos

    def check_on_path(self, pos):
        """주어진 위치가 경로 위에 있는지 확인"""
        if len(self.path) < 2:
            return True

        for i in range(len(self.path) - 1):
            dist = point_to_line_distance(pos, self.path[i], self.path[i + 1])
            if dist <= PATH_TOLERANCE:
                return True
        return False

    def check_goal_reached(self, pos):
        """골에 도달했는지 확인"""
        if not self.goal_pos:
            return False

        dx = pos[0] - self.goal_pos[0]
        dy = pos[1] - self.goal_pos[1]
        return (dx * dx + dy * dy) <= (GOAL_SIZE * GOAL_SIZE)

    def draw(self, screen):
        """스테이지 경로 그리기 (점선)"""
        if len(self.path) < 2:
            return

        # 점선 그리기
        for i in range(len(self.path) - 1):
            self._draw_dashed_line(screen, self.path[i], self.path[i + 1], GRAY, 3, 10)

        # 골 박스 그리기
        if self.goal_pos:
            goal_rect = pygame.Rect(
                self.goal_pos[0] - GOAL_SIZE // 2,
                self.goal_pos[1] - GOAL_SIZE // 2,
                GOAL_SIZE, GOAL_SIZE
            )
            pygame.draw.rect(screen, GREEN, goal_rect)
            pygame.draw.rect(screen, (0, 200, 0), goal_rect, 3)

        # 시작점 표시
        if self.start_pos:
            pygame.draw.circle(screen, (100, 100, 255), (int(self.start_pos[0]), int(self.start_pos[1])), 10)

    def _draw_dashed_line(self, screen, start, end, color, width, dash_length):
        """점선 그리기"""
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        distance = math.sqrt(dx * dx + dy * dy)

        if distance == 0:
            return

        dashes = int(distance / dash_length)
        if dashes == 0:
            dashes = 1

        for i in range(0, dashes, 2):
            t1 = i / dashes
            t2 = min((i + 1) / dashes, 1.0)
            p1 = (start[0] + dx * t1, start[1] + dy * t1)
            p2 = (start[0] + dx * t2, start[1] + dy * t2)
            pygame.draw.line(screen, color, p1, p2, width)
