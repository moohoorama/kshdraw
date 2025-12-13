import math

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
YELLOW = (255, 255, 0)

# 화면 설정
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# 게임 설정
TURTLE_SPEED = 3
PATH_TOLERANCE = 30  # 경로 이탈 허용 거리 (픽셀)
GOAL_SIZE = 30  # 골 박스 크기
MAX_LIVES = 5


def distance(p1, p2):
    """두 점 사이의 거리 계산"""
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def point_to_line_distance(point, line_start, line_end):
    """점에서 선분까지의 최단 거리 계산"""
    px, py = point
    x1, y1 = line_start
    x2, y2 = line_end

    # 선분의 길이 제곱
    line_len_sq = (x2 - x1) ** 2 + (y2 - y1) ** 2

    if line_len_sq == 0:
        # 선분이 점인 경우
        return distance(point, line_start)

    # 점을 선분에 투영했을 때의 비율 t
    t = max(0, min(1, ((px - x1) * (x2 - x1) + (py - y1) * (y2 - y1)) / line_len_sq))

    # 선분 위의 가장 가까운 점
    proj_x = x1 + t * (x2 - x1)
    proj_y = y1 + t * (y2 - y1)

    return distance(point, (proj_x, proj_y))


def point_on_path(point, path, tolerance):
    """점이 경로 위에 있는지 확인 (tolerance 이내)"""
    if len(path) < 2:
        return True

    for i in range(len(path) - 1):
        dist = point_to_line_distance(point, path[i], path[i + 1])
        if dist <= tolerance:
            return True

    return False


def has_four(number):
    """숫자에 4가 포함되어 있는지 확인"""
    return '4' in str(number)


def lerp(a, b, t):
    """선형 보간"""
    return a + (b - a) * t


def clamp(value, min_val, max_val):
    """값을 범위 내로 제한"""
    return max(min_val, min(max_val, value))
