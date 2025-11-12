from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from uuid import uuid4, UUID

class EstadoCuenta(str, Enum):
    ACTIVA = "ACTIVA"
    BLOQUEADA = "BLOQUEADA"
    CERRADA = "CERRADA"

class TipoMovimiento(str, Enum):
    CONSIGNACION = "CONSIGNACION"
    RETIRO = "RETIRO"
    TRANSFERENCIA_ENTRADA = "TRANSFERENCIA_ENTRADA"
    TRANSFERENCIA_SALIDA = "TRANSFERENCIA_SALIDA"

class Movimiento(BaseModel):
    id: UUID = uuid4()
    fecha: datetime = datetime.now()
    tipo: TipoMovimiento
    monto: float
    descripcion: str

class Cuenta(BaseModel):
    numero: str
    titular: str
    saldo: float
    estado: EstadoCuenta = EstadoCuenta.ACTIVA
