with open('static(0,3).txt', 'r') as file:
        texto = file.readlines()

u_med = 0
v_med = 0
x_med = 0
y_med = 0

for i in range(100):
    line = texto[0].split('\t')
    u = line[0].replace(',', '')
    v = line[1].replace(',', '')
    x = line[2].replace(',', '')
    y = line[3].replace(';\n', '')

    u_med = (u_med + float(u))
    v_med = (v_med + float(v))
    x_med = (x_med + float(x))
    y_med = (y_med + float(y))

u_med = (u_med / 100.0)
v_med = (v_med / 100.0)
x_med = (x_med / 100.0)
y_med = (y_med / 100.0)

print('\n=> x = ' + str(x_med))
print('\n=> y = ' + str(y_med))
print('\n=> v = ' + str(v_med))
print('\n=> u = ' + str(u_med))