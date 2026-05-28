# Simulacija transporta nevtronov

Projekt vsebuje poenostavljeno Monte Carlo simulacijo transporta nevtronov skozi materialno plast. Simulacija je narejena v Pythonu z `mpi4py`, dodatno pa je pripravljena še verzija z `numba`, da se lahko primerja navadna Python izvedba in JIT prevedena izvedba.

## Opis modela

Vsak nevtron začne v točki `(x, y) = (0, 0)`. Debelina materiala je določena v smeri `x`, smer `y` pa predstavlja stranski odmik nevtrona.

Pri vsakem koraku se naključno določi dolžina proste poti. Nevtron se premakne v trenutni smeri, nato se preveri:

- če je `x < 0`, je nevtron odbit,
- če je `x >= debelina`, je nevtron prepuščen,
- sicer se lahko absorbira,
- če se ne absorbira, se po sipanju izbere nov naključen kot gibanja v 2D.

Program meri tudi povprečen `|y|`, kar pokaže stranski odmik nevtronov pri koncu simulacije.

## Datoteke

- `main.py` - osnovna Python + MPI verzija
- `main_numba.py` - MPI verzija, kjer je glavna simulacijska zanka pospešena z `numba`
- `RESULTS.md` - surovi rezultati zagonov
- `simulacija-transporta-nevtronov-numba.pptx` - predstavitev rezultatov

## Namestitev

Na macOS je najprej potreben Open MPI:

```bash
brew install open-mpi
```

Python paketi:

```bash
pip install mpi4py numba numpy
```

## Zagon

Osnovna verzija:

```bash
mpirun -np 4 python3 main.py --neutrons 10000000
```

Numba verzija:

```bash
mpirun -np 4 python3 main_numba.py --neutrons 10000000
```

Število procesov se določi z `-np`, število nevtronov pa z argumentom `--neutrons`.

## Izračun pohitritve

Pohitritev:

```text
S(p) = T(1) / T(p)
```

Karp-Flatt metrika:

```text
e = ((1 / S(p)) - (1 / p)) / (1 - (1 / p))
```

## Povzetek rezultatov

Meritve so bile izvedene z `10000000` nevtroni.

| Procesi | Čas brez Numbe [s] | Čas Numba [s] | S brez Numbe | e brez Numbe | S Numba | e Numba |
|--------:|-------------------:|--------------:|-------------:|-------------:|--------:|--------:|
| 1       | 17.766             | 0.923         | 1.00         | 0.000        | 1.00    | 0.000   |
| 2       | 9.049              | 0.477         | 1.96         | 0.019        | 1.94    | 0.033   |
| 4       | 5.723              | 0.296         | 3.10         | 0.096        | 3.12    | 0.094   |
| 8       | 3.758              | 0.188         | 4.73         | 0.099        | 4.91    | 0.090   |

## Interpretacija

Z večanjem števila MPI procesov se čas izvajanja zmanjša pri obeh verzijah. Pohitritev ni popolnoma linearna, ker obstajajo režija zagona procesov, sinhronizacija in operacije `MPI_Reduce`.

Numba bistveno zmanjša absolutni čas izvajanja simulacije, ker je notranja zanka Monte Carlo simulacije prevedena. Pri tem pa MPI skaliranje ostane podobno: Numba pospeši računanje znotraj posameznega procesa, ne odstrani pa režije paralelnega izvajanja.
