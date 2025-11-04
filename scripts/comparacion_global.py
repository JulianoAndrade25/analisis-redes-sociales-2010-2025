# --- 1. Importaciones ---
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --- 2. Carga de datos (igual que en los anteriores) ---
ruta = Path(__file__).resolve().parents[1] / "datos" / "masdatos_de_excel.xlsx"
df = pd.read_excel(ruta, sheet_name="HORAS_PROM_USO")
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

# --- 3. Normalización de columnas ---
df = df.rename(columns={
    r'REGION\PAIS': 'pais',
    'HORAS SEMANALES PROMEDIO': 'horas_prom',
    'MINUTOS DIARIOS PROMEDIO': 'minutos_prom',
    'ANIO': 'anio'
})[['pais', 'horas_prom', 'minutos_prom', 'anio', 'fuente']]

df['horas_prom'] = pd.to_numeric(df['horas_prom'], errors='coerce')
df['minutos_prom'] = pd.to_numeric(df['minutos_prom'], errors='coerce')
df['anio'] = pd.to_numeric(df['anio'], errors='coerce')

# --- 4. Limpieza del promedio global ---
df_plot = df[df['pais'].str.upper() != 'PROMEDIO GLOBAL']

# --- 5. >>> AQUÍ VA EL BLOQUE DEL GRÁFICO COMPARATIVO <<<
plt.figure(figsize=(9,5))
x = np.arange(len(df_plot))
ancho = 0.35

plt.bar(x - ancho/2, df_plot['horas_prom'], width=ancho, label='Horas semanales', color='royalblue')
plt.bar(x + ancho/2, df_plot['minutos_prom'], width=ancho, label='Minutos diarios', color='orange')

plt.xticks(x, df_plot['pais'], rotation=20, ha='right')
plt.title('Comparación: horas semanales y minutos diarios (2025)')
plt.ylabel('Tiempo promedio')
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.4)
plt.tight_layout()

# --- 6. Guardado ---
outdir = Path(__file__).resolve().parents[1] / "graficos"
outdir.mkdir(parents=True, exist_ok=True)
output_path = outdir / "comparacion_horas_minutos.png"
plt.savefig(output_path, dpi=300, bbox_inches='tight')
plt.show()

print(f"✅ Gráfico comparativo guardado en:\n{output_path}")
