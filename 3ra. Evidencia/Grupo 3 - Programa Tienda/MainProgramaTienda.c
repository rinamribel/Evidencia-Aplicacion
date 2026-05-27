#include <stdio.h>
#include "HeaderProgramaTienda.h"

int main(){
    int CantidadProductos, Opcion;
    char Productos[CantidadProductos][50];
    float Precio[CantidadProductos];

    CantidadProductos=CantidadDeProducto();
    if (CantidadProductos==0)
    {
        return 0;
    }
    NombreProductos(CantidadProductos, Productos);
    PrecioProductos(CantidadProductos, Precio);

    do {
        Opcion=Menu();
        switch (Opcion)
        {
        case 1:
            PrecioTotalInventario(CantidadProductos, Precio);
            break;
        case 2:
            ProductoMasCaroYMasBarato(CantidadProductos, Productos, Precio);
            break;
        case 3:
            PrecioPromedio(CantidadProductos, Precio);
            break;
        case 4:
            BuscarProducto(CantidadProductos, Productos, Precio);
            break;
        case 5:
            break;
        default:
            printf("Opcion invalida. Intentelo nuevamente.\n");
            getchar();
            getchar();
            break;
        }
    } while(Opcion!=5);

    return 0;
}
