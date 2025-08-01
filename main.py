#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick # type: ignore
from pybricks.ev3devices import Motor, UltrasonicSensor  # type: ignore
from pybricks.parameters import Port, Stop, Direction  # type: ignore
from time import sleep

class Enum():
    """
    A simple (and fallible) substitute for the enum.Enum class
    """
    def __init__(self, cls_name, items):
        if type(items) == dict:
            names = items.keys()
            vals  = items.values()
        else:
            names = items
            vals  = range(len(items))
        
        self.name_str_list = names
        self.constant_map = dict(zip(names, vals))
        self.name_str_map = dict(zip(vals, names))


    def __getattr__(self, name):
        return self.constant_map[name]
    
    def __getitem__(self, item):
        return self.constant_map[item]
    def __call__(self, num):
        return self.name_str_map[num]
    
    def __iter__(self):
        yield from self.name_str_list

    def __contains__(self, val):
        return (val in self.constant_map or
                val in self.name_str_map)

    def __len__(self):
        return len(self.constant_map)

#Estados
estado = Enum("Estado", ["PARA","ANDA_RETO", "GIRA_ESQ", "GIRA_DIR"])

PARA = estado.PARA
ANDA_RETO = estado.ANDA_RETO
GIRA_ESQ = estado.GIRA_ESQ
GIRA_DIR = estado.GIRA_DIR



ev3 = EV3Brick()

motor_esq = Motor(Port.A, Direction.COUNTERCLOCKWISE)
motor_dir = Motor(Port.B, Direction.COUNTERCLOCKWISE)
ultra_esq = UltrasonicSensor(Port.S1)
ultra_dir = UltrasonicSensor(Port.S2)


# Constantes
VELOCIDADE_MAX  = 1000
VELOCIDADE_GIRO = 200
DISTANCIA_MAXIMA  = 650 # Distância máxima para detectar um objeto (em mm)


def main():
    ev3.speaker.beep()
    estado = PARA
    while True:
        estado = prox_estado(estado)
        if (estado == ANDA_RETO):
            moverRobo(VELOCIDADE_MAX, VELOCIDADE_MAX)
        elif (estado == GIRA_ESQ):
            moverRobo(VELOCIDADE_GIRO, -VELOCIDADE_GIRO)
        elif (estado == GIRA_DIR):
            moverRobo(-VELOCIDADE_GIRO, VELOCIDADE_GIRO)
        else:
            pararRobo()
        sleep(0.05)

def prox_estado(estado_atual):
    dist_esq = media_distancia(ultra_esq)
    dist_dir = media_distancia(ultra_dir)

    if (dist_esq < DISTANCIA_MAXIMA and dist_dir < DISTANCIA_MAXIMA):
        return ANDA_RETO
    elif (dist_esq < DISTANCIA_MAXIMA):
        print("ESQ")
        return GIRA_ESQ
    elif (dist_dir < DISTANCIA_MAXIMA):
        print("DIR")
        return GIRA_DIR
    else:
        print("Procurando")
        return GIRA_DIR


def moverRobo(vel_esq, vel_dir):
    motor_esq.run(vel_esq)
    motor_dir.run(vel_dir)

def pararRobo():
    motor_esq.stop()
    motor_dir.stop()

#funcao que volta media das distancias
def media_distancia(sensor, n=3):
    leituras = [sensor.distance() for _ in range(n)]
    return sum(leituras) / n


main()