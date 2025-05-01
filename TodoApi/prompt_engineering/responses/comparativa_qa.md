# Comparativa: QA Tradicional vs QA con IA

| Aspecto                   | QA Tradicional                              | QA + IA                                          |
|---------------------------|----------------------------------------------|---------------------------------------------------|
| **Tiempo de redacción**   | Manual, días/semanas en escribir casos       | Segundos con prompt a GPT-4                       |
| **Cobertura**             | Limitada al esfuerzo humano                  | Automática para todos los endpoints               |
| **Mantenimiento**         | Cada cambio en la API exige reescribir Tests | Sólo actualizas el prompt y regeneras el script   |
| **Documentación**         | Generar aparte historias, specs, manualmente | Se genera de forma simultánea con prompts         |
| **Detección de edge-cases** | Depende de la creatividad del QA            | IA sugiere casos adicionales basados en patrones  |
| **Escalabilidad**         | Se complica al crecer la API                 | Lineal: un prompt cubre cualquier tamaño          |
| **Consistencia**          | Hay variación estilo/estructura entre QA     | Uniforme: todos los tests siguen mismo template   |

## Reflexión

- **Velocidad**: Hemos pasado de días a minutos en el diseño y escritura de tests.  
- **Calidad**: La IA aporta ideas de casos límite que a veces pasan desapercibidos.  
- **Mantenimiento**: Con un pequeño ajuste al prompt, regeneras todos los scripts.  
- **Colaboración**: El equipo puede revisar y afinar el prompt en lugar de reescribir cada prueba.
