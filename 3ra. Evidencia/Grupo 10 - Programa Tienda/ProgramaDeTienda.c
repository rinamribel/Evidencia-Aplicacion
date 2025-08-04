#include <stdio.h>
#include <string.h>
#include "inventario.h"

int main() {
    char nombres[10][50];
    float precios[10];
    int numProductos;
    int resultadosExtremos[2];
    
    printf("ingrese el numero de productos (maximo %d): ", 10);
    while (scanf("%d", &numProductos) != 1 || numProductos<=0 || numProductos >10) {
        printf("Ingrese un numero valido (1-10): ");
        while(getchar() != '\n');
    }
    
    ingresarProductos(nombres, precios, numProductos);
    
    printf("\nprecio total del inventario: %.2f\n", calcularPrecioTotal(precios,numProductos));
    
    encontrarExtremos(precios, numProductos, resultadosExtremos);
    printf("producto mas caro: %s (%.2f)\n", nombres[resultadosExtremos[0]],precios[resultadosExtremos[0]]);
    printf("producto mas barato: %s (%.2f)\n", nombres[resultadosExtremos[1]], precios[resultadosExtremos[1]]);
    
    printf("precio promedio: %.2f\n", calcularPromedio(precios,numProductos));
    
    char nombreBuscado[50];
    printf("\ningrese el nombre de un producto a buscar: ");
    scanf("%49s", nombreBuscado);
    
    int indice = buscarProducto(nombres, numProductos, nombreBuscado);
    if (indice != -1) {
        printf("precio de %s: %.2f\n", nombreBuscado, precios[indice]);
    } else {
        printf("producto no encontrado\n");
    }
    
    return 0;
}
