from matplotlib.pylab import spacing
import pygame
import random
import os
import unicodedata
import re

# --- CẤU HÌNH  --- //////////////////////////
WIDTH, HEIGHT = 800, 500
FPS = 60
WHITE, BLACK, GRAY = (255, 255, 255), (0, 0, 0), (200, 200, 200)
GRID_SIZE = 4
#CARD_SIZE = 150
MARGIN = 20

# --- CẤU HÌNH NÚT BẤM (dễ chỉnh sửa) ---
BUTTON_START_X_RATIO = 0.15   # Tọa độ X bắt đầu (15% chiều rộng màn hình)
BUTTON_BOTTOM_MARGIN = 60     # Cách chân màn hình (px)
BUTTON_SPACING_RATIO = 0.03   # Khoảng cách giữa các nút (3% chiều rộng màn hình)
BUTTON_WIDTH_RATIO = 0.20     # Chiều rộng nút = 20% chiều rộng màn hình
BUTTON_HEIGHT_RATIO = 0.4    # Chiều cao nút = chiều rộng nút × 0.8

# --- DATABASE (Giao cho cả nhóm soạn nội dung) ---
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
                },
                "Phong tục": {
                    "Tết Nguyên Đán": "(Từ cuối tháng Chạp đến mùng 3 Tết): Lễ hội lớn nhất trong năm, là dịp 'tống cựu nghinh tân'. Mọi nghi thức từ dọn dẹp nhà cửa đến chúc Tết đều hướng về tinh thần đoàn viên và hiếu nghĩa.",
                    "Ông Công Ông Táo": "(Ngày 23 tháng Chạp âm lịch): Ngày các vị thần bếp cưỡi cá chép về trời. Người Việt thường chuẩn bị mũ áo giấy và cá chép thật để phóng sinh, mong những điều tốt đẹp được tâu báo với Ngọc Hoàng.",
                    "Gói bánh chưng": "(Từ 26 đến 29 Tết): Bắt nguồn từ sự tích Lang Liêu. Bánh hình vuông tượng trưng cho Đất, đại diện cho sự phồn thịnh của nền văn minh lúa nước và lòng biết ơn nguồn cội.",
                    "Đi chùa đầu năm": "(Từ đêm Giao thừa đến hết tháng Giêng): Khoảnh khắc tâm linh để gửi gắm ước vọng về sức khỏe và an nhiên. Đi kèm là tục 'hái lộc' để mang may mắn từ nơi linh thiêng về nhà.",
                    "Xin chữ": "(Những ngày đầu tháng Giêng): Nét đẹp đề cao tri thức và sự hướng thiện. Người xin thường chọn các chữ như Tâm, Phúc, Đức, Nhẫn... để thể hiện mục tiêu phấn đấu trong năm mới.",
                    "Lì xì": "(Từ mùng 1 đến mùng 10 Tết): Tiền mở hàng đặt trong bao đỏ để trừ tà ma và chúc may mắn. Quan trọng ở lời chúc tốt đẹp dành cho trẻ nhỏ và sự tôn kính dành cho người già.",
                    "Giỗ Tổ Hùng Vương": "(Ngày 10/03 âm lịch): Ngày hội tụ bản sắc dân tộc, khẳng định sức mạnh đại đoàn kết và lòng tự hào về dòng máu 'Con Rồng cháu Tiên', nhắc nhớ đạo lý 'Uống nước nhớ nguồn'.",
                    "Tết Trung thu": "(Ngày Rằm tháng Tám âm lịch): Bắt nguồn từ nghi lễ mừng mùa màng bội thu. Hình ảnh bánh nướng, bánh dẻo tượng trưng cho sự trọn vẹn của trời đất và tình cảm gia đình khăng khít.",
                    "Lễ cầu ngư": "(Tháng Giêng hoặc tháng Hai âm lịch): Gắn liền với tục thờ cá Ông. Bao gồm tế lễ trang nghiêm và phần hội (đua ghe, hò bả trạo), thể hiện sức mạnh tập thể và niềm tin vào biển cả.",
                    "Rằm tháng Giêng": "(Ngày 15/01 âm lịch): Còn gọi là Tết Thượng Nguyên. Người dân thường đến chùa dâng sao giải hạn, cầu nguyện cho mọi việc khởi đầu trong năm được hanh thông.",
                    "Tục ăn trầu": "(Diễn ra hàng ngày và trong nghi lễ): Gắn liền với 'Sự tích trầu cau'. Miếng trầu là biểu tượng cho sự gắn kết thủy chung, bền chặt giữa người với người.",
                    "Tục cưới hỏi": "(Ngày lành tháng tốt): Bao gồm các lễ Chạm ngõ, Ăn hỏi và Xin dâu. Lễ vật chứa đựng lời chúc phúc cho cặp đôi 'trăm năm tình viên mãn, bạc đầu nghĩa phu thê'.",
                    "Tục đốt vàng mã": "(Các ngày giỗ, Rằm và mồng 1): Thể hiện niềm tin 'trần sao âm vậy'. Đây là sợi dây kết nối tình cảm và lòng tưởng nhớ của người sống đối với tổ tiên.",
                    "Tục tang ma": "(Khi có người thân qua đời): Thể hiện đạo lý 'Nghĩa tử là nghĩa tận'. Các nghi lễ được thực hiện cẩn trọng để linh hồn người khuất được yên nghỉ và phù hộ cho hậu thế.",
                    "Tục treo câu đối": "(Trước đêm Giao thừa): Những đôi câu đối đỏ tượng trưng cho sự may mắn, trí tuệ và là lời nhắc nhở về đạo đức, lối sống cho con cháu trong nhà.",
                    "Tục uống trà": "(Mọi lúc trong ngày): Trà Việt thường là trà mộc hoặc ướp hoa. Thưởng trà là nghệ thuật đòi hỏi sự tĩnh lặng, thể hiện tính cách điềm đạm và lòng hiếu khách."
                },
                "Địa danh": {
                    "vinh_ha_long": "Vịnh Hạ Long là một trong những kỳ quan thiên nhiên nổi tiếng nhất của Việt Nam và đã được UNESCO công nhận là di sản thiên nhiên thế giới. Nơi đây có hàng nghìn hòn đảo đá vôi lớn nhỏ với nhiều hình dạng độc đáo nhô lên giữa làn nước xanh ngọc. Cảnh quan hùng vĩ cùng hệ thống hang động kỳ ảo khiến vịnh trở thành điểm du lịch hấp dẫn đối với du khách trong và ngoài nước.",
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
                    "chua_mot_cot":"Chùa Một Cột là ngôi chùa có kiến trúc độc đáo được xây dựng trên một cột đá giữa hồ nước. Công trình được xây dựng từ thời nhà Lý và mang ý nghĩa biểu tượng cho hoa sen - biểu tượng của sự thanh cao trong văn hóa Việt Nam. Đây là một trong những ngôi chùa nổi tiếng nhất ở Hà Nội.",
                    "cho_ben_thanh":"Chợ Bến Thành là khu chợ nổi tiếng và lâu đời của TP. Hồ Chí Minh. Chợ bày bán nhiều loại hàng hóa như quần áo, thủ công mỹ nghệ, đặc sản và đồ lưu niệm. Đây cũng là điểm tham quan quen thuộc của du khách khi đến thành phố."
                },},
    "Lịch sử": {
            "An_Duong_Vuong": "Sự kiện đánh dấu sự ra đời của nhà nước Âu Lạc với kinh đô Cổ Loa, nổi bật với kỹ thuật xây thành kiên cố và nỏ liên châu huyền thoại.",
            "Hai_Ba_Trung": "Cuộc khởi nghĩa vũ trang đầu tiên chống lại ách đô hộ phương Bắc, khẳng định sức mạnh và vai trò to lớn của phụ nữ Việt Nam.",
            "Ba_Trieu": "Hình tượng oai phong với câu nói 'cưỡi cơn gió mạnh, đạp luồng sóng dữ', biểu tượng bất diệt cho ý chí kiên cường, không chịu cúi đầu làm tì thiếp.",
            "chien_thang_bach_dang": "Trận thủy chiến vĩ đại đánh bại quân Nam Hán bằng trận địa cọc gỗ, chấm dứt vĩnh viễn 1000 năm Bắc thuộc, mở ra kỷ nguyên độc lập lâu dài.",
            "dinh_bo_linh": "Hành trình dẹp yên loạn 12 sứ quân, thống nhất đất nước và đặt quốc hiệu Đại Cồ Việt, củng cố mạnh mẽ nền độc lập non trẻ.",
            "le_hoan_pha_tong": "Cuộc kháng chiến oanh liệt đánh tan quân xâm lược nhà Tống cả trên bộ lẫn trên sông Bạch Đằng, buộc nhà Tống thừa nhận sức mạnh Đại Cồ Việt.",
            "doi_do_thang_long": "Quyết định mang tính bước ngoặt chuyển kinh đô về vùng đất 'Rồng cuộn hổ ngồi' Đại La, tạo tiền đề cho sự phát triển rực rỡ của kinh thành ngàn năm.",
            "Lý_Thường_Kiệt": "Trận chiến trên sông Như Nguyệt bẻ gãy ý chí xâm lược của nhà Tống gắn liền với bài thơ thần 'Nam quốc sơn hà' - bản Tuyên ngôn Độc lập đầu tiên.",
            "khang_chien_nguyen_mong": "Bản hùng ca chói lọi của quân dân nhà Trần với những trận đánh tan đạo quân hùng mạnh nhất thế giới, gắn liền với hào khí Đông A rực lửa.",
            "khoi_nghia_lam_son": "Cuộc kháng chiến trường kỳ 10 năm 'nằm gai nếm mật' đánh đuổi giặc Minh, mở ra thời kỳ phát triển thịnh vượng và để lại bản 'Bình Ngô Đại Cáo'.",
            "Quang_Trung": "Cuộc hành quân thần tốc mùa xuân năm Kỷ Dậu đánh tan 29 vạn quân Thanh chỉ trong 5 ngày, đỉnh cao của nghệ thuật quân sự đánh nhanh diệt gọn.",
            "phap_no_sung": "Sự kiện mở đầu cho quá trình thực dân Pháp xâm lược Việt Nam tại Đà Nẵng, đưa đất nước vào thời kỳ kháng chiến cam go chống lại vũ khí phương Tây.",
            "thanh_lap_dang": "Bước ngoặt vĩ đại hợp nhất các tổ chức cộng sản do Nguyễn Ái Quốc chủ trì, chấm dứt thời kỳ khủng hoảng về đường lối giải phóng dân tộc.",
            "cach_mang_thang_tam": "Cuộc tổng khởi nghĩa giành chính quyền rực rỡ và ngày 2/9/1945 khai sinh ra nước Việt Nam Dân chủ Cộng hòa tại quảng trường Ba Đình.",
            "dien_bien_phu": "Trận quyết chiến chiến lược kéo dài 56 ngày đêm 'lừng lẫy năm châu, chấn động địa cầu', buộc Pháp ký Hiệp định Geneva lập lại hòa bình miền Bắc.",
            "chien_dich_ho_chi_minh": "Chiến dịch quân sự cuối cùng mang tính quyết định, giải phóng hoàn toàn miền Nam và thống nhất đất nước vào trưa ngày 30/4/1975."
            },
}

class MemoryGame:
    def __init__(self):
        pygame.init()
        
        self.size_title = 75
        self.size_normal = 24
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        self.btn_images = {
            "Ẩm thực": pygame.image.load(os.path.join(BASE_DIR, "at_button.png")).convert_alpha(),
            "Văn hóa": pygame.image.load(os.path.join(BASE_DIR, "vh_button.png")).convert_alpha(),
            "Lịch sử": pygame.image.load(os.path.join(BASE_DIR, "ls_button.png")).convert_alpha(),
        }
        self.text_font_path = None
        for candidate in ["NotoSans.ttf"]:
            if os.path.exists(candidate):
                self.text_font_path = candidate
                break
        
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        #self.font = pygame.font.SysFont("Arial", self.size_normal)
        self.font = self.load_text_font(self.size_normal)
        
        sw, sh = WIDTH, HEIGHT
        grid_area_w, grid_area_h = sw * 0.8, sh * 0.8
        self.dynamic_size = int(min((grid_area_w - 3*MARGIN)/4, (grid_area_h - 3*MARGIN)/4))
            
        try:
            self.font_title = pygame.font.Font("Top Secret.ttf",self.size_title)
        except:
            # Phòng trường hợp sai đường dẫn file, dùng font mặc định để không lỗi game
            self.font_title = self.load_text_font(self.size_title)
            print("Không tìm thấy file Top Secret.ttf, đang dùng font mặc định.")

        
        # Trạng thái hệ thống
        self.scene = "MENU" # MENU, INTRO, GAMEPLAY
        self.current_theme = None
        self.running = True
        self.intro_start_time = 0
        self.sound_played = False
        
        try:
            self.bg_full = pygame.image.load("theme.jpg").convert()
        except FileNotFoundError:
            print("Không tìm thấy file ảnh background.png!")
            # Tạo một nền màu tạm thời nếu không có ảnh
            self.bg_full = pygame.Surface((self.WIDTH, self.HEIGHT))
            self.bg_full.fill((0, 0, 50)) # Màu xanh tối
        
        self.bg_current = None
        self.bg_gameplay = None
        self.scale_bg() #gọi hàm 
        self.intro_bg = None #ảnh nền intro

        self.btn_amthuc = pygame.Rect(0, 0, 0, 0)
        self.btn_vanhoa = pygame.Rect(0, 0, 0, 0)
        self.btn_lichsu = pygame.Rect(0, 0, 0, 0)
        self.update_menu_buttons((WIDTH, HEIGHT))

        
        # Logic Game ////////////////////////
        self.cards = []      # Danh sách các tấm ảnh/tên ảnh
        self.revealed = []   # Trạng thái lật (True/False)
        self.selected = []   # Lưu index của 2 ô đang chọn để so sánh
        self.matched_info = None # Lưu thông tin giáo dục để hiện Pop-up
        self.hide_pair_at = 0 # Mốc thời gian úp lại cặp thẻ không khớp
        self.flip_duration = 260 # Thời gian animation lật thẻ (ms)
        self.card_animations = {} # index -> {start, from, to}
        self.turn_count = 0
        self.game_completed = False
        self.btn_replay = pygame.Rect(0, 0, 0, 0)
        self.btn_change_theme = pygame.Rect(0, 0, 0, 0)
        self.culture_image_folders = {}
        self.popup_scroll_y = 0
        self.popup_scroll_step = 40
        self.popup_max_scroll = 0
        
        # Âm thanh chuyển cảnh
        pygame.mixer.init()
        self.intro_duration = 4000 # Thời gian dừng ở Intro (4 giây)
        try:
            self.sound_transition = pygame.mixer.Sound("transition.mp3") # Tên file âm thanh của nhóm
        except:
            self.sound_transition = None
            print("Không tìm thấy file âm thanh chuyển cảnh")

    def setup_level(self, theme):
        self.current_theme = self.normalize_text(theme)
        # Lấy danh sách tên ảnh từ Database của theme đó

        data = self.get_theme_data(self.current_theme)
        names = list(data.keys())
        self.culture_lookup = {}
        self.culture_image_folders = {}
        
        # Thêm phần load ảnh Intro Theme
        theme_files = {
            "Ẩm thực": "bg_amthuc.png",
            "Lịch sử": "bg_lichsu.jpg",
            "Văn hóa": "bg_vanhoa.jpg"
        }
        bg_path = theme_files.get(theme)
        if bg_path and os.path.exists(bg_path):
            self.intro_bg = pygame.image.load(bg_path).convert()
            # Scale ảnh cho vừa màn hình hiện tại
            sw, sh = self.screen.get_size()
            self.intro_bg = pygame.transform.smoothscale(self.intro_bg, (sw, sh))
        else:
            self.intro_bg = None # Nếu không tìm thấy ảnh thì để trống
            print(f"Cảnh báo: Không tìm thấy file {bg_path}")

        if self.current_theme == self.normalize_text("Văn hóa"):
            culture_sections = ["Trang phục Dân tộc", "Phong tục", "Địa danh"]
            section_image_folders = {
                "Trang phục Dân tộc": "Văn hóa",
                "Phong tục": "Phong tục",
                "Địa danh": "Địa danh",
            }
            names = []
            for section in culture_sections:
                section_data = data.get(section, {})
                for key, value in section_data.items():
                    names.append(key)
                    self.culture_lookup[key] = value
                    self.culture_image_folders[key] = section_image_folders.get(section, "Văn hóa")
        else:
            names = list(data.keys())
        # 2. CHỌN NGẪU NHIÊN 8 ẢNH từ 16 ảnh có trong danh sách
        if len(names) >= 8:
            selected_names = random.sample(names, 8)
        else:
            selected_names = names # Đề phòng nếu list không đủ 8

        # 3. Nhân đôi thành 16 thẻ và xáo trộn
        game_list = selected_names * 2 
        random.shuffle(game_list)
        
        self.cards = game_list
        self.revealed = [False] * 16
        self.selected = []
        self.hide_pair_at = 0
        self.card_animations = {}
        self.turn_count = 0
        self.game_completed = False
        self.matched_info = None
        self.popup_scroll_y = 0
        self.popup_max_scroll = 0
        
        # 4. TẢI ẢNH VÀO BỘ NHỚ
        self.card_images = {}
        for item_name in set(self.cards): 
            image_path = None
            # Tìm file ảnh (.png, .jpg, .jpeg, .webp) trong thư mục chủ đề tương ứng
            folder_hint = None
            if self.current_theme == self.normalize_text("Văn hóa"):
                folder_hint = self.culture_image_folders.get(item_name)

            image_path = self.find_image_path(self.current_theme, item_name, folder_hint)
            
            if image_path:
                img = pygame.image.load(image_path).convert_alpha()
                #img = pygame.transform.smoothscale(img, (self.dynamic_size, self.dynamic_size))
                self.card_images[item_name] = img
            else:
                print(f"LỖI: Chưa có ảnh cho '{item_name}' trong thư mục '{theme}'")
                temp_surface = pygame.Surface((self.dynamic_size, self.dynamic_size))
                temp_surface.fill(GRAY)
                self.card_images[item_name] = temp_surface

    def handle_click(self, pos):
        if self.scene == "MENU":
            
            if self.btn_amthuc.collidepoint(pos):
                self.start_intro("Ẩm thực")

            elif self.btn_vanhoa.collidepoint(pos):
                self.start_intro("Văn hóa")

            elif self.btn_lichsu.collidepoint(pos):
                self.start_intro("Lịch sử")
            # Kiểm tra click vào nút chọn Theme (Giao cho Sâm/Nghĩa vẽ nút)
            # if 100 < pos[0] < 300: self.start_intro("Ẩm thực")
            # elif 350 < pos[0] < 550: self.start_intro("Văn hóa")

            
        #elif self.scene == "INTRO":
            #khúc này thêm âm thanh ready go
            #self.scene = "GAMEPLAY" # Click để vào chơi
            
        elif self.scene == "GAMEPLAY":
            if self.game_completed:
                if self.btn_replay.collidepoint(pos):
                    self.setup_level(self.current_theme)
                elif self.btn_change_theme.collidepoint(pos):
                    self.scene = "MENU"
                    self.game_completed = False
                return

            if self.matched_info:
                self.matched_info = None
                self.popup_scroll_y = 0
                self.popup_max_scroll = 0
                return

            # Không cho lật thêm khi đã đủ 2 thẻ và đang chờ xử lý
            if len(self.selected) >= 2 or self.hide_pair_at or self.has_pending_hide_animation():
                return

            x, y = pos
            sw, sh = self.screen.get_size()
            
            # Tái sử dụng công thức tính toán từ draw_grid
            
            start_x = (sw - (4*self.dynamic_size + 3*MARGIN)) // 2
            start_y = (sh - (4*self.dynamic_size + 3*MARGIN)) // 2

            # Xác định tọa độ hàng/cột dựa trên vị trí chuột
            col = (x - start_x) // (self.dynamic_size + MARGIN)
            row = (y - start_y) // (self.dynamic_size + MARGIN)
            
            # Kiểm tra xem có click trúng vào phạm vi lưới 4x4 không
            if 0 <= col < 4 and 0 <= row < 4:
            # Tạo rect ảo để kiểm tra va chạm chính xác (tránh click vào khoảng trống MARGIN)
                card_rect = pygame.Rect(
                    start_x + col*(self.dynamic_size + MARGIN), 
                    start_y + row*(self.dynamic_size + MARGIN), 
                    self.dynamic_size, self.dynamic_size
            )
            if card_rect.collidepoint(pos):
                idx = row * 4 + col
                if not self.revealed[idx]:
                    self.start_card_animation(idx, True, pygame.time.get_ticks())
                    self.revealed[idx] = True
                    self.selected.append(idx)
                    if len(self.selected) == 2:
                        self.turn_count += 1

    def update(self):
        current_time = pygame.time.get_ticks()
        if self.scene == "INTRO":
            elapsed = current_time - self.intro_start_time
            if elapsed >= self.intro_duration:
                self.scene = "GAMEPLAY"
            return

        self.finish_card_animations(current_time)
                
        # Logic kiểm tra cặp bài
        if len(self.selected) == 2:
            idx1, idx2 = self.selected
            if self.cards[idx1] == self.cards[idx2]:
                # TRÙNG KHỚP -> Hiện Pop-up giáo dục
                item_name = self.cards[idx1]


                if self.current_theme == "Văn hóa":
                    self.matched_info = self.culture_lookup.get(item_name, "Chưa có dữ liệu cho mục này.")
                else:
                   self.matched_info = self.get_theme_data(self.current_theme)[item_name]
                self.popup_scroll_y = 0
                self.popup_max_scroll = 0

                self.selected = []
            else:
                # KHÔNG TRÙNG -> Chờ một nhịp ngắn rồi úp cùng lúc cả 2 thẻ
                if self.hide_pair_at == 0:
                    self.hide_pair_at = current_time + 700

        if self.hide_pair_at and current_time >= self.hide_pair_at and len(self.selected) == 2:
            idx1, idx2 = self.selected
            self.start_card_animation(idx1, False, current_time)
            self.start_card_animation(idx2, False, current_time)
            self.selected = []
            self.hide_pair_at = 0

        if (
            not self.game_completed
            and all(self.revealed)
            and not self.selected
            and not self.card_animations
        ):
            self.game_completed = True
            self.matched_info = None

    def start_card_animation(self, idx, to_state, current_time):
        from_state = self.revealed[idx]
        self.card_animations[idx] = {
            "start": current_time,
            "from": from_state,
            "to": to_state,
        }

    def finish_card_animations(self, current_time):
        finished = []
        for idx, anim in self.card_animations.items():
            if current_time - anim["start"] >= self.flip_duration:
                self.revealed[idx] = anim["to"]
                finished.append(idx)

        for idx in finished:
            del self.card_animations[idx]

    def has_pending_hide_animation(self):
        for anim in self.card_animations.values():
            if anim["to"] is False:
                return True
        return False
    
    def play_transition_sound(self):
        if self.sound_transition:
            self.sound_transition.play()

    def draw(self):

        if self.scene == "GAMEPLAY" and self.bg_gameplay:
            self.screen.blit(self.bg_gameplay, (0, 0))
        else:
            self.screen.blit(self.bg_current, (0, 0))
        #self.screen.blit(bg_full, (0, 0))
        
        if self.scene == "MENU":
            #lấy kích thước hiện tại
            self.curr_w = self.screen.get_width()
            self.curr_h = self.screen.get_height() 
            self.update_menu_buttons((self.curr_w, self.curr_h))
            
            #viết tên tiêu đề game
            #self.draw_text_title("FLIP GAME", (self.screen.get_width()*0.5, self.screen.get_height()*0.2))

            #nút bấm
            self.mouse_pos = pygame.mouse.get_pos()
            self.draw_image_button(self.btn_amthuc, "Ẩm thực")
            self.draw_image_button(self.btn_vanhoa, "Văn hóa")
            self.draw_image_button(self.btn_lichsu, "Lịch sử")
        elif self.scene == "INTRO":
            if hasattr(self, 'intro_bg') and self.intro_bg:
                self.screen.blit(self.intro_bg, (0, 0))
            else:
                self.screen.blit(self.bg_current, (0, 0))
            curr_w = self.screen.get_width()
            curr_h = self.screen.get_height()
            self.draw_text(f"Chủ đề: {self.current_theme}. Đang chuẩn bị vào game...", (curr_w // 2, curr_h // 2))

        elif self.scene == "GAMEPLAY":
            self.draw_grid()
            self.draw_side_text()
            if self.game_completed:
                self.draw_endgame_popup()
            elif self.matched_info:
                self.draw_popup(self.matched_info)

    def draw_endgame_popup(self):
        sw, sh = self.screen.get_size()

        dim = pygame.Surface((sw, sh), pygame.SRCALPHA)
        dim.fill((0, 0, 0, 170))
        self.screen.blit(dim, (0, 0))

        box_w = min(560, int(sw * 0.82))
        box_h = min(320, int(sh * 0.62))
        box_x = (sw - box_w) // 2
        box_y = (sh - box_h) // 2
        box_rect = pygame.Rect(box_x, box_y, box_w, box_h)

        pygame.draw.rect(self.screen, (18, 30, 45), box_rect, border_radius=20)
        pygame.draw.rect(self.screen, (108, 181, 255), box_rect, width=2, border_radius=20)

        title_font = self.load_text_font(max(24, int(self.size_normal * 1.45)))
        info_font = self.load_text_font(max(18, int(self.size_normal * 1.05)))
        btn_font = self.load_text_font(max(16, int(self.size_normal * 0.9)))

        title_img = title_font.render("HOAN THANH!", True, (235, 245, 255))
        title_rect = title_img.get_rect(center=(box_x + box_w // 2, box_y + 60))
        self.screen.blit(title_img, title_rect)

        info_text = f"Ban da hoan thanh trong {self.turn_count} luot"
        info_img = info_font.render(info_text, True, (209, 229, 255))
        info_rect = info_img.get_rect(center=(box_x + box_w // 2, box_y + 120))
        self.screen.blit(info_img, info_rect)

        btn_w = max(170, int(box_w * 0.33))
        btn_h = 56
        gap = 24
        total_w = btn_w * 2 + gap
        start_x = box_x + (box_w - total_w) // 2
        y = box_y + box_h - btn_h - 42

        self.btn_replay = pygame.Rect(start_x, y, btn_w, btn_h)
        self.btn_change_theme = pygame.Rect(start_x + btn_w + gap, y, btn_w, btn_h)

        self.draw_option_button(self.btn_replay, (29, 145, 95), (45, 178, 117), "Choi lai", btn_font)
        self.draw_option_button(self.btn_change_theme, (40, 90, 155), (58, 118, 195), "Doi chu de", btn_font)

    def draw_option_button(self, rect, color, hover_color, text, font):
        mouse_pos = pygame.mouse.get_pos()
        draw_color = hover_color if rect.collidepoint(mouse_pos) else color
        pygame.draw.rect(self.screen, draw_color, rect, border_radius=12)
        pygame.draw.rect(self.screen, (220, 235, 255), rect, width=1, border_radius=12)
        text_img = font.render(text, True, WHITE)
        text_rect = text_img.get_rect(center=rect.center)
        self.screen.blit(text_img, text_rect)
    
    def draw_button(self,rect, color, hover_color, text):
        if rect.collidepoint(self.mouse_pos):
            pygame.draw.rect(self.screen, hover_color, rect, border_radius=15)
        else:
            pygame.draw.rect(self.screen, color, rect, border_radius=15)
        self.draw_text(text, rect.center)

    def draw_image_button(self, rect, label):
        if label not in self.scaled_btn_images:
            return

        img = self.scaled_btn_images[label]
        mouse_pos = pygame.mouse.get_pos()

        # hover effect: màu nhạt khi bình thường, sáng khi hover
        if rect.collidepoint(mouse_pos):
            # Hover: màu đầy đủ + phóng to nhẹ
            scale = 1.05
            new_w = int(rect.width * scale)
            new_h = int(rect.height * scale)
            img_hover = pygame.transform.smoothscale(img, (new_w, new_h))
            img_hover.set_alpha(255)  # Màu đầy đủ
            draw_x = rect.centerx - new_w // 2
            draw_y = rect.centery - new_h // 2
            self.screen.blit(img_hover, (draw_x, draw_y))
        else:
            # Không hover: màu nhạt
            img_faded = img.copy()
            img_faded.set_alpha(140)  # Màu nhạt (có thể điều chỉnh 100-180)
            self.screen.blit(img_faded, rect.topleft)
            
    def update_menu_buttons(self, current_size=None):
        """
        Cập nhật vị trí và kích thước của 3 nút bấm ở menu chính.
        
        Các nút sẽ nằm thẳng hàng theo chiều ngang, bắt đầu từ tọa độ responsive
        Nút được đặt cách chân màn hình 20px (nằm ở khoảng 1/3 dưới cùng)
        Kích thước nút thay đổi theo kích thước màn hình để responsive.
        """
        if current_size is None:
            current_size = self.screen.get_size()

        sw, sh = current_size  # sw = chiều rộng, sh = chiều cao

        # 🎯 TÍNH TOÁN KÍCH THƯỚC NÚT
        # Chiều rộng nút = 20% chiều rộng màn hình (dễ điều chỉnh bằng BUTTON_WIDTH_RATIO)
        btn_w = int(sw * BUTTON_WIDTH_RATIO)
        # Chiều cao nút = chiều rộng × 1.05 (tạo hình chữ nhật hơi dài)
        btn_h = int(btn_w * BUTTON_HEIGHT_RATIO)

        # 🎯 TÍNH VỊ TRÍ CỦA 3 NÚT (dựa trên tỉ lệ màn hình)
        # Nút 1 (Ẩm thực) - ở vị trí đầu tiên
        x1 = int(sw * BUTTON_START_X_RATIO)
        # Y được tính cách chân màn hình BUTTON_BOTTOM_MARGIN px
        y1 = sh - btn_h - BUTTON_BOTTOM_MARGIN

        # Khoảng cách giữa các nút (responsive)
        btn_spacing = int(sw * BUTTON_SPACING_RATIO)

        # Nút 2 (Văn hóa) - cách nút 1 bằng (chiều rộng nút + khoảng cách)
        x2 = x1 + btn_w + btn_spacing
        y2 = y1  # Cùng hàng với nút 1

        # Nút 3 (Lịch sử) - cách nút 2 bằng (chiều rộng nút + khoảng cách)
        x3 = x2 + btn_w + btn_spacing
        y3 = y1  # Cùng hàng với các nút khác

        # 🎯 TẠO CÁC RECT CHO 3 NÚT
        self.btn_amthuc = pygame.Rect(x1, y1, btn_w, btn_h)
        self.btn_vanhoa = pygame.Rect(x2, y2, btn_w, btn_h)
        self.btn_lichsu = pygame.Rect(x3, y3, btn_w, btn_h)

        # 🎯 SCALE ẢNH CỦA 3 NÚT
        # Đảm bảo ảnh vừa vặn với kích thước các nút đã tính
        self.scaled_btn_images = {}

        for key, img in self.btn_images.items():
            # Bước 1: Cắt bỏ phần trong suốt quanh ảnh
            cropped_rect = img.get_bounding_rect()
            img_cropped = img.subsurface(cropped_rect)

            # Bước 2: Scale ảnh để vừa với kích thước nút
            img_scaled = pygame.transform.smoothscale(img_cropped, (btn_w, btn_h))

            self.scaled_btn_images[key] = img_scaled

    
    def get_rounded_image(self, surface, size, radius):
        #"""Hàm này cắt ảnh thành hình bo góc"""
        # 1. Tạo một Surface rỗng có hỗ trợ độ trong suốt
        mask = pygame.Surface(size, pygame.SRCALPHA)
        # 2. Vẽ một hình chữ nhật trắng đã bo góc lên đó
        pygame.draw.rect(mask, (255, 255, 255), (0, 0, *size), border_radius=radius)
        
        # 3. Scale ảnh gốc về đúng kích thước cần vẽ
        image = pygame.transform.smoothscale(surface, size)
        # 4. Chỉ giữ lại những phần ảnh nằm trong hình chữ nhật trắng của mask
        image.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
        return image

    def draw_grid(self):
        sw, sh = self.screen.get_size()
        # 3. Tính toán vị trí bắt đầu (offset) để lưới nằm chính giữa
        total_grid_w = GRID_SIZE * self.dynamic_size + (GRID_SIZE - 1) * MARGIN
        total_grid_h = GRID_SIZE * self.dynamic_size + (GRID_SIZE - 1) * MARGIN
        start_x = (sw - total_grid_w) // 2
        start_y = (sh - total_grid_h) // 2
        
        # Thiết lập Padding và độ bo góc
        PADDING = 6  # Khoảng cách để ảnh nằm lọt trong khung (tùy chỉnh theo ý bạn)
        CORNER_RADIUS = 15 # Độ bo góc của thẻ và ảnh
    
        # Kích thước thực tế của ảnh sau khi trừ padding
        inner_size = self.dynamic_size - (PADDING * 2)
            
        for i in range(16):
            row, col = i // 4, i % 4
            rect = pygame.Rect(
                start_x + col * (self.dynamic_size + MARGIN), 
                start_y + row * (self.dynamic_size + MARGIN), 
                self.dynamic_size, 
                self.dynamic_size
            )

            item_name = self.cards[i]
            anim = self.card_animations.get(i)

            if anim:
                progress = min(1, (pygame.time.get_ticks() - anim["start"]) / self.flip_duration)
                width_scale = max(0.06, abs(1 - 2 * progress))
                show_front = anim["from"] if progress < 0.5 else anim["to"]

                card_surface = pygame.Surface((self.dynamic_size, self.dynamic_size), pygame.SRCALPHA)
                local_rect = pygame.Rect(0, 0, self.dynamic_size, self.dynamic_size)

                if show_front:
                    self.draw_card_front(card_surface, local_rect, item_name, inner_size, PADDING, CORNER_RADIUS)
                else:
                    self.draw_card_back(card_surface, local_rect, CORNER_RADIUS)

                scaled_w = max(1, int(self.dynamic_size * width_scale))
                scaled_card = pygame.transform.smoothscale(card_surface, (scaled_w, self.dynamic_size))
                draw_x = rect.x + (self.dynamic_size - scaled_w) // 2
                self.screen.blit(scaled_card, (draw_x, rect.y))
            else:
                if self.revealed[i]:
                    self.draw_card_front(self.screen, rect, item_name, inner_size, PADDING, CORNER_RADIUS)
                else:
                    self.draw_card_back(self.screen, rect, CORNER_RADIUS)

    def draw_card_front(self, target_surface, rect, item_name, inner_size, padding, corner_radius):
        pygame.draw.rect(target_surface, WHITE, rect, border_radius=corner_radius)
        if item_name in self.card_images:
            raw_img = self.card_images[item_name]
            img_scaled = pygame.transform.smoothscale(raw_img, (inner_size, inner_size))
            mask = pygame.Surface((inner_size, inner_size), pygame.SRCALPHA)
            pygame.draw.rect(mask, (255, 255, 255), (0, 0, inner_size, inner_size), border_radius=corner_radius-2)
            img_scaled.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
            target_surface.blit(img_scaled, (rect.x + padding, rect.y + padding))
        else:
            pygame.draw.rect(target_surface, GRAY, rect, border_radius=corner_radius)

    def draw_card_back(self, target_surface, rect, corner_radius):
        pygame.draw.rect(target_surface, BLACK, rect, border_radius=corner_radius)
        pygame.draw.rect(target_surface, (58, 58, 58), rect, width=2, border_radius=corner_radius)
    

    def draw_popup(self, text):
        sw, sh = self.screen.get_size()

        # Lớp nền tối để tập trung ánh nhìn vào popup
        dim = pygame.Surface((sw, sh), pygame.SRCALPHA)
        dim.fill((8, 10, 16, 175))
        self.screen.blit(dim, (0, 0))

        # Kích thước popup responsive theo cửa sổ
        box_w = min(720, int(sw * 0.84))
        box_h = min(470, int(sh * 0.78))
        start_x = (sw - box_w) // 2
        start_y = (sh - box_h) // 2
        box_rect = pygame.Rect(start_x, start_y, box_w, box_h)

        # Bóng đổ
        shadow = pygame.Surface((box_w + 16, box_h + 16), pygame.SRCALPHA)
        pygame.draw.rect(shadow, (0, 0, 0, 120), shadow.get_rect(), border_radius=26)
        self.screen.blit(shadow, (start_x - 2, start_y + 8))

        # Khung chính kiểu glass card
        panel = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
        pygame.draw.rect(panel, (23, 28, 43, 236), (0, 0, box_w, box_h), border_radius=24)
        pygame.draw.rect(panel, (114, 159, 255, 165), (0, 0, box_w, box_h), width=2, border_radius=24)

        # Header nổi bật
        header_h = 72
        pygame.draw.rect(panel, (36, 56, 95, 210), (0, 0, box_w, header_h), border_top_left_radius=24, border_top_right_radius=24)
        pygame.draw.line(panel, (130, 180, 255, 170), (20, header_h), (box_w - 20, header_h), 1)
        self.screen.blit(panel, box_rect.topleft)

        # Font phụ cho tiêu đề/hint
        title_size = max(24, int(self.size_normal * 1.35))
        hint_size = max(14, int(self.size_normal * 0.72))
        title_font = self.load_text_font(title_size)
        hint_font = self.load_text_font(hint_size)

        title_img = title_font.render("THONG TIN VAN HOA", True, (235, 243, 255))
        title_rect = title_img.get_rect(midleft=(start_x + 24, start_y + header_h // 2))
        self.screen.blit(title_img, title_rect)

        hint_img = hint_font.render("Nhan chuot de dong", True, (180, 205, 255))
        hint_rect = hint_img.get_rect(midright=(start_x + box_w - 20, start_y + header_h // 2))
        self.screen.blit(hint_img, hint_rect)

        # Xử lý dữ liệu text
        if isinstance(text, dict):
            content = f"Nguon goc: {text['nguon_goc']}\n\nDac diem: {text['dac_diem']}"
        else:
            content = str(text)

        

        body_x = start_x + 26
        body_y = start_y + header_h + 22
        body_w = box_w - 52
        body_h = box_h - header_h - 36
        line_gap = 6

        body_lines = self.wrap_text(content, self.font, body_w)

        line_height = self.font.get_height() + line_gap
        total_content_h = len(body_lines) * line_height
        self.popup_max_scroll = max(0, total_content_h - body_h)
        self.popup_scroll_y = max(0, min(self.popup_scroll_y, self.popup_max_scroll))

        # Chỉ cho phép text vẽ trong khung nội dung để tạo hiệu ứng cuộn.
        prev_clip = self.screen.get_clip()
        self.screen.set_clip(pygame.Rect(body_x, body_y, body_w, body_h))

        y_offset = body_y - self.popup_scroll_y
        for line in body_lines:
            if line == "":
                y_offset += line_height
                continue
            text_surface = self.font.render(line, True, (244, 247, 255))
            self.screen.blit(text_surface, (body_x, y_offset))
            y_offset += line_height

        self.screen.set_clip(prev_clip)

        if self.popup_max_scroll > 0:
            note_img = hint_font.render("Lan chuot de xem them", True, (160, 196, 255))
            note_rect = note_img.get_rect(midleft=(body_x, start_y + box_h - 14))
            self.screen.blit(note_img, note_rect)

            track_x = start_x + box_w - 12
            track_y = body_y
            track_h = body_h
            pygame.draw.rect(self.screen, (70, 88, 122), (track_x, track_y, 4, track_h), border_radius=3)

            thumb_h = max(22, int(track_h * (body_h / max(total_content_h, 1))))
            thumb_y = track_y + int((self.popup_scroll_y / self.popup_max_scroll) * (track_h - thumb_h))
            pygame.draw.rect(self.screen, (170, 205, 255), (track_x - 1, thumb_y, 6, thumb_h), border_radius=4)

    def handle_popup_scroll(self, wheel_y):
        if self.scene != "GAMEPLAY" or not self.matched_info or self.game_completed:
            return

        # wheel_y > 0 là cuộn lên, < 0 là cuộn xuống.
        self.popup_scroll_y -= wheel_y * self.popup_scroll_step
        self.popup_scroll_y = max(0, min(self.popup_scroll_y, self.popup_max_scroll))
            
    # Hàm xuống dòng gọn để xử lý cả đoạn có xuống dòng thủ công
    def wrap_text(self, content_text, font_obj, width_limit):
        lines = []
        for paragraph in content_text.split("\n"):
            if not paragraph.strip():
                lines.append("")
                continue

            words = paragraph.split()
            current = words[0]
            for word in words[1:]:
                trial = f"{current} {word}"
                if font_obj.size(trial)[0] <= width_limit:
                    current = trial
                else:
                    lines.append(current)
                    current = word
            lines.append(current)
        return lines
    
    def draw_text_title(self, text, pos): #hàm này dùng để viết tên game do có font riêng
        text = self.normalize_text(text)
        img = self.font_title.render(text, True, WHITE)
        rect = img.get_rect(center=pos)
        self.screen.blit(img, rect)
        
    def draw_text(self, text, pos): #hàm này dùng để viết nội dung
        text = self.normalize_text(text)
        img = self.font.render(text, True, WHITE)
        rect = img.get_rect(center=pos)
        self.screen.blit(img, rect)
    def draw_side_text(self):
        width = self.screen.get_width()
        height = self.screen.get_height()

    # ===== GRID =====
        grid_area_w = width * 0.8
        grid_area_h = height * 0.8

        card_w = (grid_area_w - (GRID_SIZE - 1) * MARGIN) / GRID_SIZE
        card_h = (grid_area_h - (GRID_SIZE - 1) * MARGIN) / GRID_SIZE

        dynamic_size = int(min(card_w, card_h))

        total_grid_w = GRID_SIZE * dynamic_size + (GRID_SIZE - 1) * MARGIN
        start_x = (width - total_grid_w) // 2

    # ===== TEXT =====
        if self.current_theme == "Văn hóa":
            left_words = ["Văn", "Hóa"]
            right_words = ["Việt", "Nam"]
        elif self.current_theme == "Ẩm thực":
            left_words = ["Ẩm", "Thực"]
            right_words = ["Việt", "Nam"]
        elif self.current_theme == "Lịch sử":
            left_words = ["Lịch", "Sử"]
            right_words = ["Việt", "Nam"]
        else:
            return

    # ===== SPACE =====
        left_space = start_x
        right_space = width - (start_x + total_grid_w)
        side_space = min(left_space, right_space)

        margin_side = int(width * 0.03)
        safe_gap = 15

    # ===== AUTO SCALE (KHÔNG LAG) =====
    # thử tối đa 15 lần → đủ mượt
        best_size = 20
        for test_size in range(int(side_space * 0.8), 10, -4):
            font = pygame.font.Font("thu_phap.ttf", test_size)
            max_w = max(
                max(font.render(w, True, WHITE).get_width() for w in left_words),
                max(font.render(w, True, WHITE).get_width() for w in right_words)
                )

            spacing = test_size * 1.2
            total_h = spacing * len(left_words)

            if (
                max_w <= side_space - margin_side - safe_gap
                and total_h <= height * 0.9
            ):
                best_size = test_size
                break

        big_font = pygame.font.Font("thu_phap.ttf", best_size)
        spacing = best_size * 1.65 + height * 0.01

    # ===== VẼ TRÁI =====
        total_text_h = spacing * len(left_words)
        y = (height - total_text_h) // 2 + int(height * 0.07)
        for word in left_words:
            img = big_font.render(word, True, WHITE)

            x = margin_side
            if x + img.get_width() > start_x - safe_gap:
                x = start_x - img.get_width() - safe_gap

            self.screen.blit(img, (x, y))
            y += spacing

    # ===== VẼ PHẢI =====
        total_text_h = spacing * len(right_words)
        y = (height - total_text_h) // 2 + int(height * 0.07)

        for word in right_words:
            img = big_font.render(word, True, WHITE)

            x = width - img.get_width() - margin_side
            if x < start_x + total_grid_w + safe_gap:
                x = start_x + total_grid_w + safe_gap

            self.screen.blit(img, (x, y))
            y += spacing
    def start_intro(self, theme):
        self.setup_level(theme)
        self.scene = "INTRO"
        self.intro_start_time = pygame.time.get_ticks() # Lưu lúc bắt đầu Intro
        # Phát âm thanh ngay khi vào Intro
        if self.sound_transition:
            self.sound_transition.play()
        self.sound_played = True
        
    def scale_bg(self, current_size=None): #hàm này dùng để điều chỉnh kích thước
        # Hàm này sẽ lấy kích thước HIỆN TẠI của màn hình và scale ảnh gốc theo đó
        if current_size is None:
            current_size = self.screen.get_size() # Lấy (width, height) mới
        # Dùng smoothscale để chất lượng đẹp hơn khi co giãn
        self.bg_current = pygame.transform.smoothscale(self.bg_full, current_size)
        self.bg_gameplay = self.create_blurred_background(self.bg_current)
        print(f"Đã scale nền theo kích thước mới: {current_size}")
        
        # Cập nhật dynamic_size ngay tại đây
        sw, sh = current_size
        grid_area_w, grid_area_h = sw * 0.8, sh * 0.8
        self.dynamic_size = int(min((grid_area_w - 3*MARGIN)/4, (grid_area_h - 3*MARGIN)/4))
        
        #phần dưới này để fix cỡ chữ cho hợp
        scale_ratio = current_size[0] / 800 
        new_title_size = int(self.size_title * scale_ratio)
        new_normal_size = int(self.size_normal * scale_ratio)
        
        # Khởi tạo lại font với size mới
        try:
            self.font_title = pygame.font.Font("Top Secret.ttf", max(20, new_title_size))
            self.font = self.load_text_font(max(12, new_normal_size))
        except:
            self.font_title = pygame.font.SysFont("Arial", max(20, new_title_size))
            self.font = self.load_text_font(max(12, new_normal_size))
        self.update_menu_buttons(current_size)
        if hasattr(self, 'intro_bg') and self.intro_bg:
            sw, sh = self.screen.get_size()
            self.intro_bg = pygame.transform.smoothscale(self.intro_bg, (sw, sh))

    def normalize_text(self, value):
        if isinstance(value, str):
            return unicodedata.normalize("NFC", value)
        return value

    def normalize_lookup_key(self, value):
        if not isinstance(value, str):
            return ""
        text = unicodedata.normalize("NFKD", value)
        text = "".join(ch for ch in text if not unicodedata.combining(ch))
        text = text.lower().strip()
        text = re.sub(r"[\s_\-]+", "", text)
        return text

    def get_theme_data(self, theme):
        normalized_theme = self.normalize_text(theme)
        for key, value in INFO_DATA.items():
            if self.normalize_text(key) == normalized_theme:
                return value
        raise KeyError(f"Không tìm thấy dữ liệu cho chủ đề: {theme}")

    def find_image_path(self, theme, item_name, folder_hint=None):
        normalized_item_name = self.normalize_text(item_name)
        lookup_key = self.normalize_lookup_key(item_name)
        candidate_folders = []

        if folder_hint:
            candidate_folders.append(self.normalize_text(folder_hint))

        candidate_folders.append(self.normalize_text(theme))

        # Bổ sung thêm các thư mục liên quan để dự phòng sai cấu trúc thư mục ảnh
        if self.normalize_text(theme) == self.normalize_text("Văn hóa"):
            candidate_folders.extend([
                self.normalize_text("Phong tục"),
                self.normalize_text("Địa danh"),
                self.normalize_text("Văn hóa"),
            ])

        # Loại trùng nhưng giữ thứ tự ưu tiên
        ordered_unique_folders = []
        for folder in candidate_folders:
            if folder and folder not in ordered_unique_folders:
                ordered_unique_folders.append(folder)

        for folder in ordered_unique_folders:
            if not os.path.isdir(folder):
                continue
            for filename in os.listdir(folder):
                stem, ext = os.path.splitext(filename)
                if ext.lower() not in ['.png', '.jpg', '.jpeg', '.webp']:
                    continue

                # So khớp chính xác trước, sau đó fallback so khớp mềm.
                if self.normalize_text(stem) == normalized_item_name:
                    return os.path.join(folder, filename)

                if lookup_key in self.normalize_lookup_key(stem):
                    return os.path.join(folder, filename)
        return None

    def load_text_font(self, size):
        if self.text_font_path:
            return pygame.font.Font(self.text_font_path, size)
        return pygame.font.SysFont("Arial", size)

    def create_blurred_background(self, source_surface):
        sw, sh = source_surface.get_size()

        # Multi-pass blur: giảm kích thước theo nhiều mức rồi scale ngược lại.
        # Cách này cho cảm giác blur mềm hơn so với chỉ 1 lần thu/phóng.
        blurred = source_surface.copy()
        for factor in (2, 4, 6, 8):
            small_w = max(1, sw // factor)
            small_h = max(1, sh // factor)
            blurred = pygame.transform.smoothscale(blurred, (small_w, small_h))
            blurred = pygame.transform.smoothscale(blurred, (sw, sh))

        # Trộn thêm vài lớp lệch nhẹ để giảm cảm giác răng cưa/pixel.
        mixed = pygame.Surface((sw, sh), pygame.SRCALPHA)
        offsets = [(-2, 0), (2, 0), (0, -2), (0, 2), (-1, -1), (1, 1), (0, 0)]
        layer_alpha = 36
        for ox, oy in offsets:
            layer = blurred.copy()
            layer.set_alpha(layer_alpha)
            mixed.blit(layer, (ox, oy))

        return mixed.convert()
        

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
                game.screen = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)
                    
                # Gọi hàm scale lại ảnh nền theo kích thước mới này
                game.scale_bg((new_width, new_height))
                game.curr_h = new_height
                game.curr_w = new_width
                                
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                game.handle_click(event.pos)
            if event.type == pygame.MOUSEWHEEL:
                game.handle_popup_scroll(event.y)
        
        game.update()
            
        pygame.display.flip()
    pygame.quit()