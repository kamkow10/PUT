Don't panic!

kompilacja programów w MPI ($ oznacza znak prompta; nie wpisuj tego znaku)
    
    $ mpicc program.c -o program.exe

Uruchamiania programów w MPI, pięć procesów
    
    $ mpirun -np 5 ./program.exe

Najczęstsze błędy:

1) MPI pyszczy o to, że nie ma "default-hostfile"

    $ mpirun -default-hostfile none -np 5 ./program.exe

2) MPI pyszczy, że brak bibliotek współdzielonych

    w pliku ~/.bashrc dopisz w dowolnym miejscu linijkę

    export LD_LIBRARY_PATH=/usr/lib64/mpi/gcc/openmpi/lib64
