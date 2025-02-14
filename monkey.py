import numpy as np
import os, time, keyboard

# Parameters
width, height, resolution = 120, 120, 5
symbol = "o"
# Monkey saddle surface function
def monkey_saddle(x, y):
    #return np.sqrt(5 - x**2 - y**2) # Sphere
    ##return x**3 - 3 * x * y**2 # Monkey Saddle
    #return np.sin(2*x)+np.sin(2*y)
    return np.sin(2*x)

def rotate_z(x, y, z, angle_z):
    angle_z_rad = np.radians(angle_z)
    x_new = x * np.cos(angle_z_rad) - y * np.sin(angle_z_rad)
    y_new = x * np.sin(angle_z_rad) + y * np.cos(angle_z_rad)
    return x_new, y_new, z

x = np.linspace(-resolution, resolution, width)
y = np.linspace(-resolution, resolution, height)
x, y = np.meshgrid(x, y)

z = monkey_saddle(x, y)

mask = (x >= -resolution) & (x <= resolution) & (y >= -resolution) & (y <= resolution) & (z >= -resolution) & (z <= resolution)
x, y, z = x[mask], y[mask], z[mask]

# Function to project 3D coordinates to 2D screen space with camera tilt
def project(x, y, z, angle_z):
    x_rot, y_rot, z_rot = rotate_z(x, y, z, angle_z)
    camera_angle = np.radians(camera_tilt)
    y_proj = y_rot * np.cos(camera_angle) - z_rot * np.sin(camera_angle)
    z_proj = y_rot * np.sin(camera_angle) + z_rot * np.cos(camera_angle)
    x_screen = x_rot
    y_screen = z_proj

    return x_screen, y_screen

# Function to interpolate RGB values based on normalized Z
def get_rgb_gradient(value):
    value = 1-value
    if value < 0.25:
        r = 0.5 - 2 * value
        g = 0
        b = 0.5 + 2 * value
    elif value < 0.5:
        r = 0
        g = 4 * (value - 0.25)
        b = 1 - 4 * (value - 0.25)
    elif value < 0.75:
        r = 4 * (value - 0.5)
        g = 1
        b = 0
    else:
        r = 1
        g = 1 - 4 * (value - 0.75)
        b = 0
    return int(r * 255), int(g * 255), int(b * 255)

def rgb_to_ansi(r, g, b):
    return 16 + (36 * (r // 51)) + (6 * (g // 51)) + (b // 51)

def print_graph(angle_z):
    # Project 3D coordinates to 2D screen space
    x_screen, y_screen = project(x, y, z, angle_z)
    z_normalized = (z - z.min()) / (z.max() - z.min())
    grid = [[' ' for _ in range(width)] for _ in range(height)]

    # Map the projected points to the grid
    for i in range(len(x_screen)):
        x_idx = int((x_screen[i] + resolution) * (width - 1) / (2 * resolution))
        y_idx = int((y_screen[i] + resolution) * (height - 1) / (2 * resolution))
        if 0 <= x_idx < width and 0 <= y_idx < height:
            r, g, b = get_rgb_gradient(z_normalized[i])
            color_code = rgb_to_ansi(r, g, b)
            grid[y_idx][x_idx] = f"\033[38;5;{color_code}m{symbol}"

    # Clear the terminal and print the ASCII art
    os.system('clear')
    for row in grid:
        print("".join(row))
    print("\033[0m")

angle_z = 0
camera_tilt = 0

print_graph(angle_z)

while True:
    if keyboard.is_pressed("left"):
        angle_z -= 1
        print(f"rotation: {angle_z}, tilt: {camera_tilt}")
        print_graph(angle_z)

    elif keyboard.is_pressed("right"):
        print(f"rotation: {angle_z}, tilt: {camera_tilt}")
        angle_z += 1
        print_graph(angle_z)
    if keyboard.is_pressed("up"):
        camera_tilt += 1
        print(f"rotation: {angle_z}, tilt: {camera_tilt}")
        print_graph(angle_z)
    elif keyboard.is_pressed("down"):
        camera_tilt -= 1
        print(f"rotation: {angle_z}, tilt: {camera_tilt}")
        print_graph(angle_z)

# while True:
#     angle_z+=1
#     camera_tilt+=1
#     print_graph(angle_z)
#     time.sleep(0.01)
