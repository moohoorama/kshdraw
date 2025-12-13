import pygame
import random
import math
import os

# 한글 폰트 찾기
def get_korean_font(size=48):
    """시스템에서 한글 폰트 찾기"""
    # 현재 스크립트 위치 기준 경로
    script_dir = os.path.dirname(os.path.abspath(__file__))

    font_paths = [
        os.path.join(script_dir, "NanumGothic.ttf"),  # 스크립트 폴더 내
        "NanumGothic.ttf",  # 현재 폴더
        "/System/Library/Fonts/AppleSDGothicNeo.ttc",
        "/System/Library/Fonts/Supplemental/AppleGothic.ttf",
        "/Library/Fonts/NanumGothic.ttf",
        "/Library/Fonts/AppleGothic.ttf",
    ]

    for font_path in font_paths:
        try:
            if os.path.exists(font_path):
                return pygame.font.Font(font_path, size)
        except:
            continue

    # 폰트를 찾지 못하면 기본 폰트 반환
    return pygame.font.Font(None, size)

# 무서운 문구들 (한글)
CREEPY_MESSAGES = [
    "왜 우리를 버렸어?",
    "왜 구해주지 않은거야?",
    "우리를 믿었는데...",
    "우린 죽게 내버려뒀어",
    "들리니?",
    "우린 아직 여기 있어",
    "우리를 잊지마",
    "다 네 잘못이야",
    "절대 용서 안해",
    "도와줘... 제발...",
    "뒤에 있어",
    "나를 봐",
    "눈 돌리지마",
    "넌 도망칠 수 없어",
    "같이 놀자",
    "외로워...",
]


class SoundManager:
    """사운드 관리 클래스"""

    def __init__(self):
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        self.sounds = {}
        self._generate_sounds()

    def _generate_sounds(self):
        """프로시저럴 사운드 생성"""
        self.sounds['drone'] = self._create_drone_sound()
        self.sounds['scare'] = self._create_scare_sound()
        self.sounds['whisper'] = self._create_whisper_sound()
        self.sounds['heartbeat'] = self._create_heartbeat_sound()
        self.sounds['scream'] = self._create_scream_sound()
        self.sounds['static'] = self._create_static_sound()
        self.sounds['breathing'] = self._create_breathing_sound()
        self.sounds['footsteps'] = self._create_footsteps_sound()
        self.sounds['jumpscare'] = self._create_jumpscare_sound()
        self.sounds['enemy_near'] = self._create_enemy_near_sound()

    def _create_drone_sound(self):
        """저주파 드론 사운드"""
        sample_rate = 22050
        duration = 2.0
        samples = int(sample_rate * duration)

        sound_array = []
        for i in range(samples):
            t = i / sample_rate
            val = (math.sin(2 * math.pi * 50 * t) * 0.3 +
                   math.sin(2 * math.pi * 75 * t) * 0.2 +
                   math.sin(2 * math.pi * 100 * t) * 0.1 +
                   random.uniform(-0.1, 0.1))
            sound_array.append(int(val * 32767 * 0.3))

        return self._array_to_sound(sound_array, sample_rate)

    def _create_scare_sound(self):
        """갑작스러운 공포 사운드"""
        sample_rate = 22050
        duration = 0.5
        samples = int(sample_rate * duration)

        sound_array = []
        for i in range(samples):
            t = i / sample_rate
            envelope = max(0, 1 - t * 2)
            val = (math.sin(2 * math.pi * 200 * t) * 0.5 +
                   math.sin(2 * math.pi * 400 * t) * 0.3 +
                   random.uniform(-0.3, 0.3)) * envelope
            sound_array.append(int(val * 32767 * 0.5))

        return self._array_to_sound(sound_array, sample_rate)

    def _create_whisper_sound(self):
        """속삭이는 노이즈"""
        sample_rate = 22050
        duration = 1.5
        samples = int(sample_rate * duration)

        sound_array = []
        for i in range(samples):
            t = i / sample_rate
            val = random.uniform(-1, 1) * 0.2
            val *= (0.5 + 0.5 * math.sin(2 * math.pi * 3 * t))
            sound_array.append(int(val * 32767 * 0.3))

        return self._array_to_sound(sound_array, sample_rate)

    def _create_heartbeat_sound(self):
        """심장박동 사운드"""
        sample_rate = 22050
        duration = 1.0
        samples = int(sample_rate * duration)

        sound_array = []
        for i in range(samples):
            t = i / sample_rate
            pulse1 = math.exp(-((t - 0.1) ** 2) * 500) * math.sin(2 * math.pi * 60 * t)
            pulse2 = math.exp(-((t - 0.25) ** 2) * 500) * math.sin(2 * math.pi * 50 * t) * 0.7
            val = (pulse1 + pulse2) * 0.8
            sound_array.append(int(val * 32767 * 0.4))

        return self._array_to_sound(sound_array, sample_rate)

    def _create_scream_sound(self):
        """비명 사운드"""
        sample_rate = 22050
        duration = 0.8
        samples = int(sample_rate * duration)

        sound_array = []
        for i in range(samples):
            t = i / sample_rate
            envelope = math.exp(-t * 3)
            freq = 800 + 400 * math.sin(t * 20)
            val = math.sin(2 * math.pi * freq * t) * envelope
            val += random.uniform(-0.2, 0.2) * envelope
            sound_array.append(int(val * 32767 * 0.6))

        return self._array_to_sound(sound_array, sample_rate)

    def _create_static_sound(self):
        """TV 정적 노이즈"""
        sample_rate = 22050
        duration = 1.0
        samples = int(sample_rate * duration)

        sound_array = []
        for i in range(samples):
            val = random.uniform(-0.5, 0.5)
            sound_array.append(int(val * 32767 * 0.3))

        return self._array_to_sound(sound_array, sample_rate)

    def _create_breathing_sound(self):
        """거친 숨소리"""
        sample_rate = 22050
        duration = 2.0
        samples = int(sample_rate * duration)

        sound_array = []
        for i in range(samples):
            t = i / sample_rate
            breath = math.sin(2 * math.pi * 0.5 * t)
            noise = random.uniform(-0.3, 0.3)
            val = (breath * 0.3 + noise * abs(breath)) * 0.5
            sound_array.append(int(val * 32767 * 0.4))

        return self._array_to_sound(sound_array, sample_rate)

    def _create_footsteps_sound(self):
        """발소리"""
        sample_rate = 22050
        duration = 1.5
        samples = int(sample_rate * duration)

        sound_array = []
        step_times = [0.2, 0.6, 1.0, 1.4]
        for i in range(samples):
            t = i / sample_rate
            val = 0
            for st in step_times:
                if abs(t - st) < 0.05:
                    val += math.exp(-((t - st) ** 2) * 2000) * 0.8
            val += random.uniform(-0.05, 0.05)
            sound_array.append(int(val * 32767 * 0.5))

        return self._array_to_sound(sound_array, sample_rate)

    def _create_jumpscare_sound(self):
        """점프스케어 사운드"""
        sample_rate = 22050
        duration = 0.3
        samples = int(sample_rate * duration)

        sound_array = []
        for i in range(samples):
            t = i / sample_rate
            envelope = 1 - t / duration
            val = (math.sin(2 * math.pi * 150 * t) +
                   math.sin(2 * math.pi * 300 * t) * 0.5 +
                   math.sin(2 * math.pi * 600 * t) * 0.3 +
                   random.uniform(-0.5, 0.5)) * envelope
            sound_array.append(int(val * 32767 * 0.8))

        return self._array_to_sound(sound_array, sample_rate)

    def _create_enemy_near_sound(self):
        """적 근접 경고음"""
        sample_rate = 22050
        duration = 1.0
        samples = int(sample_rate * duration)

        sound_array = []
        for i in range(samples):
            t = i / sample_rate
            freq = 100 + 50 * math.sin(t * 10)
            val = math.sin(2 * math.pi * freq * t) * 0.4
            val += random.uniform(-0.1, 0.1)
            sound_array.append(int(val * 32767 * 0.5))

        return self._array_to_sound(sound_array, sample_rate)

    def _array_to_sound(self, array, sample_rate):
        """배열을 pygame Sound로 변환"""
        import array as arr
        stereo = []
        for val in array:
            stereo.extend([val, val])

        sound_buffer = arr.array('h', stereo)
        sound = pygame.mixer.Sound(buffer=sound_buffer)
        return sound

    def play(self, sound_name, volume=0.5):
        """사운드 재생"""
        if sound_name in self.sounds:
            self.sounds[sound_name].set_volume(volume)
            self.sounds[sound_name].play()

    def play_random_creepy(self):
        """랜덤 무서운 소리 재생"""
        sound_name = random.choice(['drone', 'scare', 'whisper', 'heartbeat',
                                    'scream', 'breathing', 'footsteps'])
        self.play(sound_name, random.uniform(0.3, 0.7))


class Enemy:
    """무서운 적 클래스"""

    def __init__(self, x, y, speed=1.5):
        self.x = x
        self.y = y
        self.speed = speed
        self.size = 40
        self.animation_timer = 0
        self.visible = True
        self.flicker_timer = 0

        # 적 타입 (다양한 모습)
        self.enemy_type = random.choice(['shadow', 'crawler', 'ghost', 'demon'])

    def update(self, target_x, target_y):
        """플레이어를 향해 이동"""
        dx = target_x - self.x
        dy = target_y - self.y
        dist = math.sqrt(dx * dx + dy * dy)

        if dist > 0:
            self.x += (dx / dist) * self.speed
            self.y += (dy / dist) * self.speed

        self.animation_timer += 1

        # 가끔 깜빡임
        if random.random() < 0.02:
            self.flicker_timer = 10
        if self.flicker_timer > 0:
            self.flicker_timer -= 1
            self.visible = self.flicker_timer % 2 == 0
        else:
            self.visible = True

    def check_collision(self, player_x, player_y, player_size=15):
        """플레이어와 충돌 체크"""
        dx = self.x - player_x
        dy = self.y - player_y
        dist = math.sqrt(dx * dx + dy * dy)
        return dist < (self.size + player_size) / 2

    def draw(self, screen):
        """적 그리기"""
        if not self.visible:
            return

        x, y = int(self.x), int(self.y)

        if self.enemy_type == 'shadow':
            self._draw_shadow(screen, x, y)
        elif self.enemy_type == 'crawler':
            self._draw_crawler(screen, x, y)
        elif self.enemy_type == 'ghost':
            self._draw_ghost(screen, x, y)
        elif self.enemy_type == 'demon':
            self._draw_demon(screen, x, y)

    def _draw_shadow(self, screen, x, y):
        """그림자 형태의 적"""
        # 불규칙한 검은 형체
        color = (20, 0, 20)

        # 메인 바디
        points = []
        for i in range(8):
            angle = 2 * math.pi * i / 8 + self.animation_timer * 0.05
            r = self.size + random.randint(-5, 10) + 5 * math.sin(self.animation_timer * 0.1 + i)
            px = x + r * math.cos(angle)
            py = y + r * math.sin(angle)
            points.append((px, py))
        pygame.draw.polygon(screen, color, points)

        # 빨간 눈
        eye_y = y - 5 + 3 * math.sin(self.animation_timer * 0.1)
        pygame.draw.circle(screen, (255, 0, 0), (x - 10, int(eye_y)), 5)
        pygame.draw.circle(screen, (255, 0, 0), (x + 10, int(eye_y)), 5)
        # 눈 하이라이트
        pygame.draw.circle(screen, (255, 255, 255), (x - 8, int(eye_y) - 2), 2)
        pygame.draw.circle(screen, (255, 255, 255), (x + 12, int(eye_y) - 2), 2)

    def _draw_crawler(self, screen, x, y):
        """기어다니는 형태의 적"""
        color = (50, 20, 20)

        # 몸통
        body_y = y + 5 * math.sin(self.animation_timer * 0.2)
        pygame.draw.ellipse(screen, color, (x - 30, body_y - 15, 60, 30))

        # 다리들 (여러개, 움직임)
        for i in range(6):
            leg_x = x - 25 + i * 10
            leg_phase = self.animation_timer * 0.3 + i * 0.5
            leg_y = y + 15 + 10 * abs(math.sin(leg_phase))
            pygame.draw.line(screen, color, (leg_x, int(body_y) + 10),
                           (leg_x, int(leg_y)), 3)

        # 머리
        pygame.draw.circle(screen, color, (x, int(body_y) - 10), 15)

        # 여러 개의 눈
        for i in range(4):
            ex = x - 10 + i * 7
            ey = body_y - 12
            pygame.draw.circle(screen, (200, 0, 0), (ex, int(ey)), 3)
            pygame.draw.circle(screen, (255, 100, 100), (ex, int(ey)), 1)

    def _draw_ghost(self, screen, x, y):
        """유령 형태의 적"""
        # 반투명 효과를 위한 서페이스
        ghost_surface = pygame.Surface((100, 120), pygame.SRCALPHA)

        # 유령 몸체
        color = (150, 150, 150, 180)
        wave = 5 * math.sin(self.animation_timer * 0.1)

        # 몸통
        pygame.draw.ellipse(ghost_surface, color, (20, 10, 60, 70))

        # 아래 물결 부분
        points = [(20, 60)]
        for i in range(7):
            px = 20 + i * 10
            py = 80 + 10 * math.sin(self.animation_timer * 0.15 + i)
            points.append((px, py))
        points.append((80, 60))
        pygame.draw.polygon(ghost_surface, color, points)

        # 검은 눈구멍
        pygame.draw.ellipse(ghost_surface, (0, 0, 0), (30, 30 + wave, 15, 20))
        pygame.draw.ellipse(ghost_surface, (0, 0, 0), (55, 30 + wave, 15, 20))

        # 입 (벌어진)
        pygame.draw.ellipse(ghost_surface, (0, 0, 0), (40, 55 + wave, 20, 15))

        screen.blit(ghost_surface, (x - 50, y - 60))

    def _draw_demon(self, screen, x, y):
        """악마 형태의 적"""
        color = (80, 0, 0)

        # 머리
        pygame.draw.circle(screen, color, (x, y), 25)

        # 뿔
        horn_wave = 3 * math.sin(self.animation_timer * 0.1)
        pygame.draw.polygon(screen, (40, 0, 0), [
            (x - 20, y - 15),
            (x - 30 + horn_wave, y - 45),
            (x - 10, y - 20)
        ])
        pygame.draw.polygon(screen, (40, 0, 0), [
            (x + 20, y - 15),
            (x + 30 - horn_wave, y - 45),
            (x + 10, y - 20)
        ])

        # 눈 (노란색, 빛남)
        glow = 155 + int(100 * abs(math.sin(self.animation_timer * 0.2)))
        pygame.draw.circle(screen, (glow, glow, 0), (x - 10, y - 5), 8)
        pygame.draw.circle(screen, (glow, glow, 0), (x + 10, y - 5), 8)
        pygame.draw.circle(screen, (0, 0, 0), (x - 10, y - 5), 4)
        pygame.draw.circle(screen, (0, 0, 0), (x + 10, y - 5), 4)

        # 이빨
        for i in range(5):
            tx = x - 12 + i * 6
            pygame.draw.polygon(screen, (200, 200, 200), [
                (tx, y + 15),
                (tx + 3, y + 25),
                (tx + 6, y + 15)
            ])

        # 그림자 효과
        shadow_surface = pygame.Surface((80, 80), pygame.SRCALPHA)
        pygame.draw.circle(shadow_surface, (0, 0, 0, 50), (40, 50), 35)
        screen.blit(shadow_surface, (x - 40, y - 20))


class GlitchEffect:
    """글리치 효과 관리 클래스"""

    def __init__(self):
        self.glitch_level = 0
        self.control_inverted_h = False
        self.control_inverted_v = False
        self.screen_shake = 0
        self.color_shift = 0
        self.flicker_timer = 0
        self.random_effects = []

        # 무서운 효과들
        self.darkness_level = 0
        self.show_skull = False
        self.skull_timer = 0
        self.skull_pos = (0, 0)
        self.skull_scale = 1.0
        self.bloody_screen = False
        self.static_noise = False
        self.creepy_text = ""
        self.creepy_text_timer = 0
        self.font = None

        # 사운드 매니저
        try:
            self.sound_manager = SoundManager()
        except:
            self.sound_manager = None

        # 적 리스트
        self.enemies = []
        self.enemy_spawn_timer = 0

    def add_glitch(self):
        """글리치 레벨 증가"""
        self.glitch_level += 1
        self._apply_random_effect()

        # 소리 재생
        if self.sound_manager:
            self.sound_manager.play_random_creepy()

    def spawn_enemy(self, screen_width, screen_height, player_x, player_y):
        """적 생성"""
        # 플레이어와 멀리서 스폰
        side = random.choice(['top', 'bottom', 'left', 'right'])
        if side == 'top':
            x = random.randint(50, screen_width - 50)
            y = -50
        elif side == 'bottom':
            x = random.randint(50, screen_width - 50)
            y = screen_height + 50
        elif side == 'left':
            x = -50
            y = random.randint(50, screen_height - 50)
        else:
            x = screen_width + 50
            y = random.randint(50, screen_height - 50)

        speed = 1.0 + self.glitch_level * 0.3
        enemy = Enemy(x, y, speed)
        self.enemies.append(enemy)

        if self.sound_manager:
            self.sound_manager.play('footsteps', 0.3)

    def update_enemies(self, player_x, player_y, screen_width, screen_height):
        """적들 업데이트"""
        if self.glitch_level == 0:
            return False

        # 적 스폰
        self.enemy_spawn_timer += 1
        spawn_interval = max(300 - self.glitch_level * 30, 120)  # 글리치 레벨에 따라 빨라짐

        if self.enemy_spawn_timer >= spawn_interval and len(self.enemies) < self.glitch_level + 1:
            self.spawn_enemy(screen_width, screen_height, player_x, player_y)
            self.enemy_spawn_timer = 0

        # 적 업데이트 및 충돌 체크
        for enemy in self.enemies:
            enemy.update(player_x, player_y)

            # 가까이 오면 경고음
            dist = math.sqrt((enemy.x - player_x)**2 + (enemy.y - player_y)**2)
            if dist < 150 and random.random() < 0.02:
                if self.sound_manager:
                    self.sound_manager.play('enemy_near', 0.3)

            if enemy.check_collision(player_x, player_y):
                if self.sound_manager:
                    self.sound_manager.play('jumpscare', 0.8)
                return True  # 충돌!

        return False

    def draw_enemies(self, screen):
        """적들 그리기"""
        for enemy in self.enemies:
            enemy.draw(screen)

    def _apply_random_effect(self):
        """랜덤한 글리치 효과 적용"""
        effects = [
            'invert_horizontal',
            'invert_vertical',
            'screen_shake',
            'darkness',
            'skull',
            'bloody',
            'static',
            'slow_controls',
            'fast_controls',
        ]

        num_effects = min(self.glitch_level + 1, 4)
        chosen = random.sample(effects, num_effects)

        for effect in chosen:
            if effect == 'invert_horizontal':
                self.control_inverted_h = not self.control_inverted_h
            elif effect == 'invert_vertical':
                self.control_inverted_v = not self.control_inverted_v
            elif effect == 'screen_shake':
                self.screen_shake = min(self.screen_shake + 5, 20)
            elif effect == 'darkness':
                self.darkness_level = min(self.darkness_level + 50, 180)
            elif effect == 'skull':
                self.show_skull = True
            elif effect == 'bloody':
                self.bloody_screen = True
            elif effect == 'static':
                self.static_noise = True
            elif effect not in self.random_effects:
                self.random_effects.append(effect)

    def apply_control_glitch(self, dx, dy):
        """조작에 글리치 적용"""
        if self.glitch_level == 0:
            return dx, dy

        new_dx, new_dy = dx, dy

        if self.control_inverted_h:
            new_dx = -dx
        if self.control_inverted_v:
            new_dy = -dy

        if 'slow_controls' in self.random_effects:
            new_dx *= 0.5
            new_dy *= 0.5
        if 'fast_controls' in self.random_effects:
            new_dx *= 1.5
            new_dy *= 1.5

        return new_dx, new_dy

    def apply_visual_glitch(self, screen):
        """화면에 시각적 글리치 적용"""
        if self.glitch_level == 0:
            return (0, 0)

        offset_x, offset_y = 0, 0
        width, height = screen.get_size()

        if self.font is None:
            self.font = get_korean_font(48)

        # 화면 흔들림
        if self.screen_shake > 0:
            offset_x = random.randint(-self.screen_shake, self.screen_shake)
            offset_y = random.randint(-self.screen_shake, self.screen_shake)

        # TV 정적 노이즈
        if self.static_noise and random.random() < 0.3:
            for _ in range(100 * self.glitch_level):
                x = random.randint(0, width - 3)
                y = random.randint(0, height - 3)
                gray = random.randint(0, 255)
                pygame.draw.rect(screen, (gray, gray, gray),
                                 (x, y, random.randint(1, 5), random.randint(1, 5)))
            if random.random() < 0.1 and self.sound_manager:
                self.sound_manager.play('static', 0.2)

        # 핏자국 효과
        if self.bloody_screen:
            self._draw_blood(screen)

        # 해골 표시
        if self.show_skull:
            self.skull_timer += 1
            if self.skull_timer % 90 < 60:
                if random.random() < 0.01:
                    self.skull_pos = (random.randint(50, width - 200),
                                      random.randint(50, height - 250))
                    self.skull_scale = random.uniform(0.8, 1.5)
                    # 5% 확률로 샌즈 (이스터에그)
                    self.is_sans = random.random() < 0.05
                    if self.sound_manager:
                        self.sound_manager.play('scare', 0.5)
                if hasattr(self, 'is_sans') and self.is_sans:
                    self._draw_sans(screen, self.skull_pos[0], self.skull_pos[1], self.skull_scale)
                else:
                    self._draw_realistic_skull(screen, self.skull_pos[0], self.skull_pos[1], self.skull_scale)

        # 화면 어둡게
        if self.darkness_level > 0:
            dark_overlay = pygame.Surface((width, height))
            dark_overlay.fill((0, 0, 0))
            dark_overlay.set_alpha(self.darkness_level)
            screen.blit(dark_overlay, (0, 0))

        # 무서운 텍스트 랜덤 표시
        if self.creepy_text_timer > 0:
            self.creepy_text_timer -= 1
            text_surface = self.font.render(self.creepy_text, True, (150, 0, 0))
            text_x = width // 2 - text_surface.get_width() // 2
            text_y = random.randint(100, height - 100)
            screen.blit(text_surface, (text_x + random.randint(-3, 3),
                                       text_y + random.randint(-3, 3)))
        elif random.random() < 0.005 * self.glitch_level:
            self.creepy_text = random.choice(CREEPY_MESSAGES)
            self.creepy_text_timer = 90
            if self.sound_manager:
                self.sound_manager.play('whisper', 0.4)

        # 깜빡임
        if random.random() < 0.02 * self.glitch_level:
            flash = pygame.Surface((width, height))
            flash.fill((255, 255, 255) if random.random() < 0.5 else (255, 0, 0))
            flash.set_alpha(random.randint(30, 100))
            screen.blit(flash, (0, 0))

        # 랜덤 소리
        if random.random() < 0.003 * self.glitch_level and self.sound_manager:
            self.sound_manager.play_random_creepy()

        return (offset_x, offset_y)

    def _draw_blood(self, screen):
        """핏자국 그리기"""
        if random.random() < 0.1:
            return

        width, height = screen.get_size()

        # 흘러내리는 핏자국
        for _ in range(3):
            x = random.randint(0, width)
            blood_color = (random.randint(100, 180), 0, 0)

            for y in range(0, random.randint(50, 200), 5):
                x += random.randint(-2, 2)
                pygame.draw.circle(screen, blood_color, (x, y), random.randint(2, 5))

        # 구석에 핏자국 얼룩
        for _ in range(2):
            bx = random.choice([random.randint(0, 100), random.randint(width - 100, width)])
            by = random.choice([random.randint(0, 100), random.randint(height - 100, height)])
            for _ in range(10):
                pygame.draw.circle(screen, (120, 0, 0),
                                   (bx + random.randint(-30, 30), by + random.randint(-30, 30)),
                                   random.randint(3, 15))

    def _draw_realistic_skull(self, screen, x, y, scale=1.0):
        """리얼한 해골 그리기"""
        s = scale

        # 해골 색상 (약간 노란 뼈 색)
        bone_color = (220, 210, 180)
        bone_shadow = (180, 170, 140)
        bone_highlight = (240, 235, 220)
        eye_socket = (20, 10, 10)

        # 두개골 메인 형태
        skull_width = int(140 * s)
        skull_height = int(180 * s)

        # 두개골 상단 (둥근 부분)
        pygame.draw.ellipse(screen, bone_color,
                           (x, y, skull_width, int(skull_height * 0.7)))

        # 하이라이트
        pygame.draw.ellipse(screen, bone_highlight,
                           (x + int(20*s), y + int(10*s), int(40*s), int(30*s)))

        # 그림자
        pygame.draw.ellipse(screen, bone_shadow,
                           (x + int(10*s), y + int(skull_height * 0.5),
                            int(skull_width - 20*s), int(40*s)))

        # 광대뼈
        cheek_y = y + int(90 * s)
        pygame.draw.ellipse(screen, bone_color,
                           (x - int(5*s), cheek_y, int(50*s), int(40*s)))
        pygame.draw.ellipse(screen, bone_color,
                           (x + skull_width - int(45*s), cheek_y, int(50*s), int(40*s)))

        # 눈구멍 (더 크고 깊게)
        eye_y = y + int(50 * s)
        left_eye_x = x + int(20 * s)
        right_eye_x = x + int(80 * s)
        eye_width = int(35 * s)
        eye_height = int(45 * s)

        # 눈구멍 그림자
        pygame.draw.ellipse(screen, (10, 5, 5),
                           (left_eye_x - 3, eye_y - 3, eye_width + 6, eye_height + 6))
        pygame.draw.ellipse(screen, (10, 5, 5),
                           (right_eye_x - 3, eye_y - 3, eye_width + 6, eye_height + 6))

        # 눈구멍
        pygame.draw.ellipse(screen, eye_socket,
                           (left_eye_x, eye_y, eye_width, eye_height))
        pygame.draw.ellipse(screen, eye_socket,
                           (right_eye_x, eye_y, eye_width, eye_height))

        # 눈 안에 빨간 빛 (깜빡임)
        if random.random() < 0.4:
            glow_intensity = random.randint(150, 255)
            pygame.draw.circle(screen, (glow_intensity, 0, 0),
                             (left_eye_x + int(eye_width/2), eye_y + int(eye_height/2)),
                             int(8*s))
            pygame.draw.circle(screen, (glow_intensity, 0, 0),
                             (right_eye_x + int(eye_width/2), eye_y + int(eye_height/2)),
                             int(8*s))
            # 글로우 효과
            glow_surface = pygame.Surface((int(30*s), int(30*s)), pygame.SRCALPHA)
            pygame.draw.circle(glow_surface, (glow_intensity, 0, 0, 100),
                             (int(15*s), int(15*s)), int(15*s))
            screen.blit(glow_surface,
                       (left_eye_x + int(eye_width/2) - int(15*s),
                        eye_y + int(eye_height/2) - int(15*s)))
            screen.blit(glow_surface,
                       (right_eye_x + int(eye_width/2) - int(15*s),
                        eye_y + int(eye_height/2) - int(15*s)))

        # 코 구멍 (하트 모양 역삼각형)
        nose_y = y + int(110 * s)
        nose_x = x + int(skull_width / 2)
        pygame.draw.polygon(screen, eye_socket, [
            (nose_x, nose_y),
            (nose_x - int(15*s), nose_y + int(25*s)),
            (nose_x + int(15*s), nose_y + int(25*s))
        ])
        # 코 구멍 내부 디테일
        pygame.draw.line(screen, bone_shadow,
                        (nose_x, nose_y + int(5*s)),
                        (nose_x, nose_y + int(20*s)), int(2*s))

        # 이빨 (위턱)
        teeth_y = y + int(145 * s)
        teeth_start_x = x + int(25 * s)
        tooth_width = int(12 * s)
        tooth_height = int(20 * s)

        for i in range(8):
            tx = teeth_start_x + i * int(tooth_width * 0.95)
            # 이빨 본체
            pygame.draw.rect(screen, bone_highlight,
                           (tx, teeth_y, tooth_width - int(2*s), tooth_height))
            # 이빨 사이 선
            pygame.draw.line(screen, bone_shadow,
                           (tx, teeth_y), (tx, teeth_y + tooth_height), 1)
            # 이빨 하단 둥글게
            pygame.draw.ellipse(screen, bone_highlight,
                              (tx, teeth_y + tooth_height - int(5*s),
                               tooth_width - int(2*s), int(10*s)))

        # 턱뼈
        jaw_y = y + int(165 * s)
        pygame.draw.ellipse(screen, bone_color,
                           (x + int(15*s), jaw_y, skull_width - int(30*s), int(25*s)))

        # 금이 간 효과 (랜덤)
        if random.random() < 0.3:
            crack_x = x + random.randint(int(30*s), int(100*s))
            crack_y = y + random.randint(int(20*s), int(60*s))
            points = [(crack_x, crack_y)]
            for _ in range(random.randint(3, 6)):
                crack_x += random.randint(-int(10*s), int(10*s))
                crack_y += random.randint(int(5*s), int(15*s))
                points.append((crack_x, crack_y))
            pygame.draw.lines(screen, (50, 40, 30), False, points, int(2*s))

    def _draw_sans(self, screen, x, y, scale=1.0):
        """샌즈 (언더테일) 그리기 - 이스터에그"""
        s = scale

        # 샌즈 특유의 둥근 해골
        skull_color = (255, 255, 255)

        # 둥근 머리
        pygame.draw.ellipse(screen, skull_color,
                           (x, y, int(120*s), int(100*s)))

        # 큰 눈구멍
        left_eye_x = x + int(20*s)
        right_eye_x = x + int(65*s)
        eye_y = y + int(25*s)
        eye_size = int(30*s)

        # 검은 눈구멍
        pygame.draw.ellipse(screen, (0, 0, 0),
                           (left_eye_x, eye_y, eye_size, eye_size))
        pygame.draw.ellipse(screen, (0, 0, 0),
                           (right_eye_x, eye_y, eye_size, eye_size))

        # 왼쪽 눈 - 파란 빛 (샌즈 특유)
        glow_timer = self.skull_timer * 0.1
        if math.sin(glow_timer) > 0:
            # 파란 눈 (샌즈 시그니처)
            pygame.draw.circle(screen, (0, 191, 255),
                             (left_eye_x + int(15*s), eye_y + int(15*s)), int(8*s))
            # 글로우 효과
            glow = pygame.Surface((int(40*s), int(40*s)), pygame.SRCALPHA)
            pygame.draw.circle(glow, (0, 191, 255, 100), (int(20*s), int(20*s)), int(20*s))
            screen.blit(glow, (left_eye_x - int(5*s), eye_y - int(5*s)))

        # 오른쪽 눈 - 흰 점
        pygame.draw.circle(screen, (255, 255, 255),
                          (right_eye_x + int(15*s), eye_y + int(15*s)), int(5*s))

        # 코 (작은 구멍)
        nose_x = x + int(55*s)
        nose_y = y + int(60*s)
        pygame.draw.ellipse(screen, (200, 200, 200),
                           (nose_x, nose_y, int(10*s), int(8*s)))

        # 입 - 샌즈 특유의 넓은 미소
        smile_y = y + int(72*s)
        pygame.draw.ellipse(screen, (0, 0, 0),
                           (x + int(25*s), smile_y, int(70*s), int(20*s)))

        # 이빨 (일렬)
        for i in range(7):
            tooth_x = x + int(30*s) + i * int(8*s)
            pygame.draw.rect(screen, skull_color,
                           (tooth_x, smile_y + int(2*s), int(7*s), int(12*s)))

        # "나쁜 시간을 보내게 될 거야" 텍스트 (가끔)
        if random.random() < 0.1:
            if self.font is None:
                self.font = get_korean_font(36)
            sans_text = self.font.render("* 나쁜 시간을 보내게 될 거야.", True, (255, 255, 255))
            screen.blit(sans_text, (x - int(50*s), y + int(110*s)))

    def get_status_text(self):
        """현재 글리치 상태 텍스트"""
        if self.glitch_level == 0:
            return ""

        effects = []
        if self.control_inverted_h:
            effects.append("???")
        if self.control_inverted_v:
            effects.append("???")
        if self.darkness_level > 0:
            effects.append("어둠")
        if self.show_skull:
            effects.append("...")
        if self.bloody_screen:
            effects.append("피")
        if len(self.enemies) > 0:
            effects.append("그들이 온다")

        return " | ".join(effects) if effects else "뭔가 이상해..."

    def reset(self):
        """글리치 효과 초기화"""
        self.glitch_level = 0
        self.control_inverted_h = False
        self.control_inverted_v = False
        self.screen_shake = 0
        self.color_shift = 0
        self.flicker_timer = 0
        self.random_effects = []
        self.darkness_level = 0
        self.show_skull = False
        self.skull_timer = 0
        self.bloody_screen = False
        self.static_noise = False
        self.creepy_text = ""
        self.creepy_text_timer = 0
        self.enemies = []
        self.enemy_spawn_timer = 0


def generate_help_path(center_x, center_y, scale=1.0):
    """무서운 문구를 그리기 위한 경로 생성"""
    message = random.choice(CREEPY_MESSAGES)

    paths = []
    letter_height = 50 * scale
    letter_width = 25 * scale
    spacing = 30 * scale

    alphabet = {
        'A': [(0, 1), (0.5, 0), (1, 1), (0.75, 0.5), (0.25, 0.5)],
        'B': [(0, 1), (0, 0), (0.8, 0), (0.8, 0.45), (0, 0.45), (0.8, 0.45), (0.8, 1), (0, 1)],
        'C': [(1, 0.2), (0.5, 0), (0, 0.3), (0, 0.7), (0.5, 1), (1, 0.8)],
        'D': [(0, 1), (0, 0), (0.7, 0), (1, 0.3), (1, 0.7), (0.7, 1), (0, 1)],
        'E': [(1, 0), (0, 0), (0, 0.5), (0.7, 0.5), (0, 0.5), (0, 1), (1, 1)],
        'F': [(1, 0), (0, 0), (0, 0.5), (0.7, 0.5), (0, 0.5), (0, 1)],
        'G': [(1, 0.2), (0.5, 0), (0, 0.3), (0, 0.7), (0.5, 1), (1, 0.8), (1, 0.5), (0.5, 0.5)],
        'H': [(0, 0), (0, 1), (0, 0.5), (1, 0.5), (1, 0), (1, 1)],
        'I': [(0.5, 0), (0.5, 1)],
        'J': [(1, 0), (1, 0.8), (0.5, 1), (0, 0.8)],
        'K': [(0, 0), (0, 1), (0, 0.5), (1, 0), (0, 0.5), (1, 1)],
        'L': [(0, 0), (0, 1), (1, 1)],
        'M': [(0, 1), (0, 0), (0.5, 0.4), (1, 0), (1, 1)],
        'N': [(0, 1), (0, 0), (1, 1), (1, 0)],
        'O': [(0.5, 0), (0, 0.3), (0, 0.7), (0.5, 1), (1, 0.7), (1, 0.3), (0.5, 0)],
        'P': [(0, 1), (0, 0), (1, 0), (1, 0.4), (0, 0.4)],
        'Q': [(0.5, 0), (0, 0.3), (0, 0.7), (0.5, 1), (1, 0.7), (1, 0.3), (0.5, 0), (0.6, 0.7), (1, 1)],
        'R': [(0, 1), (0, 0), (1, 0), (1, 0.4), (0, 0.4), (1, 1)],
        'S': [(1, 0.1), (0.5, 0), (0, 0.2), (0.5, 0.5), (1, 0.7), (0.5, 1), (0, 0.9)],
        'T': [(0, 0), (1, 0), (0.5, 0), (0.5, 1)],
        'U': [(0, 0), (0, 0.8), (0.5, 1), (1, 0.8), (1, 0)],
        'V': [(0, 0), (0.5, 1), (1, 0)],
        'W': [(0, 0), (0.25, 1), (0.5, 0.5), (0.75, 1), (1, 0)],
        'X': [(0, 0), (1, 1), (0.5, 0.5), (0, 1), (1, 0)],
        'Y': [(0, 0), (0.5, 0.5), (1, 0), (0.5, 0.5), (0.5, 1)],
        'Z': [(0, 0), (1, 0), (0, 1), (1, 1)],
        "'": [(0.5, 0), (0.5, 0.2)],
        '?': [(0.2, 0.1), (0.5, 0), (0.8, 0.1), (0.8, 0.3), (0.5, 0.5), (0.5, 0.7), (0.5, 0.9), (0.5, 1)],
        '.': [(0.5, 0.9), (0.5, 1)],
        ' ': [],
    }

    total_width = len(message) * spacing
    start_x = center_x - total_width / 2

    for i, char in enumerate(message.upper()):
        char_x = start_x + i * spacing

        if char in alphabet and alphabet[char]:
            char_path = alphabet[char]
            for j, (px, py) in enumerate(char_path):
                x = char_x + px * letter_width
                y = center_y - letter_height / 2 + py * letter_height
                paths.append((x, y))

    return paths if paths else [(center_x, center_y)]
