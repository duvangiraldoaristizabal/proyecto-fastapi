from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from enum import Enum
from typing import Dict, List

# ─────────────────────────────
# INICIALIZAR LA APP
# ─────────────────────────────

app = FastAPI(title="Cajero Automático Virtual", version="1.0")


# ─────────────────────────────
# MODELOS
# ─────────────────────────────

class EstadoCuenta(str, Enum):
    ACTIVA = "ACTIVA"
    BLOQUEADA = "BLOQUEADA"
    CERRADA = "CERRADA"


class TipoMovimiento(str, Enum):
    CONSIGNACION = "CONSIGNACION"
    RETIRO = "RETIRO"
    TRANSFERENCIA_SALIDA = "TRANSFERENCIA_SALIDA"
    TRANSFERENCIA_ENTRADA = "TRANSFERENCIA_ENTRADA"


class Movimiento(BaseModel):
    tipo: TipoMovimiento
    monto: float
    descripcion: str


class Cuenta(BaseModel):
    numero: str
    titular: str
    saldo: float
    estado: EstadoCuenta = EstadoCuenta.ACTIVA


# ─────────────────────────────
# BASES DE DATOS EN MEMORIA
# ─────────────────────────────

cuentas_db: Dict[str, Cuenta] = {}
movimientos_db: Dict[str, List[Movimiento]] = {}


# ─────────────────────────────
# ENDPOINTS
# ─────────────────────────────

@app.get("/")
def home():
    return {"mensaje": "💳 Bienvenido al Cajero Automático Virtual"}


# Crear cuenta
@app.post("/cuentas")
def crear_cuenta(cuenta: Cuenta):
    if cuenta.numero in cuentas_db:
        raise HTTPException(status_code=400, detail="La cuenta ya existe")

    cuentas_db[cuenta.numero] = cuenta
    movimientos_db[cuenta.numero] = []

    return {"mensaje": "Cuenta creada exitosamente", "cuenta": cuenta}


# Consultar saldo
@app.get("/cuentas/{numero}")
def consultar_cuenta(numero: str):
    if numero not in cuentas_db:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")

    return cuentas_db[numero]


# Depositar
@app.post("/depositar/{numero}")
def depositar(numero: str, monto: float):
    if numero not in cuentas_db:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")

    if monto <= 0:
        raise HTTPException(status_code=400, detail="Monto inválido")

    cuenta = cuentas_db[numero]
    cuenta.saldo += monto

    movimientos_db[numero].append(
        Movimiento(
            tipo=TipoMovimiento.CONSIGNACION,
            monto=monto,
            descripcion=f"Depósito de {monto}"
        )
    )

    return {"mensaje": "Depósito realizado", "saldo_actual": cuenta.saldo}


# Retirar
@app.post("/retirar/{numero}")
def retirar(numero: str, monto: float):
    if numero not in cuentas_db:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")

    cuenta = cuentas_db[numero]

    if monto <= 0:
        raise HTTPException(status_code=400, detail="Monto inválido")

    if monto > cuenta.saldo:
        raise HTTPException(status_code=400, detail="Fondos insuficientes")

    cuenta.saldo -= monto

    movimientos_db[numero].append(
        Movimiento(
            tipo=TipoMovimiento.RETIRO,
            monto=monto,
            descripcion=f"Retiro de {monto}"
        )
    )

    return {"mensaje": "Retiro realizado", "saldo_actual": cuenta.saldo}


# Transferencia
@app.post("/transferir")
def transferir(origen: str, destino: str, monto: float):
    if origen not in cuentas_db or destino not in cuentas_db:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")

    if monto <= 0:
        raise HTTPException(status_code=400, detail="Monto inválido")

    cuenta_origen = cuentas_db[origen]
    cuenta_destino = cuentas_db[destino]

    if monto > cuenta_origen.saldo:
        raise HTTPException(status_code=400, detail="Fondos insuficientes")

    cuenta_origen.saldo -= monto
    cuenta_destino.saldo += monto

    movimientos_db[origen].append(
        Movimiento(
            tipo=TipoMovimiento.TRANSFERENCIA_SALIDA,
            monto=monto,
            descripcion=f"Transferencia enviada a {destino}"
        )
    )

    movimientos_db[destino].append(
        Movimiento(
            tipo=TipoMovimiento.TRANSFERENCIA_ENTRADA,
            monto=monto,
            descripcion=f"Transferencia recibida de {origen}"
        )
    )

    return {
        "mensaje": "Transferencia realizada",
        "saldo_origen": cuenta_origen.saldo,
        "saldo_destino": cuenta_destino.saldo
    }


# Movimientos
@app.get("/movimientos/{numero}")
def listar_movimientos(numero: str):
    if numero not in cuentas_db:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")

    return movimientos_db[numero]


# ─────────────────────────────
# EJECUCIÓN (REQUIRED BY AZURE)
# ─────────────────────────────

if __name__ == "__main__":
    import uvicorn, os
    puerto = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=puerto)
