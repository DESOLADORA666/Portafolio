from datetime import date

import pytest

from src.models import Transaccion


def test_transaccion_valida():
    transaccion = Transaccion(
        descripcion="Compra supermercado",
        monto=25.5,
        fecha=date(2024, 1, 10),
        categoria="Comidas",
        tipo="Gasto",
    )

    assert transaccion.descripcion == "Compra supermercado"
    assert transaccion.monto == 25.5
    assert transaccion.es_gasto is True
    assert transaccion.es_ingreso is False


def test_transaccion_rechaza_monto_cero_o_negativo():
    with pytest.raises(ValueError):
        Transaccion(
            descripcion="Pago",
            monto=0,
            fecha=date(2024, 1, 10),
            categoria="Otros",
            tipo="Gasto",
        )

    with pytest.raises(ValueError):
        Transaccion(
            descripcion="Pago",
            monto=-3,
            fecha=date(2024, 1, 10),
            categoria="Otros",
            tipo="Gasto",
        )


def test_transaccion_from_dict_con_fecha_iso():
    data = {
        "descripcion": "Salario",
        "monto": 1000,
        "fecha": "2024-02-01",
        "categoria": "Otros",
        "tipo": "Ingreso",
    }

    transaccion = Transaccion.from_dict(data)

    assert transaccion.fecha == date(2024, 2, 1)
    assert transaccion.tipo == "Ingreso"
