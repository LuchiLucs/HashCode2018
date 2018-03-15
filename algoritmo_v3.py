import os
import sys
import bisect


class Ride():

    def __init__(self, i, xs, ys, xf, yf, early, late):
        self.id = i
        self.xs = xs
        self.ys = ys
        self.xf = xf
        self.yf = yf
        self.early = early
        self.late = late
        self.dist = abs(xs - xf) + abs(yf - ys)
        self.wait = 0
        self.intime = 1


class Car():

    def __init__(self, id):
        self.id = id

        # Posizione car
        self.x = 0
        self.y = 0

        # Tempo quando car diventa disponibile
        self.free = 0

        # Lista jobs assegnati alla car in ordine di esecuzione
        self.jobs = []

        self.toEnd = -1     # distanza alla destinazione
        self.toBegin = -1   # distanza dal passeggero
        self.busy = 0       # 1 assegnato 2 in corsa
        self.viaggioId = None


# Print output
def genOutput(name):
    f2 = open(name, 'w')
    for car in cars:
        f2.write(str(len(car.jobs)))
        for job in car.jobs:
            f2.write(' ' + str(job))
        f2.write('\n')
    f2.close()


# Input files
# input = ['d_Metropolis.in']
input = ['a_example.in', 'b_should_be_easy.in',
         'c_no_hurry.in', 'd_Metropolis.in', 'e_high_bonus.in']

for inp in input:
    # INIZIALIZZA

    print('\nEseguo file: ' + inp)

    # Leggo dati problema
    f1 = open(inp)
    spec = f1.readline().split(' ')
    r = int(spec[0])    # #ROWS
    c = int(spec[1])    # #COLUMNS
    f = int(spec[2])    # #VEHICLES
    n = int(spec[3])    # #RIDES
    b = int(spec[4])    # BONUS VALUE
    t = int(spec[5])    # #SIMULATION STEPS

    # Leggo jobs e creo jobs
    jobs = []
    for i in range(n):
        riga = f1.readline().split(' ')
        jobs.append(Ride(i, int(riga[0]), int(riga[1]), int(
            riga[2]), int(riga[3]), int(riga[4]), int(riga[5])))
    f1.close()

    # Creo cars
    cars = []
    for i in range(f):
        cars.append(Car(i))

    # Inizializzo timings
    next_time = 0
    next_times = []
    time = 0

    # START ALGORITHM
    while(time <= t or not jobs):
        # print('\nTempo corrente: ' + str(time))

        # Tempo rimanente da aspettare rispetto al time di simulazione
        for job in jobs:
            # job.wait = job.early - time
            job.wait = job.early - time if job.early - time >= 0 else 0
            job.intime = 1 if job.early - time >= 0 else -1

        # Rimuovo i jobs impossibili da completare (Considero quelli fattibili)
        # jobs = filter(lambda job: job.late <= time, jobs) da sistemare
        jobs = [job for job in jobs if job.late >= time and job.late >= job.wait + job.dist]

        # Considero i jobs possibili da fare:
        # current_jobs = filter(lambda job: job.late >= job.dist + job.early, jobs)

        # Considero le macchine libere
        # filter(lambda car: car.free == time, cars)
        free_cars = [car for car in cars if car.free == time]

        # Considero le macchine libere al tempo corrente e i lavori disponibili ordinati secondo il mio criterio
        # Assegno ad ogni macchina libera il primo lavoro disponibile e valido possibile
        # print('Macchine disponibili: ' + str(len(free_cars)))
        # print('Lavori ancora da assegnare: ' + str(len(jobs)))
        for car in free_cars:
            # SORT BY DISTANCE/SCORING (LONGEST PROCESSING TIME)
            jobs.sort(key=lambda job: (job.dist - job.wait + job.intime * b -
                                       abs(car.x - job.xs) - abs(car.y - job.ys)), reverse=True)

            for job in jobs:
                # Tempo speso per far arrivare la macchina al job
                distance_job_car = abs(car.x - job.xs) + abs(car.y - job.ys)
                # Tempo rimanente da aspettare rispetto al time di simulazione
                # job.wait = job.early - time

                # Tempo totale da considerare per il job
                total = distance_job_car + job.dist + job.wait

                # Controllo se posso assegnare il job alla macchina
                if total <= job.late - time:
                    # print("job id: " + str(job.id) + " car free: " + str(car.free) + " job total: " + str(total))
                    # Assegno il job alla macchina
                    car.jobs.append(job.id)
                    # Aggiorno car posizione considerando dove sarà quando tornerà disponibile
                    car.x = job.xf
                    car.y = job.yf
                    # Aggiorno quando la macchina sarà disponibile
                    car.free += total
                    # Tolgo il job dalla lista dei jobs
                    jobs.remove(job)

                    # Aggiungo il prossimo tempo di analisi
                    bisect.insort(next_times, car.free)
                    # next_times2.append(car.free)

                    # Mi fermo
                    break

        # Aggiorno il prossimo tempo di analisi
        if next_times:
            next_time = next_times[0]
        else:
            break
        # Elimino tutte le occorrenze di next_time
        next_times = [t for t in next_times if t != next_time]
        # print("Prossimo tempo di analisi: " + str(next_time))

        # Simulo prossimo step...
        time = next_time

    # Genero output
    genOutput(inp + 'Luca' + '.out')
