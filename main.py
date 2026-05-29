import argparse

import numpy as np
from mpi4py import MPI


# run simulation: mpirun -np X python3 main.py --neutrons Y
# example: mpirun -np 8 python3 main.py --neutrons 10000000

THICKNESS = 10.0
ABSORPTION_PROB = 0.15
SCATTER_MEAN = 1.0
MAX_STEPS = 10000
SEED = 42
BATCH_SIZE = 250000


def read_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--neutrons", type=int, default=1000000)
    return parser.parse_args()


def split_work(total_neutrons, rank, size):
    local_neutrons = total_neutrons // size

    if rank < total_neutrons % size:
        local_neutrons += 1

    return local_neutrons


def simulate_batch(batch_size, rng):
    x = np.zeros(batch_size)
    y = np.zeros(batch_size)
    angle = np.zeros(batch_size)
    steps = np.zeros(batch_size, dtype=np.int64)
    active = np.ones(batch_size, dtype=bool)

    absorbed = 0
    reflected = 0
    transmitted = 0
    total_abs_y = 0.0

    for _ in range(MAX_STEPS):
        active_indices = np.flatnonzero(active)
        active_count = active_indices.size

        if active_count == 0:
            break

        steps[active_indices] += 1

        free_path = rng.exponential(SCATTER_MEAN, active_count)
        active_angle = angle[active_indices]

        x[active_indices] += np.cos(active_angle) * free_path
        y[active_indices] += np.sin(active_angle) * free_path

        reflected_mask = x[active_indices] < 0.0
        transmitted_mask = x[active_indices] >= THICKNESS
        inside_mask = ~(reflected_mask | transmitted_mask)

        reflected_indices = active_indices[reflected_mask]
        transmitted_indices = active_indices[transmitted_mask]
        inside_indices = active_indices[inside_mask]

        if reflected_indices.size > 0:
            reflected += reflected_indices.size
            total_abs_y += np.abs(y[reflected_indices]).sum()
            active[reflected_indices] = False

        if transmitted_indices.size > 0:
            transmitted += transmitted_indices.size
            total_abs_y += np.abs(y[transmitted_indices]).sum()
            active[transmitted_indices] = False

        if inside_indices.size > 0:
            absorption_mask = rng.random(inside_indices.size) < ABSORPTION_PROB
            absorbed_indices = inside_indices[absorption_mask]
            scattered_indices = inside_indices[~absorption_mask]

            if absorbed_indices.size > 0:
                absorbed += absorbed_indices.size
                total_abs_y += np.abs(y[absorbed_indices]).sum()
                active[absorbed_indices] = False

            if scattered_indices.size > 0:
                angle[scattered_indices] = rng.random(scattered_indices.size) * 2.0 * np.pi

    # Safety fallback for rare particles that reached MAX_STEPS.
    active_indices = np.flatnonzero(active)
    if active_indices.size > 0:
        fallback_reflected = active_indices[x[active_indices] < THICKNESS / 2.0]
        fallback_transmitted = active_indices[x[active_indices] >= THICKNESS / 2.0]

        reflected += fallback_reflected.size
        transmitted += fallback_transmitted.size
        total_abs_y += np.abs(y[active_indices]).sum()

    total_steps = int(steps.sum())
    return absorbed, reflected, transmitted, total_steps, total_abs_y


def simulate_neutrons(local_neutrons, seed):
    rng = np.random.default_rng(seed)

    absorbed = 0
    reflected = 0
    transmitted = 0
    total_steps = 0
    total_abs_y = 0.0

    remaining = local_neutrons
    while remaining > 0:
        batch_size = min(BATCH_SIZE, remaining)
        batch_absorbed, batch_reflected, batch_transmitted, batch_steps, batch_abs_y = simulate_batch(
            batch_size,
            rng,
        )

        absorbed += batch_absorbed
        reflected += batch_reflected
        transmitted += batch_transmitted
        total_steps += batch_steps
        total_abs_y += batch_abs_y

        remaining -= batch_size

    return absorbed, reflected, transmitted, total_steps, total_abs_y


def percent(part, total):
    if total == 0:
        return 0
    return 100 * part / total


def main():
    args = read_arguments()

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    total_neutrons = args.neutrons
    local_neutrons = split_work(total_neutrons, rank, size)
    seed = SEED + rank * 1000

    comm.Barrier()
    start_time = MPI.Wtime()

    local_absorbed, local_reflected, local_transmitted, local_steps, local_abs_y = simulate_neutrons(
        local_neutrons,
        seed,
    )

    absorbed = comm.reduce(local_absorbed, op=MPI.SUM, root=0)
    reflected = comm.reduce(local_reflected, op=MPI.SUM, root=0)
    transmitted = comm.reduce(local_transmitted, op=MPI.SUM, root=0)
    total_steps = comm.reduce(local_steps, op=MPI.SUM, root=0)
    total_abs_y = comm.reduce(local_abs_y, op=MPI.SUM, root=0)

    comm.Barrier()
    end_time = MPI.Wtime()

    if rank == 0:
        runtime = end_time - start_time
        average_steps = total_steps / total_neutrons if total_neutrons > 0 else 0
        average_abs_y = total_abs_y / total_neutrons if total_neutrons > 0 else 0

        print("Simulacija transporta nevtronov - NumPy")
        print("--------------------------------------")
        print(f"MPI procesi: {size}")
        print(f"Nevtroni: {total_neutrons}")
        print(f"Absorbirani: {absorbed} ({percent(absorbed, total_neutrons):.2f} %)")
        print(f"Odbiti: {reflected} ({percent(reflected, total_neutrons):.2f} %)")
        print(f"Prepusceni: {transmitted} ({percent(transmitted, total_neutrons):.2f} %)")
        print(f"Povprecno korakov: {average_steps:.2f}")
        print(f"Povprecen |y|: {average_abs_y:.2f}")
        print(f"Cas izvajanja: {runtime:.6f} s")


if __name__ == "__main__":
    main()
