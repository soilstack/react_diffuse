# react_diffuse

###Reaction-Diffusion Experimentation


![vanilla reaction](https://raw.githubusercontent.com/soilstack/react_diffuse/master/example.png)

Was interested in the Coding Train's version of the Reaction-Diffusion model.  Coded in javascript, with a lot of 
for-loops and iteration, I thought, "gee, I'll write somethign similar using Numpy matrix 
routines and it'll be blazingly faster."  

Hmm, hasn't turned out that way -- It's a bit 
difficult to compare because CT's version live-updates the animation, while I have to 
generate the animation as an MP4 first,  but the overall time to run is not materially 
faster in my version.  Not sure  why -- I don't think I did anything grievously wrong.  

Current configuration is pretty plain vanilla; should next make a version that allows for easily
dropping in new parameters, weird kernels, and other setup routines.


####Primary Sources
1. [Karl Sims Original](http://karlsims.com/rd.html)
1. [Detailed discussion of Gray-Scott Model](http://mrob.com/pub/comp/xmorphia/)
1. [Coding Train Reaction-Diffusion (based on Karl Sims)](https://www.youtube.com/watch?v=BV9ny785UNc&t=2100s)
