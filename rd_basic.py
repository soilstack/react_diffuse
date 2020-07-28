from scipy import ndimage

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import datetime

# B's consume A's to make more B's
Da = 1.0  #diffusion rate of reagent A
Db = 0.5  #diffusion rate of reagent B
f = 0.055  # Feed rate of reagent A
k = 0.062  #kill rate of reagent B (scaled so never less than feed rate)
kernel = np.array([[0.05, 0.2, 0.05],[0.2,-1,0.2],[0.05, 0.2, 0.05]], )  #wavg diff between cell & surrounding cells

ANIMATION_FRAMES = 200
ITER_PER_ANIMATION_FRAME = 50

def display(g):
    # take grid of reagents (A, B) and return resulting color value
    #show how much more b than A
    return (g[:, :, 0] - g[:, :, 1]) * 255

def evolve_grid(g):
    #take a grid of reagents (A, B) and return one timestep evolution of their interaction
    n = g.copy()
    a = n[:, :, 0]   # A chemical
    b = n[:, :, 1]   # B chemical

    laplace_a = ndimage.convolve(a, kernel, mode='constant', cval=0)
    laplace_b = ndimage.convolve(b, kernel, mode='constant', cval=0)

    n[:, :, 0] = a + (Da * laplace_a - a * b * b + f * (1 - a))
    n[:, :, 1] = b + (Db * laplace_b + a * b * b - (k + f) * b)

    #n = np.clip(n, 0,1)  # This troubles me -- why would the calc ever yield > 1.0 in the first place?
    return n

def setup_grid_basic(rows=500, cols=500):
    #just make a block of B
    grid = np.ones((rows, cols, 2))
    grid[:, :, 1] = 0
    for i in range(30, 40):
        for j in range(30, 40):
            grid[i, j, 1] = 1
    return grid


def setup_grid_basic_noise(rows=500, cols=500):
    #just make a block of B in random concentration
    grid = np.ones((rows, cols, 2))
    grid[:, :, 1] = 0
    grid[30:40,30:50,1] = np.random.rand(10,20)
    return grid


def updatefig(*args):
    iterations = args[1]
    global grid
    for _ in range(iterations):
        grid = evolve_grid(grid)
    im.set_array(display(grid))
    return im

print("setup")
grid = setup_grid_basic_noise(rows = 300, cols=300)

fig = plt.figure()
im = plt.imshow(display(grid), animated=True, cmap=plt.get_cmap("copper"))   #https://matplotlib.org/3.1.0/tutorials/colors/colormaps.html

ani = animation.FuncAnimation(fig,  updatefig, frames=ANIMATION_FRAMES, interval=1, blit=False, fargs=(ITER_PER_ANIMATION_FRAME,))

plt.show()

# Set up formatting for the movie files
Writer = animation.writers['ffmpeg']   #https://stackoverflow.com/a/60920880/3556757
writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)

fn = datetime.datetime.now().strftime("rd_%Y_%b_%d_%H_%M_%S")
ani.save(f"{fn}.mp4", writer=writer)

print(f"done {fn}")
