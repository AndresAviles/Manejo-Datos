import re

are_rotations = lambda s_1, s_2: sorted(s_1) == sorted(s_2) and s_2 in s_1 + s_1 

def validar_cadena(cadena, nombre):
    if " " in cadena:
        print(f" Error:  '{nombre}' no debe contener espacios vacios")
        return False
    if not cadena.isalpha():
        print(f" Error:  '{nombre}' solo debe contener caracteres alfabeticos")
        return False
    
    if len(cadena) <1:
        print(f" Error:  '{nombre}' no puede estar vacio")
        return False
    return True

def main():
    print("="* 50)
    print(" Rotacion / Trsaslacion de cadenas")
    
    #Validamos la primer cadena
    while True:
        print("Ingresa la primer cadena:")
        s1 = input("S1").strip()
        if validar_cadena(s1, "S1"):
            break
    #VAlidmoas la segunda cadena
    while True:
        print("Ingresa la segunda cadena:")
        s2 = input("S2").strip()
        if validar_cadena(s2, "S2"):
            break
        
    #verificar resultados
    resultado = are_rotations(s1, s2)
    print("-" * 50)
    print("\n" + "=" * 50 )
    print (f"S1 = '{s1}'")
    print (f"S2 = '{s2}'")
    print("-" * 50)
    if resultado:
        print(f" Resultado: True")
        print(f" '{s2}' es una rotacion / traslacion de '{s1}'")
    else:
        print(f" Resultado: False")
        print(f" Resultado: False")
        print(f" '{s2}' no es una rotacion / traslacion de '{s1}'")
        print("=" * 50)
        
if __name__ == "__main__":
    main()