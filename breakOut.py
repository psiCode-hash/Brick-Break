import pygame as py

py.init()

screenWidth = 600
screenHeight = 600

screen = py.display.set_mode((screenWidth,screenHeight))
py.display.set_caption("Break-Out")

# bg = (200 , 200 , 200)
# #block colors
# block_A = (180 , 180 , 50)
# block_B = (255, 0 , 0)
# block_C = (0 , 0 , 255)

bg = (234, 218, 184)

block_A = (242,85, 96)
block_B = (86, 174, 87)
block_C = (69, 177, 232)
#define paddle colors
paddleCol = (130, 150, 170)
paddleOutline = (100, 100, 100)

cols = 6
rows = 6
strength = 0
clock = py.time.Clock()
fps = 60

class wall():
    def __init__(self):
        self.width = screenWidth // cols
        self.height = 50

    def createWall(self):
        self.block = []
        blockList = []
        for row in range(rows):
            blockRow = []
            for col in range(cols):
                block_x = col * self.width
                block_y = row * self.height
                if row < 2 :
                    strength = 3
                elif row < 4 :
                    strength = 2
                elif row < 6 :
                    strength = 1
                rect = py.Rect(block_x , block_y , self.width , self.height)
                blockList = [rect,strength]
                blockRow.append(blockList)
                self.block.append(blockRow)

    def drawWall(self):
        for rows in self.block :
            for block in rows :
                if block[1] == 3 :
                    blockColor = block_A
                elif block[1] == 2 :
                    blockColor = block_B
                elif block[1] == 1 :
                    blockColor = block_C
                py.draw.rect(screen , blockColor , block[0])
                py.draw.rect(screen , bg , block[0] , 2)

class paddle():
    def __init__(self) :
        self.width = int(screenWidth/cols) 
        self.height = 20
        self.x = (screenWidth / 2) - (self.width / 2) 
        self.y = screenHeight - (2*self.height)
        self.speed = 10
        self.direction = 0
        self.rect = py.Rect(self.x , self.y , self.width , self.height)

    def move(self) :
        key = py.key.get_pressed()
        if key[py.K_LEFT] and self.rect.left > 0 :
            # self.speed -= 10
            self.rect.x -= self.speed
            self.direction = -1
        if key[py.K_RIGHT] and self.rect.right < screenWidth :
            self.rect.x += self.speed 
            self.direction = 1

    def draw(self) :
        py.draw.rect(screen , paddleCol , self.rect)
        py.draw.rect(screen , paddleOutline , self.rect ,3)


class game_ball():
    def __init__(self,x,y) :
        self.ball_rad = 10
        self.x = x - self.ball_rad
        self.y = y
        self.rect = py.Rect(self.x , self.y , self.ball_rad*2 , self.ball_rad*2)
        self.speed_x = 3
        self.speed_y = -3
        self.speed_max = 5
        self.gameOver = 0

    def draw(self):
        py.draw.circle(screen , paddleCol , (self.x + self.ball_rad , self.y + self.ball_rad) , self.ball_rad)
        py.draw.circle(screen , paddleOutline , (self.x + self.ball_rad , self.y + self.ball_rad) , self.ball_rad , 3)

    def move(self):
        collide_thresh = 5

        #collision with the paddle 
        if self.rect.colliderect(player_paddle):
            if abs(self.rect.bottom-player_paddle.rect.top) > collide_thresh and self.speed_y > 0 :
                self.speed_y *= -1
                self.speed_x += player_paddle.direction 
                if self.speed_y > self.speed_max :
                    self.speed_y = self.speed_max
                elif self.speed_y < 0 and self.speed_y < -self.speed_max :
                    self.speed_y = -self.speed_max
            else:
                self.speed_x *= -1

        #collision with the walls 
        if self.rect.left < 0 or self.rect.right > screenWidth :
            self.speed_x *= -1
        elif self.rect.top < 0 :
            self.speed_y *= -1
        elif self.rect.bottom > screenHeight :
            self.gameOver = -1

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        self.x = self.rect.x
        self.y = self.rect.y

        return self.gameOver

player_paddle = paddle()
ball = game_ball(player_paddle.x + (player_paddle.width // 2) , player_paddle.y - player_paddle.height)

wall = wall()
wall.createWall()
                    
run = True
while run :
    clock.tick(fps)

    screen.fill(bg)
    wall.drawWall() 

    player_paddle.draw()
    player_paddle.move()

    ball.draw()
    ball.move()

    for events in py.event.get() : 
        if events.type == py.QUIT :
            run = False

    py.display.update()

py.quit()
