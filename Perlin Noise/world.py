import noise
import numpy as np
import matplotlib.pyplot as plt

shape = (1024, 1024)
blue = [65, 105, 225]
green = [34, 139, 34]
beach = [238, 214, 175]
snow = [255, 250, 250]
mountain = [139, 137, 137]
dark_green = [0, 100, 0]
sandy = [210, 180, 140]

world = np.zeros(shape)

for i in range(shape[0]):
    for j in range(shape[1]):
        rand = noise.pnoise2(i / 100, j / 100, octaves=6, persistence=.5, lacunarity=2, repeatx=1024, repeaty=1024,
                             base=0)
        world[i][j] = rand

plt.axis("off")
plt.imshow(world, cmap='gray')
plt.tight_layout()
plt.show()

colored_world = np.zeros(shape+(3,)).astype(np.uint8)

for i in range(shape[0]):
    for j in range(shape[1]):
        if world[i][j] < 0.05:
            colored_world[i][j] = blue
        elif world[i][j] < 0.1:
            colored_world[i][j] = beach
        elif world[i][j] < .25:
            colored_world[i][j] = green
        elif world[i][j] < 0.7:
            colored_world[i][j] = mountain
        elif world[i][j] < 1.0:
            colored_world[i][j] = snow

plt.axis("off")
plt.imshow(colored_world)
plt.tight_layout()
plt.show()

a, b = shape[0]/2, shape[1]/2
n = 1024
r = 125
y, x = np.ogrid[-a:n - a, -b:n - b]
mask = x ** 2 + y ** 2 <= r ** 2

black = [0, 0, 0]
island_world = np.zeros_like(colored_world)

for i in range(shape[0]):
    for j in range(shape[1]):
        if mask[i][j]:
            island_world[i][j] = colored_world[i][j]
        else:
            island_world[i][j] = black

plt.axis("off")
plt.imshow(island_world)
plt.tight_layout()
plt.show()

center_x, center_y = shape[1] // 2, shape[0] // 2
circle_grad = np.zeros(shape)

for x in range(shape[0]):
    for y in range(shape[1]):
        circle_grad[x][y] = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 1/2

max_grad = np.max(circle_grad)
circle_grad = circle_grad / max_grad
circle_grad -= 0.5
circle_grad *= 2.0
circle_grad = -circle_grad

for x in range(shape[0]):
    for y in range(shape[1]):
        if circle_grad[x][y] > 0:
            circle_grad[x][y] *= 20

max_grad = np.max(circle_grad)
circle_grad = circle_grad / max_grad

plt.axis("off")
plt.imshow(circle_grad, cmap='gray')
plt.tight_layout()
plt.show()

world_noise = np.zeros(shape)

for i in range(shape[0]):
    for j in range(shape[1]):
        world_noise[i][j] = world[i][j] * circle_grad[i][j]
        if world_noise[i][j] > 0:
            world_noise[i][j] *= 20

max_grad = np.max(world_noise)
world_noise = world_noise / max_grad

plt.axis("off")
plt.imshow(world_noise, cmap='gray')
plt.tight_layout()
plt.show()

threshold = 0
island_world_grad = np.zeros(shape+(3,)).astype(np.uint8)

for i in range(shape[0]):
    for j in range(shape[1]):
        if world_noise[i][j] < threshold + 0.05:
            island_world_grad[i][j] = blue
        elif world_noise[i][j] < threshold + 0.055:
            island_world_grad[i][j] = sandy
        elif world_noise[i][j] < threshold + 0.1:
            island_world_grad[i][j] = beach
        elif world_noise[i][j] < threshold + 0.25:
            island_world_grad[i][j] = green
        elif world_noise[i][j] < threshold + 0.6:
            island_world_grad[i][j] = dark_green
        elif world_noise[i][j] < threshold + 0.7:
            island_world_grad[i][j] = mountain
        elif world_noise[i][j] < threshold + 1.0:
            island_world_grad[i][j] = snow

plt.axis("off")
plt.imshow(island_world_grad, cmap='gray')
plt.tight_layout()
plt.show()
