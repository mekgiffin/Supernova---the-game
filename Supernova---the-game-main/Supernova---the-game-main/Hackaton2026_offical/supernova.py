import pygame

pygame.init()
screenSize = pygame.display.get_desktop_sizes()[0]
screen = pygame.display.set_mode(screenSize)
pygame.display.toggle_fullscreen()
clock = pygame.time.Clock()

DEBUG_HITBOXES = True

backgroundStorage2048x1024 = pygame.image.load("Images/backgroundStorage.png").convert_alpha()
single64x64Block = pygame.image.load("Images/single64x64Block.png").convert_alpha()
single128x64Block = pygame.transform.scale(single64x64Block, (128, 64))
single64x128Block = pygame.transform.scale(single64x64Block, (64, 128))
floor256x64 = pygame.image.load("Images/floor256x64.png").convert_alpha()
floor256x64Flipped = pygame.transform.flip(floor256x64, True, False)
floor256x64Flipped = pygame.transform.scale(floor256x64Flipped, (192,64))
floor256x64 = pygame.transform.scale(floor256x64, (192, 64))
exit = pygame.image.load("Images/exit.png").convert_alpha()
exit = pygame.transform.scale(exit, (198, 256))
ceil2176x64 = pygame.image.load("Images/Ceilling.png").convert_alpha()
wallStorage64x1024 = pygame.image.load("Images/wallStorage64x1024.png").convert_alpha()



playerImage = pygame.image.load("Images/PlayerFrames/PlayerImage.png").convert_alpha()
playerImageWalking1 = pygame.image.load("Images/PlayerFrames/PlayerImageWalking1.png").convert_alpha()
playerImageWalking2 = pygame.image.load("Images/PlayerFrames/PlayerImageWalking2.png").convert_alpha()
playerImageWalking3 = pygame.image.load("Images/PlayerFrames/PlayerImageWalking3.png").convert_alpha()
jumpImage = pygame.image.load("Images/PlayerFrames/jump.png").convert_alpha()
climbImage = pygame.image.load("Images/PlayerFrames/wall_climbing.png").convert_alpha()

playerSize = (64, 128)
# Your sprites face LEFT by default, so the "Right" names hold the as-drawn images
# (they are shown when facing == 1, which is the left key in your input code).
idleRight = pygame.transform.scale(playerImage, playerSize)
idleLeft = pygame.transform.flip(idleRight, True, False)
walkRight = [pygame.transform.scale(f, playerSize) for f in
             (playerImageWalking1, playerImageWalking2, playerImageWalking1, playerImageWalking3)]
walkLeft = [pygame.transform.flip(f, True, False) for f in walkRight]

jumpRight = pygame.transform.scale(jumpImage, playerSize)
jumpLeft = pygame.transform.flip(jumpRight, True, False)

climbOnLeftWall = pygame.transform.scale(climbImage, playerSize)
climbOnRightWall = pygame.transform.flip(climbOnLeftWall, True, False)

spike = pygame.image.load("Images/spike.png").convert_alpha()
spike = pygame.transform.scale(spike, (64, 8))
spikeBackLeft = pygame.transform.rotate(spike, 270)
spikeBackRight = pygame.transform.rotate(spike, 90)
spikeBackTop = pygame.transform.rotate(spike, 180)


running = True
pause = False
dt = 0
acceleration = 1
velocity_x = 0
velocity_y = 1
jump = 1
dash = 1
holding = False
currentLevel = 0
platformTime = 0
facing = 1        
animTimer = 0
climbSide = -1    

# [checkpoint coord,
#  [[texture, rect], ...],                      solid blocks (texture can be None = invisible)
#  [[texture, rect, distance, seconds], ...],   moving platforms
#  [[texture, rect], ...]]                      spikes
level0 = [[64, 896],
          [[wallStorage64x1024, pygame.Rect(-64, 0, 64, 1024)],
           [wallStorage64x1024, pygame.Rect(2048, 0, 64, 1024)],
           [ceil2176x64, pygame.Rect(-64, -64, 2176, 64)],
           [floor256x64, pygame.Rect(0, 960, 192, 64)],
           [floor256x64Flipped, pygame.Rect(1856, 960, 192, 64)],
           [single128x64Block, pygame.Rect((64*8), (64*12), 128, 64)],
           [single64x64Block, pygame.Rect((64*8), (64*13), 64, 64)],
           [single64x128Block, pygame.Rect((64*6), (64*3), 64, 128)],
           [single64x128Block, pygame.Rect((64*10), (64*3), 64, 128)],
           [single64x128Block, pygame.Rect((64*10), (64*5), 64, 128)],
           [single64x128Block, pygame.Rect((64*10), (64*7), 64, 128)],
           [single64x128Block, pygame.Rect((64*10), (64*9), 64, 128)],
           [single64x128Block, pygame.Rect((64*16), (64*0), 64, 128)],
           [single64x128Block, pygame.Rect((64*16), (64*2), 64, 128)],
           [single64x64Block, pygame.Rect((64*22), (64*4), 64, 64)],
           [single128x64Block, pygame.Rect((64*7), (64*4), 128, 64)],
           [single64x64Block, pygame.Rect((64*9), (64*4), 64, 64)]],
          [[single128x64Block, pygame.Rect((64*11), (64*9), 128, 64), 512, 2]],
          [[spikeBackLeft, spikeBackLeft.get_rect(topleft=((64*0), (64*11)))],
           [spikeBackLeft, spikeBackLeft.get_rect(topleft=((64*0), (64*10)))],
           [spikeBackLeft, spikeBackLeft.get_rect(topleft=((64*0), (64*9)))],
           [spikeBackLeft, spikeBackLeft.get_rect(topleft=((64*0), (64*4)))],
           [spikeBackLeft, spikeBackLeft.get_rect(topleft=((64*0), (64*3)))],
           [spikeBackLeft, spikeBackLeft.get_rect(topleft=((64*0), (64*2)))],
           [spike, spike.get_rect(topleft=((64*7), (64*4)-8))],
           [spike, spike.get_rect(topleft=((64*8), (64*4)-8))],
           [spike, spike.get_rect(topleft=((64*9), (64*4)-8))],
           [spike, spike.get_rect(topleft=((64*10), (64*3)-8))],
           [spikeBackTop, spike.get_rect(topleft=((64*6), (64*5)))],
           [spikeBackTop, spike.get_rect(topleft=((64*13), (64*0)))]]]


exitX, exitY = 64*29, 64*0
decor = [[exit, pygame.Rect(exitX, exitY, 198, 256)]]

exitParts = [(-1000, -10000, 100, 256),      # the tall bar
             (32, 224, 192, 32)]   # the foot of the L
for x, y, w, h in exitParts:
    level0[1].append([None, pygame.Rect(exitX + x, exitY + y, w, h)])

levelList = [level0]
movingRects = [p[1].copy() for p in levelList[currentLevel][2]]

player_pos = pygame.Vector2(level0[0])
middle = pygame.Vector2(int(screen.get_width() / 2),
                        int(screen.get_height() / 2 + screen.get_height() * 400 / 1800))
worldPLayerHitbox = pygame.Rect(0, 0, 64, 128)
worldPLayerHitbox.center = (round(player_pos.x), round(player_pos.y))
offset = ((player_pos.x - middle.x), (player_pos.y - middle.y))


def draw_level(currentLevel):
    for tex, rect in levelList[currentLevel][1]:
        if tex:  
            screen.blit(tex, rect.move(-offset[0], -offset[1]))

    for tex, rect in decor:
        screen.blit(tex, rect.move(-offset[0], -offset[1]))

    for tex, rect in levelList[currentLevel][3]:
        screen.blit(tex, rect.move(-offset[0], -offset[1]))

    for (tex, _, _, _), rect in zip(levelList[currentLevel][2], movingRects):
        screen.blit(tex, rect.move(-offset[0], -offset[1]))

    if DEBUG_HITBOXES:
        for r in solids():
            pygame.draw.rect(screen, "red", r.move(-offset[0], -offset[1]), 2)


def solids():
    return [r for _, r in levelList[currentLevel][1]] + movingRects


def on_ground():
    check = worldPLayerHitbox.move(0, 1)
    return any(check.colliderect(r) for r in solids())


def update_platforms(dt):
    global platformTime
    platformTime += dt
    feet = worldPLayerHitbox.move(0, 1)
    for i, (tex, base, dist, secs) in enumerate(levelList[currentLevel][2]):
        old = movingRects[i]
        t = platformTime % (secs * 2)
        frac = t / secs if t < secs else 2 - t / secs
        new = base.copy()
        new.x = base.x + round(dist * frac)

        if feet.colliderect(old) and worldPLayerHitbox.bottom <= old.top + 1:
            shift = new.x - old.x
            player_pos.x += shift
            worldPLayerHitbox.x += shift

        movingRects[i] = new


def movePlayer(velocity_x, velocity_y, jump, dt, dash, holding):
    if not holding:
        velocity_y += 0.1
    player_pos.y += velocity_y * 320 * dt
    worldPLayerHitbox.centery = round(player_pos.y)
    for rect in solids():
        if worldPLayerHitbox.colliderect(rect):
            if velocity_y > 0:
                worldPLayerHitbox.bottom = rect.top
                jump = 1
                dash = 1
            elif velocity_y < 0:
                worldPLayerHitbox.top = rect.bottom
                jump = 1
            velocity_y = 0
            player_pos.y = worldPLayerHitbox.centery

    velocity_x *= 0.85
    player_pos.x += velocity_x * 320 * dt
    worldPLayerHitbox.centerx = round(player_pos.x)
    for rect in solids():
        if worldPLayerHitbox.colliderect(rect):
            if velocity_x > 0:
                worldPLayerHitbox.right = rect.left
            elif velocity_x < 0:
                worldPLayerHitbox.left = rect.right
            velocity_x = 0
            player_pos.x = worldPLayerHitbox.centerx
    if velocity_x < 0.00005 and velocity_x > -0.00005:
        velocity_x = 0
    return velocity_x, velocity_y, jump, dash


def jumping():
    return -3, 0


def can_climb():
    for sides in (-1, 1):
        check = worldPLayerHitbox.move(sides, 0)
        for rect in solids():
            if check.colliderect(rect):
                return sides
    return 0


def dead():
    if player_pos.y > 3000:
        return True

    for _, rect in levelList[currentLevel][3]:
        if worldPLayerHitbox.colliderect(rect):
            return True
    return False


def dying():
    snapshot = screen.copy()
    overlay = pygame.Surface(screen.get_size())
    overlay.fill((0, 0, 0))

    for i in list(range(0, 31)) + list(range(30, -1, -1)):
        pygame.event.pump()
        overlay.set_alpha(int(i * 255 / 30))
        screen.blit(snapshot, (0, 0))
        screen.blit(overlay, (0, 0))
        pygame.display.flip()
        clock.tick(60)


#my game load
while running:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    offset = ((player_pos.x - middle.x), (player_pos.y - middle.y))

    screen.fill("black")
    screen.blit(backgroundStorage2048x1024, pygame.Rect(0, 0, 2048, 1024).move(-offset[0], -offset[1]))
    playerHitbox = pygame.Rect((middle.x - 32, middle.y - 64), (64, 128))


    if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
        facing = 1
    elif keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
        facing = -1

    grounded = on_ground()
    walking = abs(velocity_x) > 0.2 and grounded and not holding

    if holding:
        animTimer = 0
        sprite = climbOnLeftWall if climbSide == -1 else climbOnRightWall
    elif not grounded:
        animTimer = 0
        sprite = jumpRight if facing == 1 else jumpLeft
    elif walking:
        animTimer += dt
        frames = walkRight if facing == 1 else walkLeft
        sprite = frames[int(animTimer * 10) % len(frames)]
    else:
        animTimer = 0
        sprite = idleRight if facing == 1 else idleLeft

    screen.blit(sprite, playerHitbox)
    draw_level(currentLevel)

    pygame.draw.rect(screen, "black", (0, 0, int((screen.get_width() - 1240) / 2), screen.get_height()))
    pygame.draw.rect(screen, "black", (screen.get_width() - int((screen.get_width() - 1240) / 2), 0,
                                       int((screen.get_width() - 1240) / 2), screen.get_height()))

    # --- input
    directionx = 0
    directiony = 0
    if keys[pygame.K_UP]:
        directiony = -1
    if keys[pygame.K_DOWN]:
        directiony = 1
        velocity_y += 0.1
    if keys[pygame.K_LEFT]:
        directionx = -1
        velocity_x -= 0.3
    if keys[pygame.K_RIGHT]:
        directionx = 1
        velocity_x += 0.3

    if jump > 0 and keys[pygame.K_c] and holding == False:
        velocity_y, jump = jumping()

    if keys[pygame.K_x] and dash == 1 and (directionx != 0 or directiony != 0):
        velocity_x = 3 * directionx if directionx else velocity_x
        velocity_y = 3 * directiony if directiony else velocity_y
        dash = 0

    wall = can_climb()
    if keys[pygame.K_z] and wall:
        holding = True
        climbSide = wall          # remember which side the wall is on, for the sprite
        velocity_x = 0
        velocity_y = directiony * 0.75
        jump = 1
    else:
        holding = False

    if keys[pygame.K_q]:
        running = False

    # --- physics
    update_platforms(dt)
    velocity_x, velocity_y, jump, dash = movePlayer(velocity_x, velocity_y, jump, dt, dash, holding)

    if dead():
        player_pos.x = levelList[currentLevel][0][0]
        player_pos.y = levelList[currentLevel][0][1]
        worldPLayerHitbox.center = (round(player_pos.x), round(player_pos.y))
        jump = 1
        dash = 1
        holding = False
        velocity_x = 0
        velocity_y = 0
        dying()

    pygame.display.flip()
    dt = clock.tick(60) / 1000