import time
import threading
from planificador import Planificador
from memoria import Memoria

pausado = False

def menu_administrativo(planificador, memoria):
    global pausado
    pausado = True
    while True:
        print("\n=========== MENÚ ADMINISTRATIVO ===========")
        planificador.mostrar_estado(memoria)
        print("Opciones:")
        print("1. Finalizar proceso por PID")
        print("2. Suspender proceso por PID")
        print("3. Reanudar simulación")
        print("===========================================\n")

        opcion = input("Selecciona opción: ")
        if opcion == '1':
            try:
                pid = int(input("PID a finalizar: "))
                planificador.finalizar_proceso(pid, memoria)
            except ValueError:
                print("PID inválido.")
        elif opcion == '2':
            try:
                pid = int(input("PID a suspender: "))
                planificador.suspender_proceso(pid)
            except ValueError:
                print("PID inválido.")
        elif opcion == '3':
            print("Reanudando simulación...\n")
            pausado = False
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

def escuchar_teclado():
    global pausado
    while True:
        entrada = input()
        if entrada.lower() in ['m', 'menu', 'admin']:
            pausado = True

if __name__ == "__main__":
    planificador = Planificador(quantum=3)
    memoria = Memoria(marcos=20)

    for _ in range(5):
        planificador.crear_proceso()

    # Hilo para escuchar la entrada del usuario
    hilo_entrada = threading.Thread(target=escuchar_teclado, daemon=True)
    hilo_entrada.start()

    try:
        while True:
            if not pausado:
                planificador.siguiente_evento(memoria)
                planificador.mostrar_estado(memoria)
                time.sleep(1)
            else:
                menu_administrativo(planificador, memoria)

    except KeyboardInterrupt:
        print("\nSimulación finalizada por el usuario.")

