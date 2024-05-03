import obd
from pygame.locals import *
import pygame
import pygame.gfxdraw
from random import randint
import math

pygame.init()
obd.logger.setLevel(obd.logging.DEBUG)
WIDTH, HEIGHT = 1280, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

NUM_SYMBOLS = 22
letter_symbols = []
for i in range(NUM_SYMBOLS+1):
    #Load Image.
    temp_img = pygame.image.load('text_{}.png'.format(i))
    temp_img = pygame.transform.scale(temp_img, (40, 40))

    letter_symbols.append(temp_img)

letter_instances = []
for i in range(20):
    rect_temp = letter_symbols[0].get_rect()
    rect_temp.center = 230 + (math.trunc(i/10)*820), 60 + ((i%10)*30)
    letter_instances.append([randint(0,NUM_SYMBOLS), rect_temp])



# connection = obd.Async("/dev/rfcomm99", protocol="6", baudrate="9600", fast=False, timeout = 30)

# #Continuously query until the amount of supported commands is greater than 100
# while len(connection.supported_commands) < 100:
#     connection = obd.Async("/dev/rfcomm99", protocol="6", baudrate="9600", fast=False, timeout = 30)

WHITE = (255, 255, 255)
GREEN = (0, 143, 17)
BLACK = (0, 0, 0)
DARK_YELLOW = (231, 153, 62)
LIGHT_YELLOW = (248, 226, 90)
RED = (150, 31, 16)
pygame.mouse.set_visible(False)

# Define variables for corridor
corridor_width = 200
corridor_color = GREEN
corridor_segments = 6
wall_segments = 12
corridor_speed = 5

vanishing_point_left = (3.5*(WIDTH / 8), HEIGHT / 2)
vanishing_point_right = (4.5*(WIDTH / 8), HEIGHT / 2)

ANIMATION_SPEED = 0.02
time = 0
time_factor = 0

#Initial values for speed, rpm, and load
speed = 0
rpm = 0
load = 0

class image_blitter:
    def __init__(self, Font, path, num_frames, max_value, pos, size,title=""):
        self.Font = Font
        self.title = title
        self.path = path
        self.num_frames = num_frames
        self.max_value = max_value
        self.pos = pos
        self.size = size

    def draw(self, value):
        increments = self.max_value / self.num_frames
        frame = min(int(value / increments), self.num_frames)
        frame_path = "{}-{}.png".format(self.path,frame)

        image = pygame.image.load(frame_path)
        image = pygame.transform.scale(image, self.size)
        screen.blit(image, self.pos)

        #Write text if provided
        title_text = self.Font.render(self.title, True, LIGHT_YELLOW)
        title_text_rect = title_text.get_rect(center=(self.pos[0]+self.size[0]/2, self.pos[1]+self.size[1]))
        screen.blit(title_text, title_text_rect)


class Line_Bar:
    def __init__(self, FONT, colour, x, y, size, min, max, unit=""):
        self.Font = FONT
        self.colour=colour
        self.size=size
        self.min=min
        self.max=max
        self.x=x
        self.y=y
        self.unit=unit
    def draw(self, value):
        num_lines = 16
        increments = self.max / 16
        if value >= increments * 1:
            pygame.draw.line(screen, LIGHT_YELLOW, (self.x, self.y), (self.x-50, self.y-0), width=3)
        if value >= increments * 2:    
            pygame.draw.line(screen, LIGHT_YELLOW, (self.x+5, self.y-10), (self.x-45, self.y-10), width=3)
        if value >= increments * 3:
            pygame.draw.line(screen, LIGHT_YELLOW, (self.x+10, self.y-20), (self.x-40, self.y-20), width=3)
        if value >= increments * 4:
            pygame.draw.line(screen, LIGHT_YELLOW, (self.x+15, self.y-30), (self.x-20, self.y-30), width=3)
        if value >= increments * 5:
            pygame.draw.line(screen, LIGHT_YELLOW, (self.x+17, self.y-35), (self.x-10, self.y-40), width=3)
        if value >= increments * 6:
            pygame.draw.line(screen, LIGHT_YELLOW, (self.x+20, self.y-40), (self.x-0, self.y-50), width=3)
        if value >= increments * 7:
            pygame.draw.line(screen, LIGHT_YELLOW, (self.x+23, self.y-45), (self.x+10, self.y-60), width=3)
        if value >= increments * 8:
            pygame.draw.line(screen, LIGHT_YELLOW, (self.x+27, self.y-50), (self.x+20, self.y-65), width=3)
        if value >= increments * 9:
            pygame.draw.line(screen, LIGHT_YELLOW, (self.x+33, self.y-50), (self.x+33, self.y-70), width=3)
        if value >= increments * 10:
            pygame.draw.line(screen, LIGHT_YELLOW, (self.x+43, self.y-50), (self.x+43, self.y-70), width=3)
        if value >= increments * 11:
            pygame.draw.line(screen, LIGHT_YELLOW, (self.x+53, self.y-50), (self.x+53, self.y-70), width=3)
        if value >= increments * 12:
            pygame.draw.line(screen, LIGHT_YELLOW, (self.x+63, self.y-50), (self.x+63, self.y-70), width=3)
        if value >= increments * 13:
            pygame.draw.line(screen, LIGHT_YELLOW, (self.x+73, self.y-50), (self.x+73, self.y-70), width=3)
        if value >= increments * 14:
            pygame.draw.line(screen, RED, (self.x+83, self.y-50), (self.x+83, self.y-70), width=3)
        if value >= increments * 15:
            pygame.draw.line(screen, RED, (self.x+93, self.y-50), (self.x+93, self.y-70), width=3)
        if value >= increments * 16:
            pygame.draw.line(screen, RED, (self.x+103, self.y-50), (self.x+103, self.y-70), width=3)

        pertext = self.Font.render("{:.0f}".format(value) + self.unit, True, LIGHT_YELLOW)
        pertext_rect = pertext.get_rect(center=(int(self.x+60), int(self.y-20)))
        screen.blit(pertext, pertext_rect)


class Progress_Bar:
    def __init__(self, colour, left, top, maxwidth, height, max):
        self.colour=colour
        self.left=left
        self.top=top
        self.maxwidth=maxwidth
        self.height=height
        self.max = max
    def draw(self, value):
        percent = value / self.max
        percent = min(percent, 1.0)
        pygame.draw.rect(screen, self.colour, pygame.Rect(self.left,self.top,self.maxwidth*percent,self.height))
        pygame.draw.rect(screen, self.colour, pygame.Rect(self.left,self.top,self.maxwidth,self.height), 1)
    
class Counter_Bar:
    def __init__(self, screen, FONT, name, colour, start_loc_x, start_loc_y, square_size, count):
        self.screen=screen
        self.name=name
        self.font=FONT
        self.colour=colour
        self.start_loc_x=start_loc_x
        self.start_loc_y=start_loc_y
        self.square_size=square_size
        self.count=count
    def draw(self, num):
        for i in range(self.count):
            if(i<(self.count-num)):
                pygame.draw.rect(screen, self.colour, pygame.Rect(self.start_loc_x,self.start_loc_y+(i*self.square_size*1.5),self.square_size,self.square_size),1,border_radius=5)
            else:
                pygame.draw.rect(screen, self.colour, pygame.Rect(self.start_loc_x,self.start_loc_y+(i*self.square_size*1.5),self.square_size,self.square_size),0,border_radius=5)
        nametext = self.font.render(self.name, True, self.colour)
        nametext_rect = nametext.get_rect(center=(12+int(self.start_loc_x), self.start_loc_y+int(self.count*self.square_size*1.5)))
        self.screen.blit(nametext, nametext_rect)

def drawArc(surface, x, y, r, th, start, stop, color):
    points_outer = []
    points_inner = []
    n = round(r*abs(stop-start)/20)
    if n<2:
        n = 2
    for i in range(n):
        delta = i/(n-1)
        phi0 = start + (stop-start)*delta
        x0 = round(x+r*math.cos(phi0))
        y0 = round(y+r*math.sin(phi0))
        points_outer.append([x0,y0])
        phi1 = stop + (start-stop)*delta
        x1 = round(x+(r-th)*math.cos(phi1))
        y1 = round(y+(r-th)*math.sin(phi1))
        points_inner.append([x1,y1])
    points = points_outer + points_inner        
    pygame.gfxdraw.aapolygon(surface, points, color)
    pygame.gfxdraw.filled_polygon(surface, points, color)

class Gauge:
    def __init__(self, screen, FONT, x_cord, y_cord, thickness, radius, circle_colour, max, unit='', title='',glow=True):
        self.screen = screen
        self.Font = FONT
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.thickness = thickness
        self.radius = radius
        self.circle_colour = circle_colour
        self.glow = glow
        self.unit = unit
        self.title = title
        self.max = max

    def draw(self, value, unit=""):
        percent = value / self.max
        percent = min(percent, 1.0)
        percent = percent*100
        fill_angle = int(percent*270/100)
        per=percent
        if percent > 100:
            percent = 100
        if per <=40:
            per=0
        if per > 100:
            per = 100
        ac = [int(255-per*255/100),int(per*255/100),int(0), 255]
        ac = LIGHT_YELLOW
        for indexi in range(len(ac)):
            if ac[indexi] < 0:
                ac[indexi] = 0
            if ac[indexi] > 255:
                ac[indexi] = 255
        if(value > 1):
            pertext = self.Font.render("{:.0f}".format(value) + unit, True, ac)
        else:
            pertext = self.Font.render("{:.2f}".format(value) + unit, True, ac)
        pertext_rect = pertext.get_rect(center=(int(self.x_cord), int(self.y_cord)))
        self.screen.blit(pertext, pertext_rect)

        # Text & units
        unittext = self.Font.render(self.unit, True, ac)
        unittext_rect = unittext.get_rect(center=(int(self.x_cord), int(self.y_cord+20)))
        self.screen.blit(unittext, unittext_rect)
        small_font = pygame.font.Font('retro.ttf', 12)
        titletext = small_font.render(self.title, True, ac)
        titletext_rect = titletext.get_rect(center=(int(self.x_cord), int(self.y_cord-47)))
        self.screen.blit(titletext, titletext_rect)
        for i in range(0, self.thickness):
            pygame.gfxdraw.arc(screen, int(self.x_cord), int(self.y_cord), self.radius - i, -225, 270 - 225, self.circle_colour)
            pygame.gfxdraw.arc(screen, int(self.x_cord-1), int(self.y_cord), self.radius - i, -225, 270 - 225, self.circle_colour)
            pygame.gfxdraw.arc(screen, int(self.x_cord+1), int(self.y_cord), self.radius - i, -225, 270 - 225, self.circle_colour)
            if percent >4:
                pygame.gfxdraw.arc(screen, int(self.x_cord), int(self.y_cord), self.radius - i, -225, fill_angle - 225-8, ac)
                pygame.gfxdraw.arc(screen, int(self.x_cord-1), int(self.y_cord), self.radius - i, -225, fill_angle - 225-8, ac)
                pygame.gfxdraw.arc(screen, int(self.x_cord+1), int(self.y_cord), self.radius - i, -225, fill_angle - 225-8, ac)
        if percent < 4:
            return
        if self.glow:
            for i in range(0,15):
                ac [3] = int(150 - i*10)
                pygame.gfxdraw.arc(screen, int(self.x_cord), int(self.y_cord), self.radius + i, -225, fill_angle - 225-8, ac)
            for i in range(0,15):
                ac [3] = int(150 - i*10)
                pygame.gfxdraw.arc(screen, int(self.x_cord), int(self.y_cord), self.radius -self.thickness - i, -225, fill_angle - 225-8, ac)
            angle_r = math.radians(fill_angle-225-8)
            lx,ly = int((self.radius-self.thickness/2)*math.cos(angle_r)), int( (self.radius-self.thickness/2)*math.sin(angle_r))
            ac[3] = 255
            lx = int(lx+self.x_cord)
            ly = int(ly + self.y_cord)
            pygame.draw.circle(self.screen,ac,(lx,ly),int(self.thickness/2),0)
            for i in range(0,10):
                ac [3] = int(150 - i*15)
                pygame.gfxdraw.arc(screen, int(lx), int(ly), (self.thickness//2)+i , fill_angle -225-10, fill_angle - 225-180-10, ac)

#Method used to draw our graphics to the screen
def draw_screen():
    screen.fill(BLACK)
    # screen.fill(BLACK)
    # pygame.draw.rect(screen, WHITE, pygame.Rect(5, 5, 150, 150), 2)
    # pygame.draw.rect(screen, WHITE, pygame.Rect(270, 5, 150, 150), 2)
    # pygame.draw.rect(screen, WHITE, pygame.Rect(155, 100, 115, 115), 2)
    
    # speedF = pygame.font.Font("retro.ttf", 30)
    # speedText = speedF.render("Speed", True, WHITE)
    # screen.blit(speedText, (15, 160))
     
    # rpmF = pygame.font.Font("retro.ttf", 30)
    # rpmText = rpmF.render("RPM", True, WHITE)
    # screen.blit(rpmText, (310, 160))
    
    # loadF = pygame.font.Font("retro.ttf", 30)
    # loadText = loadF.render("Load", True, WHITE)
    # screen.blit(loadText, (175, 60))

#Commands to query for data
c1 = obd.commands.SPEED
c2 = obd.commands.RPM
c3 = obd.commands.ENGINE_LOAD

#Tracks the values of speed, rpm, and load since they will be constantly changing as you drive
def speedTracker(s):
    global speed
    if not s.is_null():
        speed = int(s.value.magnitude * .621)
    
def rpmTracker(r):
    global rpm
    if not r.is_null():
        rpm = int(r.value.magnitude)

def loadTracker(l):
    global load
    if not l.is_null():
        load = int(l.value.magnitude)

#Watches the data extracted by the obd adapter        
# connection.watch(c1, callback=speedTracker)
# connection.watch(c2, callback=rpmTracker)
# connection.watch(c3, callback=loadTracker)
# connection.start()

bar = Progress_Bar(
    colour=LIGHT_YELLOW,
    left = 310,
    top = 40,
    maxwidth = 700,
    height=30,
    max=7000
)
percentage=0.7
circle_c = (126, 245, 95)
FONT = pygame.font.Font('retro.ttf', 20)
medium_font = pygame.font.Font('retro.ttf', 15)
gear_counter = Counter_Bar(
    screen=screen,
    FONT=FONT,
    name="Gear",
    colour=LIGHT_YELLOW,
    start_loc_x=985,
    start_loc_y=100,
    square_size=25,
    count=6
)
pressure_guage = Gauge(
        screen=screen,
        FONT=medium_font,
        x_cord=340,
        y_cord=170,
        thickness=5,
        radius=40,
        circle_colour=BLACK,
        glow=False,
        unit="Pa",
        title="Manifold Pressure",
        max=1.0)
coolant_temp_guage = Gauge(
        screen=screen,
        FONT=medium_font,
        x_cord=480,
        y_cord=170,
        thickness=5,
        radius=40,
        circle_colour=BLACK,
        glow=False,
        unit="",
        title="Coolant Temp",
        max=200.0)
maf_guage = Gauge(
        screen=screen,
        FONT=medium_font,
        x_cord=610,
        y_cord=170,
        thickness=5,
        radius=40,
        circle_colour=BLACK,
        glow=False,
        unit="gps",
        title="Air Flow Rate",
        max=100.0)

mph_line_dial = Line_Bar(
    FONT,
    LIGHT_YELLOW,
    830,
    345,
    5,
    0,
    120,
    unit="mph"
)

fuel_icon = image_blitter(
    FONT,
    "resources/fuel_icons/fuel-cell",
    10,
    100,
    (670,70),
    (300, 150),
    "Fuel"
)
    
running =  True
car_state = 1
elapsed_time = 0
image_on = True
#Pygame loop which displays our graphics as well as our speed, load, and rpm values
while running:
    dt = clock.tick(60) / 1000

    #Tick for blinking.
    elapsed_time += clock.tick(60)
    if elapsed_time > 250:
        image_on = False if image_on else True
        elapsed_time = 0

    for event in pygame.event.get():
        # handle MOUSEBUTTONUP
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if(pos[0] > 330 and pos[0] < 500):
                if(pos[1] > 200 and pos[1] < 340):
                    car_state = 1 if car_state == 0 else 0

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                pygame.display.quit()
                pygame.quit()
            # if event.key == pygame.K_UP:
            #     percentage += 1
            # if event.key == pygame.K_DOWN:
            #     percentage -= 1

    key_input = pygame.key.get_pressed()

    if key_input[pygame.K_UP]:
        percentage += 0.01
    if key_input[pygame.K_DOWN]:
        percentage -= 0.01
    
    draw_screen()
    bar.draw(value=percentage*70)
    pressure_guage.draw(value=percentage)
    coolant_temp_guage.draw(value=percentage*100)
    maf_guage.draw(value=percentage*100)
    gear_counter.draw(math.trunc(percentage/20))
    mph_line_dial.draw(percentage*160)
    if(percentage > 0.01):
        fuel_icon.draw(100-(percentage*100))
    else:
        if image_on:
            fuel_icon.draw(100-(percentage*100))

    rpm_text = FONT.render("rpm", True, LIGHT_YELLOW)
    rpm_text_rect = rpm_text.get_rect(center=(280, 55))
    screen.blit(rpm_text, rpm_text_rect)

    pygame.draw.rect(screen, LIGHT_YELLOW, pygame.Rect(200, 30, WIDTH-400, HEIGHT-60), width=3)
    pygame.draw.line(screen, LIGHT_YELLOW, (0, 0), (200, 30), width=3)
    pygame.draw.line(screen, LIGHT_YELLOW, (0, HEIGHT), (200, HEIGHT-30), width=3)
    pygame.draw.line(screen, LIGHT_YELLOW, (WIDTH, 0), (WIDTH-200, 30), width=3)
    pygame.draw.line(screen, LIGHT_YELLOW, (WIDTH, HEIGHT), (WIDTH-200, HEIGHT-30), width=3)

    for i in letter_instances:
        if (time_factor%20) < 1:
            i[0] = randint(0,NUM_SYMBOLS)
        symbol=letter_symbols[i[0]]
        screen.blit(symbol,i[1])

    spacing = 50
    height_factor = 8
    for i in range (int(200 / spacing)):
        x_pos = ((i*spacing)-time_factor)%200
        y_length = ((i*height_factor)-(time_factor/6.2))
        while (y_length < 0):
            y_length += int(200 / spacing) * height_factor
        pygame.draw.line(screen, LIGHT_YELLOW, (x_pos, y_length), (x_pos, HEIGHT-y_length), width=2)

        x_pos_right = ((WIDTH-(i*spacing))+time_factor)%200
        y_length_right = ((i*height_factor)+(time_factor/6.2))
        pygame.draw.line(screen, LIGHT_YELLOW, (WIDTH-x_pos, y_length), (WIDTH-x_pos, HEIGHT-y_length), width=2)

    #Draw car schematic
    if(car_state == 0):
        car_image_top = pygame.image.load("resources/car_top.png")
        car_image_top = pygame.transform.scale(car_image_top, (250, 100))
        screen.blit(car_image_top, (340, 240))
    elif(car_state == 1):
        car_image_side = pygame.image.load("resources/car_side.png")
        car_image_side = pygame.transform.scale(car_image_side, (270, 100))
        screen.blit(car_image_side, (330, 240))

    time += dt*percentage*4
    if time > 5000:
        time = 0
    time_factor = (time)
    
    pygame.display.update()
    pygame.display.flip()
    
pygame.quit()
