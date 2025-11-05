# Instalación y configuración de Hadoop en modo pseudo-distribuido

Usaremos una máquina de **Ubuntu-server**, a la cual le pondremos dos adaptadores de red:
- Nat
![alt text](<Captura de pantalla 2025-10-31 154724.png>)
- Solo anfitrión
![alt text](<Captura de pantalla 2025-10-31 154450.png>)

Pondremos la ip con la que enlazaremos a nuestro ordenador nativo.
![alt text](<Captura de pantalla 2025-10-30 111809.png>)

Instalaremos el **ssh-server** en nuestra máquina.
![alt text](<Captura de pantalla 2025-10-30 111844.png>)

En nuestra máquina nativa accederemos por ssh a nuestra máquina y crearemos al usuario **hadoop**.
![alt text](<Captura de pantalla 2025-10-23 094906.png>)

Agregamos al nuevo usuario al grupo de sudoers.
![alt text](<Captura de pantalla 2025-10-23 094952.png>)

Accederemos al usuario creado y creamos el directorio **/opt/hadoop**.
![alt text](<Captura de pantalla 2025-10-23 095429.png>)

Para descargar Hadoop debemos ir a [Apache hadoop](https://hadoop.apache.org/). En el apartado **Download** vemos que hay disponibles diversas versiones. Comienzo copiando el fichero con el 
SHA **(checksum)**.
![alt text](<Captura de pantalla 2025-10-23 095748.png>)

Y lo descargamos usando el comando **wget**.
![alt text](<Captura de pantalla 2025-10-23 095818.png>)

Ahora copiamos el enlace de los **binarios** de la opción elegida.
![alt text](<Captura de pantalla 2025-10-23 100004.png>)

Lo descargamos con el mismo comando que el anterior.
![alt text](<Captura de pantalla 2025-10-23 100830.png>)

Con el comando verificamos que el archivo no haya sido alterado o corrompido desde su descarga.
![alt text](<Captura de pantalla 2025-10-23 100913.png>)

Ahora solo nos queda **descomprimirlo**:
- Con **strip components=1** le indicamos que no cree un directorio
- Con **–C** le indicamos el directorio donde queremos  descomprimir los datos.
![alt text](<Captura de pantalla 2025-10-23 101209.png>)
![alt text](<Captura de pantalla 2025-10-23 101351.png>)

Descargaremos la versión **Java 8**. Para descargarlo vamos a [jdk.java.net](https://jdk.java.net/) y Copiamos el enlace de la **Oracle Linux 8.6 x 64**
![alt text](<Captura de pantalla 2025-10-23 102350.png>)

Lo descargamos con el mismo comando de antes.
![alt text](<Captura de pantalla 2025-10-23 102715.png>)

Lo **descomprimimos** en el directorio **/opt/hadoop**.
![alt text](<Captura de pantalla 2025-10-23 102803.png>)

Le cambiamos de nombre a uno más fácil y comprobamos que Java funciona correctamente y que es la versión que deseamos.
![alt text](<Captura de pantalla 2025-10-23 103216.png>)

Con esa configuración en el **.bashrc** conseguimos que nuestro sistema reconozca **Hadoop** y **Java** desde cualquier terminal, sin tener que escribir rutas largas cada vez. 
![alt text](<Captura de pantalla 2025-10-23 105004.png>)

Y **recargamos** el fichero para que se apliquen los cambios.
![alt text](<Captura de pantalla 2025-10-23 105151.png>)

Accedemos a ese fichero y agregamos esa línea, la cual **vincula Hadoop con Java**, permitiendo que los servicios de Hadoop (como HDFS y YARN) se ejecuten correctamente.
![alt text](<Captura de pantalla 2025-10-23 105409.png>)
![alt text](<Captura de pantalla 2025-10-23 105508.png>)

Verificaremos ahora que todo es correcto y que Hadoop funciona. Si buscamos en esta ruta podemos ver que hay un fichero con ejemplos de **MapReduce**. Listaremos el contenido del archivo **JAR (.jar)** sin ejecutarlo ni extraerlo con este comando.
![alt text](<Captura de pantalla 2025-10-23 105809.png>)

Como necesitamos datos vamos a descargar el libro del Quijote.
![alt text](<Captura de pantalla 2025-10-23 110254-1.png>)

Con este comando (sin el clear) se ejecuta un trabajo MapReduce que busca todas las coincidencias del **patrón [sS]ancho** dentro del **archivo /tmp/quijote.txt**, y guarda los resultados en **/tmp/salida**.
![alt text](<Captura de pantalla 2025-10-23 110749.png>)

Con este comando Hadoop ha contado **cuántas veces** aparece la palabra **“Sancho” o “sancho”** (por la **expresión [sS]ancho**).
![alt text](<Captura de pantalla 2025-10-23 111612.png>)

Comenzamos generando el par de claves en el equipo, esto se hace mediante el comando **ssh-keygen**. Después configuraremos el **acceso ssh sin contraseña** para el **usuario Hadoop** como muestro en la imagen.
![alt text](<Captura de pantalla 2025-10-29 121310.png>)

Comprobamos que funciona correctamente.
![alt text](<Captura de pantalla 2025-10-29 121656.png>)

Accedemos al fichero de esta ruta llamado **core-site.xml** y pondremos este código. Esto hará que **use el sistema de archivos distribuido HDFS y se conecte al NameNode local en el puerto 8020**.
![alt text](<Captura de pantalla 2025-10-29 122336.png>)
![alt text](<Captura de pantalla 2025-10-29 122239-1.png>)

En este fichero **hdfs-site.xml** pondremos este código y esto hará **guardar los metadatos y los datos del HDFS en estas rutas locales y usar un solo bloque de copia**.
![alt text](<Captura de pantalla 2025-10-29 123336.png>)
![alt text](<Captura de pantalla 2025-10-29 123307.png>)

Debemos crear los **directorios** que hemos indicado en el **fichero de configuración**.  Finalmente, **formateamos el sistema de ficheros** con la sentencia **hdfs namenode -format**.
![alt text](<Captura de pantalla 2025-10-29 123553.png>)

Arrancaremos el sistema HDFS. Para ello utilizamos el script que se encuentra en el directorio sbin **start-dfs.cmd**.  Podemos comprobar que estos procesos se han puesto en marcha usando el comando **jps** (muestra los procesos Java activos en la máquina).
![alt text](<Captura de pantalla 2025-10-30 100108.png>)

También podemos comprobar que se ha iniciado correctamente accediendo al **puerto 9870** con nuestra ip.
![alt text](<Captura de pantalla 2025-10-31 180306.png>)

 El comando que utilizaremos para trabajar con ficheros es **hdfs dfs**.
![alt text](<Captura de pantalla 2025-10-30 102249.png>)

Copiamos un **fichero** al sistema de archivos distribuido de **Hadoop (HDFS)** y comprobamos que se haya almacenado correctamente.
![alt text](<Captura de pantalla 2025-10-30 102455.png>)