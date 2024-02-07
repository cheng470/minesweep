import random

ROWS = 15
COLS = 15
SIZE = 25
BOMBS = 20
WIDTH = SIZE * COLS
HEIGHT = SIZE * ROWS
failed = False
finished = False

# 生成方块阵列
blocks = []
for i in range(ROWS):
    for j in range(COLS):
        b = Actor("minesweep_block")
        b.left = j * SIZE
        b.top = i * SIZE
        b.isbomb = False
        b.isflag = False
        b.isopen = False
        blocks.append(b)

# 打乱地雷位置
random.shuffle(blocks)

# 埋设地雷
for i in range(BOMBS):
    blocks[i].isbomb = True

def draw():
    for b in blocks:
        b.draw()
    if finished:
        screen.draw.text("Finished", center=(WIDTH//2,HEIGHT//2), fontsize=100, color="red")
    if failed:
        screen.draw.text("Failed", center=(WIDTH//2,HEIGHT//2), fontsize=100, color="red")

def update():
    global finished
    if finished or failed:
        return
    for b in blocks:
        if not b.isbomb and not b.isopen:
            return
    finished = True
    sounds.win.play()

def on_mouse_down(pos, button):
    for b in blocks:
        if b.collidepoint(pos) and not b.isopen:
            if button == mouse.RIGHT:
                set_flag(b)
            elif button == mouse.LEFT and not b.isflag:
                if b.isbomb:
                    blow_up()
                else:
                    open_block(b)

def blow_up():
    global failed
    failed = True
    sounds.bomb.play()
    for i in range(BOMBS):
        blocks[i].image = "minesweep_bomb"

# 打开方块，方块没有雷时，调用该函数
def open_block(block):
    block.isopen = True
    bombnum = get_bomb_number(block)
    block.image = "minesweep_number" + str(bombnum)
    if bombnum != 0:
        return
    for b in get_neighbours(block):
        if not b.isopen:
            open_block(b)

# 获取周围方块
def get_neighbours(block):
    nblocks = []
    for b in blocks:
        if b.isopen:
            continue
        if b.x == block.x - SIZE and b.y == block.y \
                or b.x == block.x + SIZE and b.y == block.y \
                or b.x == block.x and b.y == block.y - SIZE \
                or b.x == block.x and b.y == block.y + SIZE \
                or b.x == block.x - SIZE and b.y == block.y - SIZE \
                or b.x == block.x + SIZE and b.y == block.y - SIZE \
                or b.x == block.x - SIZE and b.y == block.y + SIZE \
                or b.x == block.x + SIZE and b.y == block.y + SIZE:
            nblocks.append(b)
    return nblocks

# 获取周围方块的地雷数量
def get_bomb_number(block):
    num = 0
    for b in get_neighbours(block):
        if b.isbomb:
            num += 1
    return num


def set_flag(block):
    if block.isflag :
        block.image = "minesweep_block"
        block.isflag = False
    else:
        block.image = "minesweep_flag"
        block.isflag = True

