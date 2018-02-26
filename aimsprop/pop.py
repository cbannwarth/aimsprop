import numpy as np

def compute_population(
    traj,
    ):

    """ Compute the state populations for a trajectory

    Pararms:
        traj (Trajectory) - the Trajectory object to compute the property for 
    Returns:
        populations (dict of np.ndarray) - dictionary from I to time
        population of I. The indices of each vector in populations
        corresponds to the set of traj.ts
    """

    ts = traj.ts
    populations = {}
    for I in traj.Is:
        traj2 = traj.subset_by_I(I)
        populations[I] = np.zeros((len(ts),))
        for tind, t in enumerate(ts):
            traj3 = traj2.subset_by_t(t)
            populations[I][tind] += sum([frame.w for frame in traj3.frames])
    return populations
