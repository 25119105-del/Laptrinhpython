import pygame
import random

# --- CẤU HÌNH  --- //////////////////////////
WIDTH, HEIGHT = 800, 600
FPS = 30
WHITE, BLACK, GRAY = (255, 255, 255), (0, 0, 0), (200, 200, 200)
GRID_SIZE = 4
CARD_SIZE = 150
MARGIN = 20

# --- DATABASE (Giao cho cả nhóm soạn nội dung) ---
INFO_DATA = {
    "Ẩm thực": {"pho": "'Quốc hồn quốc túy' với sợi bánh gạo mềm, nước dùng trong vắt, thanh ngọt từ xương ống và hương hồi, quế đặc trưng. Được khẳng định chỗ đứng trên thị trường quốc tế khi đã được liệt kê vào từ điển Oxford từ những năm 2011.", 
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
                "Bánh Mì": "'Vua đường phố' thế giới với vỏ ngoài giòn tan, bên trong đầy ắp pate, thịt nguội, bơ và rau dưa tươi mát. Một trong những món ăn đã được đưa vào từ điển Oxford. Nhiều chuyên trang ẩm thực uy tín như The Guardian hay Lonely Planet liên tục xếp bánh mì Việt Nam vào danh sách những món ăn đường phố ngon nhất hành tinh."
                },
    "Văn hóa": {"Trang phục Dân tộc": {
                "Ba Na": {
                    "nguon_goc": "Từ nghề dệt thổ cẩm thủ công, nhuộm từ lá và vỏ cây rừng.",
                    "dac_diem": "Màu đen/đỏ chủ đạo. Nam đóng khố, nữ váy hở, hoa văn đối xứng."
                },
                "Thái": {
                    "nguon_goc": "Gắn liền với vùng thung lũng Tây Bắc và nghề dệt tằm tang.",
                    "dac_diem": "Áo cỏm ôm sát, hàng khuy bạc hình bướm và chiếc khăn Piêu thêu tay."
                },
                "Chăm": {
                    "nguon_goc": "Nền văn minh Chămpa cổ đại, ảnh hưởng Ấn Độ và Hồi giáo.",
                    "dac_diem": "Áo dài chui đầu Patra, quấn xà rông và thắt lưng dệt tinh xảo."
                },
                "Dao Đỏ": {
                    "nguon_goc": "Đời sống du canh vùng núi cao, tự dệt vải lanh nhuộm chàm.",
                    "dac_diem": "Sắc đỏ rực rỡ, khăn đội đầu khổ lớn kèm tua rua và trang sức bạc."
                },
                "Ê Đê": {
                    "nguon_goc": "Truyền thống mẫu hệ Tây Nguyên, dệt sợi bông nhuộm màu tự nhiên.",
                    "dac_diem": "Áo chui đầu, váy tấm đen-đỏ, kỹ thuật dệt Kteh đính cườm độc đáo."
                },
                "H'Mông": {
                    "nguon_goc": "Văn hóa rẻo cao, kỹ thuật vẽ sáp ong và nhuộm chàm thủ công.",
                    "dac_diem": "Váy xòe dập ly, thêu ghép vải màu rực rỡ và bộ xà tích bạc."
                },
                "Kinh": {
                    "nguon_goc": "Văn minh lúa nước, biến đổi từ áo giao lĩnh đến áo dài hiện đại.",
                    "dac_diem": "Áo dài xẻ tà cao, quần ống rộng, nón lá, chất liệu lụa thanh lịch."
                },
                "Khmer": {
                    "nguon_goc": "Văn hóa Angkor và Phật giáo Nam tông, sử dụng tơ lụa dệt Hol.",
                    "dac_diem": "Quấn Săm-pốt, áo tầm vông, khăn Sbay quàng vai màu sắc rực rỡ."
                },
                "Mường": {
                    "nguon_goc": "Vùng đất cổ Hòa Bình, Thanh Hóa với nghề dệt thổ cẩm lâu đời.",
                    "dac_diem": "Áo cánh ngắn, váy đen dài nổi bật với cạp váy dệt hoa văn tinh xảo."
                },
                "Nùng": {
                    "nguon_goc": "Truyền thống canh tác vùng Việt Bắc, nhuộm chàm xanh đen đặc trưng.",
                    "dac_diem": "Trang phục màu chàm đơn giản, áo cài cúc vải, viền tay áo màu sáng."
                },
                "Pà Thẻn": {
                    "nguon_goc": "Cư dân vùng núi cao Hà Giang, dệt hoa văn trực tiếp trên khung cửi.",
                    "dac_diem": "Màu đỏ rực rỡ như chim phượng hoàng, khăn đội đầu xếp nhiều lớp."
                },
                "Tày": {
                    "nguon_goc": "Cư dân thung lũng Việt Bắc, dệt vải chàm tự nhiên giản dị.",
                    "dac_diem": "Áo dài năm thân màu chàm, thắt lưng xanh, vòng cổ bạc bản lớn."
                },
                "Hoa": {
                    "nguon_goc": "Ảnh hưởng từ văn hóa Hán, sử dụng chất liệu gấm lụa cao cấp.",
                    "dac_diem": "Xường xám hoặc áo năm thân cài cúc vải, họa tiết rồng phượng thêu tay."
                },
                "Mảng": {
                    "nguon_goc": "Cư dân vùng cao Lai Châu, tự may váy áo phối hợp với vải mộc trắng.",
                    "dac_diem": "Tấm choàng trắng (Tà xịa) thêu chỉ đỏ và áo trang trí bằng nhiều hàng đồng xu bạc."
                },
                "Sán Dìu": {
                    "nguon_goc": "Cư dân trung du miền núi phía Bắc, dệt vải chàm bền chắc cho đi rừng.",
                    "dac_diem": "Áo dài bốn thân, váy xẻ hai mảnh quấn quanh hông và xà cạp bảo vệ chân."
                },
                "Thổ": {
                    "nguon_goc": "Giao thoa văn hóa Kinh - Mường vùng Nghệ An, Thanh Hóa.",
                        "dac_diem": "Váy đen có cạp dệt hoa văn tinh xảo, thắt lưng màu nổi và khăn vuông trắng."},
                }},
    "Lịch sử": {"dien_bien": "Chiến thắng Điện Biên Phủ...", "vua_hung": "Giỗ tổ Hùng Vương..."}
    
}

class MemoryGame:
    def __init__(self):
        pygame.init()
        
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24)
        
        # Trạng thái hệ thống
        self.scene = "MENU" # MENU, INTRO, GAMEPLAY
        self.current_theme = None
        self.running = True
        
        try:
            self.bg_full = pygame.image.load("theme.jpg").convert()
        except FileNotFoundError:
            print("Không tìm thấy file ảnh background.png!")
            # Tạo một nền màu tạm thời nếu không có ảnh
            self.bg_full = pygame.Surface((self.WIDTH, self.HEIGHT))
            self.bg_full.fill((0, 0, 50)) # Màu xanh tối
        
        self.bg_current = None
        self.scale_bg() #gọi hàm 
        
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
        self.screen.blit(self.bg_current, (0, 0))
        #self.screen.blit(bg_full, (0, 0))
        
        
        
        #self.screen.blit(self.bg_current, (0, 0))
        
        if self.scene == "MENU":
            curr_w = self.screen.get_width()
            curr_h = self.screen.get_height()
            self.draw_text("CHON CHU DE BAN MUON", (curr_w // 2, curr_h - 200))
            # Vẽ 3 nút ở đây...
            
        elif self.scene == "INTRO":
            # Vẽ ảnh nền theme /////////////////////////////////
            curr_w = self.screen.get_width()
            curr_h = self.screen.get_height()
            self.draw_text(f"Chủ đề: {self.current_theme}. Click để bắt đầu!", (curr_w // 2, curr_h // 2))

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
        img = self.font.render(text, True, WHITE)
        rect = img.get_rect(center=pos)
        self.screen.blit(img, rect)

    def start_intro(self, theme):
        self.setup_level(theme)
        self.scene = "INTRO"
    
    def scale_bg(self):
        # Hàm này sẽ lấy kích thước HIỆN TẠI của màn hình và scale ảnh gốc theo đó
        current_size = self.screen.get_size() # Lấy (width, height) mới
        # Dùng smoothscale để chất lượng đẹp hơn khi co giãn
        self.bg_current = pygame.transform.smoothscale(self.bg_full, current_size)
        print(f"Đã scale nền theo kích thước mới: {current_size}")

# --- CHẠY GAME ---
if __name__ == "__main__":
    game = MemoryGame()
    while game.running:
        game.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                game.running = False
            if event.type == pygame.VIDEORESIZE:
                new_width, new_height = event.w, event.h
                    
                # Cập nhật lại chế độ màn hình với kích thước mới
                screen = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)
                    
                # Gọi hàm scale lại ảnh nền theo kích thước mới này
                game.scale_bg()
                
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                game.handle_click(event.pos)
        
        #self.screen.blit(self.bg_current, (0, 0))
        
        if game.scene == "GAMEPLAY":
            game.update()
            
        pygame.display.flip()

