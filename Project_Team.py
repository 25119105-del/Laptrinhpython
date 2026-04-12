import pygame
import random
import os

# --- CẤU HÌNH  --- //////////////////////////
WIDTH, HEIGHT = 800, 600
FPS = 30
WHITE, BLACK, GRAY = (255, 255, 255), (0, 0, 0), (200, 200, 200)
GRID_SIZE = 4
CARD_SIZE = 150
MARGIN = 20

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
                }},
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
            "vinh_ha_Long": "Vịnh Hạ Long là một trong những kỳ quan thiên nhiên nổi tiếng nhất của Việt Nam và đã được UNESCO công nhận là di sản thiên nhiên thế giới. Nơi đây có hàng nghìn hòn đảo đá vôi lớn nhỏ với nhiều hình dạng độc đáo nhô lên giữa làn nước xanh ngọc. Cảnh quan hùng vĩ cùng hệ thống hang động kỳ ảo khiến vịnh trở thành điểm du lịch hấp dẫn đối với du khách trong và ngoài nước.",
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
            "cho_ben_thanh":"Chợ Bến Thành là khu chợ nổi tiếng và lâu đời của TP. Hồ Chí Minh. Chợ bày bán nhiều loại hàng hóa như quần áo, thủ công mỹ nghệ, đặc sản và đồ lưu niệm. Đây cũng là điểm tham quan quen thuộc của du khách khi đến thành phố."
        }


}

class MemoryGame:
    def __init__(self):
        pygame.init()
        
        self.size_title = 75
        self.size_normal = 24
        
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        #self.font = pygame.font.SysFont("Arial", self.size_normal)
        self.font = pygame.font.Font("font.ttf", 24)
        
        try:
            self.font_title = pygame.font.Font("Top Secret.ttf",self.size_title)
        except:
            # Phòng trường hợp sai đường dẫn file, dùng font mặc định để không lỗi game
            self.font_title = pygame.font.SysFont("Arial", self.size_title)
            print("Không tìm thấy file Top Secret.ttf, đang dùng font mặc định.")

        
        # Trạng thái hệ thống
        self.scene = "MENU" # MENU, INTRO, GAMEPLAY
        self.current_theme = None
        self.running = True
        
        try:
            self.bg_full = pygame.image.load("theme.png").convert()
        except FileNotFoundError:
            print("Không tìm thấy file ảnh background.png!")
            # Tạo một nền màu tạm thời nếu không có ảnh
            self.bg_full = pygame.Surface((self.WIDTH, self.HEIGHT))
            self.bg_full.fill((0, 0, 50)) # Màu xanh tối
        
        self.bg_current = None
        self.scale_bg() #gọi hàm 

        self.btn_amthuc = pygame.Rect(100, 250, 180, 80)
        self.btn_vanhoa = pygame.Rect(310, 250, 180, 80)
        self.btn_lichsu = pygame.Rect(520, 250, 180, 80)

        
        # Logic Game ////////////////////////
        self.cards = []      # Danh sách các tấm ảnh/tên ảnh
        self.revealed = []   # Trạng thái lật (True/False)
        self.selected = []   # Lưu index của 2 ô đang chọn để so sánh
        self.matched_info = None # Lưu thông tin giáo dục để hiện Pop-up

    def setup_level(self, theme):
        self.current_theme = theme
        data = INFO_DATA[theme]

        # 1. Lấy danh sách tên từ Database
        if theme == "Văn hóa":
            names = list(data["Trang phục Dân tộc"].keys())
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
        
        # 4. TẢI ẢNH VÀO BỘ NHỚ
        self.card_images = {}
        for item_name in set(self.cards): 
            image_path = None
            # Tìm file ảnh (.png, .jpg, .jpeg, .webp) trong thư mục chủ đề tương ứng
            for ext in ['.png', '.jpg', '.jpeg', '.webp']:
                temp_path = os.path.join(theme, item_name + ext)
                if os.path.exists(temp_path):
                    image_path = temp_path
                    break
            
            if image_path:
                img = pygame.image.load(image_path).convert_alpha()
                img = pygame.transform.smoothscale(img, (CARD_SIZE, CARD_SIZE))
                self.card_images[item_name] = img
            else:
                print(f"LỖI: Chưa có ảnh cho '{item_name}' trong thư mục '{theme}'")
                temp_surface = pygame.Surface((CARD_SIZE, CARD_SIZE))
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


                if self.current_theme == "Văn hóa":
                    self.matched_info = INFO_DATA["Văn hóa"]["Trang phục Dân tộc"][item_name]
                else:
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
        
        if self.scene == "MENU":
            #lấy kích thước hiện tại
            self.curr_w = self.screen.get_width()
            self.curr_h = self.screen.get_height()
            
            #viết tên tiêu đề game
            self.draw_text_title("FLIP GAME", (self.screen.get_width()*0.6, self.screen.get_height()*0.2))

            #nút bấm
            self.mouse_pos = pygame.mouse.get_pos()
            self.draw_button(self.btn_amthuc, (0,0,0), (255,255,255), "Ẩm thực")
            self.draw_button(self.btn_vanhoa, (50,150,255), (100,200,255), "Văn hóa")
            self.draw_button(self.btn_lichsu, (50,200,100), (100,255,150), "Lịch sử")
            
        elif self.scene == "INTRO":
            # Vẽ ảnh nền theme /////////////////////////////////
            curr_w = self.screen.get_width()
            curr_h = self.screen.get_height()
            self.draw_text(f"Chủ đề: {self.current_theme}. Click để bắt đầu!", (curr_w // 2, curr_h // 2))

        elif self.scene == "GAMEPLAY":
            self.draw_grid()
            if self.matched_info:
                self.draw_popup(self.matched_info)
    
    def draw_button(self,rect, color, hover_color, text):
        if rect.collidepoint(self.mouse_pos):
            pygame.draw.rect(self.screen, hover_color, rect, border_radius=15)
        else:
            pygame.draw.rect(self.screen, color, rect, border_radius=15)
            self.draw_text(text, rect.center)

    def draw_grid(self):
        # Đã cập nhật lại để vẽ Ảnh thay vì vẽ hình xám
        for i in range(16):
            row, col = i // 4, i % 4
            rect = pygame.Rect(80 + col*(CARD_SIZE+MARGIN), 80 + row*(CARD_SIZE+MARGIN), CARD_SIZE, CARD_SIZE)
            
            if self.revealed[i]:
                # Gọi ảnh đã tải ra để dán lên thẻ
                item_name = self.cards[i]
                if hasattr(self, 'card_images') and item_name in self.card_images:
                    self.screen.blit(self.card_images[item_name], rect.topleft)
                else:
                    pygame.draw.rect(self.screen, GRAY, rect)
            else:
                pygame.draw.rect(self.screen, BLACK, rect)

    def draw_popup(self, text):
        # 1. Vẽ bảng thông báo giáo dục (khung nền)
        overlay = pygame.Surface((600, 400))
        overlay.set_alpha(230) # Tăng độ mờ lên một chút để dễ đọc chữ hơn
        overlay.fill((40, 40, 40))
        
        # Đặt bảng ở giữa màn hình (tạm tính theo kích thước mặc định 800x600)
        start_x = (self.screen.get_width() - 600) // 2
        start_y = (self.screen.get_height() - 400) // 2
        self.screen.blit(overlay, (start_x, start_y))

        # 2. Xử lý dữ liệu text (Vì chủ đề Văn hóa là Dictionary, các chủ đề khác là String)
        content = ""
        if isinstance(text, dict):
            content = f"Nguồn gốc: {text['nguon_goc']}\n\nĐặc điểm: {text['dac_diem']}"
        else:
            content = str(text)

        # 3. Thuật toán tự động xuống dòng (Word Wrap)
        words = content.replace('\n', ' \n ').split(' ')
        lines = []
        current_line = []
        max_width = 560 # Giới hạn chiều rộng chữ để không tràn khỏi overlay (600 - lề 40)
        
        for word in words:
            if word == '\n':
                lines.append(' '.join(current_line))
                current_line = []
                continue
                
            current_line.append(word)
            # Tính toán kích thước của dòng hiện tại
            fw, fh = self.font.size(' '.join(current_line))
            if fw > max_width: # Nếu vượt quá giới hạn thì đẩy từ cuối xuống dòng mới
                current_line.pop()
                lines.append(' '.join(current_line))
                current_line = [word]
                
        if current_line:
            lines.append(' '.join(current_line))

        # 4. Vẽ từng dòng chữ lên màn hình
        y_offset = start_y + 30 # Cách lề trên của khung 30px
        for line in lines:
            text_surface = self.font.render(line, True, WHITE)
            self.screen.blit(text_surface, (start_x + 20, y_offset)) # Cách lề trái 20px
            y_offset += self.font.get_height() + 5 # Khoảng cách giữa các dòng
        
    def draw_text_title(self, text, pos): #hàm này dùng để viết tên game do có font riêng
        img = self.font_title.render(text, True, WHITE)
        rect = img.get_rect(center=pos)
        self.screen.blit(img, rect)
        
    def draw_text(self, text, pos): #hàm này dùng để viết nội dung
        img = self.font.render(text, True, WHITE)
        rect = img.get_rect(center=pos)
        self.screen.blit(img, rect)
        
    def start_intro(self, theme):
        self.setup_level(theme)
        self.scene = "INTRO"
    
    def scale_bg(self, current_size=None): #hàm này dùng để điều chỉnh kích thước
        # Hàm này sẽ lấy kích thước HIỆN TẠI của màn hình và scale ảnh gốc theo đó
        if current_size is None:
            current_size = self.screen.get_size() # Lấy (width, height) mới
        # Dùng smoothscale để chất lượng đẹp hơn khi co giãn
        self.bg_current = pygame.transform.smoothscale(self.bg_full, current_size)
        print(f"Đã scale nền theo kích thước mới: {current_size}")
        
        #phần dưới này để fix cỡ chữ cho hợp
        scale_ratio = current_size[0] / 800 
        new_title_size = int(self.size_title * scale_ratio)
        new_normal_size = int(self.size_normal * scale_ratio)
        
        # Khởi tạo lại font với size mới
        try:
            self.font_title = pygame.font.Font("Top Secret.ttf", max(20, new_title_size))
            self.font = pygame.font.SysFont("Arial", max(12, new_normal_size))
        except:
            self.font_title = pygame.font.SysFont("Arial", max(20, new_title_size))


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
                game.scale_bg((new_width, new_height))
                game.curr_h = new_height
                game.curr_w = new_width
                
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                game.handle_click(event.pos)
        
        #self.screen.blit(self.bg_current, (0, 0))
        
        if game.scene == "GAMEPLAY":
            game.update()
            
        pygame.display.flip()