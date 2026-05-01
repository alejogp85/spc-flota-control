Centro de Control Operacional - Telemetría de Flota Pesada
Contexto del Negocio
En operaciones logísticas de transporte pesado, la variabilidad no controlada en el consumo de diésel (Lts/100km) es una de las principales fugas de rentabilidad (P&L). Este desarrollo es un Proof of Concept (PoC) de un sistema de alerta temprana basado en Control Estadístico de Procesos (SPC).

Arquitectura de la Solución
Se aplica un modelo de distribución normal (Campana de Gauss) sobre datos de telemetría GPS para identificar anomalías en tiempo real que superen los límites de física del vehículo:

Media (μ): 38.5 Lts/100km (Rendimiento estándar).
Desviación Estándar (σ): 2.2 Lts/100km (Variabilidad por tráfico/vía).
UCL / LCL (±3σ): 45.1 / 31.9 Lts/100km.
Cualquier lectura por fuera de estos límites tiene un 99.7% de probabilidad de no ser casualidad, disparando un protocolo de investigación.

Casos de Uso Detectados por el Sistema
El dashboard resalta automáticamente tres escenarios críticos:

Punto B (51.5 Lts/100km - Cola Derecha): Supera el UCL (+3σ). Diagnóstico operativo inmediato: Sospecha de extracción no autorizada de combustible ("ordeño"). Requiere auditoría.
Punto A (48.2 Lts/100km): Diagnóstico mecánico: Posible fuga de combustible o falla severa en el sistema de inyección.
Punto C (31.0 Lts/100km - Cola Izquierda): Anomalía por debajo del -3σ. Diagnóstico técnico: Error en el sensor de telemetría o carga incompleta no reportada al sistema.
Tech Stack
Backend / Lógica: Python (SciPy, NumPy, Matplotlib).
Frontend Operacional: Streamlit (Diseñado para ser consumido por el Centro de Control en tiempo real).
Impacto Esperado
Protección del P&L: Reducción de mermas por accidentes o sabotaje.
Mantenimiento Predictivo: Detección de fallas (Punto A) antes de que el vehículo sufra una avería mayor en ruta.
Cero inversión en hardware: Aprovecha la telemetría GPS actual de la flota.
