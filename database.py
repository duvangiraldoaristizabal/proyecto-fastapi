from typing import Dict, List
from domain import Cuenta, Movimiento

cuentas_db: Dict[str, Cuenta] = {}
movimientos_db: Dict[str, List[Movimiento]] = {}

def crear_cuenta(cuenta: Cuenta):
    if cuenta.numero in cuentas_db:
        raise ValueError("La cuenta ya existe.")
    cuentas_db[cuenta.numero] = cuenta
    movimientos_db[cuenta.numero] = []

def obtener_cuenta(numero: str) -> Cuenta:
    cuenta = cuentas_db.get(numero)
    if not cuenta:
        raise ValueError("Cuenta no encontrada.")
    return cuenta

def registrar_movimiento(numero: str, movimiento: Movimiento):
    movimientos_db[numero].append(movimiento)
