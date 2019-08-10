cadena= 'I want 2 bread'
number = [int(s) for s in cadena.split() if s.isdigit()]
if len(number) > 0:
    cadena = cadena.rstrip('s')
    indice = cadena.index(str(number[0])) + len(str(number[0])) + 1
    print(cadena[indice::])
    print(number)
else: 
    print(cadena.split()[-1])
Tot=0
cant = 21
imp = 2
Tot += cant * imp 
Tot += cant * imp 
print(Tot)