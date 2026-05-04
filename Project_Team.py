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
BUTTON_BOTTOM_MARGIN = 80     # Cách chân màn hình (px)
BUTTON_SPACING_RATIO = 0.03   # Khoảng cách giữa các nút (3% chiều rộng màn hình)
BUTTON_WIDTH_RATIO = 0.20     # Chiều rộng nút = 20% chiều rộng màn hình
BUTTON_HEIGHT_RATIO = 0.4    # Chiều cao nút = chiều rộng nút × 0.8

# --- DATABASE (Giao cho cả nhóm soạn nội dung) ---
INFO_DATA = {
    "Ẩm thực": {
            "pho": "Phở: 'Quốc hồn quốc túy' với sợi bánh gạo mềm, nước dùng trong vắt, thanh ngọt từ xương ống. Linh hồn của món ăn nằm ở hương hồi, quế và gừng nướng tạo nên mùi thơm nồng nàn đặc trưng. Món ăn đã khẳng định vị thế quốc tế khi được liệt kê chính thức vào từ điển Oxford từ năm 2011. Đây là biểu tượng không thể thay thế, đại diện cho sự tinh tế trong cách ăn uống của người Việt.",
            "bun_bo_hue": "Bún Bò Huế: Món ăn đặc trưng của miền Trung, gây ấn tượng bởi nước dùng cay nồng, đậm đà. Sự kết hợp hoàn hảo giữa mắm ruốc thơm nồng, sả tươi và những sợi bún to, tròn, dẻo dai. Ăn kèm với bắp bò thái mỏng, giò heo ninh mềm, huyết và chả cua tạo nên hương vị cố đô khó quên. Món ăn phản ánh nét văn hóa ẩm thực cung đình cầu kỳ nhưng vẫn gần gũi với đời sống người dân.",
            "ruou_can": "Rượu Cần: Biểu tượng văn hóa cộng đồng của Tây Nguyên, mang hương vị nồng nàn của núi rừng. Nguyên liệu từ gạo, ngô hoặc sắn trộn với men lá rừng đặc hữu, ủ kỹ trong các ché đất nung cổ. Cách thưởng thức độc đáo bằng cách dùng các cần tre dài hút trực tiếp, thể hiện sự gắn kết và đoàn kết. Thường được dùng trong các lễ hội đâm trâu, mừng lúa mới để tạ ơn thần linh và thắt chặt tình làng nghĩa xóm.",
            "trung_vit_lon": "Trứng Vịt Lộn: Món ăn dân dã đầy bổ dưỡng, là bài thuốc quý giúp cân bằng âm dương theo Đông y. Thường được thưởng thức kèm với rau răm cay nồng, gừng thái chỉ và một chút muối tiêu chanh đậm đà. Vị béo ngậy của lòng đỏ hòa quyện cùng vị ngọt của nước trứng tạo nên trải nghiệm ẩm thực độc đáo. Đây là món ăn đường phố quen thuộc, gắn liền với nhịp sống ban đêm hối hả tại mảnh đất hình chữ S.",
            "banh_xeo": "Bánh Xèo: Lớp vỏ vàng giòn rụm từ bột gạo và nghệ, mang theo âm thanh 'xèo xèo' vui tai khi chế biến. Nhân bánh đầy đặn với tôm tươi, thịt ba chỉ, giá đỗ và đậu xanh bùi bùi tỏa hương thơm hấp dẫn. Được gói trọn trong các loại rau sống vườn nhà và chấm cùng nước mắm chua ngọt pha chế cầu kỳ. Món ăn là hiện thân của sự trù phú từ vùng sông nước, gắn liền với những buổi họp mặt gia đình ấm cúng.",
            "bánh Chưng - bánh Tét": "Bánh Chưng - Bánh Tét: Biểu tượng văn hóa thiêng liêng gắn liền với ký ức sum họp trong ngày Tết cổ truyền. Gạo nếp dẻo thơm quấn lấy nhân đậu xanh bùi và thịt mỡ béo ngậy, ướp tiêu nồng nàn thơm phức. Hình dáng vuông tròn (Bánh Chưng đại diện cho Đất, Bánh Tét đại diện cho Trời) chứa đựng triết lý nhân sinh. Sự khác biệt vùng miền được thể hiện qua cách gói nhưng luôn thống nhất trong tinh thần hướng về nguồn cội.",
            "bánh Pía": "Bánh Pía: Đặc sản trứ danh của vùng đất Sóc Trăng với lớp vỏ mỏng nhiều lớp xếp chồng tinh tế. Nhân bánh là sự hòa quyện giữa đậu xanh xay nhuyễn, sầu riêng tươi thơm nức và trứng muối mặn nhẹ. Món bánh có nguồn gốc từ người Hoa di cư, trải qua thời gian đã trở thành niềm tự hào của ẩm thực miền Tây. Hương vị ngọt thanh, béo bùi khiến bánh Pía trở thành món quà quý giá cho khách phương xa ghé thăm.",
            "bún Chả Hà Nội": "Bún Chả Hà Nội: Sự kết hợp hài hòa giữa thịt nướng cháy cạnh thơm nức xì dầu và bát nước chấm đậm đà.  Những viên chả được nướng trên than củi hồng rực, tỏa mùi thơm đặc trưng len lỏi khắp các con phố cổ.  Ăn kèm với bún tươi và dưa góp từ đu đủ xanh, cà rốt hài hòa đủ vị chua, cay, mặn, ngọt tinh tế. Từng được cựu Tổng thống Mỹ Obama thưởng thức và khen ngợi, góp phần đưa tinh túy Tràng An ra thế giới.",
            "Cà Phê Trứng": "Cà Phê Trứng: Sự giao thoa tinh tế giữa vị đắng của cà phê và lớp kem trứng đánh bông mịn màng. Vị béo ngậy của lòng đỏ trứng gà kết hợp cùng mật ong tạo nên lớp màng mịn màng như món tráng miệng cao cấp. Thường được đặt trong bát nước nóng để giữ độ ấm, giúp hương vị cà phê luôn đậm đà và không bị tanh. Sáng tạo độc đáo này của người Hà Nội đã chinh phục những thực khách sành sỏi nhất trên toàn cầu.",
            "Cơm Tấm": "Cơm Tấm: Món ăn đặc trưng của Sài Gòn với những hạt cơm vụn độc đáo, mang hơi thở của đô thị năng động. Thành phần kinh điển bao gồm sườn nướng than hoa, bì heo thính thơm, chả trứng và một chút mỡ hành béo ngậy. Điểm nhấn quan trọng nhất là bát nước mắm kẹo sánh đặc, cay cay mặn mặn tưới đều lên đĩa cơm nóng hổi. Từ một món ăn bình dân của người lao động, cơm Tấm đã vươn mình trở thành biểu tượng ẩm thực sầm uất.",
            "Cơm Lam Gà Nướng": "Cơm Lam Gà Nướng: Hương vị đặc trưng của vùng cao với gạo nếp dẻo thơm được nướng chín trong ống tre xanh. Gà thả vườn được tẩm ướp gia vị núi rừng, nướng vàng óng trên lửa than tạo nên lớp da giòn, thịt ngọt. Là 'cặp bài trùng' hoàn hảo khi thưởng thức cùng muối lá é hoặc muối mè giữa không gian đại ngàn lộng gió. Món ăn không chỉ là thực phẩm mà còn là cách người dân vùng cao giữ gìn hồn cốt của rừng già.",
            "Bún Đậu Mắm Tôm": "Bún Đậu Mắm Tôm: Món ăn gây 'nghiện' bởi sự tương phản thú vị giữa các nguyên liệu mộc mạc và đậm đà. Bún lá thanh mát ăn kèm đậu hũ rán giòn tan, thịt chân giò luộc và các loại rau thơm đặc trưng như kinh giới. Linh hồn nằm ở bát mắm tôm được đánh bông với chanh ớt, tỏa mùi hương nồng nàn kích thích vị giác mạnh mẽ. Ngày nay, món ăn đã có nhiều biến thể phong phú nhưng mắm tôm vẫn là giá trị cốt lõi không thể thay thế.",
            "Gỏi Cuốn": "Gỏi Cuốn: Món ăn dân dã vô cùng quen thuộc, đại diện cho nét ẩm thực thanh đạm và tươi mới của người miền Nam. Nguyên liệu đơn giản gồm tôm luộc đỏ âu, thịt ba chỉ, bún tươi và hẹ xanh được cuộn chặt trong lớp bánh tráng mỏng. Chấm cùng tương đậu béo bùi hoặc mắm nêm đậm đà, tạo nên sự bùng nổ hương vị ngay từ miếng đầu tiên. Được CNN bình chọn là một trong những món ăn ngon nhất thế giới, phù hợp cho mọi lứa tuổi và chế độ ăn.",
            "Mì Quảng": "Mì Quảng: Tinh túy của vùng đất Quảng Nam nắng gió với sợi mì vàng, to, mang đậm dấu ấn miền Trung. Nước lèo được hầm đậm đặc, ít nhưng tinh túy, thấm đẫm vào từng sợi mì và miếng thịt gà xé phay ngọt lịm. Ăn kèm bánh tráng nướng giòn tan, đậu phộng rang thơm bùi và các loại rau sống Trà Quế nức tiếng gần xa. Món ăn thể hiện sự chân chất, nồng hậu của người dân xứ Quảng, ăn một lần là nhớ mãi hương vị quê hương.",
            "Nem Chua": "Nem Chua: Đặc sản trứ danh của Thanh Hóa với vị chua thanh đặc trưng được lên men từ thịt lợn tươi sống. Độ giòn sần sật của bì lợn kết hợp cùng vị cay nồng của tỏi ớt và mùi thơm của lá đinh lăng quấn quanh. Là món nhắm lý tưởng trong mọi cuộc vui, thường xuất hiện trong các mâm cỗ trang trọng hoặc bữa cơm sum họp. Nem chua không chỉ là món ăn mà còn là món quà tình thân, mang theo hơi thở của vùng đất miền Trung kiên cường.",
            "Bánh Mì": "Bánh Mì: 'Vua đường phố' thế giới với lớp vỏ ngoài giòn tan, bên trong mềm mại đầy ắp các loại nhân hấp dẫn. Sự hòa quyện giữa pate béo ngậy, thịt nguội, bơ, dưa chuột và rau dưa tạo nên một bản giao hưởng hương vị. Tự hào được đưa vào từ điển Oxford và liên tục đứng đầu các bảng xếp hạng ẩm thực uy tín như The Guardian. Bánh mì là minh chứng cho sự sáng tạo không giới hạn của người Việt, biến tấu từ món ăn ngoại quốc thành quốc bảo."
                },
    "Văn hóa": {
                "trang_phuc_dan_toc": {
                    "ba_na": "Trang phục Ba Na có nguồn gốc từ nghề dệt thổ cẩm thủ công, nhuộm màu từ lá và vỏ cây rừng. Đặc trưng với màu đen và đỏ, nam đóng khố, nữ mặc váy hở với hoa văn đối xứng.",

                    "thai": "Trang phục người Thái gắn với vùng Tây Bắc và nghề dệt tằm tang. Nổi bật với áo cóm ôm sát, hàng khuy bạc hình bướm và khăn Piêu thêu tay.",

                    "cham": "Trang phục Chăm bắt nguồn từ nền văn minh Chămpa cổ, chịu ảnh hưởng Ấn Độ và Hồi giáo. Đặc trưng với áo dài chui đầu Patra, xà rông và thắt lưng dệt tinh xảo.",

                    "dao_do": "Trang phục Dao Đỏ xuất phát từ đời sống vùng núi cao, sử dụng vải lanh nhuộm chàm. Nổi bật với sắc đỏ, khăn đội đầu lớn và trang sức bạc.",

                    "e_de": "Trang phục Ê Đê mang dấu ấn văn hóa mẫu hệ Tây Nguyên, sử dụng sợi bông nhuộm tự nhiên. Áo chui đầu, váy đen đỏ và kỹ thuật dệt Kteh độc đáo.",

                    "hmong": "Trang phục H'Mông thể hiện văn hóa vùng cao với kỹ thuật vẽ sáp ong và nhuộm chàm. Váy xòe, màu sắc rực rỡ và trang sức bạc đặc trưng.",

                    "kinh": "Trang phục người Kinh phát triển từ văn minh lúa nước, tiêu biểu là áo dài với tà xẻ cao, quần rộng và nón lá.",

                    "khmer": "Trang phục Khmer chịu ảnh hưởng văn hóa Angkor và Phật giáo Nam tông. Đặc trưng với Săm-pốt, áo tầm vông và khăn Sbay.",

                    "muong": "Trang phục Mường có nguồn gốc từ vùng Hòa Bình, Thanh Hóa. Áo cánh ngắn, váy đen dài và cạp váy dệt hoa văn tinh xảo.",

                    "nung": "Trang phục Nùng gắn với văn hóa Việt Bắc, sử dụng màu chàm. Áo đơn giản, cài cúc vải và viền tay áo sáng màu.",

                    "pa_then": "Trang phục Pà Thẻn nổi bật với màu đỏ rực, khăn đội đầu nhiều lớp và hoa văn dệt trực tiếp.",

                    "tay": "Trang phục Tày đơn giản với áo dài màu chàm, thắt lưng xanh và vòng cổ bạc.",

                    "hoa": "Trang phục người Hoa chịu ảnh hưởng văn hóa Hán, sử dụng gấm lụa. Thường là xường xám hoặc áo năm thân với họa tiết thêu.",

                    "mang": "Trang phục Mảng có tấm choàng trắng thêu chỉ đỏ và áo trang trí bằng nhiều đồng xu bạc.",

                    "san_diu": "Trang phục Sán Dìu gồm áo dài bốn thân, váy quấn và xà cạp bảo vệ chân.",
                    "tho": "Trang phục Thổ là sự giao thoa văn hóa Kinh - Mường, với váy đen, cạp hoa văn và thắt lưng màu nổi."
                }},
                "Phong tục": {
                    "Tết Nguyên Đán": "Tết Nguyên Đán(Từ cuối tháng Chạp đến mùng 3 Tết): Đây là cái Tết lớn nhất, khi mọi người gác lại lo toan để về nhà sum họp. Không chỉ là dọn dẹp nhà cửa cho sạch sẽ, sáng sủa mà còn là dịp để 'làm mới' tâm hồn, tha thứ cho nhau và cùng chúc nhau một năm mới vạn sự hanh thông, gia đình êm ấm.",
                    "Ông Công Ông Táo": "Ông Công Ông Táo(Ngày 23 tháng Chạp): Người Việt tin rằng đây là ngày các vị thần bếp cưỡi cá chép lên trời để 'báo cáo' việc lớn nhỏ trong nhà. Hình ảnh phóng sinh cá chép xuống sông hồ không chỉ là nghi lễ tâm linh mà còn thể hiện tấm lòng nhân ái, mong muốn những điều tốt đẹp nhất sẽ đến với gia đình.",
                    "Gói bánh chưng": "Gói bánh chưng(Từ 26 đến 29 Tết): Chiếc bánh vuông vức gói ghém bên trong là gạo nếp, đậu xanh, thịt mỡ - những hạt ngọc của đất trời. Cảm giác cả nhà quây quân bên nồi bánh đỏ lửa, thức xuyên đêm trò chuyện chính là hình ảnh ấm áp nhất của sự đoàn viên và lòng biết ơn tổ tiên.",
                    "Đi chùa đầu năm": "Đi chùa đầu năm(Từ Giao thừa đến hết tháng Giêng): Giữa không khí tĩnh lặng và mùi hương trầm thơm ngát, người ta đến chùa để tìm sự bình an trong tâm hồn. Tục 'hái lộc' hay xin quẻ đầu năm là cách người Việt gửi gắm hy vọng vào một năm mới sức khỏe dồi dào và gặp nhiều điều may mắn.",
                    "Xin chữ": "Xin chữ(Những ngày đầu tháng Giêng): Hình ảnh ông đồ già bên mực tàu giấy đỏ là nét đẹp tri thức của người Việt. Người ta đi xin chữ không chỉ để trang trí nhà cửa mà còn là cách để rèn tâm, hướng thiện, mong muốn con chữ ấy sẽ vận vào người để cả năm thông tuệ, học hành đỗ đạt.",
                    "Lì xì": "Lì xì(Từ mùng 1 đến mùng 10 Tết): Những phong bao đỏ thắm chứa đựng niềm vui dành cho con trẻ và sự kính trọng đối với người già. Quan trọng nhất không phải số tiền bên trong, mà là lời chúc 'hay ăn chóng lớn' cho trẻ nhỏ và 'sống lâu trăm tuổi' cho ông bà, cha mẹ.",
                    "Giỗ Tổ Hùng Vương": "Giỗ Tổ Hùng Vương(Ngày 10/03 âm lịch): Là ngày để mỗi người dân Việt dù ở đâu cũng hướng về cội nguồn dân tộc. Ngày này nhắc nhở chúng ta về tình đồng bào, về sức mạnh của sự đoàn kết và đạo lý sống đẹp: luôn nhớ về gốc gác, cha ông đã có công dựng nước.",
                    "Tết Trung thu": "Tết Trung thu(Ngày Rằm tháng Tám âm lịch): Là dịp trăng tròn và đẹp nhất, khi trẻ em được rước đèn, phá cỗ, còn người lớn thì cùng nhau thưởng trà, ăn bánh nướng, bánh dẻo. Đây là cái Tết của sự tình thân, là lúc mọi người dành thời gian chăm sóc và tạo niềm vui cho thế hệ mầm non.",
                    "Lễ cầu ngư": "Lễ cầu ngư(Tháng Giêng hoặc tháng Hai âm lịch): Đối với bà con vùng biển, đây là lễ hội quan trọng nhất để cảm ơn biển cả và thờ cúng cá Ông (cá voi). Tiếng hò bả trạo và những cuộc đua ghe sôi động thể hiện niềm tin mãnh liệt vào một mùa biển lặng, tôm cá đầy khoang.",
                    "Rằm tháng Giêng": "Rằm tháng Giêng(Ngày 15/01 âm lịch): Người xưa có câu 'Lễ Phật quanh năm không bằng Rằm tháng Giêng'. Đây là lúc mọi người đi chùa cầu nguyện cho sự khởi đầu của một năm mới được thuận buồm xuôi gió, công việc hanh thông và mọi sự dữ hóa lành.",
                    "Tục ăn trầu": "Tục ăn trầu(Diễn ra hàng ngày và trong nghi lễ): Miếng trầu cay nồng là 'đầu câu chuyện', giúp mọi người xích lại gần nhau hơn. Dù ngày nay ít người ăn trầu thường xuyên, nhưng trong các dịp lễ tết, cưới hỏi, cơi trầu vẫn là lễ vật quan trọng nhất để thể hiện tình cảm gắn bó, sắt son.",
                    "Tục cưới hỏi": "Tục cưới hỏi(Ngày lành tháng tốt): Đám cưới là sự kiện trọng đại, đánh dấu sự gắn kết của hai dòng họ. Từ lễ dạm ngõ đến lễ rước dâu, mỗi chi tiết đều mang ý nghĩa chúc phúc cho đôi trẻ có một đời sống vợ chồng hòa thuận, yêu thương và cùng nhau xây dựng tổ ấm vững bền.",
                    "Lễ mừng thọ": "Lễ mừng thọ(Dịp đầu Xuân hoặc sinh nhật): Khi ông bà, cha mẹ bước sang tuổi xế chiều, con cháu tổ chức lễ mừng thọ để tỏ lòng hiếu thảo. Hình ảnh con cháu quây quần chúc rượu, tặng bức tranh chữ 'Thọ' là niềm hạnh phúc lớn nhất của người già, khẳng định giá trị của gia đình.",
                    "Tục tang ma": "Tục tang ma(Khi có người thân qua đời): Đây là lúc tình làng nghĩa xóm và lòng hiếu thảo của con cái thể hiện rõ nhất. Các nghi lễ dù buồn thương nhưng luôn được thực hiện chu đáo để tiễn đưa người đã khuất về nơi yên nghỉ cuối cùng một cách thanh thản và trang nghiêm.",
                    "Tục treo câu đối": "Tục treo câu đối(Trước đêm Giao thừa): Những đôi câu đối đỏ dán hai bên cửa không chỉ làm ngôi nhà thêm rực rỡ mà còn là những lời răn dạy về đạo đức, lối sống. Màu đỏ tượng trưng cho may mắn, hy vọng xua đuổi điều không may và đón nhận niềm vui vào nhà.",
                    "Tục uống trà": "Tục uống trà(Mọi lúc trong ngày): Người Việt uống trà rất mộc mạc nhưng cũng đầy tinh tế. Một chén trà xanh nóng hổi mời khách hay chén trà ướp hoa thơm dịu của ông bà là cách thể hiện lòng hiếu khách, sự điềm đạm và thói quen sống chậm lại để lắng nghe, chia sẻ với nhau."
                },
               "Địa danh": {
    "vinh_ha_long": "Vịnh Hạ Long là một trong những kỳ quan thiên nhiên nổi tiếng nhất của Việt Nam và đã được UNESCO công nhận là di sản thiên nhiên thế giới. Nơi đây có hàng nghìn hòn đảo đá vôi lớn nhỏ với nhiều hình dạng độc đáo nhô lên giữa làn nước xanh ngọc. Cảnh quan hùng vĩ cùng hệ thống hang động kỳ ảo khiến vịnh trở thành điểm du lịch hấp dẫn đối với du khách trong và ngoài nước. Không chỉ nổi bật bởi vẻ đẹp ngoạn mục, vịnh còn mang giá trị địa chất đặc biệt với lịch sử hình thành kéo dài hàng trăm triệu năm, ghi dấu quá trình vận động của vỏ Trái Đất. Những hang động như Sửng Sốt, Thiên Cung ẩn chứa hệ thống nhũ đá lung linh tạo nên không gian huyền bí. Khi hoàng hôn buông xuống, toàn bộ mặt vịnh chuyển sang sắc vàng cam rực rỡ, phản chiếu trên mặt nước tĩnh lặng như một bức tranh sống động. Truyền thuyết Rồng mẹ hạ thế giúp dân đánh giặc càng làm tăng thêm chiều sâu văn hóa, khiến nơi đây không chỉ là danh thắng mà còn là biểu tượng thiêng liêng của thiên nhiên Việt Nam.",

    "pho_co_hoi_an": "Phố cổ Hội An là đô thị cổ nổi tiếng với những ngôi nhà mái ngói rêu phong và những con phố nhỏ yên bình. Nơi đây từng là thương cảng sầm uất từ thế kỷ XVI đến XVII, nơi giao lưu văn hóa giữa nhiều quốc gia. Vào buổi tối, ánh đèn lồng rực rỡ tạo nên khung cảnh rất thơ mộng và đặc trưng. Không gian phố cổ gần như giữ nguyên cấu trúc hàng trăm năm, tạo cảm giác như dòng thời gian ngưng đọng. Những công trình kiến trúc mang dấu ấn Nhật Bản, Trung Hoa và phương Tây hòa quyện tạo nên bản sắc độc nhất. Các lễ hội như thả hoa đăng trên sông Hoài mang lại trải nghiệm văn hóa sâu sắc. Ẩm thực địa phương, âm nhạc dân gian và nhịp sống chậm rãi khiến Hội An trở thành nơi không chỉ để tham quan mà còn để cảm nhận và sống cùng lịch sử.",

    "hang_son_doong": "Hang Sơn Đoòng được xem là hang động tự nhiên lớn nhất thế giới, nằm trong Vườn quốc gia Phong Nha Kẻ Bàng. Bên trong hang có những khối thạch nhũ khổng lồ, sông ngầm và cả khu rừng nguyên sinh. Đây là địa điểm khám phá nổi tiếng dành cho các nhà thám hiểm và du khách yêu thiên nhiên. Không gian bên trong rộng đến mức có thể chứa cả tòa nhà cao tầng, tạo cảm giác choáng ngợp tuyệt đối. Những hố sụt tự nhiên cho phép ánh sáng chiếu vào, hình thành hệ sinh thái riêng biệt với cây cối và khí hậu độc lập. Các khối thạch nhũ có hình thù kỳ lạ được hình thành qua hàng triệu năm. Sơn Đoòng không chỉ là điểm du lịch mà còn là biểu tượng cho vẻ đẹp nguyên sơ, bí ẩn và sức mạnh kiến tạo của thiên nhiên.",

    "dao_phu_quoc": "Đảo Phú Quốc là hòn đảo lớn nhất của Việt Nam, nằm trong vịnh Thái Lan. Hòn đảo nổi tiếng với những bãi biển cát trắng, làn nước trong xanh và hệ sinh thái đa dạng. Ngoài ra, Phú Quốc còn nổi tiếng với nước mắm truyền thống, hồ tiêu và nhiều khu nghỉ dưỡng hiện đại. Bên cạnh đó, đảo còn sở hữu các khu rừng nguyên sinh rộng lớn thuộc vườn quốc gia, nơi bảo tồn nhiều loài động thực vật quý hiếm. Các làng chài truyền thống mang đến cái nhìn chân thực về đời sống người dân ven biển. Hoàng hôn trên biển Phú Quốc được xem là một trong những khoảnh khắc đẹp nhất Việt Nam. Sự kết hợp giữa thiên nhiên hoang sơ và phát triển du lịch cao cấp đã giúp Phú Quốc trở thành điểm đến mang tầm quốc tế.",

    "cau_vang_ba_na_hills":"Cầu Vàng là cây cầu du lịch nổi tiếng nằm trong khu du lịch Bà Nà Hills. Điểm đặc biệt của cây cầu là hai bàn tay khổng lồ nâng đỡ cầu giữa núi rừng, tạo nên kiến trúc vô cùng độc đáo. Từ đây, du khách có thể ngắm nhìn toàn cảnh núi non và thiên nhiên tuyệt đẹp của Đà Nẵng. Công trình mang thiết kế sáng tạo, kết hợp giữa yếu tố nghệ thuật và cảnh quan thiên nhiên. Lớp rêu phong giả cổ tạo cảm giác như cây cầu đã tồn tại hàng trăm năm. Khi mây bao phủ, nơi đây giống như một lối đi giữa trời. Cầu Vàng nhanh chóng trở thành biểu tượng du lịch mới của Việt Nam trên truyền thông quốc tế.",

    "thanh_dia_my_son":"Thánh địa Mỹ Sơn là quần thể đền tháp cổ của vương quốc Chăm Pa được xây dựng từ nhiều thế kỷ trước. Nơi đây từng là trung tâm tôn giáo quan trọng của người Chăm. Những công trình kiến trúc bằng gạch với hoa văn tinh xảo thể hiện trình độ nghệ thuật và kỹ thuật cao của nền văn minh Chăm. Các đền tháp được xây dựng theo tín ngưỡng Hindu giáo, thờ thần Shiva. Dù bị tàn phá bởi thời gian và chiến tranh, nơi đây vẫn giữ được nét linh thiêng đặc biệt. Không gian thung lũng bao quanh tạo nên cảm giác huyền bí. Mỹ Sơn là minh chứng rõ nét cho một nền văn hóa cổ từng phát triển rực rỡ tại Việt Nam.",

    "kinh_thanh_hue": "Kinh thành Huế là quần thể cung điện, thành quách và lăng tẩm của triều Nguyễn triều đại phong kiến cuối cùng của Việt Nam. Công trình có kiến trúc đồ sộ và mang đậm phong cách truyền thống. Đây là một di sản văn hóa thế giới và là biểu tượng lịch sử của cố đô Huế. Toàn bộ công trình được xây dựng theo nguyên tắc phong thủy chặt chẽ, phản ánh tư duy phương Đông. Các cung điện, sân chầu và lăng tẩm đều mang nét trang nghiêm, tinh xảo. Không gian nơi đây gợi lên sự trầm mặc và cổ kính. Huế không chỉ là di tích mà còn là nơi lưu giữ ký ức của một thời kỳ lịch sử.",

    "ruong_bac_thang":"Ruộng bậc thang Sa Pa là cảnh quan nông nghiệp độc đáo của vùng núi Tây Bắc do người dân tộc thiểu số tạo nên. Những thửa ruộng uốn lượn theo sườn núi tạo thành khung cảnh rất đẹp. Vào mùa lúa chín, cả vùng núi được phủ một màu vàng rực rỡ. Đây là kết quả của quá trình lao động bền bỉ qua nhiều thế hệ. Mỗi mùa mang một vẻ đẹp khác nhau: mùa nước đổ lấp lánh, mùa xanh mướt tràn đầy sức sống. Ruộng bậc thang còn phản ánh sự thích nghi thông minh của con người với địa hình khắc nghiệt. Đây là biểu tượng văn hóa đặc trưng của vùng cao Việt Nam.",

    "ho_xuan_huong": "Hồ Xuân Hương nằm ngay trung tâm thành phố Đà Lạt và được xem là biểu tượng của thành phố này. Hồ có hình dạng cong nhẹ như vầng trăng và được bao quanh bởi rừng thông và vườn hoa. Khung cảnh nơi đây rất thơ mộng và thích hợp cho việc dạo bộ, đạp xe hay ngắm cảnh. Vào buổi sáng, sương mù bao phủ tạo nên vẻ đẹp huyền ảo. Buổi chiều, ánh hoàng hôn phản chiếu trên mặt nước mang lại cảm giác yên bình. Đây là nơi gắn liền với hình ảnh Đà Lạt mộng mơ và lãng mạn.",

    "van_mieu_quoc_tu_giam": "Văn Miếu Quốc Tử Giám được xây dựng từ thế kỷ XI và được xem là trường đại học đầu tiên của Việt Nam. Nơi đây thờ Khổng Tử và tôn vinh những người đỗ đạt trong các kỳ thi Nho học. Công trình là biểu tượng cho truyền thống hiếu học và tôn sư trọng đạo của dân tộc. Những tấm bia tiến sĩ ghi danh hiền tài là minh chứng cho lịch sử giáo dục lâu đời. Không gian trang nghiêm tạo cảm giác tôn kính. Đây là nơi gửi gắm ước vọng học hành của nhiều thế hệ.",

    "dinh_doc_lap": "Dinh Độc Lập, còn gọi là Hội trường Thống Nhất, là một công trình lịch sử quan trọng của Việt Nam. Nơi đây gắn liền với sự kiện ngày 30/4/1975 khi chiến tranh kết thúc. Hiện nay dinh là một điểm tham quan nổi tiếng thu hút nhiều du khách. Bên trong lưu giữ nguyên trạng nhiều phòng chức năng và hiện vật lịch sử. Kiến trúc kết hợp hài hòa giữa hiện đại và truyền thống. Đây là biểu tượng của hòa bình và độc lập dân tộc.",

    "thac_ban_gioc":"Thác Bản Giốc là một trong những thác nước đẹp nhất Việt Nam, nằm trên biên giới giữa Việt Nam và Trung Quốc. Thác có nhiều tầng nước đổ xuống từ độ cao lớn tạo nên khung cảnh rất hùng vĩ. Vào mùa nước nhiều, dòng thác trắng xóa giữa núi rừng tạo nên cảnh tượng tuyệt đẹp. Âm thanh thác nước vang vọng tạo cảm giác mạnh mẽ và sống động. Cảnh quan xung quanh hoang sơ, hùng tráng. Đây là điểm đến lý tưởng cho du khách yêu thiên nhiên.",

    "nui_ba_den":"Núi Bà Đen được mệnh danh là “nóc nhà Nam Bộ” với độ cao hơn 900 mét. Đây là địa điểm du lịch tâm linh nổi tiếng với nhiều chùa và tượng Phật lớn. Du khách có thể leo núi hoặc đi cáp treo để ngắm toàn cảnh vùng đồng bằng xung quanh. Ngọn núi gắn liền với nhiều truyền thuyết linh thiêng. Không gian trên đỉnh núi thoáng đãng và mát mẻ. Đây là nơi kết hợp giữa khám phá thiên nhiên và hành hương.",

    "ho_hoan_kiem":"Hồ Hoàn Kiếm nằm ở trung tâm thủ đô Hà Nội và gắn liền với truyền thuyết vua Lê trả gươm thần cho rùa vàng. Giữa hồ có Tháp Rùa cổ kính, tạo nên hình ảnh đặc trưng của thành phố. Đây là nơi người dân và du khách thường đến tham quan, dạo bộ và thư giãn. Không gian xung quanh kết hợp hài hòa giữa cổ kính và hiện đại. Hồ mang giá trị lịch sử và văn hóa sâu sắc. Đây là biểu tượng không thể thiếu của Hà Nội.",

    "chua_mot_cot":"Chùa Một Cột là ngôi chùa có kiến trúc độc đáo được xây dựng trên một cột đá giữa hồ nước. Công trình được xây dựng từ thời nhà Lý và mang ý nghĩa biểu tượng cho hoa sen - biểu tượng của sự thanh cao trong văn hóa Việt Nam. Đây là một trong những ngôi chùa nổi tiếng nhất ở Hà Nội. Kiến trúc đơn giản nhưng mang giá trị tinh thần sâu sắc. Chùa là nơi sinh hoạt tín ngưỡng quen thuộc. Đây là biểu tượng văn hóa tâm linh đặc trưng.",

    "cho_ben_thanh":"Chợ Bến Thành là khu chợ nổi tiếng và lâu đời của TP. Hồ Chí Minh. Chợ bày bán nhiều loại hàng hóa như quần áo, thủ công mỹ nghệ, đặc sản và đồ lưu niệm. Đây cũng là điểm tham quan quen thuộc của du khách khi đến thành phố. Không khí buôn bán nhộn nhịp phản ánh đời sống đô thị. Chợ là nơi giao thoa văn hóa giữa nhiều vùng miền. Đây là biểu tượng sôi động của Sài Gòn."
},
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

        # Pause & Mute state
        self.is_paused = False
        self.is_muted = False
        self.pause_start_time = 0
        self.total_pause_duration = 0

        # UI buttons for settings
        self.btn_settings = pygame.Rect(0, 0, 0, 0)
        self.show_settings_menu = False
        self.btn_pause = pygame.Rect(0, 0, 0, 0)
        self.btn_mute = pygame.Rect(0, 0, 0, 0)
        self.btn_close_settings = pygame.Rect(0, 0, 0, 0)

        # ⚙️ CONFIG SETTINGS MENU UI (dễ sửa)
        self.settings_menu_config = {
            "bg_color": (25, 35, 50),          # Màu nền menu
            "bg_alpha": 245,                    # Độ trong suốt nền (0-255)
            "border_color": (100, 150, 200),   # Màu border
            "border_width": 3,                  # Độ dày border (px)
            "border_radius": 15,                # Độ cong góc (px)
            "shadow_color": (0, 0, 0),          # Màu shadow
            "shadow_alpha": 120,                # Độ trong suốt shadow (0-255)
            "shadow_offset_x": 8,               # Offset shadow X
            "shadow_offset_y": 8,               # Offset shadow Y
        }

        # MENU buttons (mute & guide)
        self.btn_menu_mute = pygame.Rect(0, 0, 0, 0)
        self.btn_menu_guide = pygame.Rect(0, 0, 0, 0)

        # Guide popup
        self.show_guide_popup = False
        self.guide_scroll_y = 0
        self.guide_scroll_max = 0
        self.guide_content = ""  # Nội dung file hướng dẫn

        # Tracking thời gian & điểm
        self.game_start_time = 0
        self.game_end_time = 0
        self.combo_count = 0           # Combo hiện tại
        self.combo_best = 0            # Combo cao nhất
        self.match_count = 0           # Số cặp ghép thành công
        self.score = 0                 # Tổng điểm

        # --- PHẦN XỬ LÝ ÂM THANH ---
        # Khởi tạo mixer (pygame.init() đã gọi ở dòng 166)
        try:
            pygame.mixer.init()
        except:
            pass

        # Nhạc nền
        self.bg_music_loaded = False
        try:
            pygame.mixer.music.load("nhac_nen.mp3")
            pygame.mixer.music.set_volume(0.6)
            self.bg_music_loaded = True
            print("✓ Nhạc nền (nhac_nen.mp3) đã load thành công")
        except FileNotFoundError:
            print("✗ Lỗi: Không tìm thấy file nhac_nen.mp3")
        except Exception as e:
            print(f"✗ Lỗi tải nhạc nền: {e}")

        # Âm thanh chuyển cảnh
        self.intro_duration = 4000
        self.sound_transition = None
        try:
            self.sound_transition = pygame.mixer.Sound("transition.mp3")
            self.sound_transition.set_volume(0.7)
        except:
            print("Không tìm thấy file âm thanh chuyển cảnh")

        # Âm thanh lật thẻ
        self.flip_sound = None
        try:
            self.flip_sound = pygame.mixer.Sound("flip_sound.mp3")
            self.flip_sound.set_volume(0.7)
        except:
            print("Không tìm thấy file âm thanh flip_sound.mp3")

        # Âm thanh vỖ tay (hoàn thành game)
        self.clap_sound = None
        

        # Trạng thái mute
        self.is_muted = False

        # Phát nhạc nền khi menu
        self.play_background_music()

        # Load hướng dẫn chơi
        self.load_guide_file()

    def load_guide_file(self):
        """Đọc nội dung từ file huong_dan_choi.txt"""
        try:
            with open("huong_dan_choi.txt", "r", encoding="utf-8") as f:
                self.guide_content = f.read()
        except FileNotFoundError:
            print("Không tìm thấy file huong_dan_choi.txt!")
            self.guide_content = "Không tìm thấy file hướng dẫn.\n\nVui lòng kiểm tra file huong_dan_choi.txt"
        except Exception as e:
            print(f"Lỗi đọc file: {e}")
            self.guide_content = f"Lỗi: {e}"

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

        # Reset các biến điểm khi bắt đầu game
        self.combo_count = 0
        self.combo_best = 0
        self.match_count = 0
        self.score = 0
        self.game_start_time = pygame.time.get_ticks()
        self.game_end_time = 0
        
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
            # Mute button
            if self.btn_menu_mute.collidepoint(pos):
                self.toggle_mute()
                return

            # Guide button
            if self.btn_menu_guide.collidepoint(pos):
                self.show_guide_popup = not self.show_guide_popup
                self.guide_scroll_y = 0  # Reset scroll
                return

            if self.btn_amthuc.collidepoint(pos):
                self.stop_background_music() # Dừng nhạc nền khi bắt đầu intro
                self.start_intro("Ẩm thực")

            elif self.btn_vanhoa.collidepoint(pos):
                self.stop_background_music() # Dừng nhạc nền khi bắt đầu intro
                self.start_intro("Văn hóa")

            elif self.btn_lichsu.collidepoint(pos):
                self.stop_background_music() # Dừng nhạc nền khi bắt đầu intro
                self.start_intro("Lịch sử")
            # Kiểm tra click vào nút chọn Theme (Giao cho Sâm/Nghĩa vẽ nút)
            # if 100 < pos[0] < 300: self.start_intro("Ẩm thực")
            # elif 350 < pos[0] < 550: self.start_intro("Văn hóa")


        #elif self.scene == "INTRO":
            #khúc này thêm âm thanh ready go
            #self.scene = "GAMEPLAY" # Click để vào chơi

        elif self.scene == "GAMEPLAY":
            # Settings button
            if self.btn_settings.collidepoint(pos) and not self.game_completed:
                self.show_settings_menu = not self.show_settings_menu
                return

            # Settings menu options (nếu menu đang hiển thị)
            if self.show_settings_menu and not self.game_completed:
                if self.btn_pause.collidepoint(pos):
                    self.toggle_pause()
                    return
                if self.btn_mute.collidepoint(pos):
                    self.toggle_mute()
                    return
                if self.btn_close_settings.collidepoint(pos):
                    # Nút THOÁT: Reset game + Quay về MENU với fade nhạc
                    self.fade_out_music(400)  # Fade out nhạc gameplay (0.4 giây)

                    # 🔄 Reset game state (xóa hết trò chơi hiện tại)
                    self.cards = []
                    self.revealed = []
                    self.selected = []
                    self.matched_info = None
                    self.game_completed = False
                    self.turn_count = 0
                    self.combo_count = 0
                    self.combo_best = 0
                    self.match_count = 0
                    self.score = 0
                    self.stop_clap_sound()  # Tắt âm thanh vỗ tay
                    self.show_settings_menu = False

                    # Chuyển về MENU
                    self.scene = "MENU"
                    return

            if self.game_completed:
                if self.btn_replay.collidepoint(pos):
                    self.stop_clap_sound()  # Tắt âm thanh vỖ tay
                    self.setup_level(self.current_theme)
                    # Phát lại nhạc nền khi chơi lại
                    self.play_background_music()
                elif self.btn_change_theme.collidepoint(pos):
                    self.stop_clap_sound()  # Tắt âm thanh vỖ tay
                    self.scene = "MENU"
                    self.game_completed = False
                    # Phát nhạc nền khi quay lại MENU
                    self.play_background_music()
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

                # Chỉ xử lý nếu click trúng thẻ bài (không phải khoảng trống)
                if card_rect.collidepoint(pos):
                    idx = row * 4 + col
                    if not self.revealed[idx]:
                        self.start_card_animation(idx, True, pygame.time.get_ticks())
                        # Phát âm thanh lật thẻ
                        if self.flip_sound:
                            self.flip_sound.play()
                        self.revealed[idx] = True
                        self.selected.append(idx)
                        if len(self.selected) == 2:
                            self.turn_count += 1
                # Nếu click vào khoảng trống giữa các thẻ → không làm gì, không crash

    def update(self):
        current_time = pygame.time.get_ticks()

        if self.scene == "MENU":
            self.ensure_background_music() # Đảm bảo nhạc nền luôn phát khi ở menu
            self.stop_clap_sound()  # Đảm bảo khi ở menu thì âm thanh vỗ tay đã tắt

        # Nếu đang pause, không update logic game
        if self.is_paused and self.scene == "GAMEPLAY":
            return    

        if self.scene == "INTRO":
            elapsed = current_time - self.intro_start_time
            if elapsed >= self.intro_duration:
                self.scene = "GAMEPLAY"

                # Phát lại nhạc nền khi vào GAMEPLAY
                self.play_background_music()

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

                # Cập nhật combo & điểm khi match thành công
                self.match_count += 1
                self.combo_count += 1
                if self.combo_count > self.combo_best:
                    self.combo_best = self.combo_count

                self.selected = []
            else:
                # KHÔNG TRÙNG -> Chờ một nhịp ngắn rồi úp cùng lúc cả 2 thẻ
                if self.hide_pair_at == 0:
                    self.hide_pair_at = current_time + 700
                    # Reset combo khi sai
                    self.combo_count = 0

        if self.hide_pair_at and current_time >= self.hide_pair_at and len(self.selected) == 2:
            idx1, idx2 = self.selected
            self.start_card_animation(idx1, False, current_time)
            self.start_card_animation(idx2, False, current_time)
            # Phát âm thanh lật thẻ khi úp lại
            if self.flip_sound:
                self.flip_sound.play()
            self.selected = []
            self.hide_pair_at = 0

        if (
            not self.game_completed
            and all(self.revealed)
            and not self.selected
            and not self.card_animations
        ):
            self.game_end_time = current_time
            self.calculate_score()  # Gọi hàm tính điểm
            self.game_completed = True
            self.matched_info = None
            # Phát âm thanh tiếng vỖ tay khi hoàn thành
            # Tắt nhạc nền trước để không bị nhiễu
            self.stop_background_music()
            # # if self.clap_sound:
            #     self.clap_sound.play()
            self.play_clap_sound()

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
        """Phát âm thanh chuyển cảnh"""
        if self.sound_transition and not self.is_muted:
            self.sound_transition.play()

    def play_background_music(self):
        """Phát nhạc nền lặp lại"""
        if self.bg_music_loaded and not self.is_muted:
            try:
                pygame.mixer.music.play(-1)  # -1 để lặp lại vô tận
            except:
                print("Lỗi phát nhạc nền")

    def stop_background_music(self):
        """Tắt nhạc nền"""
        try:
            pygame.mixer.music.stop()
        except:
            print("Lỗi tắt nhạc nền")

    def ensure_background_music(self):
        """Đảm bảo nhạc nền luôn phát ở MENU (nếu không bị mute)

        Kiểm tra xem nhạc có đang phát không.
        Nếu nhạc bị stop, sẽ tự động restart nó với fade in smooth.
        Hàm này an toàn - có thể gọi nhiều lần mỗi frame.
        """
        # Nếu chưa load nhạc hoặc đang mute, không làm gì
        if not self.bg_music_loaded or self.is_muted:
            return

        try:
            # get_busy() = True nếu nhạc đang phát, False nếu không
            if not pygame.mixer.music.get_busy():
                # Nhạc không phát → restart nó với fade in smooth
                pygame.mixer.music.play(-1, fade_ms=300)
                print("🔊 Nhạc nền được restart ở MENU (fade in)")
        except Exception as e:
            print(f"Lỗi restart nhạc nền: {e}")

    def fade_out_music(self, duration_ms=500):
        """Fade out nhạc nền (dần yên tĩnh)

        Args:
            duration_ms: Thời gian fade (ms). VD: 500 = 0.5 giây
        """
        if self.bg_music_loaded:
            try:
                pygame.mixer.music.fadeout(duration_ms)
                print(f"🔇 Fade out nhạc nền ({duration_ms}ms)")
            except Exception as e:
                print(f"Lỗi fade out: {e}")

    def fade_in_music(self, duration_ms=500):
        """Fade in nhạc nền (dần lớn dần)

        Args:
            duration_ms: Thời gian fade (ms). VD: 500 = 0.5 giây
        """
        if self.bg_music_loaded and not self.is_muted:
            try:
                pygame.mixer.music.play(-1, fade_ms=duration_ms)
                print(f"🔊 Fade in nhạc nền ({duration_ms}ms)")
            except Exception as e:
                print(f"Lỗi fade in: {e}")

    def play_clap_sound(self):         
        """Phát âm thanh vỖ tay"""
        try:
            self.clap_sound = pygame.mixer.Sound("tieng-vo-tay.mp3")
            self.clap_sound.set_volume(0.8)
        except:
            print("Không tìm thấy file âm thanh tieng-vo-tay.mp3")
        if self.clap_sound and not self.is_muted:
            self.clap_sound.play()


    def stop_clap_sound(self):
        """Tắt âm thanh vỖ tay"""
        if self.clap_sound:
            self.clap_sound.stop()

    def calculate_score(self):
        """Tính tổng điểm dựa trên combo, thời gian, và lượt chơi"""
        if self.game_end_time == 0 or self.game_start_time == 0:
            self.score = 0
            return

        # 1. Điểm cơ bản
        base_score = 1000

        # 2. Điểm combo
        combo_points = self.combo_best * 200

        # 3. Điểm thời gian (bonus nếu nhanh) - trừ đi thời gian pause
        elapsed_time = (self.game_end_time - self.game_start_time - self.total_pause_duration) // 1000  # đơn vị giây
        time_bonus = max(0, (60 - elapsed_time) * 10)

        # 4. Điểm lượt chơi (penalty nếu chơi nhiều lượt)
        ideal_turns = 8
        turns_bonus = max(0, (ideal_turns - self.turn_count) * 100)

        # Tổng điểm (không bao giờ âm)
        self.score = max(0, base_score + combo_points + time_bonus + turns_bonus)

    def toggle_pause(self):
        """Toggle pause state"""
        if self.is_paused:
            # Resume
            self.total_pause_duration += (pygame.time.get_ticks() - self.pause_start_time)
            self.is_paused = False
            if not self.is_muted:
                pygame.mixer.music.unpause()
        else:
            # Pause
            self.pause_start_time = pygame.time.get_ticks()
            self.is_paused = True
            pygame.mixer.music.pause()

    def toggle_mute(self):
        """Toggle mute state"""
        self.is_muted = not self.is_muted
        volume = 0.0 if self.is_muted else 0.6
        pygame.mixer.music.set_volume(volume)

        # Điều chỉnh volume cho sound effects
        if self.flip_sound:
            self.flip_sound.set_volume(0.0 if self.is_muted else 0.7)
        if self.clap_sound:
            self.clap_sound.set_volume(0.0 if self.is_muted else 0.8)
        
        # Nếu tắt âm thanh, dừng nhạc nền
        if self.is_muted:
            self.stop_background_music()
        # Nếu bật lại âm thanh, phát nhạc nền nếu đang ở MENU hoặc GAMEPLAY (và chưa hoàn thành game)
        elif self.scene in ["MENU", "GAMEPLAY"] and not self.game_completed:
            self.play_background_music()

    def update_settings_button(self):
        """Cập nhật vị trí nút settings ở góc trên phải"""
        sw, sh = self.screen.get_size()

        # Kích thước nút responsive
        btn_size = max(40, int(sh * 0.06))  # 6% chiều cao màn hình
        margin = max(10, int(sw * 0.015))   # Margin từ góc (1.5% chiều rộng)

        # Vị trí: góc trên phải
        self.btn_settings = pygame.Rect(
            sw - btn_size - margin,
            margin,
            btn_size,
            btn_size
        )

    def update_menu_buttons_circle(self):
        """Cập nhật vị trí nút tròn (Mute & Guide) ở MENU"""
        sw, sh = self.screen.get_size()

        # Kích thước nút responsive (giống settings button)
        btn_size = max(40, int(sh * 0.06))  # 6% chiều cao
        margin = max(10, int(sw * 0.015))   # Margin từ góc
        gap_between = 15  # Khoảng cách giữa 2 nút

        # Nút Mute - góc trên phải
        self.btn_menu_mute = pygame.Rect(
            sw - btn_size - margin,
            margin,
            btn_size,
            btn_size
        )

        # Nút Guide - Dưới nút Mute, bên phải (cùng cột)
        self.btn_menu_guide = pygame.Rect(
            sw - btn_size - margin,  # Cùng X với nút mute
            margin + btn_size + gap_between,  # Dưới nút mute + gap
            btn_size,
            btn_size
        )

    def draw_menu_button_circle(self, rect, icon, hover_color_factor=1.2):
        """Vẽ nút tròn với border, shadow cho MENU"""
        mouse_pos = pygame.mouse.get_pos()
        is_hover = rect.collidepoint(mouse_pos)

        # 🎨 Màu nút
        base_color = (218, 165, 32)  
        border_color = (139, 101, 8) 
        shadow_color = (0, 0, 0)

        # Đổi màu khi hover
        if is_hover:
            bg_color = tuple(min(255, int(c * 1.3)) for c in base_color)
            border_color = (200, 240, 255)
        else:
            bg_color = base_color

        radius = rect.width // 2
        center = rect.center

        # ✨ Vẽ shadow (chiều sâu)
        shadow_offset = 2
        pygame.draw.circle(
            self.screen,
            (*shadow_color, 80),
            (center[0] + shadow_offset, center[1] + shadow_offset),
            radius,
        )

        # 🎨 Vẽ nền nút tròn
        pygame.draw.circle(
            self.screen,
            bg_color,
            center,
            radius
        )

        # 🟦 Vẽ border (khác màu nền)
        pygame.draw.circle(
            self.screen,
            border_color,
            center,
            radius,
            width=2  # Độ dày border
        )

        # Vẽ icon từ hình ảnh
        icon_size = int(rect.width * 0.6)

        # Nếu là nút mute, dựa vào is_muted để chọn ảnh
        if icon == "🔇":
            icon_path = "mo.png" if self.is_muted else "tat.png"
        elif icon == "❓":
            icon_path = "chamhoi.png"
        else:
            icon_font = self.load_text_font(max(18, icon_size))
            icon_text = icon_font.render(icon, True, (255, 255, 255))
            icon_rect = icon_text.get_rect(center=center)
            self.screen.blit(icon_text, icon_rect)
            return

        try:
            icon_img = pygame.image.load(icon_path)
            icon_img = pygame.transform.scale(icon_img, (icon_size, icon_size))
            icon_rect = icon_img.get_rect(center=center)
            self.screen.blit(icon_img, icon_rect)
        except:
            icon_font = self.load_text_font(max(18, icon_size))
            icon_text = icon_font.render(icon, True, (255, 255, 255))
            icon_rect = icon_text.get_rect(center=center)
            self.screen.blit(icon_text, icon_rect)

    def draw_settings_button(self):
        """Vẽ nút settings ở góc trên phải với border + shadow"""
        mouse_pos = pygame.mouse.get_pos()
        is_hover = self.btn_settings.collidepoint(mouse_pos)

        # 🎨 Màu nút
        base_color = (60, 100, 150)  # Xanh dương
        border_color = (150, 200, 255)  # Xanh sáng cho border
        shadow_color = (0, 0, 0)

        # Đổi màu khi hover
        if is_hover:
            bg_color = tuple(min(255, int(c * 1.3)) for c in base_color)
            border_color = (200, 240, 255)
        else:
            bg_color = base_color

        radius = self.btn_settings.width // 2
        center = self.btn_settings.center

        # ✨ Vẽ shadow (chiều sâu)
        shadow_offset = 2
        pygame.draw.circle(
            self.screen,
            (*shadow_color, 80),
            (center[0] + shadow_offset, center[1] + shadow_offset),
            radius,
        )

        # 🎨 Vẽ nền nút tròn
        pygame.draw.circle(
            self.screen,
            bg_color,
            center,
            radius
        )

        # 🟦 Vẽ border (khác màu nền)
        pygame.draw.circle(
            self.screen,
            border_color,
            center,
            radius,
            width=3  # Độ dày border
        )

        # Vẽ icon từ hình ảnh
        icon_size = int(self.btn_settings.width * 0.6)
        try:
            icon_img = pygame.image.load("caidat.png")
            icon_img = pygame.transform.scale(icon_img, (icon_size, icon_size))
            icon_rect = icon_img.get_rect(center=center)
            self.screen.blit(icon_img, icon_rect)
        except:
            icon_font = self.load_text_font(max(18, icon_size))
            icon_text = icon_font.render("⚙", True, (255, 255, 255))
            icon_rect = icon_text.get_rect(center=center)
            self.screen.blit(icon_text, icon_rect)

    def draw_settings_menu(self):
        """Vẽ popup menu settings với border, shadow, và chiều sâu"""
        sw, sh = self.screen.get_size()
        cfg = self.settings_menu_config  # Lấy config

        # Kích thước menu
        menu_w = min(280, int(sw * 0.35))
        menu_h = 240
        menu_x = sw - menu_w - max(10, int(sw * 0.015))
        menu_y = self.btn_settings.bottom + 10
        menu_rect = pygame.Rect(menu_x, menu_y, menu_w, menu_h)

        # ✨ Vẽ Shadow (chiều sâu)
        shadow_rect = menu_rect.copy()
        shadow_rect.x += cfg["shadow_offset_x"]
        shadow_rect.y += cfg["shadow_offset_y"]
        shadow_surface = pygame.Surface((shadow_rect.width, shadow_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(
            shadow_surface,
            (*cfg["shadow_color"], cfg["shadow_alpha"]),
            (0, 0, shadow_rect.width, shadow_rect.height),
            border_radius=cfg["border_radius"]
        )
        self.screen.blit(shadow_surface, shadow_rect.topleft)

        # 🎨 Vẽ nền menu (với độ trong suốt)
        menu_surface = pygame.Surface((menu_w, menu_h), pygame.SRCALPHA)
        pygame.draw.rect(
            menu_surface,
            (*cfg["bg_color"], cfg["bg_alpha"]),
            (0, 0, menu_w, menu_h),
            border_radius=cfg["border_radius"]
        )
        self.screen.blit(menu_surface, menu_rect.topleft)

        # 🟦 Vẽ border
        pygame.draw.rect(
            self.screen,
            cfg["border_color"],
            menu_rect,
            width=cfg["border_width"],
            border_radius=cfg["border_radius"]
        )

        # Font
        title_font = self.load_text_font(max(16, int(self.size_normal * 0.95)))
        btn_font = self.load_text_font(max(13, int(self.size_normal * 0.8)))

        # Tiêu đề
        title_img = title_font.render("CÀI ĐẶT", True, (220, 240, 255))
        self.screen.blit(title_img, (menu_x + 15, menu_y + 12))

        # ────────────────────────
        # Nút Mute/Unmute
        # ────────────────────────
        mute_label = "Âm thanh"

        self.btn_mute = pygame.Rect(menu_x + 10, menu_y + 50, menu_w - 20, 45)
        self.draw_option_button_with_icon(
            self.btn_mute,
            (50, 100, 150),
            (70, 130, 180),
            mute_label,
            btn_font,
            "tat.png" if self.is_muted else "mo.png"
        )

        # ────────────────────────
        # Nút Pause/Resume
        # ────────────────────────
        pause_status = "TIẾP TỤC" if self.is_paused else "DỪNG"
        pause_label = pause_status

        self.btn_pause = pygame.Rect(menu_x + 10, menu_y + 110, menu_w - 20, 45)
        self.draw_option_button_with_icon(
            self.btn_pause,
            (100, 50, 50),
            (150, 80, 80),
            pause_label,
            btn_font,
            "dung.png"
        )

        # ────────────────────────
        # Nút Đóng
        # ────────────────────────
        self.btn_close_settings = pygame.Rect(menu_x + 10, menu_y + 170, menu_w - 20, 35)
        self.draw_option_button(
            self.btn_close_settings,
            (60, 60, 60),
            (100, 100, 100),
            "THOÁT",
            btn_font
        )

    def draw_guide_popup(self):
        """Vẽ popup hướng dẫn chơi (tái sử dụng logic từ draw_popup)"""
        sw, sh = self.screen.get_size()

        # Lớp tối
        dim = pygame.Surface((sw, sh), pygame.SRCALPHA)
        dim.fill((8, 10, 16, 175))
        self.screen.blit(dim, (0, 0))

        # Kích thước popup
        box_w = min(700, int(sw * 0.85))
        box_h = min(500, int(sh * 0.82))
        start_x = (sw - box_w) // 2
        start_y = (sh - box_h) // 2
        box_rect = pygame.Rect(start_x, start_y, box_w, box_h)

        # Vẽ nền popup
        pygame.draw.rect(self.screen, (23, 28, 43), box_rect, border_radius=24)
        pygame.draw.rect(self.screen, (114, 159, 255), box_rect, width=2, border_radius=24)

        # Header
        header_h = 70
        pygame.draw.rect(self.screen, (36, 56, 95), (start_x, start_y, box_w, header_h), border_top_left_radius=24, border_top_right_radius=24)
        pygame.draw.line(self.screen, (130, 180, 255), (start_x + 20, start_y + header_h), (start_x + box_w - 20, start_y + header_h), 1)

        # Font
        title_font = self.load_text_font(max(22, int(self.size_normal * 1.4)))
        hint_font = self.load_text_font(max(14, int(self.size_normal * 0.7)))

        # Tiêu đề với icon
        title_font = self.load_text_font(max(22, int(self.size_normal * 1.4)))
        
        # Tải hình ảnh dấu chấm hỏi
        try:
            question_img = pygame.image.load("chamhoi.jpg")
            question_size = int(title_font.get_height() * 1.2)
            question_img = pygame.transform.scale(question_img, (question_size, question_size))
            self.screen.blit(question_img, (start_x + 24, start_y + 16))
            title_text = title_font.render(" HƯỚNG DẪN CHƠI", True, (235, 243, 255))
            self.screen.blit(title_text, (start_x + 24 + question_size + 10, start_y + 18))
        except:
            title_img = title_font.render("❓ HƯỚNG DẪN CHƠI", True, (235, 243, 255))
            self.screen.blit(title_img, (start_x + 24, start_y + 18))

        # Hint text
        hint_img = hint_font.render("Nhan chuot de dong", True, (180, 205, 255))
        self.screen.blit(hint_img, (start_x + box_w - 180, start_y + 22))

        # Nội dung text
        body_x = start_x + 26
        body_y = start_y + header_h + 20
        body_w = box_w - 52
        body_h = box_h - header_h - 36
        line_gap = 8

        # Parse nội dung & tính scroll
        guide_lines = self.wrap_text(self.guide_content, self.font, body_w)

        line_height = self.font.get_height() + line_gap
        total_content_h = len(guide_lines) * line_height
        self.guide_scroll_max = max(0, total_content_h - body_h)
        self.guide_scroll_y = max(0, min(self.guide_scroll_y, self.guide_scroll_max))

        # Vẽ text với scroll
        prev_clip = self.screen.get_clip()
        self.screen.set_clip(pygame.Rect(body_x, body_y, body_w, body_h))

        y_offset = body_y - self.guide_scroll_y
        for i, line in enumerate(guide_lines):
            # Dòng đầu là tiêu đề (format đặc biệt)
            if i == 0 or (line.strip() and line.isupper()):
                text_font = self.load_text_font(max(16, int(self.size_normal * 1.1)))
                text_surface = text_font.render(line, True, (255, 215, 0))  # Vàng
            else:
                text_surface = self.font.render(line, True, (244, 247, 255))  # Trắng

            self.screen.blit(text_surface, (body_x, y_offset))
            y_offset += line_height

        self.screen.set_clip(prev_clip)

        # Scrollbar
        if self.guide_scroll_max > 0:
            track_x = start_x + box_w - 12
            track_y = body_y
            track_h = body_h
            pygame.draw.rect(self.screen, (70, 88, 122), (track_x, track_y, 4, track_h), border_radius=3)

            thumb_h = max(22, int(track_h * (body_h / max(total_content_h, 1))))
            thumb_y = track_y + int((self.guide_scroll_y / self.guide_scroll_max) * (track_h - thumb_h))
            pygame.draw.rect(self.screen, (170, 205, 255), (track_x - 1, thumb_y, 6, thumb_h), border_radius=4)

            # Hint scroll
            note_img = hint_font.render("Lan chuot de xem them", True, (160, 196, 255))
            self.screen.blit(note_img, (body_x, start_y + box_h - 18))

        # Hint text ở dưới cùng
        hint_font = self.load_text_font(max(12, int(self.size_normal * 0.7)))
        hint_text = hint_font.render("Ấn để đóng", True, (150, 180, 220))
        hint_rect = hint_text.get_rect(center=(sw // 2, start_y + box_h - 12))
        self.screen.blit(hint_text, hint_rect)

    def draw_intro_loading(self):
        """Vẽ loading screen đẹp khi chuẩn bị vào game"""
        sw, sh = self.screen.get_size()
        
        # Lớp phủ nửa trong suốt ở giữa
        overlay = pygame.Surface((sw, sh), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 100))
        self.screen.blit(overlay, (0, 0))
        
        # Hộp loading chính
        box_w = min(500, int(sw * 0.7))
        box_h = 280
        box_x = (sw - box_w) // 2
        box_y = (sh - box_h) // 2
        
        # Vẽ hộp với gradient effect (từ tối đến sáng)
        pygame.draw.rect(self.screen, (20, 35, 60), (box_x, box_y, box_w, box_h), border_radius=20)
        pygame.draw.rect(self.screen, (100, 150, 220), (box_x, box_y, box_w, box_h), width=3, border_radius=20)
        
        # Tiêu đề chủ đề (lớn, sáng)
        title_font = self.load_text_font(max(32, int(sh * 0.08)))
        title_text = title_font.render(self.current_theme, True, (255, 215, 0))
        title_rect = title_text.get_rect(center=(sw // 2, box_y + 50))
        self.screen.blit(title_text, title_rect)
        
        # Text "Đang chuẩn bị..."
        body_font = self.load_text_font(max(20, int(sh * 0.05)))
        body_text = body_font.render("Đang chuẩn bị vào game", True, (200, 220, 255))
        body_rect = body_text.get_rect(center=(sw // 2, box_y + 130))
        self.screen.blit(body_text, body_rect)
        
        # Tính progress dựa trên thời gian INTRO thực tế
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.intro_start_time
        progress = min(100, (elapsed / self.intro_duration) * 100)  # 0-100%
        
        # Animated loading dots (dựa trên progress)
        loading_cycle = int((progress / 100) * 4) % 4  # Sync với progress
        
        dot_font = self.load_text_font(max(28, int(sh * 0.07)))
        dots_text = "●" * loading_cycle + "○" * (3 - loading_cycle)
        dots_surface = dot_font.render(dots_text, True, (150, 200, 255))
        dots_rect = dots_surface.get_rect(center=(sw // 2, box_y + 200))
        self.screen.blit(dots_surface, dots_rect)
        
        # Thanh tiến trình (progress bar)
        progress_bar_w = int(box_w * 0.6)
        progress_bar_h = 8
        progress_bar_x = (sw - progress_bar_w) // 2
        progress_bar_y = box_y + 240
        
        # Nền thanh tiến trình
        pygame.draw.rect(self.screen, (40, 60, 100), 
                        (progress_bar_x, progress_bar_y, progress_bar_w, progress_bar_h), 
                        border_radius=4)
        
        # Thanh tiến trình chạy (dựa trên thời gian thực)
        filled_w = int(progress_bar_w * (progress / 100))
        pygame.draw.rect(self.screen, (100, 200, 255), 
                        (progress_bar_x, progress_bar_y, filled_w, progress_bar_h), 
                        border_radius=4)
        
        # Viền thanh tiến trình
        pygame.draw.rect(self.screen, (150, 180, 220), 
                        (progress_bar_x, progress_bar_y, progress_bar_w, progress_bar_h), 
                        width=1, border_radius=4)
        
        # Text phần trăm tiến độ (tuỳ chọn)
        percent_font = self.load_text_font(max(14, int(sh * 0.04)))
        percent_text = percent_font.render(f"{int(progress)}%", True, (150, 200, 255))
        percent_rect = percent_text.get_rect(center=(sw // 2, box_y + 265))
        self.screen.blit(percent_text, percent_rect)

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

            # Update menu circle buttons
            self.update_menu_buttons_circle()

            #viết tên tiêu đề game
            #self.draw_text_title("FLIP GAME", (self.screen.get_width()*0.5, self.screen.get_height()*0.2))

            #nút bấm
            self.mouse_pos = pygame.mouse.get_pos()
            self.draw_image_button(self.btn_amthuc, "Ẩm thực")
            self.draw_image_button(self.btn_vanhoa, "Văn hóa")
            self.draw_image_button(self.btn_lichsu, "Lịch sử")

            # Draw menu circle buttons
            self.draw_menu_button_circle(self.btn_menu_mute, "🔇")
            self.draw_menu_button_circle(self.btn_menu_guide, "❓")

            # Draw guide popup nếu hiển thị
            if self.show_guide_popup:
                self.draw_guide_popup()
        elif self.scene == "INTRO":
            if hasattr(self, 'intro_bg') and self.intro_bg:
                self.screen.blit(self.intro_bg, (0, 0))
            else:
                self.screen.blit(self.bg_current, (0, 0))
            
            # Vẽ loading screen đẹp hơn
            self.draw_intro_loading()

        elif self.scene == "GAMEPLAY":
            self.update_settings_button()  # Cập nhật vị trí
            self.draw_grid()
            self.draw_side_text()

            # Draw settings button
            self.draw_settings_button()

            # Draw settings menu nếu hiển thị
            if self.show_settings_menu and not self.game_completed:
                self.draw_settings_menu()

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

        # Tính thời gian
        elapsed_time = (self.game_end_time - self.game_start_time) // 1000
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60

        title_img = title_font.render("HOAN THANH!", True, (235, 245, 255))
        title_rect = title_img.get_rect(center=(box_x + box_w // 2, box_y + 40))
        self.screen.blit(title_img, title_rect)

        # Điểm số chính (vàng)
        score_img = info_font.render(f"Diem so: {self.score}", True, (255, 215, 0))
        score_rect = score_img.get_rect(center=(box_x + box_w // 2, box_y + 100))
        self.screen.blit(score_img, score_rect)

        # Thống kê chi tiết
        stats_font = self.load_text_font(max(14, int(self.size_normal * 0.85)))
        stats_lines = [
            f"Thoi gian: {minutes}m {seconds}s",
            f"So luot: {self.turn_count} | Combo cao nhat: {self.combo_best}",
            f"Toc do: {8/max(1, minutes or 1):.1f} cap/phut"
        ]
        stats_y = box_y + 150
        for line in stats_lines:
            stats_img = stats_font.render(line, True, (209, 229, 255))
            stats_rect = stats_img.get_rect(center=(box_x + box_w // 2, stats_y))
            self.screen.blit(stats_img, stats_rect)
            stats_y += 28

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
    
    def draw_option_button_with_icon(self, rect, color, hover_color, text, font, icon_path):
        """Vẽ nút option với icon hình ảnh bên trái"""
        mouse_pos = pygame.mouse.get_pos()
        draw_color = hover_color if rect.collidepoint(mouse_pos) else color
        pygame.draw.rect(self.screen, draw_color, rect, border_radius=12)
        pygame.draw.rect(self.screen, (220, 235, 255), rect, width=1, border_radius=12)
        
        # Vẽ icon
        icon_size = int(rect.height * 0.6)
        try:
            icon_img = pygame.image.load(icon_path)
            icon_img = pygame.transform.scale(icon_img, (icon_size, icon_size))
            icon_rect = icon_img.get_rect(center=(rect.x + icon_size // 2 + 8, rect.centery))
            self.screen.blit(icon_img, icon_rect)
        except:
            pass
        
        # Vẽ text bên phải icon
        text_img = font.render(text, True, WHITE)
        text_x = rect.x + icon_size + 18
        text_rect = text_img.get_rect(midleft=(text_x, rect.centery))
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

    def handle_guide_scroll(self, wheel_y):
        """Xử lý scroll trong popup hướng dẫn"""
        if not self.show_guide_popup:
            return

        self.guide_scroll_y -= wheel_y * self.popup_scroll_step
        self.guide_scroll_y = max(0, min(self.guide_scroll_y, self.guide_scroll_max))

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
        # Tắt nhạc nền trước khi phát transition
        self.stop_background_music()
        
        # Phát âm thanh chuyển cảnh (transition)
        self.play_transition_sound()
        
        # Setup level
        self.setup_level(theme)
        self.scene = "INTRO"
        self.intro_start_time = pygame.time.get_ticks() # Lưu lúc bắt đầu Intro
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

        # Cập nhật settings button
        self.update_settings_button()

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
                # Xử lý click nút đóng popup guide (ấn bất cứ chỗ nào)
                if game.show_guide_popup:
                    game.show_guide_popup = False
                else:
                    game.handle_click(event.pos)

            if event.type == pygame.MOUSEWHEEL:
                game.handle_popup_scroll(event.y)

                # Xử lý scroll popup guide
                game.handle_guide_scroll(event.y)
        
        game.update()
            
        pygame.display.flip()
    pygame.quit()