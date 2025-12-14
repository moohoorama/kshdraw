import pygame
import sys
import random
import math
import asyncio
import platform
from utils import (
    WHITE, BLACK, RED, GREEN, GRAY,
    SCREEN_WIDTH, SCREEN_HEIGHT, MAX_LIVES, has_four
)
from turtle_player import TurtlePlayer, AutoDrawer
from stage import Stage
from effects import GlitchEffect, generate_help_path


class VirtualDPad:
    """Virtual D-Pad for touch controls"""

    def __init__(self, x, y, size=120):
        self.x = x
        self.y = y
        self.size = size
        self.button_size = size // 3
        self.pressed = {'up': False, 'down': False, 'left': False, 'right': False}
        self.alpha = 150

    def get_button_rects(self):
        """Get rectangles for each button"""
        bs = self.button_size
        return {
            'up': pygame.Rect(self.x + bs, self.y, bs, bs),
            'down': pygame.Rect(self.x + bs, self.y + bs * 2, bs, bs),
            'left': pygame.Rect(self.x, self.y + bs, bs, bs),
            'right': pygame.Rect(self.x + bs * 2, self.y + bs, bs, bs),
            'center': pygame.Rect(self.x + bs, self.y + bs, bs, bs)
        }

    def handle_touch(self, pos, is_down):
        """Handle touch event"""
        rects = self.get_button_rects()
        for direction, rect in rects.items():
            if direction != 'center' and rect.collidepoint(pos):
                self.pressed[direction] = is_down
                return True
        return False

    def handle_touch_move(self, pos):
        """Handle touch move - update all buttons based on position"""
        rects = self.get_button_rects()
        for direction in ['up', 'down', 'left', 'right']:
            self.pressed[direction] = rects[direction].collidepoint(pos)

    def release_all(self):
        """Release all buttons"""
        for key in self.pressed:
            self.pressed[key] = False

    def get_direction(self):
        """Get current direction as (dx, dy)"""
        dx, dy = 0, 0
        if self.pressed['left']:
            dx = -1
        if self.pressed['right']:
            dx = 1
        if self.pressed['up']:
            dy = -1
        if self.pressed['down']:
            dy = 1
        return dx, dy

    def draw(self, screen):
        """Draw the D-Pad"""
        rects = self.get_button_rects()

        # Create surface with alpha
        surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)

        # Draw buttons
        colors = {
            'up': (100, 100, 100, self.alpha) if not self.pressed['up'] else (150, 150, 200, self.alpha),
            'down': (100, 100, 100, self.alpha) if not self.pressed['down'] else (150, 150, 200, self.alpha),
            'left': (100, 100, 100, self.alpha) if not self.pressed['left'] else (150, 150, 200, self.alpha),
            'right': (100, 100, 100, self.alpha) if not self.pressed['right'] else (150, 150, 200, self.alpha),
        }

        bs = self.button_size
        margin = bs // 5  # Arrow margin from button edge

        # Up button
        pygame.draw.rect(surface, colors['up'], (bs, 0, bs, bs), border_radius=12)
        pygame.draw.polygon(surface, (255, 255, 255, 220),
                          [(bs + bs//2, margin),
                           (bs + margin, bs - margin),
                           (bs + bs - margin, bs - margin)])

        # Down button
        pygame.draw.rect(surface, colors['down'], (bs, bs * 2, bs, bs), border_radius=12)
        pygame.draw.polygon(surface, (255, 255, 255, 220),
                          [(bs + bs//2, bs * 3 - margin),
                           (bs + margin, bs * 2 + margin),
                           (bs + bs - margin, bs * 2 + margin)])

        # Left button
        pygame.draw.rect(surface, colors['left'], (0, bs, bs, bs), border_radius=12)
        pygame.draw.polygon(surface, (255, 255, 255, 220),
                          [(margin, bs + bs//2),
                           (bs - margin, bs + margin),
                           (bs - margin, bs + bs - margin)])

        # Right button
        pygame.draw.rect(surface, colors['right'], (bs * 2, bs, bs, bs), border_radius=12)
        pygame.draw.polygon(surface, (255, 255, 255, 220),
                          [(bs * 3 - margin, bs + bs//2),
                           (bs * 2 + margin, bs + margin),
                           (bs * 2 + margin, bs + bs - margin)])

        # Center
        pygame.draw.rect(surface, (80, 80, 80, self.alpha), (bs, bs, bs, bs), border_radius=12)

        screen.blit(surface, (self.x, self.y))


class ActionButton:
    """Action button for touch (Start/Restart)"""

    def __init__(self, x, y, size=80):
        self.x = x
        self.y = y
        self.size = size
        self.pressed = False
        self.alpha = 150

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)

    def handle_touch(self, pos, is_down):
        if self.get_rect().collidepoint(pos):
            self.pressed = is_down
            return is_down  # Return True only on press
        return False

    def draw(self, screen, text="OK"):
        surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        color = (100, 100, 100, self.alpha) if not self.pressed else (150, 150, 200, self.alpha)
        pygame.draw.rect(surface, color, (0, 0, self.size, self.size), border_radius=12)

        # Draw text
        font = pygame.font.Font(None, 32)
        text_surf = font.render(text, True, (255, 255, 255))
        text_x = (self.size - text_surf.get_width()) // 2
        text_y = (self.size - text_surf.get_height()) // 2
        surface.blit(text_surf, (text_x, text_y))

        screen.blit(surface, (self.x, self.y))


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Turtle Drawing Game")

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        # 기본 시스템 폰트 사용 (영어 호환)
        self.font = pygame.font.Font(None, 36)
        self.large_font = pygame.font.Font(None, 72)
        self.small_font = pygame.font.Font(None, 24)

        # Virtual controls for touch (larger for mobile)
        dpad_size = 240  # 4x bigger
        self.dpad = VirtualDPad(20, SCREEN_HEIGHT - dpad_size - 20, dpad_size)
        self.action_btn = ActionButton(SCREEN_WIDTH - 120, SCREEN_HEIGHT - 120, 100)
        self.touch_active = False
        self.active_touch_id = None

        self.reset_game()

    def reset_game(self):
        """게임 초기화"""
        self.current_stage = 1
        self.lives = MAX_LIVES
        self.game_state = "title"
        self.glitch = GlitchEffect()
        self.hospital_timer = 0
        self.ending_shown = False

        self._load_stage()

    def _load_stage(self):
        """현재 스테이지 로드"""
        self.stage = Stage(self.current_stage)
        start_pos = self.stage.get_start_pos()

        if start_pos:
            self.turtle = TurtlePlayer(start_pos[0], start_pos[1])
        else:
            self.turtle = TurtlePlayer(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        self.on_path = True
        self.auto_drawer = None

        if self.stage.is_special_stage():
            self.game_state = "special_wait"
            self.turtle.set_color(RED)

    def _reset_stage(self):
        """현재 스테이지 리셋 (목숨 감소)"""
        self.lives -= 1
        if self.lives <= 0:
            self.game_state = "gameover"
            if self.glitch.sound_manager:
                self.glitch.sound_manager.play('jumpscare', 0.8)
        else:
            self._load_stage()

    def _next_stage(self):
        """다음 스테이지로"""
        if self.stage.is_special_stage():
            self.glitch.add_glitch()

        self.current_stage += 1

        # 44 스테이지 클리어 시 병실 엔딩
        if self.current_stage > 44 and not self.ending_shown:
            self.game_state = "hospital_ending"
            self.hospital_timer = 0
            self.ending_shown = True
            # 삐- 소리
            if self.glitch.sound_manager:
                self._play_beep_sound()
            return

        if self.current_stage > 50:
            self.game_state = "win"
        else:
            self._load_stage()
            if not self.stage.is_special_stage():
                self.game_state = "playing"

    def _play_beep_sound(self):
        """병원 삐- 소리"""
        import array as arr
        sample_rate = 22050
        duration = 2.0
        samples = int(sample_rate * duration)

        sound_array = []
        for i in range(samples):
            t = i / sample_rate
            # 지속적인 삐- 소리
            val = math.sin(2 * math.pi * 1000 * t) * 0.5
            sound_array.append(int(val * 32767 * 0.4))

        stereo = []
        for val in sound_array:
            stereo.extend([val, val])

        sound_buffer = arr.array('h', stereo)
        sound = pygame.mixer.Sound(buffer=sound_buffer)
        sound.play()

    def _get_touch_pos(self, event):
        """Convert touch event to screen position"""
        if hasattr(event, 'x') and hasattr(event, 'y'):
            return (int(event.x * SCREEN_WIDTH), int(event.y * SCREEN_HEIGHT))
        return None

    def handle_events(self):
        """이벤트 처리"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            # Keyboard events
            if event.type == pygame.KEYDOWN:
                self._handle_key_action()

            # Mouse events (also work as touch on some platforms)
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                self.touch_active = True
                if self.game_state == "playing":
                    self.dpad.handle_touch(pos, True)
                if self.action_btn.handle_touch(pos, True):
                    self._handle_action_button()

            if event.type == pygame.MOUSEBUTTONUP:
                self.touch_active = False
                self.dpad.release_all()
                self.action_btn.pressed = False

            if event.type == pygame.MOUSEMOTION and self.touch_active:
                pos = event.pos
                if self.game_state == "playing":
                    self.dpad.handle_touch_move(pos)

            # Touch events (for mobile)
            if event.type == pygame.FINGERDOWN:
                pos = self._get_touch_pos(event)
                if pos:
                    self.touch_active = True
                    if self.game_state == "playing":
                        self.dpad.handle_touch(pos, True)
                    if self.action_btn.handle_touch(pos, True):
                        self._handle_action_button()

            if event.type == pygame.FINGERUP:
                self.touch_active = False
                self.dpad.release_all()
                self.action_btn.pressed = False

            if event.type == pygame.FINGERMOTION:
                pos = self._get_touch_pos(event)
                if pos and self.game_state == "playing":
                    self.dpad.handle_touch_move(pos)

        return True

    def _handle_key_action(self):
        """Handle key/touch action for state changes"""
        if self.game_state == "title":
            self.game_state = "playing"
        elif self.game_state == "special_wait":
            self._start_auto_draw()
        elif self.game_state == "hospital_ending":
            self._load_stage()
            if not self.stage.is_special_stage():
                self.game_state = "playing"
        elif self.game_state == "gameover" or self.game_state == "win":
            self.reset_game()

    def _handle_action_button(self):
        """Handle action button press"""
        self._handle_key_action()

    def _start_auto_draw(self):
        """자동 그리기 시작 (특수 스테이지)"""
        self.game_state = "special_drawing"
        help_path = generate_help_path(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 1.5)
        self.turtle.reset(help_path[0][0], help_path[0][1])
        self.turtle.set_color(RED)
        self.auto_drawer = AutoDrawer(self.turtle, help_path)

        # 무서운 소리
        if self.glitch.sound_manager:
            self.glitch.sound_manager.play('scream', 0.5)

    def update(self):
        """게임 상태 업데이트"""
        if self.game_state == "playing":
            self._update_playing()
        elif self.game_state == "special_drawing":
            self._update_special_drawing()
        elif self.game_state == "hospital_ending":
            self.hospital_timer += 1

    def _update_playing(self):
        """플레이 상태 업데이트"""
        keys = pygame.key.get_pressed()

        # Keyboard input
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]:
            dx = -1
        if keys[pygame.K_RIGHT]:
            dx = 1
        if keys[pygame.K_UP]:
            dy = -1
        if keys[pygame.K_DOWN]:
            dy = 1

        # Virtual D-Pad input (combine with keyboard)
        dpad_dx, dpad_dy = self.dpad.get_direction()
        if dpad_dx != 0:
            dx = dpad_dx
        if dpad_dy != 0:
            dy = dpad_dy

        dx, dy = self.glitch.apply_control_glitch(dx, dy)

        if dx != 0 or dy != 0:
            self.turtle.move(dx, dy)

            pos = self.turtle.get_position()
            self.on_path = self.stage.check_on_path(pos)

            if self.stage.check_goal_reached(pos):
                if self.on_path:
                    self._next_stage()
                else:
                    self._reset_stage()

        # 적 업데이트
        player_pos = self.turtle.get_position()
        if self.glitch.update_enemies(player_pos[0], player_pos[1], SCREEN_WIDTH, SCREEN_HEIGHT):
            # 적에게 잡힘 = 게임오버
            self.game_state = "gameover"

    def _update_special_drawing(self):
        """특수 스테이지 자동 그리기 업데이트"""
        if self.auto_drawer:
            self.auto_drawer.update()
            if self.auto_drawer.is_finished():
                # 타이머 기반 대기 (웹 호환)
                if not hasattr(self, '_wait_timer'):
                    self._wait_timer = 60  # 60프레임 = 약 1초
                self._wait_timer -= 1
                if self._wait_timer <= 0:
                    del self._wait_timer
                    self._next_stage()

    def draw(self):
        """화면 그리기"""
        self.screen.fill(WHITE)

        if self.game_state == "title":
            self._draw_title()
        elif self.game_state in ["playing", "special_wait", "special_drawing"]:
            self._draw_game()
        elif self.game_state == "hospital_ending":
            self._draw_hospital_ending()
        elif self.game_state == "gameover":
            self._draw_gameover()
        elif self.game_state == "win":
            self._draw_win()

        # 글리치 시각 효과
        if self.game_state not in ["hospital_ending"]:
            self.glitch.apply_visual_glitch(self.screen)

        pygame.display.flip()

    def _draw_title(self):
        """타이틀 화면"""
        title = self.large_font.render("TURTLE DRAWING", True, BLACK)
        subtitle = self.font.render("Press any key to start", True, GRAY)
        hint = self.font.render("Follow the dotted line!", True, GRAY)
        warning = self.small_font.render("WARNING: Contains horror elements", True, RED)

        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 200))
        self.screen.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, 350))
        self.screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, 400))
        self.screen.blit(warning, (SCREEN_WIDTH // 2 - warning.get_width() // 2, 500))

        pygame.draw.polygon(self.screen, BLACK, [
            (SCREEN_WIDTH // 2, 250),
            (SCREEN_WIDTH // 2 - 30, 320),
            (SCREEN_WIDTH // 2 + 30, 320)
        ])

        # Action button for touch
        self.action_btn.draw(self.screen, "START")

    def _draw_game(self):
        """게임 화면"""
        self.stage.draw(self.screen)
        self.turtle.draw(self.screen)

        # 적 그리기
        self.glitch.draw_enemies(self.screen)

        self._draw_ui()

        if self.game_state == "special_wait":
            msg = self.font.render("Press any key...", True, RED)
            self.screen.blit(msg, (SCREEN_WIDTH // 2 - msg.get_width() // 2, 50))

        if self.game_state == "playing" and not self.on_path:
            warning = self.font.render("OFF PATH!", True, RED)
            self.screen.blit(warning, (SCREEN_WIDTH // 2 - warning.get_width() // 2, 80))

        # Virtual controls (for touch devices)
        self.dpad.draw(self.screen)
        if self.game_state == "special_wait":
            self.action_btn.draw(self.screen, "GO")

    def _draw_ui(self):
        """UI 요소 그리기"""
        stage_text = self.font.render(f"Stage: {self.current_stage}", True, BLACK)
        self.screen.blit(stage_text, (10, 10))

        lives_text = self.font.render(f"Lives: {'*' * self.lives}", True, RED)
        self.screen.blit(lives_text, (10, 50))

        glitch_status = self.glitch.get_status_text()
        if glitch_status:
            glitch_text = self.font.render(f"{glitch_status}", True, (150, 0, 150))
            self.screen.blit(glitch_text, (10, 90))

        controls = self.font.render("Arrow keys to move", True, GRAY)
        self.screen.blit(controls, (SCREEN_WIDTH - controls.get_width() - 10, 10))

    def _draw_hospital_ending(self):
        """병실 엔딩 화면"""
        # 병실 배경 (흰색/밝은 파란색)
        self.screen.fill((240, 248, 255))

        # 침대
        bed_color = (200, 200, 220)
        pygame.draw.rect(self.screen, bed_color, (200, 300, 400, 200))  # 침대 프레임
        pygame.draw.rect(self.screen, (255, 255, 255), (210, 310, 380, 100))  # 이불
        pygame.draw.rect(self.screen, (220, 220, 240), (210, 310, 380, 100), 3)

        # 베개
        pygame.draw.ellipse(self.screen, (255, 255, 255), (220, 280, 100, 50))

        # 환자 (단순화)
        pygame.draw.ellipse(self.screen, (255, 220, 200), (240, 270, 60, 40))  # 머리
        pygame.draw.rect(self.screen, (255, 255, 255), (250, 320, 200, 80))  # 몸

        # 심전도 모니터
        pygame.draw.rect(self.screen, (50, 50, 50), (550, 150, 150, 120))
        pygame.draw.rect(self.screen, (0, 50, 0), (560, 160, 130, 80))

        # 심전도 선 (flat line - 사망)
        if self.hospital_timer > 60:
            pygame.draw.line(self.screen, (0, 255, 0), (560, 200), (690, 200), 2)
        else:
            # 처음엔 약간의 파동
            for i in range(13):
                x1 = 560 + i * 10
                x2 = 560 + (i + 1) * 10
                y1 = 200 + random.randint(-20, 20)
                y2 = 200 + random.randint(-20, 20)
                pygame.draw.line(self.screen, (0, 255, 0), (x1, y1), (x2, y2), 2)

        # 창문
        pygame.draw.rect(self.screen, (135, 206, 235), (50, 100, 120, 150))
        pygame.draw.rect(self.screen, (255, 255, 255), (50, 100, 120, 150), 5)
        pygame.draw.line(self.screen, (255, 255, 255), (110, 100), (110, 250), 5)
        pygame.draw.line(self.screen, (255, 255, 255), (50, 175), (170, 175), 5)

        # 텍스트
        if self.hospital_timer > 120:
            text = self.font.render("...", True, BLACK)
            self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 500))

        if self.hospital_timer > 180:
            text2 = self.small_font.render("Press any key to continue", True, GRAY)
            self.screen.blit(text2, (SCREEN_WIDTH // 2 - text2.get_width() // 2, 550))
            # Action button for touch
            self.action_btn.draw(self.screen, "NEXT")

    def _draw_gameover(self):
        """게임오버 화면 - 인형들"""
        # 어두운 그라데이션 배경
        for y in range(SCREEN_HEIGHT):
            darkness = int(20 + (y / SCREEN_HEIGHT) * 15)
            pygame.draw.line(self.screen, (darkness, darkness - 5, darkness + 10),
                           (0, y), (SCREEN_WIDTH, y))

        # 바닥 (나무 마루)
        floor_y = 450
        for i in range(0, SCREEN_WIDTH, 60):
            color = (60, 40, 25) if (i // 60) % 2 == 0 else (50, 35, 20)
            pygame.draw.rect(self.screen, color, (i, floor_y, 60, 150))
            pygame.draw.line(self.screen, (40, 25, 15), (i, floor_y), (i, SCREEN_HEIGHT), 2)

        # 벽 무늬 (벽지)
        for y in range(0, floor_y, 40):
            alpha = 30 if (y // 40) % 2 == 0 else 20
            pygame.draw.line(self.screen, (alpha, alpha - 5, alpha + 5),
                           (0, y), (SCREEN_WIDTH, y), 1)

        # 창문 (달빛)
        pygame.draw.rect(self.screen, (40, 50, 70), (50, 80, 120, 160))
        pygame.draw.rect(self.screen, (20, 25, 35), (50, 80, 120, 160), 4)
        pygame.draw.line(self.screen, (20, 25, 35), (110, 80), (110, 240), 4)
        pygame.draw.line(self.screen, (20, 25, 35), (50, 160), (170, 160), 4)
        # 달
        pygame.draw.circle(self.screen, (200, 200, 180), (90, 120), 25)
        pygame.draw.circle(self.screen, (40, 50, 70), (100, 115), 20)

        # 달빛 효과
        moonlight = pygame.Surface((200, 300), pygame.SRCALPHA)
        for i in range(100, 0, -2):
            pygame.draw.polygon(moonlight, (100, 100, 150, i // 10),
                              [(60, 0), (0, 300), (140, 300)])
        self.screen.blit(moonlight, (30, 240))

        # 선반 (뒤쪽 인형들)
        pygame.draw.rect(self.screen, (45, 30, 20), (500, 150, 250, 15))
        self._draw_creepy_doll_detailed(550, 140, facing_right=False, scale=0.5)
        self._draw_creepy_doll_detailed(620, 140, facing_right=False, scale=0.45)
        self._draw_creepy_doll_detailed(690, 140, facing_right=False, scale=0.5)

        # 왼쪽 의자 위 인형
        pygame.draw.rect(self.screen, (50, 35, 25), (80, 380, 80, 70))  # 의자
        pygame.draw.rect(self.screen, (55, 40, 28), (80, 320, 80, 60))  # 등받이
        self._draw_creepy_doll_detailed(120, 340, facing_right=True, scale=0.8)

        # 오른쪽 바닥 인형들
        self._draw_creepy_doll_detailed(650, 420, facing_right=False, scale=0.9)
        self._draw_clown_doll(720, 430, facing_right=False, scale=0.7)

        # 중앙 곰돌이 인형 (메인, 스포트라이트)
        bear_x, bear_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70
        self._draw_teddy_bear_detailed(bear_x, bear_y, 1.2)

        # 스포트라이트 효과 (더 부드럽게)
        spotlight = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        for r in range(250, 0, -3):
            alpha = int((250 - r) / 250 * 40)
            pygame.draw.circle(spotlight, (255, 240, 200, alpha), (bear_x, bear_y), r)
        self.screen.blit(spotlight, (0, 0))

        # 가까이 있는 인형 (앞쪽, 일부만 보임)
        self._draw_creepy_doll_detailed(50, 500, facing_right=True, scale=1.3)
        self._draw_creepy_doll_detailed(750, 500, facing_right=False, scale=1.2)

        # 비네팅 효과 (가장자리 어둡게)
        vignette = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        for i in range(100):
            alpha = int(i * 1.5)
            pygame.draw.rect(vignette, (0, 0, 0, alpha),
                           (i, i, SCREEN_WIDTH - i*2, SCREEN_HEIGHT - i*2), 3)
        self.screen.blit(vignette, (0, 0))

        # 텍스트 (글리치 효과)
        text = self.large_font.render("GAME OVER", True, (180, 0, 0))
        text_x = SCREEN_WIDTH // 2 - text.get_width() // 2
        # 글리치 복제
        if random.random() < 0.3:
            offset = random.randint(-3, 3)
            self.screen.blit(text, (text_x + offset, 25 + random.randint(-2, 2)))
        self.screen.blit(text, (text_x, 25))

        stage_text = self.font.render(f"Reached Stage: {self.current_stage}", True, (120, 120, 120))
        self.screen.blit(stage_text, (SCREEN_WIDTH // 2 - stage_text.get_width() // 2, 540))

        restart = self.font.render("Press SPACE to restart", True, (100, 100, 100))
        self.screen.blit(restart, (SCREEN_WIDTH // 2 - restart.get_width() // 2, 570))

        # Action button for touch
        self.action_btn.draw(self.screen, "RETRY")

    def _draw_teddy_bear(self, x, y, scale=1.0):
        """곰돌이 인형 그리기"""
        s = scale
        brown = (139, 90, 43)
        light_brown = (205, 133, 63)
        dark_brown = (101, 67, 33)

        # 몸통
        pygame.draw.ellipse(self.screen, brown,
                           (x - int(40*s), y - int(20*s), int(80*s), int(100*s)))

        # 머리
        pygame.draw.circle(self.screen, brown, (x, y - int(60*s)), int(50*s))

        # 귀
        pygame.draw.circle(self.screen, brown, (x - int(40*s), y - int(95*s)), int(20*s))
        pygame.draw.circle(self.screen, brown, (x + int(40*s), y - int(95*s)), int(20*s))
        pygame.draw.circle(self.screen, light_brown, (x - int(40*s), y - int(95*s)), int(12*s))
        pygame.draw.circle(self.screen, light_brown, (x + int(40*s), y - int(95*s)), int(12*s))

        # 주둥이
        pygame.draw.ellipse(self.screen, light_brown,
                           (x - int(20*s), y - int(50*s), int(40*s), int(30*s)))

        # 코
        pygame.draw.ellipse(self.screen, dark_brown,
                           (x - int(8*s), y - int(45*s), int(16*s), int(12*s)))

        # 눈 (버튼 눈, 하나가 떨어져 있음 - 무서운 효과)
        pygame.draw.circle(self.screen, (20, 20, 20), (x - int(20*s), y - int(65*s)), int(8*s))
        # X 표시된 눈 (꿰맨 자국)
        pygame.draw.line(self.screen, (20, 20, 20),
                        (x + int(12*s), y - int(73*s)), (x + int(28*s), y - int(57*s)), int(3*s))
        pygame.draw.line(self.screen, (20, 20, 20),
                        (x + int(28*s), y - int(73*s)), (x + int(12*s), y - int(57*s)), int(3*s))

        # 팔
        pygame.draw.ellipse(self.screen, brown,
                           (x - int(65*s), y - int(10*s), int(35*s), int(60*s)))
        pygame.draw.ellipse(self.screen, brown,
                           (x + int(30*s), y - int(10*s), int(35*s), int(60*s)))

        # 다리
        pygame.draw.ellipse(self.screen, brown,
                           (x - int(35*s), y + int(50*s), int(30*s), int(40*s)))
        pygame.draw.ellipse(self.screen, brown,
                           (x + int(5*s), y + int(50*s), int(30*s), int(40*s)))

    def _draw_creepy_doll(self, x, y, facing_right=True, scale=1.0):
        """무서운 인형 그리기 (곰돌이를 쳐다보는)"""
        s = scale
        skin = (255, 220, 200)
        dress = (100, 50, 80)
        hair = (40, 30, 20)

        # 몸 (드레스)
        pygame.draw.ellipse(self.screen, dress,
                           (x - int(25*s), y - int(10*s), int(50*s), int(70*s)))

        # 머리
        pygame.draw.circle(self.screen, skin, (x, y - int(40*s)), int(30*s))

        # 머리카락
        pygame.draw.ellipse(self.screen, hair,
                           (x - int(35*s), y - int(70*s), int(70*s), int(50*s)))

        # 눈 (큰 검은 눈, 중앙을 쳐다봄)
        eye_offset = int(5*s) if facing_right else -int(5*s)
        # 흰자
        pygame.draw.ellipse(self.screen, (255, 255, 255),
                           (x - int(18*s), y - int(50*s), int(15*s), int(20*s)))
        pygame.draw.ellipse(self.screen, (255, 255, 255),
                           (x + int(3*s), y - int(50*s), int(15*s), int(20*s)))
        # 동공 (중앙을 향해)
        pygame.draw.circle(self.screen, (0, 0, 0),
                          (x - int(10*s) + eye_offset, y - int(42*s)), int(5*s))
        pygame.draw.circle(self.screen, (0, 0, 0),
                          (x + int(10*s) + eye_offset, y - int(42*s)), int(5*s))
        # 하이라이트
        pygame.draw.circle(self.screen, (255, 255, 255),
                          (x - int(8*s) + eye_offset, y - int(44*s)), int(2*s))
        pygame.draw.circle(self.screen, (255, 255, 255),
                          (x + int(12*s) + eye_offset, y - int(44*s)), int(2*s))

        # 입 (미소, 하지만 무섭게)
        pygame.draw.arc(self.screen, (100, 50, 50),
                       (x - int(10*s), y - int(30*s), int(20*s), int(15*s)),
                       3.14, 0, int(2*s))

    def _draw_teddy_bear_detailed(self, x, y, scale=1.0):
        """고퀄리티 곰돌이 인형"""
        s = scale
        brown = (120, 80, 40)
        light_brown = (160, 110, 60)
        dark_brown = (80, 50, 25)
        patch_color = (100, 70, 35)

        # 그림자
        shadow = pygame.Surface((int(120*s), int(40*s)), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow, (0, 0, 0, 80), (0, 0, int(120*s), int(40*s)))
        self.screen.blit(shadow, (x - int(60*s), y + int(75*s)))

        # 다리
        pygame.draw.ellipse(self.screen, brown,
                           (x - int(40*s), y + int(40*s), int(35*s), int(50*s)))
        pygame.draw.ellipse(self.screen, brown,
                           (x + int(5*s), y + int(40*s), int(35*s), int(50*s)))
        # 발바닥
        pygame.draw.ellipse(self.screen, light_brown,
                           (x - int(35*s), y + int(70*s), int(25*s), int(15*s)))
        pygame.draw.ellipse(self.screen, light_brown,
                           (x + int(10*s), y + int(70*s), int(25*s), int(15*s)))

        # 몸통
        pygame.draw.ellipse(self.screen, brown,
                           (x - int(45*s), y - int(30*s), int(90*s), int(100*s)))
        # 배 패치
        pygame.draw.ellipse(self.screen, light_brown,
                           (x - int(25*s), y - int(5*s), int(50*s), int(45*s)))

        # 팔
        pygame.draw.ellipse(self.screen, brown,
                           (x - int(70*s), y - int(20*s), int(35*s), int(55*s)))
        pygame.draw.ellipse(self.screen, brown,
                           (x + int(35*s), y - int(20*s), int(35*s), int(55*s)))
        # 손바닥
        pygame.draw.ellipse(self.screen, light_brown,
                           (x - int(65*s), y + int(20*s), int(20*s), int(15*s)))
        pygame.draw.ellipse(self.screen, light_brown,
                           (x + int(45*s), y + int(20*s), int(20*s), int(15*s)))

        # 머리
        pygame.draw.circle(self.screen, brown, (x, y - int(60*s)), int(55*s))

        # 귀
        pygame.draw.circle(self.screen, brown, (x - int(45*s), y - int(100*s)), int(22*s))
        pygame.draw.circle(self.screen, brown, (x + int(45*s), y - int(100*s)), int(22*s))
        pygame.draw.circle(self.screen, light_brown, (x - int(45*s), y - int(100*s)), int(12*s))
        pygame.draw.circle(self.screen, light_brown, (x + int(45*s), y - int(100*s)), int(12*s))

        # 주둥이
        pygame.draw.ellipse(self.screen, light_brown,
                           (x - int(22*s), y - int(55*s), int(44*s), int(35*s)))

        # 코
        pygame.draw.ellipse(self.screen, (30, 20, 15),
                           (x - int(10*s), y - int(50*s), int(20*s), int(14*s)))
        # 코 하이라이트
        pygame.draw.ellipse(self.screen, (60, 40, 30),
                           (x - int(6*s), y - int(48*s), int(8*s), int(5*s)))

        # 입 (꿰맨 자국)
        pygame.draw.arc(self.screen, (40, 25, 15),
                       (x - int(12*s), y - int(40*s), int(24*s), int(16*s)),
                       3.14, 0, int(2*s))
        # 꿰맨 실
        for i in range(5):
            sx = x - int(10*s) + i * int(5*s)
            pygame.draw.line(self.screen, (40, 25, 15),
                           (sx, y - int(35*s)), (sx, y - int(30*s)), 1)

        # 왼쪽 눈 (버튼)
        pygame.draw.circle(self.screen, (20, 15, 10), (x - int(20*s), y - int(70*s)), int(10*s))
        pygame.draw.circle(self.screen, (40, 30, 20), (x - int(20*s), y - int(70*s)), int(6*s))
        # 버튼 구멍
        pygame.draw.circle(self.screen, (15, 10, 5), (x - int(22*s), y - int(72*s)), int(2*s))
        pygame.draw.circle(self.screen, (15, 10, 5), (x - int(18*s), y - int(68*s)), int(2*s))

        # 오른쪽 눈 (X자 - 떨어진 버튼)
        pygame.draw.line(self.screen, (30, 20, 10),
                        (x + int(10*s), y - int(80*s)), (x + int(30*s), y - int(60*s)), int(3*s))
        pygame.draw.line(self.screen, (30, 20, 10),
                        (x + int(30*s), y - int(80*s)), (x + int(10*s), y - int(60*s)), int(3*s))
        # 실 자국
        for i in range(3):
            pygame.draw.line(self.screen, (50, 35, 20),
                           (x + int(15*s) + i*int(5*s), y - int(75*s)),
                           (x + int(17*s) + i*int(5*s), y - int(65*s)), 1)

        # 패치 (기운 자국)
        pygame.draw.polygon(self.screen, patch_color, [
            (x + int(25*s), y - int(45*s)),
            (x + int(40*s), y - int(40*s)),
            (x + int(35*s), y - int(25*s)),
            (x + int(20*s), y - int(30*s))
        ])
        # 패치 꿰맨 자국
        patch_points = [(x + int(25*s), y - int(45*s)), (x + int(40*s), y - int(40*s)),
                       (x + int(35*s), y - int(25*s)), (x + int(20*s), y - int(30*s))]
        for i in range(4):
            p1 = patch_points[i]
            p2 = patch_points[(i + 1) % 4]
            for j in range(3):
                t = (j + 1) / 4
                px = int(p1[0] + (p2[0] - p1[0]) * t)
                py = int(p1[1] + (p2[1] - p1[1]) * t)
                pygame.draw.line(self.screen, (40, 25, 15),
                               (px - 2, py - 2), (px + 2, py + 2), 1)

    def _draw_creepy_doll_detailed(self, x, y, facing_right=True, scale=1.0):
        """고퀄리티 무서운 인형"""
        s = scale
        skin = (240, 210, 190)
        skin_shadow = (200, 170, 150)
        dress = (80, 40, 60)
        dress_dark = (50, 25, 40)
        hair = (30, 25, 20)

        # 그림자
        if scale > 0.6:
            shadow = pygame.Surface((int(60*s), int(20*s)), pygame.SRCALPHA)
            pygame.draw.ellipse(shadow, (0, 0, 0, 60), (0, 0, int(60*s), int(20*s)))
            self.screen.blit(shadow, (x - int(30*s), y + int(55*s)))

        # 다리
        pygame.draw.rect(self.screen, skin,
                        (x - int(15*s), y + int(30*s), int(12*s), int(30*s)))
        pygame.draw.rect(self.screen, skin,
                        (x + int(3*s), y + int(30*s), int(12*s), int(30*s)))
        # 신발
        pygame.draw.ellipse(self.screen, (20, 15, 15),
                           (x - int(18*s), y + int(55*s), int(18*s), int(10*s)))
        pygame.draw.ellipse(self.screen, (20, 15, 15),
                           (x, y + int(55*s), int(18*s), int(10*s)))

        # 드레스
        points = [
            (x - int(25*s), y + int(35*s)),
            (x + int(25*s), y + int(35*s)),
            (x + int(20*s), y - int(5*s)),
            (x - int(20*s), y - int(5*s))
        ]
        pygame.draw.polygon(self.screen, dress, points)
        # 드레스 주름
        for i in range(3):
            fx = x - int(15*s) + i * int(15*s)
            pygame.draw.line(self.screen, dress_dark,
                           (fx, y), (fx - int(5*s), y + int(35*s)), 1)

        # 팔
        pygame.draw.rect(self.screen, skin,
                        (x - int(30*s), y - int(5*s), int(12*s), int(25*s)))
        pygame.draw.rect(self.screen, skin,
                        (x + int(18*s), y - int(5*s), int(12*s), int(25*s)))

        # 목
        pygame.draw.rect(self.screen, skin, (x - int(6*s), y - int(15*s), int(12*s), int(12*s)))

        # 머리
        pygame.draw.circle(self.screen, skin, (x, y - int(40*s)), int(28*s))

        # 머리카락
        pygame.draw.ellipse(self.screen, hair,
                           (x - int(32*s), y - int(70*s), int(64*s), int(45*s)))
        # 앞머리
        for i in range(5):
            hx = x - int(20*s) + i * int(10*s)
            pygame.draw.ellipse(self.screen, hair,
                              (hx, y - int(55*s), int(12*s), int(20*s)))
        # 옆머리
        pygame.draw.ellipse(self.screen, hair,
                           (x - int(35*s), y - int(50*s), int(15*s), int(40*s)))
        pygame.draw.ellipse(self.screen, hair,
                           (x + int(20*s), y - int(50*s), int(15*s), int(40*s)))

        # 눈 (중앙을 쳐다봄)
        eye_offset = int(4*s) if facing_right else -int(4*s)
        # 흰자
        pygame.draw.ellipse(self.screen, (255, 255, 255),
                           (x - int(18*s), y - int(48*s), int(14*s), int(18*s)))
        pygame.draw.ellipse(self.screen, (255, 255, 255),
                           (x + int(4*s), y - int(48*s), int(14*s), int(18*s)))
        # 홍채
        pygame.draw.circle(self.screen, (60, 40, 30),
                          (x - int(11*s) + eye_offset, y - int(40*s)), int(6*s))
        pygame.draw.circle(self.screen, (60, 40, 30),
                          (x + int(11*s) + eye_offset, y - int(40*s)), int(6*s))
        # 동공
        pygame.draw.circle(self.screen, (10, 5, 5),
                          (x - int(11*s) + eye_offset, y - int(40*s)), int(3*s))
        pygame.draw.circle(self.screen, (10, 5, 5),
                          (x + int(11*s) + eye_offset, y - int(40*s)), int(3*s))
        # 하이라이트
        pygame.draw.circle(self.screen, (255, 255, 255),
                          (x - int(9*s) + eye_offset, y - int(42*s)), int(2*s))
        pygame.draw.circle(self.screen, (255, 255, 255),
                          (x + int(13*s) + eye_offset, y - int(42*s)), int(2*s))

        # 볼터치
        pygame.draw.circle(self.screen, (255, 180, 180),
                          (x - int(20*s), y - int(30*s)), int(5*s))
        pygame.draw.circle(self.screen, (255, 180, 180),
                          (x + int(20*s), y - int(30*s)), int(5*s))

        # 입 (미소)
        pygame.draw.arc(self.screen, (150, 80, 80),
                       (x - int(8*s), y - int(28*s), int(16*s), int(12*s)),
                       3.14, 0, int(2*s))

    def _draw_clown_doll(self, x, y, facing_right=True, scale=1.0):
        """무서운 광대 인형"""
        s = scale
        white = (240, 235, 230)
        red = (180, 30, 30)

        # 몸통
        pygame.draw.ellipse(self.screen, (100, 80, 120),
                           (x - int(20*s), y - int(10*s), int(40*s), int(50*s)))

        # 머리
        pygame.draw.circle(self.screen, white, (x, y - int(35*s)), int(25*s))

        # 광대 머리카락 (양옆 뿔뿔이)
        pygame.draw.circle(self.screen, red, (x - int(25*s), y - int(40*s)), int(12*s))
        pygame.draw.circle(self.screen, red, (x + int(25*s), y - int(40*s)), int(12*s))
        pygame.draw.circle(self.screen, (255, 200, 0), (x, y - int(55*s)), int(10*s))

        # 눈 (무섭게)
        eye_offset = int(3*s) if facing_right else -int(3*s)
        pygame.draw.ellipse(self.screen, (255, 255, 0),
                           (x - int(15*s), y - int(45*s), int(12*s), int(15*s)))
        pygame.draw.ellipse(self.screen, (255, 255, 0),
                           (x + int(3*s), y - int(45*s), int(12*s), int(15*s)))
        pygame.draw.circle(self.screen, (0, 0, 0),
                          (x - int(9*s) + eye_offset, y - int(38*s)), int(4*s))
        pygame.draw.circle(self.screen, (0, 0, 0),
                          (x + int(9*s) + eye_offset, y - int(38*s)), int(4*s))

        # 코 (빨간 공)
        pygame.draw.circle(self.screen, red, (x, y - int(30*s)), int(8*s))
        pygame.draw.circle(self.screen, (220, 50, 50), (x - int(2*s), y - int(32*s)), int(3*s))

        # 입 (무서운 미소)
        pygame.draw.arc(self.screen, red,
                       (x - int(15*s), y - int(25*s), int(30*s), int(20*s)),
                       3.14, 0, int(3*s))
        # 이빨
        for i in range(4):
            tx = x - int(10*s) + i * int(7*s)
            pygame.draw.rect(self.screen, (255, 255, 240),
                           (tx, y - int(20*s), int(5*s), int(8*s)))

    def _draw_win(self):
        """승리 화면"""
        text = self.large_font.render("YOU WIN!", True, GREEN)
        congrats = self.font.render("Congratulations! You escaped!", True, BLACK)
        restart = self.font.render("Press SPACE to play again", True, GRAY)

        self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 200))
        self.screen.blit(congrats, (SCREEN_WIDTH // 2 - congrats.get_width() // 2, 300))
        self.screen.blit(restart, (SCREEN_WIDTH // 2 - restart.get_width() // 2, 400))

        # Action button for touch
        self.action_btn.draw(self.screen, "AGAIN")

    async def run(self):
        """메인 게임 루프 (async for Pygbag)"""
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

            # 브라우저에 제어권 반환 (Pygbag 필수)
            await asyncio.sleep(0)

        pygame.quit()


async def main():
    game = Game()
    await game.run()


if __name__ == "__main__":
    asyncio.run(main())
