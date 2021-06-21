import pybullet as p
import pybullet_data

import os
import time
import numpy as np

class Rack:
    def __init__(self, radius):
        self.r = radius

        theta = np.pi/6
        self.u = 2*self.r * np.array([np.cos(-theta), np.sin(-theta)])
        self.v = 2*self.r * np.array([np.cos( theta), np.sin( theta)])

    def __call__(self, i):
        a, b = self.get_ab(i)
        pos = a * self.u + b * self.v
        return pos[0], pos[1], self.r

    def get_ab(self, i):
        if i == 0:
            return 0, 0
        elif i <= 2:
            return 2-i, i-1
        elif i <= 5:
            return 5-i, i-3
        elif i <= 9:
            return 9-i, i-6
        else:
            return 14-i, i-10

def main():
    p.connect(p.GUI)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())

    # First, let's make sure we start with a fresh new simulation.
    # Otherwise, we can keep adding objects by running this cell over again.
    p.resetSimulation()

    g = 9.807
    dt = 0.001

    H = 2.90            # the length of the long rail [m] (along the x-axis)
    W = 1.60            # the length of the short rail [m] (along the y-axis)
    h = 0.5             # the height of the table [m] (along the z-axis)

    r = 0.028575        # the radius of balls [m]
    num_targets = 15    # the nuber of target balls
    Vmax = 12           # the maximum value of the que's exit velocity [m/sec]
    T = 3               # the interval between shots [sec]

    p.setTimeStep(dt)
    p.setGravity(0, 0, -g)

    assets_path = os.path.join(os.path.dirname(__file__), 'assets')

    # Load our simulation floor plane at the origin (0, 0, 0).
    plane_path = os.path.join(assets_path, 'plane.urdf')
    #plane_path = 'plane.urdf'
    p.loadURDF(plane_path)

    # Set a table
    table_path = os.path.join(assets_path, 'table.urdf')
    table = p.loadURDF(table_path, [0, 0, h/2], useFixedBase=True)

    long_rail = os.path.join(assets_path, 'rail_long.urdf')
    short_rail = os.path.join(assets_path, 'rail_short.urdf')

    head = p.loadURDF(short_rail, [-H/2, 0, h], useFixedBase=True)
    tail = p.loadURDF(short_rail, [H/2, 0, h], useFixedBase=True)
    right_head = p.loadURDF(long_rail, [H/4, W/2, h], useFixedBase=True)
    right_tail = p.loadURDF(long_rail, [-H/4, W/2, h], useFixedBase=True)
    left_head = p.loadURDF(long_rail, [H/4, -W/2, h], useFixedBase=True)
    left_tail = p.loadURDF(long_rail, [-H/4, -W/2, h], useFixedBase=True)

    objects = [table, head, tail, right_head, right_tail, left_head, left_tail]

    # Place balls at the initial positions
    balls = []

    ## the cue ball
    cue_path = os.path.join(assets_path, 'cue.urdf') 
    cue = p.loadURDF(cue_path, [-1, 0, r+h])
    balls.append(cue)

    ## the object balls
    rack = Rack(r)
    for i in range(num_targets):
        x, y, z = rack(i)
        ball_name = 'ball' + str(i+1) + '.urdf'
        ball_path = os.path.join(assets_path, ball_name)
        ball = p.loadURDF(ball_path, [x+0.8, y, z+h])
        balls.append(ball)

    # We can check the number of bodies we have in the simulation.
    p.getNumBodies()

    time.sleep(3)

    # the break shot
    p.resetBaseVelocity(cue, [Vmax, 0, 0])

    for i in range(int(1e7)):
        # Make a shot every T seconds
        if (i != 0) and (i * dt % T == 0):
            # reset the cue's position after scratch
            (_, _, z), _ = p.getBasePositionAndOrientation(cue)
            if z < h - 2*r:
                x = np.random.uniform(-1, 1) * (H/2-0.1)
                y = np.random.uniform(-1, 1) * (W/2-0.1)
                p.resetBasePositionAndOrientation(cue, [x, y, r+h], [1,0,0,0])

            # reset the cue's velocity
            V = np.random.uniform(-1, 1) * Vmax
            phi = np.random.uniform(-1, 1) * np.pi/2
            vx, vy = V * np.array([np.cos(phi), np.sin(phi)])
            p.resetBaseVelocity(cue, [vx, vy, 0])

        # Step simulation
        p.stepSimulation()

        time.sleep(dt)

    p.disconnect()

if __name__=="__main__":
    main()
