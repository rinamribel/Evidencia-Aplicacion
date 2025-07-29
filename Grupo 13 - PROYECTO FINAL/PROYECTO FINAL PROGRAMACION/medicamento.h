#ifndef MEDICAMENTO_H
#define MEDICAMENTO_H

typedef struct {
    char nombre[50];
    char dosis[30];
    int frecuencia_horas;
    int hora;
    int minutos;
    char am_pm[3];
} Medicamento;

void cargarMedicamentos(Medicamento meds[], int *n);
void guardarMedicamentos(Medicamento meds[], int n);
void agregarMedicamento(Medicamento meds[], int *n);
void mostrarMedicamentos(Medicamento meds[], int n);
void marcarComoTomado(Medicamento meds[], int n);

#endif
