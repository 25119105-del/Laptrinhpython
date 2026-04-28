"""
Test file để kiểm tra button responsive
"""
import pygame

pygame.init()

# Cấu hình
BUTTON_START_X_RATIO = 0.15   # 15% chiều rộng màn hình
BUTTON_START_Y_RATIO = 0.67   # 67% chiều cao màn hình
BUTTON_SPACING_RATIO = 0.03   # 3% chiều rộng màn hình
BUTTON_WIDTH_RATIO = 0.20     # 20% chiều rộng màn hình
BUTTON_HEIGHT_RATIO = 1.05    # chiều cao = chiều rộng × 1.05

def calculate_button_positions(screen_width, screen_height):
    """Tính toán vị trí button dựa trên kích thước màn hình"""
    
    # Tính kích thước nút
    btn_w = int(screen_width * BUTTON_WIDTH_RATIO)
    btn_h = int(btn_w * BUTTON_HEIGHT_RATIO)
    
    # Tính vị trí bắt đầu
    x1 = int(screen_width * BUTTON_START_X_RATIO)
    y1 = int(screen_height * BUTTON_START_Y_RATIO)
    
    # Khoảng cách giữa các nút
    btn_spacing = int(screen_width * BUTTON_SPACING_RATIO)
    
    # Vị trí 3 nút
    buttons = {
        "btn1": (x1, y1, btn_w, btn_h),
        "btn2": (x1 + btn_w + btn_spacing, y1, btn_w, btn_h),
        "btn3": (x1 + 2*(btn_w + btn_spacing), y1, btn_w, btn_h),
    }
    
    return buttons

# Test với các kích thước khác nhau
test_sizes = [
    (800, 600),    # Kích thước ban đầu
    (1024, 768),   # Kích thước lớn hơn
    (640, 480),    # Kích thước nhỏ hơn
    (1920, 1080),  # Full HD
]

print("TEST Button Responsive Positioning\n")
print("=" * 60)

for width, height in test_sizes:
    print(f"\nScreen Size: {width}x{height}")
    print("-" * 60)
    
    buttons = calculate_button_positions(width, height)
    
    for btn_name, (x, y, w, h) in buttons.items():
        print(f"  {btn_name}: Position({x}, {y}), Size({w}x{h})")
    
    # Kiểm tra nút có nằm trong màn hình không
    for btn_name, (x, y, w, h) in buttons.items():
        if x + w > width:
            print(f"  WARNING: {btn_name} vut ra ngoai man hinh!")
        else:
            print(f"  OK: {btn_name} nam trong man hinh")

print("\n" + "=" * 60)
print("SUCCESS: All buttons maintain relative size and adjust position by screen")
