from datetime import date
from typing import Union
import re

def validar_fecha(fecha_str: str) -> bool:
    """
    Valida que una fecha esté en formato ISO (YYYY-MM-DD).
    """
    patron = r'^\d{4}-\d{2}-\d{2}$'
    if not re.match(patron, fecha_str):
        return False
    
    try:
        date.fromisoformat(fecha_str)
        return True
    except ValueError:
        return False

def validar_monto(monto: Union[int, float, str]) -> bool:
    """
    Valida que un monto sea un número positivo.
    """
    try:
        monto_float = float(monto)
        return monto_float >= 0
    except (ValueError, TypeError):
        return False

def validar_categoria(categoria: str, categorias_validas: list) -> bool:
    """
    Valida que una categoría esté en la lista de categorías válidas.
    """
    return categoria in categorias_validas

def formatear_moneda(monto: float) -> str:
    """
    Formatea un monto como moneda con separador de miles.
    """
    return f"${monto:,.2f}".replace(",", ".")

def sanitizar_texto(texto: str) -> str:
    """
    Limpia un texto eliminando espacios extras y caracteres especiales.
    """
    if not texto:
        return ""
    return " ".join(texto.strip().split())