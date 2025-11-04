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

print(df_uso[['anio', 'horas_prom']])
print(df_usuarios[['anio', 'usuarios_miles_millones']])

promedio_2025 = df_uso['horas_prom'].mean()  
anio_ultimo = df_usuarios['anio'].max()      

# === 4) Gráfico combinado: usuarios vs tiempo de uso (2010–2025) ===

# --- 5. Creación del gráfico combinado ---


# Figura base
fig, ax1 = plt.subplots(figsize=(9,5))

# --- EJE IZQUIERDO: evolución de usuarios ---
ax1.plot(df_usuarios["anio"], df_usuarios["usuarios_miles_millones"],
         color="tab:blue", marker="o", linewidth=2,
         label="Usuarios (miles de millones)")

# Relleno suave bajo la línea
ax1.fill_between(df_usuarios["anio"], df_usuarios["usuarios_miles_millones"],
                 alpha=0.15, color="tab:blue")

# Etiquetas y estética del eje izquierdo
ax1.set_xlabel("Año")
ax1.set_ylabel("Usuarios (miles de millones)", color="tab:blue")
ax1.tick_params(axis='y', colors="tab:blue")
ax1.grid(axis='y', linestyle='--', alpha=0.4)

# --- EJE DERECHO: punto del promedio 2025 ---
promedio_2025 = df_uso["horas_prom"].mean()
anio_ultimo = df_usuarios["anio"].max()

ax2 = ax1.twinx()

# Línea horizontal en el nivel del promedio
ax2.axhline(promedio_2025, linestyle='--', linewidth=2, alpha=0.85,
            color="tab:orange", label=f"Horas semanales prom. (2025): {promedio_2025:.1f}")

# Punto marcador en 2025
ax2.scatter([anio_ultimo], [promedio_2025], s=120, marker='D', color="tab:orange", zorder=3)

# Etiquetas y color del eje derecho
ax2.set_ylabel("Horas semanales promedio", color="tab:orange")
ax2.tick_params(axis='y', colors="tab:orange")
ax2.spines['right'].set_color("tab:orange")
ax2.set_ylim(0, max(12, promedio_2025 + 1))

# --- Leyenda combinada ---
h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax1.legend(h1 + h2, l1 + l2, loc="upper left")

# --- Título y disposición ---
plt.title("Evolución global: usuarios vs tiempo de uso (2010–2025)")
plt.tight_layout()

plt.show()

# --- Guardado automático ---
from pathlib import Path

outdir = Path(__file__).resolve().parents[1] / "graficos"
outdir.mkdir(parents=True, exist_ok=True)

output_path = outdir / "evolucion_usuarios_tiempo.png"
plt.savefig(output_path, dpi=300, bbox_inches="tight")

print(f"✅ Gráfico guardado en:\n{output_path}")
