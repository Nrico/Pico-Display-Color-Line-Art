import board
import displayio
import busio
import adafruit_st7789
import adafruit_display_shapes.line as Line
import random
import time
from math import cos, sin

# Release any resources currently in use for the displays
displayio.release_displays()

# Initialize SPI0
spi = busio.SPI(clock=board.GP18, MOSI=board.GP19)

# Pimoroni Pico Display configuration and initialization
tft_cs = board.GP17
tft_dc = board.GP16
tft_reset = board.GP15

display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=tft_reset)
display = adafruit_st7789.ST7789(display_bus, width=240, height=135, rowstart=40, colstart=53, rotation=270)

def generate_random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def draw_thick_line(x_start, y_start, x_end, y_end, thickness, color, group):
    # For simplicity, this function draws multiple parallel lines for thickness.
    # It works best for vertical or horizontal lines, diagonal lines will have a stepped appearance.
    for i in range(thickness):
        line = Line.Line(int(x_start), int(y_start) + i, int(x_end), int(y_end) + i, color=color)
        group.append(line)

def generate_random_line_coords(display_width, display_height):
    x_start = random.randint(0, display_width - 1)
    y_start = random.randint(0, display_height - 1)
    angle = random.uniform(0, 2 * 3.14159265)  # Random angle between 0 and 2*pi
    length = random.randint(5, 50)  # Random line length between 5 and 50 pixels
    x_end = x_start + int(length * cos(angle))
    y_end = y_start + int(length * sin(angle))
    return (x_start, y_start, x_end, y_end)

while True:
    num_lines = random.randint(5, 20)

    current_coords = [generate_random_line_coords(240, 135) for _ in range(num_lines)]
    target_coords = [generate_random_line_coords(240, 135) for _ in range(num_lines)]

    STEPS = 100  # number of steps for the transition
    PAUSE = 0.1  # pause for each step (controls the speed of the transition)

    for step in range(STEPS):
        group = displayio.Group()

        for i in range(num_lines):
            x_start = current_coords[i][0] + (target_coords[i][0] - current_coords[i][0]) * step / STEPS
            y_start = current_coords[i][1] + (target_coords[i][1] - current_coords[i][1]) * step / STEPS
            x_end = current_coords[i][2] + (target_coords[i][2] - current_coords[i][2]) * step / STEPS
            y_end = current_coords[i][3] + (target_coords[i][3] - current_coords[i][3]) * step / STEPS
            
            color = generate_random_color()
            thickness = random.randint(1, 3)  # Random thickness between 1 and 3 pixels
            draw_thick_line(x_start, y_start, x_end, y_end, thickness, color, group)

        display.show(group)
        time.sleep(PAUSE)

    time.sleep(5)  # pause for 5 seconds after each transition
