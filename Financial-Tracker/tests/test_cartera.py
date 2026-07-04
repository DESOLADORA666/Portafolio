from datetime import date

from src.models import Cartera, Transaccion


def test_cartera_agrega_y_calcula_balance():
    cartera = Cartera()
    cartera.agregar(
        Transaccion(
            descripcion="Salario",
            monto=1000,
            fecha=date(2024, 1, 1),
            categoria="Otros",
            tipo="Ingreso",
        )
    )
    cartera.agregar(
        Transaccion(
            descripcion="Comida",
            monto=50,
            fecha=date(2024, 1, 2),
            categoria="Comidas",
            tipo="Gasto",
        )
    )

    assert len(cartera) == 2
    assert cartera.ingresos() == 1000
    assert cartera.gastos() == 50
    assert cartera.balance() == 950


def test_cartera_filtra_por_categoria_y_fecha():
    cartera = Cartera()
    cartera.agregar(
        Transaccion(
            descripcion="Comida",
            monto=20,
            fecha=date(2024, 1, 5),
            categoria="Comidas",
            tipo="Gasto",
        )
    )
    cartera.agregar(
        Transaccion(
            descripcion="Transporte",
            monto=15,
            fecha=date(2024, 2, 5),
            categoria="Transporte",
            tipo="Gasto",
        )
    )

    filtrada = cartera.filtrar(
        categorias=["Comidas"],
        fecha_desde=date(2024, 1, 1),
        fecha_hasta=date(2024, 1, 31),
    )

    assert len(filtrada) == 1
    assert filtrada.transacciones[0].categoria == "Comidas"
