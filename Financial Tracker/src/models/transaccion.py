from datetime import date
from dataclasses import dataclass, field
from typing import Dict, Any
from src.utils.validadores import sanitizar_texto

@dataclass
class Transaccion:
    """
    Representa una transacción individual con validación de datos.
    """
    descripcion: str
    monto: float
    fecha: date
    categoria: str
    tipo: str  # "Ingreso" o "Gasto"
    
    def __post_init__(self):
        """Validaciones automáticas al instanciar."""
        # Validar descripción
        self.descripcion = sanitizar_texto(self.descripcion)
        if not self.descripcion:
            raise ValueError("La descripción no puede estar vacía")
        
        # Validar monto
        if self.monto < 0:
            raise ValueError(f"El monto no puede ser negativo: {self.monto}")
        if self.monto == 0:
            raise ValueError("El monto debe ser mayor a cero")
        
        # Validar tipo
        if self.tipo not in ["Ingreso", "Gasto"]:
            raise ValueError(f"Tipo debe ser 'Ingreso' o 'Gasto', recibido: {self.tipo}")
        
        # Validar fecha
        if not isinstance(self.fecha, date):
            raise ValueError(f"Fecha debe ser tipo date, recibido: {type(self.fecha)}")
    
    @property
    def es_gasto(self) -> bool:
        """Indica si la transacción es un gasto."""
        return self.tipo == "Gasto"
    
    @property
    def es_ingreso(self) -> bool:
        """Indica si la transacción es un ingreso."""
        return self.tipo == "Ingreso"
    
    @property
    def monto_formateado(self) -> str:
        """Retorna el monto formateado como moneda."""
        from src.utils.validadores import formatear_moneda
        return formatear_moneda(self.monto)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte la transacción a diccionario para serialización."""
        return {
            "descripcion": self.descripcion,
            "monto": self.monto,
            "fecha": self.fecha.isoformat(),
            "categoria": self.categoria,
            "tipo": self.tipo
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Transaccion':
        """
        Crea una transacción desde un diccionario.
        Útil para cargar desde CSV o JSON.
        """
        # Manejar diferentes formatos de fecha
        fecha = data["fecha"]
        if isinstance(fecha, str):
            fecha = date.fromisoformat(fecha)
        elif isinstance(fecha, date):
            fecha = fecha
        else:
            raise ValueError(f"Formato de fecha no soportado: {type(fecha)}")
        
        return cls(
            descripcion=str(data["descripcion"]),
            monto=float(data["monto"]),
            fecha=fecha,
            categoria=str(data["categoria"]),
            tipo=str(data["tipo"])
        )
    
    def __repr__(self) -> str:
        return f"Transaccion({self.descripcion[:20]}... ${self.monto:.2f})"