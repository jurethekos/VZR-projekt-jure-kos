import argparse
import random

from mpi4py import MPI


# run simulation: mpirun -np X python3 main.py --neutrons Y
# example: mpirun -np 8 python3 main.py --neutrons 1000000

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

    # First few processes get one extra neutron if division is not exact.
    if rank < total_neutrons % size:
        local_neutrons += 1

    return local_neutrons


def simulate_one_neutron(rng):
    x = 0.0
    direction = 1

    for step in range(MAX_STEPS):
        free_path = rng.expovariate(1.0 / SCATTER_MEAN)
        x += direction * free_path

        if x < 0:
            return "reflected", step + 1

        if x >= THICKNESS:
            return "transmitted", step + 1

        if rng.random() < ABSORPTION_PROB:
            return "absorbed", step + 1

        # After scattering, the neutron randomly goes left or right.
        if rng.random() < 0.5:
            direction = 1
        else:
            direction = -1

    # Safety fallback, so a neutron cannot run forever.
    if x < THICKNESS / 2:
        return "reflected", MAX_STEPS
    return "transmitted", MAX_STEPS


def simulate_neutrons(local_neutrons, seed):
    rng = random.Random(seed)

    absorbed = 0
    reflected = 0
    transmitted = 0
    total_steps = 0

    for _ in range(local_neutrons):
        result, steps = simulate_one_neutron(rng)
        total_steps += steps

        if result == "absorbed":
            absorbed += 1
        elif result == "reflected":
            reflected += 1
        else:
            transmitted += 1

    return absorbed, reflected, transmitted, total_steps


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

    # Different seed for each process, but still deterministic.
    seed = SEED + rank * 1000

    comm.Barrier()
    start_time = MPI.Wtime()

    local_absorbed, local_reflected, local_transmitted, local_steps = simulate_neutrons(
        local_neutrons,
        seed,
    )

    absorbed = comm.reduce(local_absorbed, op=MPI.SUM, root=0)
    reflected = comm.reduce(local_reflected, op=MPI.SUM, root=0)
    transmitted = comm.reduce(local_transmitted, op=MPI.SUM, root=0)
    total_steps = comm.reduce(local_steps, op=MPI.SUM, root=0)

    comm.Barrier()
    end_time = MPI.Wtime()

    if rank == 0:
        runtime = end_time - start_time
        average_steps = total_steps / total_neutrons if total_neutrons > 0 else 0

        print("Simulacija transporta nevtronov")
        print("-------------------------------")
        print(f"MPI procesi: {size}")
        print(f"Nevtroni: {total_neutrons}")
        print(f"Absorbirani: {absorbed} ({percent(absorbed, total_neutrons):.2f} %)")
        print(f"Odbiti: {reflected} ({percent(reflected, total_neutrons):.2f} %)")
        print(f"Prepusceni: {transmitted} ({percent(transmitted, total_neutrons):.2f} %)")
        print(f"Povprecno korakov: {average_steps:.2f}")
        print(f"Cas izvajanja: {runtime:.6f} s")


if __name__ == "__main__":
    main()
