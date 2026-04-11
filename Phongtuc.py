import pygame
import random
import sys

# --- CẤU HÌNH HỢP NHẤT ---
WIDTH, HEIGHT = 800, 600 
FPS = 30
WHITE, BLACK, GRAY = (255, 255, 255), (0, 0, 0), (200, 200, 200)
BLUE = (50, 150, 255)
GRID_SIZE = 4
CARD_SIZE = 160
MARGIN = 20

INFO_DATA = {
    "Ẩm thực": {
        "pho": "'Quốc hồn quốc túy' với sợi bánh gạo mềm, nước dùng trong vắt, thanh ngọt từ xương ống và hương hồi, quế đặc trưng. Được khẳng định chỗ đứng trên thị trường quốc tế khi đã được liệt kê vào từ điển Oxford từ những năm 2011.", 
        "bun_bo_hue": "Bún Bò Huế là món ăn đặc trưng của miền Trung, gây ấn tượng bởi nước dùng cay nồng, thơm mùi mắm ruốc với những sợi bún to, đậm đà.",
        "ruou_can": "Rượu Cần là biểu tượng văn hóa cộng đồng của Tây Nguyên, mang hương vị nồng nàn của núi rừng, thường được thưởng thức chung qua những chiếc cần tre.",
        "trung_vit_lon": "Trứng Vịt Lộn: món ăn dân dã đầy bổ dưỡng, thường ăn kèm cùng rau răm và gừng thái chỉ để cân bằng hương vị. Một món không thể bỏ qua khi đến thăm mảnh đất hình chữ S này",
        "banh_xeo": "Bánh Xèo: lớp vỏ vàng giòn rụm, nhân tôm thịt đầy đặn, gói trọn trong rau sống và chấm cùng nước mắm chua ngọt.", 
        "bánh Chưng - bánh Tét": "Bánh chưng và bánh tét không chỉ là món ăn ngày Tết mà còn là biểu tượng văn hóa gắn liền với ký ức sum họp của người Việt. Qua hình dáng, cách gói và ý nghĩa, hai loại bánh truyền thống phản ánh sự đa dạng vùng miền nhưng vẫn thống nhất trong tinh thần Tết cổ truyền.",
        "bánh Pía": "Đặc sản Sóc Trăng với lớp vỏ mỏng nhiều lớp ôm lấy nhân đậu xanh, sầu riêng và trứng muối thơm lừng.",
        "bún Chả Hà Nội": "Sự kết hợp hài hòa giữa thịt nướng cháy cạnh thơm nức xì dầu và bát nước chấm đu đủ xanh hài hòa vị chua cay mặn ngọt.",
        "Cà Phê Trứng": "Sự giao thoa tinh tế giữa vị đắng của cà phê và lớp kem trứng đánh bông mịn màng, béo ngậy như một món tráng miệng cao cấp.",
        "Cơm Tấm": "Món ăn đặc trưng của Sài Gòn với hạt cơm vụn độc đáo, ăn kèm sườn nướng than, bì chả và nước mắm kẹo.",
        "Cơm Lam Gà Nướng": "Hương vị vùng cao với gạo nếp dẻo thơm trong ống tre nướng, ăn cùng gà thả vườn nướng vàng óng, là một cặp bài trùng khi được thưởng thức cùng với muối lá é đặc trưng",
        "Bún Đậu Mắm Tôm": "Món ăn gây 'nghiện' bởi sự tương phản thú vị giữa bún lá thanh mát, đậu rán giòn và mùi vị nồng nàn, đặc trưng của mắm tôm. Song, lâu dần cũng xuất hiện thêm nhiều biến thể như bún đậu nước mắm, nước tương ,...",
        "Gỏi Cuốn": "Món ăn dân dã vô cùng quen thuộc với người dân miền Nam. Với những nguyên liệu đơn giản như tôm, thịt, rau, bánh tráng, bạn có thể vào bếp chế biến ngay những chiếc gỏi cuốn thơm ngon ngay tại nhà.",
        "Mì Quảng": "Tinh túy ẩm thực Quảng Nam với sợi mì vàng, to,  ít nước lèo đậm đặc, ăn kèm bánh tráng nướng, đậu phộng rang và gà xé phay.",
        "Nem Chua": "Đặc sản Thanh Hóa có vị chua thanh, giòn sần sật từ bì lợn và tỏi ớt, món nhắm lý tưởng trong mọi cuộc vui.",
        "Bánh Mì": "'Vua đường phố' thế giới với vỏ ngoài giòn tan, bên trong đầy ắp pate, thịt nguội, bơ và rau dưa tươi mát."
    },
    "Văn hóa": {
        "Ba Na": "Từ nghề dệt thổ cẩm thủ công, nhuộm từ lá và vỏ cây rừng. Màu đen/đỏ chủ đạo. Nam đóng khố, nữ váy hở, hoa văn đối xứng.",
        "Thái": "Gắn liền với vùng thung lũng Tây Bắc và nghề dệt tằm tang. Áo cỏm ôm sát, hàng khuy bạc hình bướm và chiếc khăn Piêu thêu tay.",
        "Chăm": "Nền văn minh Chămpa cổ đại, ảnh hưởng Ấn Độ và Hồi giáo. Áo dài chui đầu Patra, quấn xà rông và thắt lưng dệt tinh xảo.",
        "Dao Đỏ": "Đời sống du canh vùng núi cao, tự dệt vải lanh nhuộm chàm. Sắc đỏ rực rỡ, khăn đội đầu khổ lớn kèm tua rua và trang sức bạc.",
        "Ê Đê": "Truyền thống mẫu hệ Tây Nguyên, dệt sợi bông nhuộm màu tự nhiên. Áo chui đầu, váy tấm đen-đỏ, kỹ thuật dệt Kteh đính cườm độc đáo.",
        "H'Mông": "Văn hóa rẻo cao, kỹ thuật vẽ sáp ong và nhuộm chàm thủ công. Váy xòe dập ly, thêu ghép vải màu rực rỡ và bộ xà tích bạc.",
        "Kinh": "Văn minh lúa nước, biến đổi từ áo giao lĩnh đến áo dài hiện đại. Áo dài xẻ tà cao, quần ống rộng, nón lá, chất liệu lụa thanh lịch.",
        "Khmer": "Văn hóa Angkor và Phật giáo Nam tông, sử dụng tơ lụa dệt Hol. Quấn Săm-pốt, áo tầm vông, khăn Sbay quàng vai màu sắc rực rỡ."
    },
   "Phong tục": {
        "Tết Nguyên Đán": "(Từ 23 tháng Chạp đến mùng 3 Tết): Lễ hội lớn nhất trong năm của người Việt, đánh dấu sự giao thoa giữa năm cũ và năm mới. Đây là dịp để gia đình sum vầy, tri ân tổ tiên qua mâm ngũ quả và những bữa cơm tất niên ấm cúng.",
        "Ông Công Ông Táo": "(Ngày 23 tháng Chạp âm lịch): Người Việt thực hiện nghi lễ thả cá chép ra sông hồ để tiễn các vị thần Bếp về trời báo cáo việc nhà, cầu mong một năm mới sung túc.",
        "Gói bánh chưng": "(Từ 26 đến 29 Tết): Bánh chưng vuông tượng trưng cho Đất và lòng biết ơn nguồn cội. Tục quây quần bên nồi bánh đỏ lửa đêm cuối năm là biểu tượng thiêng liêng nhất của sự gắn kết gia đình.",
        "Đi chùa đầu năm": "(Từ đêm Giao thừa đến hết tháng Giêng): Không chỉ để cầu xin bình an, tài lộc mà còn là khoảnh khắc tìm về sự thanh tịnh. Đây là nét đẹp tâm linh gắn liền với tục 'hái lộc' mang may mắn về nhà.",
        "Xin chữ": "(Những ngày đầu xuân): Thường diễn ra tại các 'phố ông đồ', thể hiện truyền thống hiếu học và tinh thần tôn sư trọng đạo. Mỗi nét chữ gửi gắm ước nguyện về sự thành đạt và bình an.",
        "Lì xì": "(Mùng 1 đến mùng 3 Tết): Những phong bao đỏ rực rỡ tượng trưng cho may mắn kèm theo lời chúc 'hay ăn chóng lớn' cho trẻ nhỏ và sức khỏe cho người già. Ý nghĩa nằm ở tình cảm dành cho nhau.",
        "Giỗ Tổ": "(Ngày 10/03 âm lịch): Ngày hội toàn dân hướng về Đền Hùng (Phú Thọ) để tưởng nhớ công ơn dựng nước của các vị vua Hùng, nhắc nhở đạo lý 'Uống nước nhớ nguồn'.",
        "Tết Trung thu": "(Rằm tháng Tám âm lịch): Được coi là ngày tết của tình thân và sự đoàn viên cho trẻ em với các hoạt động rước đèn cá chép, múa lân và phá cỗ trông trăng dưới ánh rằm."
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
                small_txt = self.font.render(str(self.cards[i]), True, BLACK)
                txt_rect = small_txt.get_rect(center=rect.center)
                self.screen.blit(small_txt, txt_rect)
            else:
                pygame.draw.rect(self.screen, BLUE, rect, border_radius=15)
                pygame.draw.rect(self.screen, BLACK, rect, 2, border_radius=15)

    def draw_popup(self, text):
        overlay = pygame.Surface((700, 450)) # Tăng chiều cao popup
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
