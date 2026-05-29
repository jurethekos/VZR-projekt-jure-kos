mpirun -np 1 python3 main.py --neutrons 10000000
mpirun -np 1 python3 main_numba.py --neutrons 10000000

mpirun -np 2 python3 main.py --neutrons 10000000
mpirun -np 2 python3 main_numba.py --neutrons 10000000

mpirun -np 4 python3 main.py --neutrons 10000000
mpirun -np 4 python3 main_numba.py --neutrons 10000000

mpirun -np 8 python3 main.py --neutrons 10000000
mpirun -np 8 python3 main_numba.py --neutrons 10000000
Simulacija transporta nevtronov - NumPy
--------------------------------------
MPI procesi: 1
Nevtroni: 10000000
Absorbirani: 6197508 (61.98 %)
Odbiti: 3750407 (37.50 %)
Prepusceni: 52085 (0.52 %)
Povprecno korakov: 4.51
Povprecen |y|: 1.17
Cas izvajanja: 1.567197 s
Simulacija transporta nevtronov - NumPy + Numba
-----------------------------------------------
MPI procesi: 1
Nevtroni: 10000000
Absorbirani: 6195800 (61.96 %)
Odbiti: 3752479 (37.52 %)
Prepusceni: 51721 (0.52 %)
Povprecno korakov: 4.51
Povprecen |y|: 1.17
Cas izvajanja: 1.736051 s
Simulacija transporta nevtronov - NumPy
--------------------------------------
MPI procesi: 2
Nevtroni: 10000000
Absorbirani: 6197523 (61.98 %)
Odbiti: 3750620 (37.51 %)
Prepusceni: 51857 (0.52 %)
Povprecno korakov: 4.51
Povprecen |y|: 1.17
Cas izvajanja: 0.849760 s
Simulacija transporta nevtronov - NumPy + Numba
-----------------------------------------------
MPI procesi: 2
Nevtroni: 10000000
Absorbirani: 6197021 (61.97 %)
Odbiti: 3751373 (37.51 %)
Prepusceni: 51606 (0.52 %)
Povprecno korakov: 4.51
Povprecen |y|: 1.17
Cas izvajanja: 0.920387 s
Simulacija transporta nevtronov - NumPy
--------------------------------------
MPI procesi: 4
Nevtroni: 10000000
Absorbirani: 6197594 (61.98 %)
Odbiti: 3750604 (37.51 %)
Prepusceni: 51802 (0.52 %)
Povprecno korakov: 4.51
Povprecen |y|: 1.17
Cas izvajanja: 0.497668 s
Simulacija transporta nevtronov - NumPy + Numba
-----------------------------------------------
MPI procesi: 4
Nevtroni: 10000000
Absorbirani: 6197275 (61.97 %)
Odbiti: 3750918 (37.51 %)
Prepusceni: 51807 (0.52 %)
Povprecno korakov: 4.51
Povprecen |y|: 1.17
Cas izvajanja: 0.522207 s
Simulacija transporta nevtronov - NumPy
--------------------------------------
MPI procesi: 8
Nevtroni: 10000000
Absorbirani: 6196211 (61.96 %)
Odbiti: 3751609 (37.52 %)
Prepusceni: 52180 (0.52 %)
Povprecno korakov: 4.51
Povprecen |y|: 1.17
Cas izvajanja: 0.364219 s
Simulacija transporta nevtronov - NumPy + Numba
-----------------------------------------------
MPI procesi: 8
Nevtroni: 10000000
Absorbirani: 6196148 (61.96 %)
Odbiti: 3752114 (37.52 %)
Prepusceni: 51738 (0.52 %)
Povprecno korakov: 4.51
Povprecen |y|: 1.17
Cas izvajanja: 0.367284 s