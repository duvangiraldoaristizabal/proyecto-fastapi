from domain import Movimiento, TipoMovimiento
from database import obtener_cuenta, registrar_movimiento

def depositar(numero: str, monto: float):
    cuenta = obtener_cuenta(numero)
    if monto <= 0:
        raise ValueError("El monto debe ser mayor a 0.")
    cuenta.saldo += monto
    registrar_movimiento(numero, Movimiento(
        tipo=TipoMovimiento.CONSIGNACION,
        monto=monto,
        descripcion=f"Depósito de {monto}"
    ))
    return cuenta.saldo

def retirar(numero: str, monto: float):
    cuenta = obtener_cuenta(numero)
    if monto <= 0:
        raise ValueError("El monto debe ser mayor a 0.")
    if monto > cuenta.saldo:
        raise ValueError("Fondos insuficientes.")
    cuenta.saldo -= monto
    registrar_movimiento(numero, Movimiento(
        tipo=TipoMovimiento.RETIRO,
        monto=monto,
        descripcion=f"Retiro de {monto}"
    ))
    return cuenta.saldo

def transferir(origen: str, destino: str, monto: float):
    origen_cuenta = obtener_cuenta(origen)
    destino_cuenta = obtener_cuenta(destino)
    if monto <= 0:
        raise ValueError("Monto inválido.")
    if origen_cuenta.saldo < monto:
        raise ValueError("Fondos insuficientes.")
    origen_cuenta.saldo -= monto
    destino_cuenta.saldo += monto

    registrar_movimiento(origen, Movimiento(
        tipo=TipoMovimiento.TRANSFERENCIA_SALIDA,
        monto=monto,
        descripcion=f"Transferencia enviada a {destino}"
    ))
    registrar_movimiento(destino, Movimiento(
        tipo=TipoMovimiento.TRANSFERENCIA_ENTRADA,
        monto=monto,
        descripcion=f"Transferencia recibida de {origen}"
    ))

    return {
        "saldo_origen": origen_cuenta.saldo,
        "saldo_destino": destino_cuenta.saldo
    }
