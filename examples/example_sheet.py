#!/usr/bin/python

import numpy as np

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pyrodeo

# Domain half-width in x and y
Lx = 2.0
Ly = 20.0

# Create simulation, setting grid dimensions and domain
sim = pyrodeo.Simulation.from_geom('sheet',
                                   dimensions=[32, 64],
                                   domain=([-Lx, Lx], [-Ly, Ly]))
sim.param.boundaries[0] = 'shear periodic'
sim.param.boundaries[1] = 'periodic'

# Density profile: single maximum in middle of domain
sim.state.dens = 0.5*np.cos(np.pi*sim.coords.x/Lx) + 1.0
# Equilibrium vy to compensate for pressure gradient
sim.state.vely = -0.25*np.pi*np.sin(np.pi*sim.coords.x/Lx)/(sim.state.dens*Lx)
# Add some noise to seed instability
sim.state.dens += 0.01*np.random.random_sample(np.shape(sim.state.dens))

# Evolve until t = 100.0
sim.evolve(0.25*np.arange(400), new_file=True)
