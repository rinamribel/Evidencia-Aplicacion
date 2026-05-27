#include "inventario.h"
#include <string.h>
#include <stdio.h>

void ingresarProductos(char nombres[][50], float precios[],int numProductos) {
    for (int i=0; i<numProductos; i++) {
        printf("\nProducto %d:\n", i + 1);
        printf("Nombre: ");
        scanf("%49s", nombres[i]);
        printf("Precio: ");
        while (scanf("%f", &precios[i]) != 1) {
            printf("Ingrese un numero valido: ");
            while(getchar() != '\n');
        }
    }
}

float calcularPrecioTotal(float precios[], int numProductos) {
    float total=0;
    for (int i=0; i < numProductos;i++) {
        total += precios[i];
    }
    return total;
}

void encontrarExtremos(float precios[], int numProductos, int resultados[]) {
    resultados[0] = resultados[1] = 0;
    
    for (int i=1; i < numProductos;i++) {
        if (precios[i] > precios[resultados[0]]) {
            resultados[0]=i;
        }
        if (precios[i] < precios[resultados[1]]) {
            resultados[1]=i;
        }
    }
}

float calcularPromedio(float precios[], int numProductos) {
    if (numProductos == 0) return 0;
    float suma=0;
    for (int i=0; i<numProductos; i++) {
        suma += precios[i];
    }
    return suma / numProductos;
}

int buscarProducto(char nombres[][50], int numProductos, char nombreBuscado[]) {
    for (int i=0; i < numProductos; i++) {
        if (strcmp(nombres[i], nombreBuscado) == 0) {
            return i;
        }
    }
    return -1;
}