# react_diffuse

###Reaction-Diffusion Experimentation

Gray-Scott simulator.  In the gallery, I have simulated examples of all of Pearson's categories.  Karl Sims found some 
more esoteric ones, which weren't immediately reproducible. Maybe I'll mess with them later.

* `universal.py` is the simulator engine
* `systems.py` holds dictionaries of convolution kernels and parameter (`Da, Db, F, k`) combinations, along with scaling and color scheme metadata
* `rd_utils.py` is where I add routines to setup the grid before the reaction starts.


####Primary Sources
1. [Karl Sims Original](http://karlsims.com/rd.html)
1. [Detailed discussion of Gray-Scott Model](http://mrob.com/pub/comp/xmorphia/)
1. [Coding Train Reaction-Diffusion (based on Karl Sims)](https://www.youtube.com/watch?v=BV9ny785UNc&t=2100s)
1. [Pearson canonical labelling of systems](https://arxiv.org/abs/patt-sol/9304003)
