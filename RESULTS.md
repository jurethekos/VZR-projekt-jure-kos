mpirun -np 1 python3 main.py --neutrons 10000000
mpirun -np 1 python3 main_numba.py --neutrons 10000000

mpirun -np 2 python3 main.py --neutrons 10000000
mpirun -np 2 python3 main_numba.py --neutrons 10000000

mpirun -np 4 python3 main.py --neutrons 10000000
mpirun -np 4 python3 main_numba.py --neutrons 10000000

mpirun -np 8 python3 main.py --neutrons 10000000
mpirun -np 8 python3 main_numba.py --neutrons 10000000


Simulacija transporta nevtronov
-------------------------------
MPI procesi: 1
Nevtroni: 10000000
Absorbirani: 6198135 (61.98 %)
Odbiti: 3750495 (37.50 %)
Prepusceni: 51370 (0.51 %)
Povprecno korakov: 4.51
Povprecen |y|: 1.17
Cas izvajanja: 17.765934 s

Simulacija transporta nevtronov - Numba
---------------------------------------
MPI procesi: 1
Nevtroni: 10000000
Absorbirani: 6196340 (61.96 %)
Odbiti: 3752213 (37.52 %)
Prepusceni: 51447 (0.51 %)
Povprecno korakov: 4.51
Povprecen |y|: 1.17
Cas izvajanja: 0.922659 s

Simulacija transporta nevtronov
-------------------------------
MPI procesi: 2
Nevtroni: 10000000
Absorbirani: 6197110 (61.97 %)
Odbiti: 3751301 (37.51 %)
Prepusceni: 51589 (0.52 %)
Povprecno korakov: 4.51
Povprecen |y|: 1.17
Cas izvajanja: 9.048578 s

Simulacija transporta nevtronov - Numba
---------------------------------------
MPI procesi: 2
Nevtroni: 10000000
Absorbirani: 6199323 (61.99 %)
Odbiti: 3749127 (37.49 %)
Prepusceni: 51550 (0.52 %)
Povprecno korakov: 4.51
Povprecen |y|: 1.17
Cas izvajanja: 0.476522 s

Simulacija transporta nevtronov
-------------------------------
MPI procesi: 4
Nevtroni: 10000000
Absorbirani: 6198547 (61.99 %)
Odbiti: 3749734 (37.50 %)
Prepusceni: 51719 (0.52 %)
Povprecno korakov: 4.51
Povprecen |y|: 1.17
Cas izvajanja: 5.722684 s

Simulacija transporta nevtronov - Numba
---------------------------------------
MPI procesi: 4
Nevtroni: 10000000
Absorbirani: 6196532 (61.97 %)
Odbiti: 3751526 (37.52 %)
Prepusceni: 51942 (0.52 %)
Povprecno korakov: 4.51
Povprecen |y|: 1.17
Cas izvajanja: 0.295930 s

Simulacija transporta nevtronov
-------------------------------
MPI procesi: 8
Nevtroni: 10000000
Absorbirani: 6198435 (61.98 %)
Odbiti: 3749827 (37.50 %)
Prepusceni: 51738 (0.52 %)
Povprecno korakov: 4.51
Povprecen |y|: 1.17
Cas izvajanja: 3.757964 s

Simulacija transporta nevtronov - Numba
---------------------------------------
MPI procesi: 8
Nevtroni: 10000000
Absorbirani: 6196180 (61.96 %)
Odbiti: 3751379 (37.51 %)
Prepusceni: 52441 (0.52 %)
Povprecno korakov: 4.51
Povprecen |y|: 1.17
Cas izvajanja: 0.188110 s