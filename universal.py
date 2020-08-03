from scipy import ndimage

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import datetime

import random


import rd_utils as rdu
import systems as rds

frame = 0
def display(g, icl, im, icu, debug=False, bins=5):
    global frame
    if debug:
        frame+=1
        #print("\n", np.histogram(g, bins=bins))
        #print(  np.histogram(g, bins=bins)[1] )
        h = np.histogram(g, bins=bins)[1]
        #print(h)
        print(f"Frame {frame}: {min(h):.4f} {((max(h)+min(h))/2):.4f} {max(h):.4f}")
    else:
        pass
    return (rdu.remap(g, icl, im, icu))


def evolve_grid(g, kernel,mode, Da, Db, f, k):
    #take a grid of reagents (A, B) and return one timestep evolution of their interaction
    n = g.copy()
    a = n[:, :, 0]   # A chemical
    b = n[:, :, 1]   # B chemical

    laplace_a = ndimage.convolve(a, kernel, mode=mode, cval=0)
    laplace_b = ndimage.convolve(b, kernel, mode=mode, cval=0)

    n[:, :, 0] = a + (Da * laplace_a - a * b * b + f * (1 - a))
    n[:, :, 1] = b + (Db * laplace_b + a * b * b - (k + f) * b)

    return n


def updatefig(*args):
    iterations = args[1]
    grid = args[2]
    dg={
        'a': grid[:,:,0],
        'b': grid[:,:,1]
    }
    reagent= args[3]
    factors = args[4]
    im = args[5]
    kernel = args[6]
    icl = args[7]
    mid = args[8]
    icu = args[9]
    debug = args[10]
    mode = args[11]

    for _ in range(iterations):
        grid[:,:,:] = evolve_grid(grid, kernel, mode, factors['Da'], factors['Db'], factors['f'], factors['k'])
    im.set_array(display(dg[reagent],  icl, mid, icu, debug))



def run(model, setup_func, reagent,  frames, iterations, kernel, edge_mode,
        rows=300, cols=300, debug=False ):

    reagent = reagent.lower()
    try:
        params = rds.pearson[model]
        cmap = params['cmap'][reagent.lower()]
    except KeyError:
        print(f"Unknown model '{model}'")
        return

    grid = setup_func(rows, cols)

    fig = plt.figure()
    ax = plt.gca()
    ax.axes.xaxis.set_visible(False)
    ax.axes.yaxis.set_visible(False)

    scales = params['scaling']
    icl = scales[reagent]['icl']
    mid = scales[reagent]['im']
    icu = scales[reagent]['icu']

    dg={
        'a': grid[:,:,0],
        'b': grid[:,:,1]
    }


    im = plt.imshow(display(dg[reagent], icl, mid, icu, debug), animated=True,
                    cmap=plt.get_cmap(cmap), vmin=0, vmax=1)
    ani = animation.FuncAnimation(fig,  updatefig, frames=frames, interval=1,
            blit=False, fargs=(iterations,grid, reagent, params['factors'],im, kernel, icl,mid, icu, debug, edge_mode))
    plt.show()

    Writer = animation.writers['ffmpeg']   #https://stackoverflow.com/a/60920880/3556757
    writer = Writer(fps=15, metadata=dict(artist='by Rumple Mâché'), bitrate=1800)

    #fn = datetime.datetime.now().strftime(f"gallery\\type_{params['file_stub']}_({reagent.upper()})_%Y_%b_%d_%H_%M_%S")
    fn = f"gallery\\pearson_{params['file_stub']}_({reagent.upper()})"
    ani.save(f"{fn}.mp4", writer=writer)
    print(f"Done reagent {reagent.upper()} as {fn}")
    print(f"{params['description']}")



if __name__ == "__main__":
    print("Running")

    BATCH = False
    if BATCH:
        for category  in rds.pearson.keys():
            frame=0
            if category[0] != "*":
                print(category)
                for reagent in ['a', 'b']:
                    run(model=category,
                        setup_func=rdu.setup_grid_pearson,
                        reagent=reagent,
                        frames=500,
                        iterations=50,
                        kernel=rds.kernels['standard'],
                        edge_mode="wrap",
                        debug=True
                        )
            else:
                print(f"excluding {category}")
    else:
        run(model='gamma_right',
            setup_func=rdu.setup_grid_pearson,
            reagent="a",
            frames=500,
            iterations=50,
            kernel = rds.kernels['standard'],
            edge_mode="wrap",
            debug=True
            )
