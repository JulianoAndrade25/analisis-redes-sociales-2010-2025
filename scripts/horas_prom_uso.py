from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# === 1. Leer el archivo Excel ===
ruta = Path(__file__).resolve().parents[1] / "datos" / "masdatos_de_excel.xlsx"
df = pd.read_excel(ruta, sheet_name="HORAS_PROM_USO")

# === 2. Eliminar columnas innecesarias ===
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

# === 3. Normalizar nombres de columnas ===
df = df.rename(columns={
    r'REGION\PAIS': 'pais',  # ← nota la r antes de las comillas, evita el warning
    'HORAS SEMANALES PROMEDIO': 'horas_prom',
    'MINUTOS DIARIOS PROMEDIO': 'minutos_prom',
    'ANIO': 'anio'
})[['pais', 'horas_prom', 'minutos_prom', 'anio', 'fuente']]

# === 4. Convertir a valores numéricos ===
df['horas_prom'] = pd.to_numeric(df['horas_prom'], errors='coerce')
df['minutos_prom'] = pd.to_numeric(df['minutos_prom'], errors='coerce')
df['anio'] = pd.to_numeric(df['anio'], errors='coerce')

# === 5. Mostrar estructura ===
print(df.shape)
print(df.head())
print(df.dtypes)

# === 6. Preparar datos para el gráfico ===
df_plot = df[df['pais'].str.upper() != "PROMEDIO GLOBAL"].sort_values('horas_prom', ascending=False)

# === 7. Crear gráfico ===
plt.figure(figsize=(9, 5))
plt.bar(df_plot['pais'], df_plot['horas_prom'], color='royalblue')

plt.title('Horas semanales promedio en redes sociales (2025)')
plt.ylabel('Horas por semana')
plt.xlabel('País / Región')
plt.xticks(rotation=20, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.4)

# Etiquetas encima de las barras
for x, y in zip(df_plot['pais'], df_plot['horas_prom']):
    plt.text(x, y + 0.1, f'{y:.1f}', ha='center', va='bottom', fontsize=9)

plt.tight_layout()

# === 8. Guardar gráfico en carpeta 'graficos' ===
outdir = Path(__file__).resolve().parents[1] / "graficos"
outdir.mkdir(parents=True, exist_ok=True)

output_path = outdir / "horas_semanales_promedio.png"
plt.savefig(output_path, dpi=300, bbox_inches='tight')
plt.show()

print(f"✅ Gráfico guardado correctamente en:\n{output_path}")
