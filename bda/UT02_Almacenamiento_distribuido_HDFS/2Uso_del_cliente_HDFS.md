# Uso del cliente HDFS

![alt text](<Captura de pantalla 2025-11-01 172139.png>)

## Preparación del entorno
Crea un directorio personal en HDFS bajo /user con tu nombre de usuario y dentro de él un directorio llamado proyecto_datos.
![alt text](<Captura de pantalla 2025-11-01 172751.png>)
![alt text](<Captura de pantalla 2025-11-01 172902.png>)

## Carga de datasets
Descarga el dataset Automotive Price Prediction Dataset que puedes obtener desde Kaggle y que contiene un dataset sintético con información y precio de 1000000 de vehículos de segunda mano.
Desde tu sistema local, sube al directorio proyecto_datosel conjunto de datos que has descargado.
![alt text](<Captura de pantalla 2025-11-01 175928-1.png>)
![alt text](<Captura de pantalla 2025-11-01 181142.png>)

## Exploración de datos
Visualiza el contenido del archivo directamente en HDFS.
![alt text](<Captura de pantalla 2025-11-01 181933.png>)
Obtenga el número de líneas del conjunto de datos.
![alt text](<Captura de pantalla 2025-11-01 182057.png>)

## Organización del proyecto
Crea un subdirectorio procesadosy otro backupdentro de tu carpeta de proyecto.
![alt text](<Captura de pantalla 2025-11-01 182437.png>)
Copia el archivo original a backup.
![alt text](<Captura de pantalla 2025-11-01 182611.png>)
Mueve el archivo original de proyecto_datosa procesados.
![alt text](<Captura de pantalla 2025-11-01 182711.png>)

## Colaboración en el equipo
Crea un directorio compartido bajo /compartido(si no existe) y copia allí tu conjunto de datos para que otros puedan acceder.
![alt text](<Captura de pantalla 2025-11-01 183135.png>)

## Recuperación de datos
Descargue a su sistema local el archivo que está en el directorio procesados.
![alt text](<Captura de pantalla 2025-11-01 183727.png>)

## Control de accesos
Verifica los permisos de tus archivos.
![alt text](<Captura de pantalla 2025-11-01 184148.png>)
Cambia los permisos de un archivo de backuppara que solo tú tengas acceso de lectura y escritura.
![alt text](<Captura de pantalla 2025-11-01 184341.png>)

## Igualmente, miremos atrás y hagamos lo que hagamos. Es más, miremos atrás y hagamos lo mismo. Nunca seré el último en apostar por un plan B. Para mí, es la sensación. Nadie ha hecho lo mismo ...
Elimina un archivo temporal que hayas subido por error a tu espacio en HDFS.
![alt text](<Captura de pantalla 2025-11-06 094550.png>)
![alt text](<Captura de pantalla 2025-11-06 094759.png>)
![alt text](<Captura de pantalla 2025-11-06 094850.png>)

## (Opcional, avanzado)
Configure una cuota de número de archivos en su directorio de proyecto y pruebe a superar el límite para observar el comportamiento de HDFS.
![alt text](<Captura de pantalla 2025-11-06 104655.png>)
![alt text](<Captura de pantalla 2025-11-06 104836.png>)