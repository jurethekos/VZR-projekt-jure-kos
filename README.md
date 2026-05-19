## Rezultati meritev

Meritve so bile izvedene za 1, 2, 4 in 8 MPI procesov. Za vsako konfiguracijo so bili izvedeni 3 zagoni, izračunano pa je povprečje časa izvajanja.

Povprečni časi izvajanja:

- 1 proces: 1.121 s
- 2 procesa: 0.586 s
- 4 procesi: 0.307 s
- 8 procesov: 0.207 s

Izračun pospeška:

S(p) = T(1) / T(p)

Izračun Karp-Flatt metrike:

e = ((1 / S(p)) - (1 / p)) / (1 - (1 / p))

Izračunani rezultati:

- 1 proces:
  - speedup = 1.00
  - Karp-Flatt e = 0.000

- 2 procesa:
  - speedup = 1.91
  - Karp-Flatt e = 0.048

- 4 procesi:
  - speedup = 3.65
  - Karp-Flatt e = 0.032

- 8 procesov:
  - speedup = 5.41
  - Karp-Flatt e = 0.068


### Interpretacija rezultatov

Rezultati kažejo, da se čas izvajanja zmanjšuje s povečevanjem števila MPI procesov. Pospešek je relativno blizu idealnemu linearnemu pospešku, vendar zaradi MPI overheada ni popolnoma linearen.

Pri večjem številu procesov se pojavi dodaten overhead zaradi ustvarjanja procesov, sinhronizacije in izvajanja operacije MPI_Reduce. Zaradi tega se učinkovitost programa z večanjem števila procesov nekoliko zmanjša.

Na rezultate vpliva tudi operacijski sistem, saj procesi tekmujejo za procesorski čas in druge sistemske vire. Prisotna so tudi manjša odstopanja zaradi naključne narave Monte Carlo simulacije.

Karp-Flattova metrika ostaja relativno nizka, kar pomeni, da je sekvenčni del programa majhen in da je problem primeren za paralelizacijo.

V tem problemu ni večjih težav z neenakomerno porazdelitvijo dela, saj vsak proces obdeluje približno enako število nevtronov. Zaradi tega je komunikacijskega overheada malo in program dobro skalira tudi pri večjem številu procesov.