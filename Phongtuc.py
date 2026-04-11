import pygame
import random
import sys

# --- CẤU HÌNH HỢP NHẤT ---
WIDTH, HEIGHT = 900, 900
FPS = 30
WHITE, BLACK, GRAY = (255, 255, 255), (0, 0, 0), (200, 200, 200)
BLUE = (50, 150, 255)
GRID_SIZE = 4
CARD_SIZE = 160
MARGIN = 20

INFO_DATA = {
    "Ẩm thực": {
        "Phở": "'Quốc hồn quốc túy' với sợi bánh gạo mềm, nước dùng thanh ngọt...",
        "Bánh Mì": "'Vua đường phố' thế giới với vỏ ngoài giòn tan...",
        "Cà Phê Trứng": "Sự giao thoa giữa vị đắng cà phê và kem trứng béo ngậy...",
        "Cơm Tấm": "Món ăn đặc trưng Sài Gòn với hạt cơm vụn độc đáo...",
        "Bún Bò Huế": "Đặc trưng miền Trung với nước dùng cay nồng mùi mắm ruốc...",
        "Gỏi Cuốn": "Món ăn dân dã với tôm, thịt, rau tươi mát...",
        "Mì Quảng": "Tinh túy Quảng Nam với sợi mì to và nước lèo đậm đặc...",
        "Bánh Xèo": "Vỏ vàng giòn rụm, nhân tôm thịt đầy đặn..."
    },
    "Văn hóa": {
        "Dân tộc Kinh": "Áo dài xẻ tà cao, nón lá, chất liệu lụa thanh lịch.",
        "Dân tộc Thái": "Áo cỏm ôm sát, hàng khuy bạc hình bướm và khăn Piêu.",
        "Dân tộc H'Mông": "Váy xòe dập ly, thêu ghép vải màu rực rỡ.",
        "Dân tộc Chăm": "Áo dài chui đầu Patra, quấn xà rông tinh xảo.",
        "Dân tộc Dao Đỏ": "Sắc đỏ rực rỡ, khăn đội đầu khổ lớn kèm tua rua.",
        "Dân tộc Ê Đê": "Áo chui đầu, váy tấm đen-đỏ, dệt Kteh đính cườm.",
        "Dân tộc Khmer": "Quấn Săm-pốt, áo tầm vông, khăn Sbay rực rỡ.",
        "Dân tộc Mường": "Áo cánh ngắn, váy đen dài, cạp váy dệt tinh xảo."
    },
    "Phong tục": {
        "Đi chùa": "Đi chùa đầu năm: Dịp cầu bình an và hái lộc may mắn.",
        "Tết Nguyên Đán": "Từ 23 tháng Chạp đến mùng 3 Tết. Dịp đoàn viên lớn nhất.",
        "Tết Trung thu": "Rằm tháng Tám âm lịch. Tết đoàn viên cho trẻ em.",
        "Ông Công Ông Táo": "Ngày 23 tháng Chạp. Nghi lễ thả cá chép về trời.",
        "Gói bánh chưng": "Bánh chưng vuông tượng trưng cho Đất và lòng biết ơn nguồn cội.",
        "Xin chữ": "Xin chữ đầu năm thể hiện truyền thống hiếu học.",
        "Lì xì": "Phong bao đỏ chúc may mắn, trẻ nhỏ hay ăn chóng lớn.",
        "Giỗ Tổ": "Ngày 10/03 âm lịch hướng về công ơn dựng nước của vua Hùng."
    }
}

class MemoryGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Đồ Án Nhóm: Khám Phá Văn Hóa Việt Nam")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 20)
        self.big_font = pygame.font.SysFont("Arial", 40)
        
        self.scene = "MENU"
        self.current_theme = None
        self.running = True
        
        self.cards = []
        self.revealed = []
        self.selected = []
        self.matched_info = None 

    def setup_level(self, theme):
        self.current_theme = theme
        all_names = list(INFO_DATA[theme].keys())
        selected_items = random.sample(all_names, 8) if len(all_names) >= 8 else all_names[:8]
        game_list = selected_items * 2
        random.shuffle(game_list)
        
        self.cards = game_list
        self.revealed = [False] * 16
        self.selected = []

    def handle_click(self, pos):
        if self.scene == "MENU":
            # Tọa độ các nút chọn Theme
            if WIDTH//2 - 150 < pos[0] < WIDTH//2 + 150:
                if 350 < pos[1] < 420: self.start_intro("Ẩm thực")
                elif 450 < pos[1] < 520: self.start_intro("Văn hóa")
                elif 550 < pos[1] < 620: self.start_intro("Phong tục")
            
        elif self.scene == "INTRO":
            self.scene = "GAMEPLAY"
            
        elif self.scene == "GAMEPLAY":
            if self.matched_info:
                self.matched_info = None
                return

            x, y = pos
            offset_x = (WIDTH - (GRID_SIZE * (CARD_SIZE + MARGIN))) // 2
            offset_y = 150
            
            col = (x - offset_x) // (CARD_SIZE + MARGIN)
            row = (y - offset_y) // (CARD_SIZE + MARGIN)
            
            if 0 <= col < 4 and 0 <= row < 4:
                idx = row * GRID_SIZE + col
                if not self.revealed[idx] and len(self.selected) < 2:
                    self.revealed[idx] = True
                    self.selected.append(idx)

    def update(self):
        if len(self.selected) == 2:
            idx1, idx2 = self.selected
            if self.cards[idx1] == self.cards[idx2]:
                item_name = self.cards[idx1]
                self.matched_info = INFO_DATA[self.current_theme][item_name]
                self.selected = []
            else:
                pygame.display.flip()
                pygame.time.delay(800)
                self.revealed[idx1] = self.revealed[idx2] = False
                self.selected = []

    def draw_text_wrap(self, text, rect, color):
        words = text.split(' ')
        lines = []
        current_line = []
        for word in words:
            test_line = ' '.join(current_line + [word])
            if self.font.size(test_line)[0] < rect.width - 20:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
        lines.append(' '.join(current_line))
        
        y = rect.y + 20
        for line in lines:
            img = self.font.render(line, True, color)
            self.screen.blit(img, (rect.x + 10, y))
            y += 30

    def draw_grid(self):
        offset_x = (WIDTH - (GRID_SIZE * (CARD_SIZE + MARGIN))) // 2
        offset_y = 150
        for i in range(16):
            row, col = i // 4, i % 4
            rect = pygame.Rect(offset_x + col*(CARD_SIZE+MARGIN), offset_y + row*(CARD_SIZE+MARGIN), CARD_SIZE, CARD_SIZE)
            if self.revealed[i]:
                pygame.draw.rect(self.screen, GRAY, rect, border_radius=15)
                small_txt = self.font.render(self.cards[i], True, BLACK)
                txt_rect = small_txt.get_rect(center=rect.center)
                self.screen.blit(small_txt, txt_rect)
            else:
                pygame.draw.rect(self.screen, BLUE, rect, border_radius=15)
                pygame.draw.rect(self.screen, BLACK, rect, 2, border_radius=15)

    def draw_popup(self, text):
        overlay = pygame.Surface((700, 350))
        overlay.fill((255, 250, 240))
        rect = overlay.get_rect(center=(WIDTH//2, HEIGHT//2))
        pygame.draw.rect(self.screen, (139, 69, 19), rect, 6, border_radius=10)
        self.screen.blit(overlay, rect)
        
        title_img = self.font.render("KIẾN THỨC VĂN HÓA", True, (200, 0, 0))
        self.screen.blit(title_img, (rect.x + 20, rect.y + 20))
        
        content_rect = pygame.Rect(rect.x + 20, rect.y + 70, rect.width - 40, rect.height - 100)
        self.draw_text_wrap(text, content_rect, BLACK)
        
        msg = self.font.render("- Click để tiếp tục -", True, (100, 100, 100))
        self.screen.blit(msg, (rect.centerx - msg.get_width()//2, rect.bottom - 40))

    def draw(self):
        self.screen.fill(WHITE)
        if self.scene == "MENU":
            title = self.big_font.render("TRÒ CHƠI VĂN HÓA VIỆT", True, BLACK)
            self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 200))
            
            # Vẽ các nút chủ đề
            themes = ["Ẩm thực", "Văn hóa", "Phong tục"]
            for i, t in enumerate(themes):
                btn_rect = pygame.Rect(WIDTH//2 - 150, 350 + i*100, 300, 70)
                pygame.draw.rect(self.screen, BLUE, btn_rect, border_radius=15)
                txt = self.font.render(t, True, WHITE)
                self.screen.blit(txt, (btn_rect.centerx - txt.get_width()//2, btn_rect.centery - txt.get_height()//2))
            
        elif self.scene == "INTRO":
            txt = f"Chủ đề: {self.current_theme}. Click để bắt đầu!"
            img = self.font.render(txt, True, BLACK)
            self.screen.blit(img, (WIDTH//2 - img.get_width()//2, HEIGHT//2))
            
        elif self.scene == "GAMEPLAY":
            title = self.font.render(f"Đang chơi: {self.current_theme}", True, (50, 50, 50))
            self.screen.blit(title, (30, 30))
            self.draw_grid()
            if self.matched_info:
                self.draw_popup(self.matched_info)

    def start_intro(self, theme):
        self.setup_level(theme)
        self.scene = "INTRO"

if __name__ == "__main__":
    game = MemoryGame()
    while game.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                game.handle_click(event.pos)
        
        game.update()
        game.draw()
        pygame.display.flip()
        game.clock.tick(FPS)

    pygame.quit()
    sys.exit()