#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include "medicamento.h"

int stricmp(const char *a, const char *b) {
    while (*a && *b) {
        if (tolower(*a) != tolower(*b)) return 0;
        a++;
        b++;
    }
    return *a == *b;
}

void cargarMedicamentos(Medicamento meds[], int *n) {
    FILE *f = fopen("medicamentos.txt", "r");
    if (f == NULL) return;

    while (fscanf(f, "%49[^;];%29[^;];%d;%d;%d;%2s\n",
                  meds[*n].nombre,
                  meds[*n].dosis,
                  &meds[*n].frecuencia_horas,
                  &meds[*n].hora,
                  &meds[*n].minutos,
                  meds[*n].am_pm) == 6) {
        (*n)++;
    }
    fclose(f);
}

void guardarMedicamentos(Medicamento meds[], int n) {
    FILE *f = fopen("medicamentos.txt", "w");
    for (int i = 0; i < n; i++) {
        fprintf(f, "%s;%s;%d;%d;%d;%s\n",
                meds[i].nombre,
                meds[i].dosis,
                meds[i].frecuencia_horas,
                meds[i].hora,
                meds[i].minutos,
                meds[i].am_pm);
    }
    fclose(f);
}

void agregarMedicamento(Medicamento meds[], int *n) {
    printf("Nombre del medicamento: ");
    getchar();
    fgets(meds[*n].nombre, 50, stdin);
    meds[*n].nombre[strcspn(meds[*n].nombre, "\n")] = 0;

    printf("Dosis (ej: 1 tableta): ");
    fgets(meds[*n].dosis, 30, stdin);
    meds[*n].dosis[strcspn(meds[*n].dosis, "\n")] = 0;

    printf("Frecuencia (en horas): ");
    scanf("%d", &meds[*n].frecuencia_horas);

    printf("Hora de la proxima toma (ej: 8): ");
    scanf("%d", &meds[*n].hora);

    printf("Minutos (ej: 30): ");
    scanf("%d", &meds[*n].minutos);

    printf("AM o PM: ");
    scanf("%s", meds[*n].am_pm);

    (*n)++;
    guardarMedicamentos(meds, *n);
    printf("Medicamento registrado correctamente.\n");
}

void mostrarMedicamentos(Medicamento meds[], int n) {
    printf("\n--- Lista de Medicamentos ---\n");
    for (int i = 0; i < n; i++) {
        printf("%d. %s - %s - cada %d h - Proxima: %02d:%02d %s\n",
               i + 1,
               meds[i].nombre,
               meds[i].dosis,
               meds[i].frecuencia_horas,
               meds[i].hora,
               meds[i].minutos,
               meds[i].am_pm);
    }
}

void marcarComoTomado(Medicamento meds[], int n) {
    char nombre[50];
    getchar();

    printf("Escriba el nombre del medicamento tomado: ");
    fgets(nombre, 50, stdin);
    nombre[strcspn(nombre, "\n")] = 0;

    for (int i = 0; i < n; i++) {
        if (stricmp(nombre, meds[i].nombre)) {
            int totalHoras = meds[i].hora;
            if ((strcmp(meds[i].am_pm, "PM") == 0 || strcmp(meds[i].am_pm, "pm") == 0) && totalHoras != 12)
                totalHoras += 12;
            if ((strcmp(meds[i].am_pm, "AM") == 0 || strcmp(meds[i].am_pm, "am") == 0) && totalHoras == 12)
                totalHoras = 0;

            totalHoras += meds[i].frecuencia_horas;
            totalHoras %= 24;

            if (totalHoras >= 12) strcpy(meds[i].am_pm, "PM");
            else strcpy(meds[i].am_pm, "AM");

            if (totalHoras == 0) meds[i].hora = 12;
            else if (totalHoras > 12) meds[i].hora = totalHoras - 12;
            else meds[i].hora = totalHoras;

            guardarMedicamentos(meds, n);
            printf("Proxima toma actualizada correctamente.\n");
            return;
        }
    }

    printf("Medicamento no encontrado.\n");
}
