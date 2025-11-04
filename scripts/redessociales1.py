import pandas as pd
import matplotlib.pyplot as plt

# Leer archivo CSV
df = pd.read_csv('datos/datos_10_25.csv', sep=';')

# Filtrar columnas necesarias
df = df[['Año', 'USUARIOS X MIL MILLONES']]

# Calcular diferencia anual
df['DIFERENCIA ANUAL'] = df['USUARIOS X MIL MILLONES'].diff()

# Eliminar la primera fila con valor NaN en diferencia
df = df.dropna()

# Descripción estadística
desc = df.describe()

# Mostrar DataFrame y descripción
print(df)
print(desc)

# Datos para el gráfico
x = df['Año']
y = df['USUARIOS X MIL MILLONES']

# Crear gráfico
plt.plot(x, y, marker='o', linestyle='-', color='blue')  # línea azul con puntos
plt.xlabel("Año")
plt.ylabel("Usuarios (x mil millones)")
plt.title("Crecimiento del uso de redes sociales (2010–2025)")
plt.grid(True)

# Guardar en carpeta /scripts (misma del script actual)
plt.savefig('grafico_usuarios_totales.png', dpi=300, bbox_inches='tight')

# Mostrar gráfico
plt.show()
