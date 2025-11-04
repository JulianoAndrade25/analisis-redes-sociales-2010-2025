# --- 1. Importaciones ---
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

ruta = Path(__file__).resolve().parents[1] / "datos" / "masdatos_de_excel.xlsx"

# Hojas
df_uso = pd.read_excel(ruta, sheet_name="HORAS_PROM_USO")
df_usuarios = pd.read_excel(ruta, sheet_name="crecimiento")

# Limpiar columnas “Unnamed” en cada DF
df_uso = df_uso.loc[:, ~df_uso.columns.str.contains('^Unnamed')]
df_usuarios = df_usuarios.loc[:, ~df_usuarios.columns.str.contains('^Unnamed')]


# Crecimiento (usuarios por año)
df_usuarios = df_usuarios.rename(columns={
    'anio': 'anio',
    'USUARIOS REDES (MILES DE MILLONES)': 'usuarios_miles_millones'
})

# Uso (promedios)
df_uso = df_uso.rename(columns={
    'ANIO': 'anio',
    'HORAS SEMANALES PROMEDIO': 'horas_prom',
    'MINUTOS DIARIOS PROMEDIO': 'minutos_prom'
})

# Tipos para crecimiento
df_usuarios['anio'] = pd.to_numeric(df_usuarios['anio'], errors='coerce')
df_usuarios['usuarios_miles_millones'] = pd.to_numeric(df_usuarios['usuarios_miles_millones'], errors='coerce')

# (Opcional si vas a usar luego)
df_uso['anio'] = pd.to_numeric(df_uso['anio'], errors='coerce')
df_uso['horas_prom'] = pd.to_numeric(df_uso['horas_prom'], errors='coerce')
df_uso['minutos_prom'] = pd.to_numeric(df_uso['minutos_prom'], errors='coerce')

# === 4) Gráfico: evolución global de usuarios (2010–2025) ===

# Filtramos y ordenamos los datos por año
df_plot = (
    df_usuarios[['anio', 'usuarios_miles_millones']]
    .dropna()
    .sort_values('anio')
)

# Crear la figura
fig, ax = plt.subplots(figsize=(9, 5))

# Trazar línea con marcadores
ax.plot(
    df_plot['anio'],
    df_plot['usuarios_miles_millones'],
    color='royalblue',
    marker='o',
    linewidth=2,
    label='Usuarios (miles de millones)'
)

# Relleno suave debajo de la curva (solo para estética)
ax.fill_between(
    df_plot['anio'],
    df_plot['usuarios_miles_millones'],
    color='royalblue',
    alpha=0.15
)

# Títulos y etiquetas
ax.set_title('Evolución global de usuarios de redes sociales (2010–2025)', fontsize=11)
ax.set_xlabel('Año')
ax.set_ylabel('Usuarios (miles de millones)')
ax.grid(axis='y', linestyle='--', alpha=0.4)
ax.legend(loc='upper left')

# Ajustes finales de ejes y formato
ax.set_xticks(df_plot['anio'])
plt.xticks(rotation=20, ha='right')
plt.tight_layout()

# === 5) Guardar gráfico ===
outdir = Path(__file__).resolve().parents[1] / 'graficos'
outdir.mkdir(parents=True, exist_ok=True)
output_path = outdir / 'evolucion_usuarios_2010_2025.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')
plt.show()

print(f'✅ Gráfico guardado correctamente en:\n{output_path}')
