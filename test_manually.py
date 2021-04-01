import os
import tempfile
import sys
sys.path.insert(0, "/media/alice/Elements/aimsprop/aimsprop_2/")
import numpy as np

import aimsprop as ai


trajs = [ai.parse_fms90("/media/alice/Elements/aimsprop_2/aimsprop/tests/test_data/%04d" % x) 
    for x in [2, 3]
]
# 2. Merge the trajectories into one super-big Trajectory with uniform weights
trajectory = ai.Trajectory.merge(trajs, ws=[1.0 / len(trajs)] * len(trajs), labels=[2, 3])

# 3. Interpolate trajectory with ~1 fs intervals, removing adaptive timesteps from AIMS
ts = np.arange(0.0, max(trajectory.ts), 40.0)
trajectory = trajectory.interpolate_nearest(ts)

# ----------------------------------------------------------------------------------------- #

ai.compute_bond(trajectory, "R01", 0, 1)

#bond_R01 = ai.extract_property(trajectory, "R01", False, False)
#print(bond_R01)

R = [[0, 1, 0,],[1, 0 , 1],[0, 1, 1]]

ai.rotate_frames(trajectory, R)
print(trajectory.frames[0].xyz[0][0])

z = [0.2, 0.1, 0.1]

ai.rotate_frames_to_z(trajectory, z)
print(trajectory.frames[0].xyz[0][0])
#print(trajectory)


#pop = ai.compute_population(trajectory)

#print(pop[1][24])

#R = np.linspace(0.0, 6.0, 200)
#trajectory = ai.compute_ued_simple(trajectory, "UED", R=R, alpha=8.0)
#print(trajectory.frames[0].properties["UED"][0]) #8.95739037e-07

#ICs = np.arange(2,3,1)

#trajectory, trajs = ai.build_traj(ICs)


#resampled_trajs = ai.bootstrap(trajs, 10, ICs)

#avg, std = ai.extract_stats(resampled_trajs, "UED", diff=True)
#print(avg)
#print(std)


#blur_property O
#compute_time_blur []
#bootstrap []
#extract_stats []
#compute_pes
#rotate_frames
  #This also might require info about where to orient the geom relative to a separate vector not in traj obj
#rotate_frames_to_z
  #This might require data about transition dipole in Z direction as a vector not in traj obj/loaded separately
#compute_sine_transform



