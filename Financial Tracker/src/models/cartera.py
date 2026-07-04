import pandas as pd
from typing import List, Optional, Dict, Iterator
from datetime import date
from .transaccion import Transaccion
from config.settings import Config

class Cartera:
    """
    Representa un conjunto de transacciones con operaciones agregadas.
    Optimizado con pandas para mejor rendimiento.
    """
    
    def __init__(self, transacciones: Optional[List[Transaccion]] = None):
        self.transacciones = transacciones or []
        self._df_cache = None  # Cache para evitar recalcular DataFrame
    
    def agregar(self, transaccion: Transaccion) -> None:
        """
        Agrega una transacción a la cartera.
        Limpia el cache para forzar recálculo.
        """
        self.transacciones.append(transaccion)
        self._df_cache = None
    
    def _to_dataframe(self) -> pd.DataFrame:
        """
        Convierte las transacciones a DataFrame con cache.
        Esta es la base para todas las operaciones agregadas.
        """
        if self._df_cache is None:
            if not self.transacciones:
                self._df_cache = pd.DataFrame()
            else:
                data = [t.to_dict() for t in self.transacciones]
                df = pd.DataFrame(data)
                df['fecha'] = pd.to_datetime(df['fecha'])
                self._df_cache = df
        return self._df_cache
    
    def filtrar(self, 
                categorias: Optional[List[str]] = None,
                fecha_desde: Optional[date] = None,
                fecha_hasta: Optional[date] = None) -> 'Cartera':
        """
        Filtra las transacciones por categorías y rango de fechas.
        Usa pandas para un filtrado eficiente.
        """
        df = self._to_dataframe()
        if df.empty:
            return Cartera()
        
        # Aplicar filtros
        if categorias:
            df = df[df['categoria'].isin(categorias)]
        
        if fecha_desde:
            df = df[df['fecha'] >= pd.Timestamp(fecha_desde)]
        
        if fecha_hasta:
            df = df[df['fecha'] <= pd.Timestamp(fecha_hasta)]
        
        # Convertir de vuelta a objetos Transaccion
        transacciones = []
        for _, row in df.iterrows():
            transaccion = Transaccion.from_dict(row.to_dict())
            transacciones.append(transaccion)
        
        return Cartera(transacciones)
    
    # ========== MÉTRICAS FINANCIERAS ==========
    
    def ingresos(self) -> float:
        """Total de ingresos."""
        df = self._to_dataframe()
        if df.empty:
            return 0.0
        return df[df['tipo'] == 'Ingreso']['monto'].sum()
    
    def gastos(self) -> float:
        """Total de gastos."""
        df = self._to_dataframe()
        if df.empty:
            return 0.0
        return df[df['tipo'] == 'Gasto']['monto'].sum()
    
    def balance(self) -> float:
        """Balance neto (ingresos - gastos)."""
        return self.ingresos() - self.gastos()
    
    def gasto_promedio(self) -> float:
        """Promedio de gastos por transacción."""
        df = self._to_dataframe()
        if df.empty:
            return 0.0
        
        gastos = df[df['tipo'] == 'Gasto']
        if gastos.empty:
            return 0.0
        
        return gastos['monto'].mean()
    
    def gastos_por_categoria(self) -> Dict[str, float]:
        """
        Agrupa gastos por categoría.
        Retorna diccionario con todas las categorías (incluyendo las que no tienen gastos).
        """
        df = self._to_dataframe()
        if df.empty:
            return {cat: 0.0 for cat in Config.CATEGORIAS}
        
        gastos = df[df['tipo'] == 'Gasto']
        if gastos.empty:
            return {cat: 0.0 for cat in Config.CATEGORIAS}
        
        # Agrupar y sumar
        resultado = gastos.groupby('categoria')['monto'].sum().to_dict()
        
        # Asegurar que todas las categorías estén presentes
        for cat in Config.CATEGORIAS:
            resultado.setdefault(cat, 0.0)
        
        return resultado
    
    def gastos_por_fecha(self) -> Dict[date, float]:
        """
        Agrupa gastos por fecha.
        Retorna diccionario {fecha: monto_total}.
        """
        df = self._to_dataframe()
        if df.empty:
            return {}
        
        gastos = df[df['tipo'] == 'Gasto']
        if gastos.empty:
            return {}
        
        # Agrupar por fecha
        resultado = gastos.groupby('fecha')['monto'].sum().to_dict()
        
        # Convertir keys a date
        return {k.date(): v for k, v in resultado.items()}
    
    def gastos_por_mes(self) -> Dict[str, float]:
        """
        Agrupa gastos por mes (formato: 'YYYY-MM').
        Útil para análisis temporal.
        """
        df = self._to_dataframe()
        if df.empty:
            return {}
        
        gastos = df[df['tipo'] == 'Gasto']
        if gastos.empty:
            return {}
        
        # Crear columna de mes
        gastos['mes'] = gastos['fecha'].dt.strftime('%Y-%m')
        resultado = gastos.groupby('mes')['monto'].sum().to_dict()
        
        return dict(sorted(resultado.items()))
    
    def transacciones_recientes(self, n: int = 10) -> List[Transaccion]:
        """
        Retorna las n transacciones más recientes.
        """
        if not self.transacciones:
            return []
        
        ordenadas = sorted(self.transacciones, key=lambda t: t.fecha, reverse=True)
        return ordenadas[:n]
    
    # ========== MÉTODOS DE CONVERSIÓN ==========
    
    def to_dataframe(self) -> pd.DataFrame:
        """Retorna una copia del DataFrame para la interfaz."""
        df = self._to_dataframe()
        return df.copy() if not df.empty else df
    
    def to_dict_list(self) -> List[Dict]:
        """Convierte todas las transacciones a lista de diccionarios."""
        return [t.to_dict() for t in self.transacciones]
    
    # ========== MÉTODOS MÁGICOS ==========
    
    def __len__(self) -> int:
        return len(self.transacciones)
    
    def __iter__(self) -> Iterator[Transaccion]:
        return iter(self.transacciones)
    
    def __repr__(self) -> str:
        return f"Cartera({len(self)} transacciones)"
    
    def __bool__(self) -> bool:
        return len(self) > 0