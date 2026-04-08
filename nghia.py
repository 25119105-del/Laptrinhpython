import pygame
import random
import sys

# --- CẤU HÌNH ---
WIDTH, HEIGHT = 900, 900  # Tăng kích thước để hiển thị nội dung tốt hơn
FPS = 30
WHITE, BLACK, GRAY = (255, 255, 255), (0, 0, 0), (200, 200, 200)
BLUE = (50, 150, 255)
GRID_SIZE = 4
CARD_SIZE = 160
MARGIN = 20

# --- DATABASE: NỘI DUNG PHONG TỤC CÓ THỜI GIAN/ĐẶC ĐIỂM ---
INFO_DATA = {
    "Phong tục": {
        "Đi chùa": "Đi chùa đầu năm: Từ đêm Giao thừa đến hết tháng Giêng. Dịp cầu bình an và hái lộc may mắn cho gia đình.",
        "Lễ cầu ngư": "Lễ cầu ngư: Tháng Giêng hoặc tháng Hai âm lịch. Ngư dân thờ cúng cá Ông để cầu mong biển lặng, mùa cá bội thu.",
        "Rằm tháng Giêng": "Rằm tháng Giêng: Ngày 15/01 âm lịch. Lễ rằm quan trọng nhất năm, cầu nguyện mọi sự khởi đầu hanh thông.",
        "Tết Nguyên Đán": "Tết Nguyên Đán: Từ 23 tháng Chạp đến mùng 3 Tết. Dịp đoàn viên lớn nhất để tri ân tổ tiên và đón năm mới.",
        "Tết Trung thu": "Tết Trung thu: Rằm tháng Tám âm lịch. Tết đoàn viên cho trẻ em với các hoạt động rước đèn, phá cỗ, ngắm trăng.",
        "Tục ăn trầu": "Tục ăn trầu: Diễn ra hàng ngày và lễ nghi. Biểu tượng thủy chung, 'miếng trầu là đầu câu chuyện'.",
        "Ông Công Ông Táo": "Cúng Ông Công Ông Táo: Ngày 23 tháng Chạp. Nghi lễ thả cá chép tiễn thần bếp về trời báo cáo việc nhà.",
        "Tục cưới hỏi": "Tục cưới hỏi: Tổ chức vào ngày lành tháng tốt. Gồm lễ dạm ngõ, ăn hỏi, đón dâu để tác hợp duyên lứa.",
        "Đốt vàng mã": "Tục đốt vàng mã: Dịp giỗ, rằm và Tết. Thể hiện lòng thành kính và sự chăm sóc đối với tổ tiên ở cõi âm.",
        "Tục tang ma": "Tục tang ma: Khi có người thân qua đời. Nghi thức tiễn biệt trang trọng thể hiện đạo hiếu và nghĩa tình cuối cùng.",
        "Treo câu đối": "Tục treo câu đối: Trước đêm Giao thừa. Chữ đỏ mang ý nghĩa cầu may mắn và răn dạy đạo đức cho con cháu.",
        "Tục uống trà": "Tục uống trà: Thói quen hàng ngày. Thể hiện sự tinh tế, điềm đạm và phong cách tiếp đãi lịch sự của người Việt.",
        "Xin chữ": "Xin chữ đầu năm: Những ngày đầu xuân. Thể hiện truyền thống hiếu học và mong ước qua từng nét chữ phượng múa.",
        "Gói bánh chưng": "Gói bánh chưng: Từ 26-29 Tết. Bánh chưng vuông tượng trưng cho Đất và lòng biết ơn sâu sắc với nguồn cội.",
        "Giỗ Tổ": "Giỗ Tổ Hùng Vương: Ngày 10/03 âm lịch. Ngày hội toàn dân hướng về nguồn cội và công ơn dựng nước của vua Hùng.",
        "Lì xì": "Lì xì đầu năm: Trong những ngày Tết. Phong bao đỏ chúc may mắn, trẻ nhỏ hay ăn chóng lớn, người già thọ tỷ nam sơn."
    }
}

class MemoryGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Game Trí Nhớ: Phong Tục Việt Nam")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 20)
        self.big_font = pygame.font.SysFont("Arial", 40)
        
        self.scene = "MENU"
        self.current_theme = "Phong tục"
        self.running = True
        
        self.cards = []
        self.revealed = []
        self.selected = []
        self.matched_info = None 

    def setup_level(self, theme):
        self.current_theme = theme
        all_names = list(INFO_DATA[theme].keys())
        # Chọn ngẫu nhiên 8 phong tục từ 16 phong tục để tạo thành 16 ô (8 cặp)
        selected_items = random.sample(all_names, 8)
        game_list = selected_items * 2
        random.shuffle(game_list)
        
        self.cards = game_list
        self.revealed = [False] * 16
        self.selected = []

    def handle_click(self, pos):
        if self.scene == "MENU":
            if WIDTH//2 - 100 < pos[0] < WIDTH//2 + 100 and 400 < pos[1] < 480:
                self.start_intro("Phong tục")
            
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
        """Hàm tự động xuống dòng cho văn bản dài"""
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
                # Vẽ tên ngắn gọn lên thẻ
                small_txt = self.font.render(self.cards[i], True, BLACK)
                txt_rect = small_txt.get_rect(center=rect.center)
                self.screen.blit(small_txt, txt_rect)
            else:
                pygame.draw.rect(self.screen, BLUE, rect, border_radius=15)
                pygame.draw.rect(self.screen, BLACK, rect, 2, border_radius=15)

    def draw_popup(self, text):
        """Hiện thông tin chi tiết về phong tục khi tìm đúng cặp"""
        overlay = pygame.Surface((700, 350))
        overlay.fill((255, 250, 240)) # Màu nền giấy cũ
        rect = overlay.get_rect(center=(WIDTH//2, HEIGHT//2))
        pygame.draw.rect(self.screen, (139, 69, 19), rect, 6, border_radius=10) # Viền gỗ
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
            title = self.big_font.render("TRÒ CHƠI PHONG TỤC VIỆT", True, BLACK)
            self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 250))
            
            btn_rect = pygame.Rect(WIDTH//2 - 100, 450, 200, 80)
            pygame.draw.rect(self.screen, BLUE, btn_rect, border_radius=20)
            btn_txt = self.font.render("BẮT ĐẦU", True, WHITE)
            self.screen.blit(btn_txt, (btn_rect.centerx - btn_txt.get_width()//2, btn_rect.centery - btn_txt.get_height()//2))
            
        elif self.scene == "INTRO":
            txt = "Tìm các cặp phong tục giống nhau để khám phá văn hóa!"
            img = self.font.render(txt, True, BLACK)
            self.screen.blit(img, (WIDTH//2 - img.get_width()//2, HEIGHT//2))
            msg = self.font.render("Click bất kỳ để vào trò chơi", True, BLUE)
            self.screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2 + 60))
            
        elif self.scene == "GAMEPLAY":
            title = self.font.render(f"Chủ đề đang chơi: {self.current_theme}", True, (50, 50, 50))
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