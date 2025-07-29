#include <stdio.h>
#include "medicamento.h"

int main() {
    Medicamento medicamentos[100];
    int cantidad = 0;
    int opcion;

    cargarMedicamentos(medicamentos, &cantidad);

    do {
        printf("\n--- SISTEMA DE MEDICAMENTOS ---\n");
        printf("1. Ver medicamentos\n");
        printf("2. Registrar nuevo medicamento\n");
        printf("3. Marcar medicamento como tomado\n");
        printf("4. Salir\n");
        printf("Seleccione una opcion: ");
        scanf("%d", &opcion);

        switch (opcion) {
            case 1:
                mostrarMedicamentos(medicamentos, cantidad);
                break;
            case 2:
                agregarMedicamento(medicamentos, &cantidad);
                break;
            case 3:
                marcarComoTomado(medicamentos, cantidad);
                break;
            case 4:
                printf("Hasta pronto.\n");
                break;
            default:
                printf("Opcion invalida.\n");
        }
    } while (opcion != 4);

    return 0;
}
