# Uso del cliente HDFS (2)

## Preparación el espacio de trabajo en HDFS
Crea un directorio principal /proyectos/ecommerce en HDFS.
Dentro de él, crea tres subdirectorios:
- /raw → para los logs originales.
- /procesados → para los logs ya tratados.
- /backup → para copias de seguridad.
![alt text](<Captura de pantalla 2025-11-07 182659.png>)

## Carga inicial de logs
Desde tu sistema local, sube al directorio /raw los siguientes logs de un servidor Web Apache:
- Fichero de log 1
- Fichero de log 2
- Fichero de log 3
![alt text](<Captura de pantalla 2025-11-07 184032.png>)
![alt text](<Captura de pantalla 2025-11-07 184231.png>)
![alt text](<Captura de pantalla 2025-11-07 190822.png>)

## Inspección de datos
Lista los archivos en /raw y visualiza su contenido.
Muestra el número total de líneas en cada archivo subido.
![alt text](<Captura de pantalla 2025-11-07 191211.png>)
![alt text](<Captura de pantalla 2025-11-07 191321.png>)

## Organización de los logs
Copia los archivos de /raw a /backup.
Mueve los archivos originales de /raw a /procesados.
![alt text](<Captura de pantalla 2025-11-07 191520.png>)
![alt text](<Captura de pantalla 2025-11-07 191611.png>)

## Acceso compartido para analistas
Verifica los permisos actuales de /proyectos/ecommerce.
Cambia los permisos de /procesados para que todos los usuarios tengan solo permisos de lectura, pero no de escritura ni eliminación.
![alt text](<Captura de pantalla 2025-11-07 191749.png>)
![alt text](<Captura de pantalla 2025-11-07 191907.png>)
![alt text](<Captura de pantalla 2025-11-07 192050.png>)

## Simulación de trabajo con analistas
Descarga desde HDFS uno de los archivos de /procesados a tu sistema local para compartirlo externamente.
![alt text](<Captura de pantalla 2025-11-07 192228.png>)

## Mantenimiento y limpieza
Sube un archivo temporal al directorio /raw.
Elimínalo de HDFS para mantener el espacio limpio.
![alt text](<Captura de pantalla 2025-11-07 192422.png>)
![alt text](<Captura de pantalla 2025-11-07 192506.png>)

## (Opcional, avanzado)
Configura una cuota de espacio en /backup (ejemplo: 10 MB).
Intenta subir archivos hasta alcanzar el límite y observa el comportamiento del sistema.
![alt text](<Captura de pantalla 2025-11-06 103921-1.png>) 
![alt text](<Captura de pantalla 2025-11-06 104133-1.png>)