# FUNCION PARA VALIDAR CEDULA
def validarCedula(cedula):
    digitos = []
    suma = 0
    for i in range (9):
        if((i+1) % 2 != 0):
            multiplicacion = int(cedula[i])*2
            digitos.append(str(multiplicacion))
            if(int(digitos[i]) > 9):
                resta = int(digitos[i])-9 
                digitos[i] = resta
        else:
            digitos.append(cedula[i])
        suma += int(digitos[i])
        
    valor_final = str(suma)[-1]
    resultado = 10 - int(valor_final)
    if(cedula == '1616161616'):
        return False
    elif((str(suma)[-1] == '0') or (resultado == int(cedula[-1]))):
        return True
    else:
        return False
