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
    "Sự kiện Lịch sử": {
    "lap_nuoc_au_lac": "Sự kiện đánh dấu sự ra đời của nhà nước Âu Lạc năm 258 TCN với kinh đô chuyển về Cổ Loa. Điểm nhấn lịch sử là việc xây dựng thành Cổ Loa kiên cố cùng huyền thoại về nỏ thần liên châu, thể hiện bước tiến lớn về kỹ thuật quân sự.",
    "khoi_nghia_hai_ba_trung": "Cuộc khởi nghĩa quy mô lớn đầu tiên năm 40 chống lại ách đô hộ phương Bắc do Trưng Trắc và Trưng Nhị lãnh đạo, giành lại độc lập trong thời gian ngắn và khẳng định khí phách anh hùng của phụ nữ Việt Nam.",
    "khoi_nghia_ba_trieu": "Cuộc nổi dậy mạnh mẽ năm 248 chống lại nhà Ngô, gắn liền với hình tượng oai phong của Bà Triệu cưỡi voi ra trận cùng câu nói rực lửa 'cưỡi cơn gió mạnh, đạp luồng sóng dữ' trở thành biểu tượng bất diệt cho ý chí kiên cường.",
    "chien_thang_song_bach_dang": "Trận thủy chiến vĩ đại năm 938 của Ngô Quyền đánh bại quân Nam Hán bằng nghệ thuật cắm cọc gỗ bọc sắt dưới lòng sông, chấm dứt vĩnh viễn hơn 1000 năm Bắc thuộc và mở ra kỷ nguyên độc lập lâu dài cho dân tộc.",
    "dep_loan_12_su_quan": "Hành trình dẹp yên tình trạng cát cứ, thống nhất đất nước của Đinh Bộ Lĩnh năm 967 sau khi nhà Ngô suy yếu, dẫn đến việc lập nên nhà Đinh, xưng đế và đặt quốc hiệu là Đại Cồ Việt.",
    "le_hoan_pha_tong": "Cuộc kháng chiến oanh liệt năm 981 do Thập đạo tướng quân Lê Hoàn chỉ huy, đánh tan quân Tống xâm lược, bảo vệ vững chắc bờ cõi và buộc nhà Tống phải thừa nhận sức mạnh của Đại Cồ Việt.",
    "doi_do_ve_thang_long": "Quyết định mang tính bước ngoặt năm 1010 của Lý Công Uẩn, chuyển kinh đô từ Hoa Lư ra vùng đất 'Rồng cuộn hổ ngồi' Đại La, tạo tiền đề cho sự phát triển rực rỡ của kinh thành ngàn năm văn hiến.",
    "phong_tuyen_song_nhu_nguyet": "Trận chiến bẻ gãy ý chí xâm lược của quân Tống năm 1077 do Lý Thường Kiệt chỉ huy. Nơi đây vang lên bài thơ 'Nam quốc sơn hà', được xem như bản Tuyên ngôn Độc lập đầu tiên khẳng định chủ quyền quốc gia.",
    "chong_quan_nguyen_mong": "Bản hùng ca chói lọi của nhà Trần năm 1285 & 1288, đánh tan đạo quân hùng mạnh nhất thế giới bằng nghệ thuật chiến tranh du kích, 'vườn không nhà trống' và sức mạnh đoàn kết từ Hội nghị Diên Hồng.",
    "khoi_nghia_lam_son": "Cuộc kháng chiến trường kỳ mười năm (1418-1427) 'nếm mật nằm gai' đánh đuổi giặc Minh do Lê Lợi lãnh đạo, lập nên nhà Hậu Lê và để lại bản 'Bình Ngô Đại Cáo' bất hủ.",
    "chien_thang_ngoc_hoi_dong_da": "Cuộc hành quân thần tốc mùa xuân Kỷ Dậu 1789 của hoàng đế Quang Trung, đập tan 29 vạn quân Thanh xâm lược chỉ trong 5 ngày, đánh dấu đỉnh cao của nghệ thuật quân sự đánh nhanh, diệt gọn.",
    "phap_no_sung_tai_da_nang": "Sự kiện liên quân Pháp - Tây Ban Nha tấn công bán đảo Sơn Trà năm 1858, mở đầu xâm lược Việt Nam, đưa đất nước bước vào thời kỳ kháng chiến cam go chống lại vũ khí hiện đại phương Tây.",
    "thanh_lap_dang_cong_san": "Sự kiện hợp nhất các tổ chức cộng sản năm 1930 do Nguyễn Ái Quốc chủ trì, đánh dấu bước ngoặt vĩ đại trong phong trào cách mạng, chấm dứt thời kỳ khủng hoảng về đường lối giải phóng dân tộc.",
    "cach_mang_thang_tam": "Cuộc tổng khởi nghĩa năm 1945 thành công rực rỡ. Ngày 2/9, Chủ tịch Hồ Chí Minh đọc Tuyên ngôn Độc lập tại Ba Đình, chính thức khai sinh nước Việt Nam Dân chủ Cộng hòa.",
    "chien_thang_dien_bien_phu": "Trận quyết chiến chiến lược kéo dài 56 ngày đêm năm 1954, đập tan tập đoàn cứ điểm của Pháp, buộc Pháp ký Hiệp định Geneva mang ý nghĩa 'lừng lẫy năm châu, chấn động địa cầu'.",
    "chien_dich_ho_chi_minh": "Chiến dịch quân sự cuối cùng mang tính quyết định, với đỉnh điểm là xe tăng tiến vào Dinh Độc Lập trưa 30/4/1975, kết thúc 21 năm chiến tranh, giải phóng hoàn toàn miền Nam, thống nhất đất nước."
}
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