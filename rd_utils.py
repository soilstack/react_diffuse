import numpy as np
import random

def remap(a, icl, im, icu, ):
    # clip the input upper and lower limits. Then map the lower section to ouput (0,0.5], and upper to output (0.5,1)
    # input_clip_lower, input_mid, input_clip_upper
    a = np.clip(a, icl, icu)  # clip levels
    ibr = im - icl  # input bottom range
    iur = icu - im  # input upper range
    lower_mask = a[:, :] <= im
    upper_mask = a[:, :] > im

    # lower-half
    m = (0.5 - 0) / (im - icl)
    b = 0 - m * icl
    a[lower_mask] = m * a[lower_mask] + b

    # upper-half
    m = (1 - 0.5) / (icu - im)
    b = 0.5 - m * im  # b = y-mx
    a[upper_mask] = m * a[upper_mask] + b  # y = mx+b

    return a


def setup_grid_pearson(rows=500, cols=500, blob_scale=0.1):
    #20x20 mesh point area located symmetrically around center to U(a) = 1/2,  V(b)=1/4.
    #These conditions perturbed +/- 1% random noise to break the square symmetery
    grid = np.ones((rows, cols, 2))
    grid[:, :, 1] = 0

    DEV = 0.09
    from_row = int((rows/2) - rows*blob_scale/2)
    to_row = int((rows/2) + rows*blob_scale/2)
    from_col = int((cols / 2) - cols * blob_scale / 2)
    to_col = int((cols / 2) + cols * blob_scale / 2)

    for i in range(from_row, to_row):
        for j in range(int(random.uniform(1-DEV, 1+DEV)*from_col),
                       int(random.uniform(1-DEV, 1+DEV)*to_col)
                       ):
            grid[i,j,0] = 0.5
            grid[i,j,1] = 0.25

    grid[from_row:to_row, from_col:to_col,:] = (
                            (1+np.random.rand(to_row-from_row, to_col-from_col, 2) / 10)
                            *
                            grid[from_row:to_row, from_col:to_col, :]
    )

    return grid

