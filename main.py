import math
import random
import pygame
from pygame import mixer

# Khởi tạo Pygame
pygame.init()

# Tạo cửa sổ trò chơi với kích thước
screen = pygame.display.set_mode((900, 600))

# Tải hình nền
background = pygame.image.load('background.png')

# Phát nhạc nền
mixer.music.load("background.wav")
mixer.music.play(-1)  # Chơi nhạc nền lặp lại vô hạn

# Thiết lập tiêu đề và biểu tượng của trò chơi
pygame.display.set_caption("Soldier vs Zombie")
icon = pygame.image.load('enemy.gif')
pygame.display.set_icon(icon)

# Người chơi
playerImg = pygame.image.load('player.png')
playerImg = pygame.transform.scale(playerImg, (70, 70))  # Thay đổi kích thước của hình ảnh người chơi
playerX = 836  # Vị trí ban đầu của người chơi ở bên phải màn hình
playerY = 300  # Vị trí theo chiều dọc của người chơi
playerX_change = 0  # Biến thay đổi vị trí người chơi theo chiều ngang
playerY_change = 0  # Biến thay đổi vị trí người chơi theo chiều dọc

# Tải hình ảnh dưới người chơi (ví dụ: một hình ảnh nền hoặc icon)
player_base_img = pygame.image.load('base_image.png')  # Thay đổi bằng hình ảnh của bạn
player_base_img = pygame.transform.scale(player_base_img, (70, 70))  # Điều chỉnh kích thước hình ảnh

# Kẻ thù
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 3  # Số lượng kẻ thù loại 1
num_of_enemies_type2 = 2  # Số lượng kẻ thù loại 2

# Kẻ thù loại 1 (Zombie)
for i in range(num_of_enemies):
    enemyImg.append(pygame.transform.scale(pygame.image.load('enemy.gif'), (68, 68)))  # Hình ảnh kẻ thù loại 1
    enemyX.append(random.randint(0, 100))  # Vị trí ngẫu nhiên của kẻ thù trên trục X (bắt đầu từ trái màn hình)
    enemyY.append(random.randint(50, 550))  # Vị trí ngẫu nhiên của kẻ thù trên trục Y (dọc theo màn hình)
    enemyX_change.append(random.choice([0.5, 1, 1.5]))  # Tốc độ di chuyển ngẫu nhiên của kẻ thù loại 1

# Kẻ thù loại 2 (Zombie với hình ảnh khác)
for i in range(num_of_enemies_type2):
    enemyImg.append(pygame.transform.scale(pygame.image.load('enemy2.gif'), (68, 68)))  # Hình ảnh kẻ thù loại 2
    enemyX.append(random.randint(0, 100))  # Vị trí ngẫu nhiên của kẻ thù loại 2 trên trục X (bắt đầu từ trái màn hình)
    enemyY.append(random.randint(50, 550))  # Vị trí ngẫu nhiên của kẻ thù loại 2 trên trục Y
    enemyX_change.append(random.choice([0.5, 1, 1.5]))  # Tốc độ di chuyển ngẫu nhiên của kẻ thù loại 2

# Đạn
bulletImg = pygame.image.load('bullet.png')
bulletImg = pygame.transform.scale(bulletImg, (40, 20))  # Điều chỉnh kích thước của đạn
bulletX = 0  # Vị trí ban đầu của đạn (trong không gian trò chơi)
bulletY = 300  # Vị trí Y của đạn (bắt đầu ngang với người chơi)
bulletX_change = -10  # Tốc độ di chuyển của đạn (theo chiều ngang từ phải qua trái)
bullet_state = "ready"  # Trạng thái của đạn (sẵn sàng bắn hay đã bắn)

# Điểm số
score_value = 0  # Điểm ban đầu
font = pygame.font.Font('freesansbold.ttf', 32)  # Font hiển thị điểm số

textX = 10  # Vị trí X hiển thị điểm số
testY = 10  # Vị trí Y hiển thị điểm số

# Thông báo khi kết thúc trò chơi
over_font = pygame.font.Font('freesansbold.ttf', 64)

# Biến theo dõi số lượng zombie đã vượt qua màn hình
zombies_passed = 0

# Hàm hiển thị điểm số
def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))  # Render điểm số với màu trắng
    screen.blit(score, (x, y))  # Hiển thị điểm trên màn hình

# Hàm hiển thị thông báo Game Over
def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))  # Render Game Over với font lớn
    screen.blit(over_text, (200, 250))  # Hiển thị thông báo Game Over tại vị trí (200, 250)

# Hàm vẽ người chơi lên màn hình
def player(x, y):
    screen.blit(playerImg, (x, y))  # Vẽ người chơi
    screen.blit(player_base_img, (x, y + 30))  # Vẽ hình ảnh dưới chân người chơi (cộng thêm 70px vào Y để đặt dưới)

# Hàm vẽ kẻ thù lên màn hình
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

# Hàm bắn đạn
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"  # Thay đổi trạng thái của đạn khi bắn
    screen.blit(bulletImg, (x - 20, y))  # Hiển thị đạn trên màn hình

# Hàm kiểm tra va chạm giữa đạn và kẻ thù
def isCollision(x1, y1, x2, y2):
    bullet_width = bulletImg.get_width()  # Lấy chiều rộng của đạn
    bullet_height = bulletImg.get_height()  # Lấy chiều cao của đạn
    enemy_width = enemyImg[0].get_width()  # Lấy chiều rộng của kẻ thù (giả sử tất cả kẻ thù có cùng kích thước)
    enemy_height = enemyImg[0].get_height()  # Lấy chiều cao của kẻ thù

    # Điều chỉnh vị trí của đạn một chút xuống dưới so với vị trí ban đầu để tránh lệch
    bullet_y_adjusted = y1 + bullet_height - 5  # Dịch đạn xuống 5 pixel để tránh lệch lên trên

    # Tính khoảng cách giữa các đối tượng và kiểm tra va chạm
    distance = math.sqrt(math.pow(x1 - x2, 2) + math.pow(bullet_y_adjusted - y2, 2))
    if distance < (bullet_width / 2 + enemy_width / 2) and distance < (bullet_height / 2 + enemy_height / 2):
        return True
    return False 

# Vòng lặp chính của trò chơi
running = True
while running:
    screen.fill((0, 0, 0))  # Lấp đầy màn hình với màu đen
    screen.blit(background, (0, 0))  # Vẽ hình nền lên màn hình

    # Lắng nghe sự kiện từ người dùng
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Nếu người dùng đóng cửa sổ, thoát trò chơi
            running = False

        if event.type == pygame.KEYDOWN:  # Khi một phím được nhấn
            if event.key == pygame.K_UP:
                playerY_change = -5  # Di chuyển lên
            if event.key == pygame.K_DOWN:
                playerY_change = 5  # Di chuyển xuống
            if event.key == pygame.K_LEFT:
                playerX_change = -5  # Di chuyển sang trái
            if event.key == pygame.K_RIGHT:
                playerX_change = 5  # Di chuyển sang phải
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletSound = mixer.Sound("laser.wav")  # Âm thanh khi bắn
                    bulletSound.play()
                    bulletX = playerX - 40  # Vị trí ban đầu của đạn (xảy ra ở phía trước người chơi)
                    bulletY = playerY + 20  # Vị trí bắn ngang ở giữa người chơi
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:  # Khi phím được thả ra
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0  # Dừng di chuyển lên xuống
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0  # Dừng di chuyển trái phải

    # Cập nhật vị trí người chơi
    playerX += playerX_change
    playerY += playerY_change

    # Giới hạn vị trí người chơi trên màn hình
    if playerY <= 0:
        playerY = 0
    elif playerY >= 536:
        playerY = 536
    if playerX <= 0:
        playerX = 0  # Người chơi không thể ra ngoài bên trái
    elif playerX >= 836:  # Giới hạn bên phải sao cho không ra ngoài màn hình
        playerX = 836

    # Di chuyển kẻ thù
    for i in range(num_of_enemies + num_of_enemies_type2):  # Cập nhật cho cả hai loại kẻ thù
        if enemyX[i] < 0:  # Nếu zombie ra khỏi màn hình bên trái
            zombies_passed += 1
            enemyX[i] = random.randint(0, 100)  # Đặt lại zombie từ bên trái
            enemyY[i] = random.randint(50, 550)  # Đặt lại vị trí Y ngẫu nhiên
            if zombies_passed >= 5:  # Nếu số zombie vượt qua >= 5, kết thúc trò chơi
                game_over_text()  # Hiển thị thông báo Game Over
                pygame.display.update()
                pygame.time.delay(2000)  # Delay 2 giây trước khi thoát trò chơi
                running = False  # Kết thúc trò chơi
            break

        # Cập nhật vị trí zombie theo hướng phải và di chuyển lên xuống
        enemyX[i] += enemyX_change[i]  # Di chuyển zombie sang phải
        if enemyY[i] <= 50:  # Giới hạn di chuyển lên
            enemyY_change[i] = abs(enemyY_change[i])  # Di chuyển xuống
        elif enemyY[i] >= 550:  # Giới hạn di chuyển xuống
            enemyY_change[i] = -abs(enemyY_change[i])  # Di chuyển lên

        # Kiểm tra va chạm giữa đạn và zombie
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound("explosion.wav")  # Âm thanh va chạm
            explosionSound.play()
            bulletY = 480  # Đưa đạn về trạng thái "ready"
            bullet_state = "ready"
            score_value += 1  # Tăng điểm khi zombie bị bắn
            enemyX[i] = random.randint(0, 100)  # Đặt lại vị trí zombie
            enemyY[i] = random.randint(50, 550)

        # Vẽ kẻ thù lên màn hình
        enemy(enemyX[i], enemyY[i], i)

    # Di chuyển đạn
    if bulletX <= 0:  # Nếu đạn ra ngoài màn hình, đưa nó về lại trạng thái "ready"
        bulletX = 0
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletX += bulletX_change  # Di chuyển đạn theo chiều ngang

    # Cài đặt FPS để giới hạn tốc độ khung hình
    clock = pygame.time.Clock()
    clock.tick(90)  # FPS = 90

    # Vẽ người chơi lên màn hình
    player(playerX, playerY)
    # Hiển thị điểm số
    show_score(textX, testY)
    # Cập nhật màn hình
    pygame.display.update()
