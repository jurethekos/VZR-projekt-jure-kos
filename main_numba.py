import argparse
import math

import numpy as np
from mpi4py import MPI
from numba import njit


# run simulation: mpirun -np X python3 main_numba.py --neutrons Y
# example: mpirun -np 8 python3 main_numba.py --neutrons 1000000

THICKNESS = 10.0
ABSORPTION_PROB = 0.15
SCATTER_MEAN = 1.0
MAX_STEPS = 10000
SEED = 42


def read_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--neutrons", type=int, default=1000000)
    return parser.parse_args()


def split_work(total_neutrons, rank, size):
    local_neutrons = total_neutrons // size

    if rank < total_neutrons % size:
        local_neutrons += 1

    return local_neutrons


@njit
def simulate_neutrons_numba(local_neutrons, seed):
    np.random.seed(seed)

    absorbed = 0
    reflected = 0
    transmitted = 0
    total_steps = 0
    total_abs_y = 0.0

    for _ in range(local_neutrons):
        x = 0.0
        y = 0.0
        angle = 0.0

        result = 2
        steps = MAX_STEPS

        for step in range(MAX_STEPS):
            free_path = np.random.exponential(SCATTER_MEAN)
            x += math.cos(angle) * free_path
            y += math.sin(angle) * free_path

            if x < 0.0:
                result = 1
                steps = step + 1
                break

            if x >= THICKNESS:
                result = 2
                steps = step + 1
                break

            if np.random.random() < ABSORPTION_PROB:
                result = 0
                steps = step + 1
                break

            angle = np.random.random() * 2.0 * math.pi

        if steps == MAX_STEPS:
            if x < THICKNESS / 2.0:
                result = 1
            else:
                result = 2

        total_steps += steps
        total_abs_y += abs(y)

        if result == 0:
            absorbed += 1
        elif result == 1:
            reflected += 1
        else:
            transmitted += 1

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

    # Warm-up call compiles the Numba function before timing starts.
    simulate_neutrons_numba(1, seed)

    comm.Barrier()
    start_time = MPI.Wtime()

    local_absorbed, local_reflected, local_transmitted, local_steps, local_abs_y = simulate_neutrons_numba(
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

        print("Simulacija transporta nevtronov - Numba")
        print("---------------------------------------")
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
