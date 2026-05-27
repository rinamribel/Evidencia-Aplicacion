#include <stdio.h>
#include <string.h>
#include "HeaderProgramaTienda.h"

int CantidadDeProducto(){
    int CantidadProductos;
    do {
        printf("Ingrese la cantidad de productos que desea agregar: ");
        scanf("%d", &CantidadProductos);
        getchar();
        if (CantidadProductos>10)
        {
            printf("El numero maximo de productos que el sistema maneja es de 10. Intentelo nuevamente.\n");
        }
        if (CantidadProductos==0)
        {
            printf("No se ingresaron productos. Saliendo del programa.\n");
            getchar();
        }
        if (CantidadProductos<0)
        {
            printf("La cantidad de productos no puede ser negativo. Intentelo nuevamente.\n");
        }
        
    } while(CantidadProductos>10 || CantidadProductos<0);
    
    return CantidadProductos;
}

void NombreProductos(int CantidadProductos, char Productos[CantidadProductos][50]){
    for (int i = 0; i < CantidadProductos; i++)
    {
        printf("Ingrese el nombre del producto %d: ", i+1);
        fflush(stdin);
        fgets(Productos[i], 50, stdin);
        Productos[i][strcspn(Productos[i], "\n")] = '\0';
    }
}

void PrecioProductos(int CantidadProductos, float Precio[CantidadProductos]){
    for (int i = 0; i < CantidadProductos; i++)
    {
        do {
            printf("Ingrese el precio del producto %d: ", i+1);
            scanf("%f", &Precio[i]);
            getchar();
            if (Precio[i]<0)
            {
                printf("El precio del producto no puede ser negativo. Intentelo nuevamente.\n");
            }
        } while(Precio[i]<0);
    }
}

int Menu(){
    int Opcion;
    printf("--------Menu--------\n");
    printf("1. Precio total del inventario\n");
    printf("2. Mostrar el producto mas caro y el mas barato\n");
    printf("3. Precio promedio de todos los productos\n");
    printf("4. Buscar un producto y mostrar su precio\n");
    printf("5. Salir\n");
    printf("Seleccione una opcion: ");
    scanf("%d", &Opcion);
    return Opcion;
}

void PrecioTotalInventario(int CantidadProductos, float Precio[CantidadProductos]){
    float PrecioTotal=0;
    for (int i = 0; i < CantidadProductos; i++)
    {
        PrecioTotal+=Precio[i];
    }
    printf("El precio total del inventario es: $%.2f\n", PrecioTotal);
    getchar();
    getchar();
}

void ProductoMasCaroYMasBarato(int CantidadProductos, char Productos[CantidadProductos][50], float Precio[CantidadProductos]){
    int NombreProductoMasCaro=0, NombreProductoMasBarato=0;
    float PrecioMasAlto=Precio[0], PrecioMasBajo=Precio[0];
    for (int i = 1; i < CantidadProductos; i++)
    {
        if (Precio[i]>PrecioMasAlto)
        {
            PrecioMasAlto=Precio[i];
            NombreProductoMasCaro=i;
        }
        if (Precio[i]<PrecioMasBajo)
        {
            PrecioMasBajo=Precio[i];
            NombreProductoMasBarato=i;
        }
        
    }
    printf("El producto mas caro es %s con un precio de: $%.2f\n", Productos[NombreProductoMasCaro], PrecioMasAlto);
    printf("El producto mas barato es %s con un precio de: $%.2f\n", Productos[NombreProductoMasBarato], PrecioMasBajo);
    getchar();
    getchar();
}

void PrecioPromedio(int CantidadProductos, float Precio[CantidadProductos]){
    float PrecioTotal=0, Promedio;
    for (int i = 0; i < CantidadProductos; i++)
    {
        PrecioTotal+=Precio[i];
    }
    Promedio=PrecioTotal/CantidadProductos;
    printf("El precio promedio de todos los productos es de: $%.2f\n", Promedio);
    getchar();
    getchar();
}

void BuscarProducto(int CantidadProductos, char Productos[CantidadProductos][50], float Precio[CantidadProductos]){
    char ProductoPorBuscar[50];
    int Encontrado=0;
    printf("Ingrese el nombre del producto que desea buscar: ");
    fflush(stdin);
    fgets(ProductoPorBuscar, 50, stdin);
    ProductoPorBuscar[strcspn(ProductoPorBuscar, "\n")] = '\0';

    for (int i = 0; i < CantidadProductos; i++)
    {
        if (strcmp(Productos[i], ProductoPorBuscar)==0)
        {
            printf("El precio del producto %s es: $%.2f\n", Productos[i], Precio[i]);
            Encontrado=1;
            getchar();
        }
        
    }
    if (Encontrado==0)
    {
        printf("El producto no fue encontrado.\n");
        getchar();
    }
}