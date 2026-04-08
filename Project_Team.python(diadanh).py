import pygame
import random

# --- CẤU HÌNH  --- //////////////////////////
WIDTH, HEIGHT = 800, 800
FPS = 30
WHITE, BLACK, GRAY = (255, 255, 255), (0, 0, 0), (200, 200, 200)
GRID_SIZE = 4
CARD_SIZE = 150
MARGIN = 20

# --- DATABASE (Giao cho cả nhóm soạn nội dung) ---
INFO_DATA = {
    "Ẩm thực": {"pho": "Phở là món ăn truyền thống...", "banh_mi": "Bánh mì Việt Nam..."},
    "Văn hóa": {"ao_dai": "Áo dài là trang phục...", "ca_tru": "Ca trù là loại hình..."},
    "Lịch sử": {"dien_bien": "Chiến thắng Điện Biên Phủ...", "vua_hung": "Giỗ tổ Hùng Vương..."}
}

class MemoryGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24)
        
        # Trạng thái hệ thống
        self.scene = "MENU" # MENU, INTRO, GAMEPLAY
        self.current_theme = None
        self.running = True
        
        # Logic Game ////////////////////////
        self.cards = []      # Danh sách các tấm ảnh/tên ảnh
        self.revealed = []   # Trạng thái lật (True/False)
        self.selected = []   # Lưu index của 2 ô đang chọn để so sánh
        self.matched_info = None # Lưu thông tin giáo dục để hiện Pop-up

    def setup_level(self, theme):
        #"""Khởi tạo lưới 4x4 cho theme đã chọn"""
        self.current_theme = theme
        # Lấy danh sách tên ảnh từ Database của theme đó
        names = list(INFO_DATA[theme].keys()) 
        # Chọn 8 món ngẫu nhiên, nhân đôi thành 16
        game_list = names[:8] * 2 
        random.shuffle(game_list)
        
        self.cards = game_list
        self.revealed = [False] * 16
        self.selected = []

    def handle_click(self, pos):
        if self.scene == "MENU":
            # Kiểm tra click vào nút chọn Theme (Giao cho Sâm/Nghĩa vẽ nút)
            if 100 < pos[0] < 300: self.start_intro("Ẩm thực")
            elif 350 < pos[0] < 550: self.start_intro("Văn hóa")
            
        elif self.scene == "INTRO":
            self.scene = "GAMEPLAY" # Click để vào chơi
            
        elif self.scene == "GAMEPLAY":
            if self.matched_info: # Nếu đang hiện Pop-up, click để đóng
                self.matched_info = None
                return

            # Tính tọa độ lưới (Quan trọng nhất)
            x, y = pos
            col = (x - 80) // (CARD_SIZE + MARGIN)
            row = (y - 80) // (CARD_SIZE + MARGIN)
            idx = row * GRID_SIZE + col
            
            if 0 <= idx < 16 and not self.revealed[idx]:
                self.revealed[idx] = True
                self.selected.append(idx)

    def update(self):
        #"""Logic kiểm tra cặp bài """//////////////////////////////////
        if len(self.selected) == 2:
            idx1, idx2 = self.selected
            if self.cards[idx1] == self.cards[idx2]:
                # TRÙNG KHỚP -> Hiện Pop-up giáo dục
                item_name = self.cards[idx1]
                self.matched_info = INFO_DATA[self.current_theme][item_name]
                self.selected = []
            else:
                # KHÔNG TRÙNG -> Đợi 1 giây rồi úp lại
                pygame.display.flip()
                pygame.time.delay(1000)
                self.revealed[idx1] = self.revealed[idx2] = False
                self.selected = []

    def draw(self):
        self.screen.fill(WHITE)
        if self.scene == "MENU":
            self.draw_text("CHỌN CHỦ ĐỀ", (WIDTH//2, 100))
            # Vẽ 3 nút ở đây...
            
        elif self.scene == "INTRO":
            # Vẽ ảnh nền theme /////////////////////////////////
            self.draw_text(f"Chủ đề: {self.current_theme}. Click để bắt đầu!", (WIDTH//2, HEIGHT//2))
            
        elif self.scene == "GAMEPLAY":
            self.draw_grid()
            if self.matched_info:
                self.draw_popup(self.matched_info)

    def draw_grid(self):
        """Vẽ lưới 4x4 (Giao cho Sâm/Nghĩa)"""
        for i in range(16):
            row, col = i // 4, i % 4
            rect = pygame.Rect(80 + col*(CARD_SIZE+MARGIN), 80 + row*(CARD_SIZE+MARGIN), CARD_SIZE, CARD_SIZE)
            if self.revealed[i]:
                pygame.draw.rect(self.screen, GRAY, rect) # Thay bằng ảnh thật
                self.draw_text(self.cards[i], rect.center)
            else:
                pygame.draw.rect(self.screen, BLACK, rect)

    def draw_popup(self, text):
        #"""Vẽ bảng thông báo giáo dục """//////////////////////////////////////////
        overlay = pygame.Surface((600, 400))
        overlay.set_alpha(200)
        overlay.fill((50, 50, 50))
        self.screen.blit(overlay, (100, 200))
        # Vẽ text nội dung giáo dục lên trên overlay
        
    def draw_text(self, text, pos):
        img = self.font.render(text, True, BLACK)
        rect = img.get_rect(center=pos)
        self.screen.blit(img, rect)

    def start_intro(self, theme):
        self.setup_level(theme)
        self.scene = "INTRO"

# --- CHẠY GAME ---
if __name__ == "__main__":
    game = MemoryGame()
    while game.running:
        game.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: game.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                game.handle_click(event.pos)
        if game.scene == "GAMEPLAY":
            game.update()
        pygame.display.flip()