#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick  # type: ignore
from pybricks.ev3devices import Motor, InfraredSensor  # type: ignore
from pybricks.parameters import Port, Direction  # type: ignore
from time import sleep
import urandom as random

# ===== ENUM SIMPLES =====
class Enum():
    def _init_(self, cls_name, items):
        if type(items) == dict:
            names = items.keys()
            vals = items.values()
        else:
            names = items
            vals = range(len(items))
        self.name_str_list = names
        self.constant_map = dict(zip(names, vals))
        self.name_str_map = dict(zip(vals, names))
    def _getattr_(self, name):
        return self.constant_map[name]
    def _getitem_(self, item):
        return self.constant_map[item]
    def _call_(self, num):
        return self.name_str_map[num]
    def _iter_(self):
        yield from self.name_str_list
    def _contains_(self, val):
        return (val in self.constant_map or val in self.name_str_map)
    def _len_(self):
        return len(self.constant_map)

# ===== ESTADOS =====
estado = Enum("Estado", ["ANDA_RETO", "GIRA"])
ANDA_RETO = estado.ANDA_RETO
GIRA = estado.GIRA

# ===== HARDWARE =====
ev3 = EV3Brick()
motor_esq = Motor(Port.A, Direction.COUNTERCLOCKWISE)
motor_dir = Motor(Port.B, Direction.COUNTERCLOCKWISE)
infra = InfraredSensor(Port.S2)

# ===== CONSTANTES =====
VELOCIDADE_MAX = 100      # Potência máxima para ataque (%)
VELOCIDADE_GIRO = 50      # Velocidade base de giro
DISTANCIA_MAXIMA = 80     # (% de detecção do IR) 0-100
TEMPO_PERSEGUINDO = 0.3   # Segundos de ataque antes de reavaliar
GIRO = 1 # 1 -> direita e 0 -> esquerda

def randint(a, b):
    return a + urandom.getrandbits(8) % (b - a + 1)


# ===== FUNÇÕES DE MOVIMENTO =====
def moverRoboDc(vel_esq, vel_dir):
    motor_esq.dc(vel_esq)
    motor_dir.dc(vel_dir)

def pararRobo():
    motor_esq.stop()
    motor_dir.stop()

# ===== LÓGICA DE ESTADO =====
def prox_estado(estado_atual):
    global GIRO
    distancia = infra.distance()
    # ev3.screen.print(distancia)
    '''if distancia > 95:  
        pararRobo()
        moverRoboDc(-VELOCIDADE_GIRO, VELOCIDADE_GIRO)  
        sleep(0.3)
        return GIRA'''
    if distancia <= DISTANCIA_MAXIMA:  
        return ANDA_RETO
    else:
        if estado_atual == ANDA_RETO:
            GIRO = random.randint(0,1)
        return GIRA

# ===== PROGRAMA PRINCIPAL =====
def main():
    # Ré em caso de empate
    moverRoboDc(-VELOCIDADE_MAX, -VELOCIDADE_MAX)
    sleep(1.5)
    estado_atual = GIRA
    while True:
        estado_atual = prox_estado(estado_atual)

        if estado_atual == ANDA_RETO:
            moverRoboDc(VELOCIDADE_MAX, VELOCIDADE_MAX)
            sleep(TEMPO_PERSEGUINDO)  

        elif estado_atual == GIRA:
            if GIRO == 1:
                moverRoboDc(VELOCIDADE_GIRO, -VELOCIDADE_GIRO)
            elif GIRO == 0:
                moverRoboDc(-VELOCIDADE_GIRO, VELOCIDADE_GIRO)
                

        
        sleep(0.01)

main()