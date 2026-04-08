import pygame
import random

# --- CẤU HÌNH  --- //////////////////////////
WIDTH, HEIGHT = 800, 800
FPS = 30
WHITE, BLACK, GRAY = (255, 255, 255), (0, 0, 0), (200, 200, 200)
GRID_SIZE = 4
CARD_SIZE = 150
MARGIN = 20

# --- DATABASE (Giao cho cả nhóm soạn nội dung) ---ss
INFO_DATA = {
    "Ẩm thực": {"pho": "Phở là món ăn truyền thống...", "banh_mi": "Bánh mì Việt Nam..."},
    "Văn hóa": {"ao_dai": "Áo dài là trang phục...", "ca_tru": "Ca trù là loại hình..."},
    "Lịch sử": {"dien_bien": "Chiến thắng Điện Biên Phủ...", "vua_hung": "Giỗ tổ Hùng Vương..."},
    "Địa danh": {"vinh_ha_Long": "Vịnh Hạ Long là một trong những kỳ quan thiên nhiên nổi tiếng nhất của Việt Nam và đã được UNESCO công nhận là di sản thiên nhiên thế giới. Nơi đây có hàng nghìn hòn đảo đá vôi lớn nhỏ với nhiều hình dạng độc đáo nhô lên giữa làn nước xanh ngọc. Cảnh quan hùng vĩ cùng hệ thống hang động kỳ ảo khiến vịnh trở thành điểm du lịch hấp dẫn đối với du khách trong và ngoài nước.",
                 "pho_co_hoi_an": "Phố cổ Hội An là đô thị cổ nổi tiếng với những ngôi nhà mái ngói rêu phong và những con phố nhỏ yên bình. Nơi đây từng là thương cảng sầm uất từ thế kỷ XVI đến XVII, nơi giao lưu văn hóa giữa nhiều quốc gia. Vào buổi tối, ánh đèn lồng rực rỡ tạo nên khung cảnh rất thơ mộng và đặc trưng.",
                 "hang_son_doong": "Hang Sơn Đoòng được xem là hang động tự nhiên lớn nhất thế giới, nằm trong Vườn quốc gia Phong Nha Kẻ Bàng. Bên trong hang có những khối thạch nhũ khổng lồ, sông ngầm và cả khu rừng nguyên sinh. Đây là địa điểm khám phá nổi tiếng dành cho các nhà thám hiểm và du khách yêu thiên nhiên.",
                "dao_phu_quoc": "Đảo Phú Quốc là hòn đảo lớn nhất của Việt Nam, nằm trong vịnh Thái Lan. Hòn đảo nổi tiếng với những bãi biển cát trắng, làn nước trong xanh và hệ sinh thái đa dạng. Ngoài ra, Phú Quốc còn nổi tiếng với nước mắm truyền thống, hồ tiêu và nhiều khu nghỉ dưỡng hiện đại.",
                "cau_vang_ba_na_hills":"Cầu Vàng là cây cầu du lịch nổi tiếng nằm trong khu du lịch Bà Nà Hills. Điểm đặc biệt của cây cầu là hai bàn tay khổng lồ nâng đỡ cầu giữa núi rừng, tạo nên kiến trúc vô cùng độc đáo. Từ đây, du khách có thể ngắm nhìn toàn cảnh núi non và thiên nhiên tuyệt đẹp của Đà Nẵng.",
                "thanh_dia_my_son":"Thánh địa Mỹ Sơn là quần thể đền tháp cổ của vương quốc Chăm Pa được xây dựng từ nhiều thế kỷ trước. Nơi đây từng là trung tâm tôn giáo quan trọng của người Chăm. Những công trình kiến trúc bằng gạch với hoa văn tinh xảo thể hiện trình độ nghệ thuật và kỹ thuật cao của nền văn minh Chăm.",
                "kinh_thanh_hue": "Kinh thành Huế là quần thể cung điện, thành quách và lăng tẩm của triều Nguyễn triều đại phong kiến cuối cùng của Việt Nam. Công trình có kiến trúc đồ sộ và mang đậm phong cách truyền thống. Đây là một di sản văn hóa thế giới và là biểu tượng lịch sử của cố đô Huế.",
                "ruong_bac_thang":"Ruộng bậc thang Sa Pa là cảnh quan nông nghiệp độc đáo của vùng núi Tây Bắc do người dân tộc thiểu số tạo nên. Những thửa ruộng uốn lượn theo sườn núi tạo thành khung cảnh rất đẹp. Vào mùa lúa chín, cả vùng núi được phủ một màu vàng rực rỡ.",
                "ho_xuan_huong": "Hồ Xuân Hương nằm ngay trung tâm thành phố Đà Lạt và được xem là biểu tượng của thành phố này. Hồ có hình dạng cong nhẹ như vầng trăng và được bao quanh bởi rừng thông và vườn hoa. Khung cảnh nơi đây rất thơ mộng và thích hợp cho việc dạo bộ, đạp xe hay ngắm cảnh.",
                "van_mieu_quoc_tu_giam": "Văn Miếu Quốc Tử Giám được xây dựng từ thế kỷ XI và được xem là trường đại học đầu tiên của Việt Nam. Nơi đây thờ Khổng Tử và tôn vinh những người đỗ đạt trong các kỳ thi Nho học. Công trình là biểu tượng cho truyền thống hiếu học và tôn sư trọng đạo của dân tộc.",
                "dinh_doc_lap": "Dinh Độc Lập, còn gọi là Hội trường Thống Nhất, là một công trình lịch sử quan trọng của Việt Nam. Nơi đây gắn liền với sự kiện ngày 30/4/1975 khi chiến tranh kết thúc. Hiện nay dinh là một điểm tham quan nổi tiếng thu hút nhiều du khách.",
                "thac_ban_gioc":"Thác Bản Giốc là một trong những thác nước đẹp nhất Việt Nam, nằm trên biên giới giữa Việt Nam và Trung Quốc. Thác có nhiều tầng nước đổ xuống từ độ cao lớn tạo nên khung cảnh rất hùng vĩ. Vào mùa nước nhiều, dòng thác trắng xóa giữa núi rừng tạo nên cảnh tượng tuyệt đẹp.",
                "nui_ba_den":"Núi Bà Đen được mệnh danh là “nóc nhà Nam Bộ” với độ cao hơn 900 mét. Đây là địa điểm du lịch tâm linh nổi tiếng với nhiều chùa và tượng Phật lớn. Du khách có thể leo núi hoặc đi cáp treo để ngắm toàn cảnh vùng đồng bằng xung quanh.",
                "ho_hoan_kiem":"Hồ Hoàn Kiếm nằm ở trung tâm thủ đô Hà Nội và gắn liền với truyền thuyết vua Lê trả gươm thần cho rùa vàng. Giữa hồ có Tháp Rùa cổ kính, tạo nên hình ảnh đặc trưng của thành phố. Đây là nơi người dân và du khách thường đến tham quan, dạo bộ và thư giãn.",
                "chua_mot_cot":"Chùa Một Cột là ngôi chùa có kiến trúc độc đáo được xây dựng trên một cột đá giữa hồ nước. Công trình được xây dựng từ thời nhà Lý và mang ý nghĩa biểu tượng cho hoa sen – biểu tượng của sự thanh cao trong văn hóa Việt Nam. Đây là một trong những ngôi chùa nổi tiếng nhất ở Hà Nội.",
                "cho_ben_thanh":"Chợ Bến Thành là khu chợ nổi tiếng và lâu đời của TP. Hồ Chí Minh. Chợ bày bán nhiều loại hàng hóa như quần áo, thủ công mỹ nghệ, đặc sản và đồ lưu niệm. Đây cũng là điểm tham quan quen thuộc của du khách khi đến thành phố."}
                
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