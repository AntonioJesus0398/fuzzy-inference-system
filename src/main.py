from robot_motion import FIS, Distance, Angle

class InputError(Exception):
    pass

while True:
    while True:
        distance = input("Introduzca la distancia a la que se encuentra el objeto. (Debe ser un número entre 0 y 100): ")
        try:
            distance = int(distance)
            if distance < 0 or distance > 100: raise InputError()
            break
        except:
            print("La distancia debe de ser un número entre 0 y 100")
            continue

    while True:
        angle = input("Introduzca el ángulo que forma el objeto con el robot. (Debe ser un número entre 0 y 180): ")
        try:
            angle = int(angle)
            if angle < 0 or angle > 180: raise InputError()
            break
        except:
            print("El ángulo debe ser un número entre 0 y 180")
            continue

    result = FIS.solve([('distance', Distance.build_singleton(distance)), ('angle', Angle.build_singleton(angle))], defuzzification_method="mom")
    print(f"El ángulo de la dirección que debe tomar el robot es: {result['direction']}")

    while True:
        choice = input("Desea continuar(s/n)?: ")
        if choice == 's':
            print('\n')
            break
        if choice == 'n':
            exit(0)
