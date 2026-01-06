# **PR0403: Análisis de logs con MapReduce**

## **1. Estadísticas básicas**

### **Contador de Códigos de Estado HTTP**

Queremos saber cuántas peticiones resultaron exitosas (200), cuántas no encontradas (404), errores de servidor (500), etc.
Para conseguirlo, tienes que hacer lo siguiente:

**Mapper**:
- Lee la línea.
- Busca el código de estado (el número después de ``"HTTP/1.0"``). En tu ejemplo son: ``502``, ``200``, ``404``, ``304``, etc.
- Emite (``código, 1``).

**Reducer**: Suma los contadores.

**Salida esperada**: 200: 50, 404: 10, 500: 5...


```python
%%writefile mapperlogs1.py
#!/usr/bin/env python3
import sys

for line in sys.stdin:
    parts = line.strip().split()

    if len(parts) < 9:
        continue

    status_code = parts[8]  

    print(f"{status_code}\t1")

```

    Overwriting mapperlogs1.py



```python
%%writefile reducerlogs1.py
#!/usr/bin/env python3
import sys

current_code = None
current_count = 0

for line in sys.stdin:
    code, value = line.strip().split("\t")
    value = int(value)

    if code == current_code:
        current_count += value
    else:
        if current_code is not None:
            print(f"{current_code}: {current_count}")
        current_code = code
        current_count = value

if current_code is not None:
    print(f"{current_code}: {current_count}")

```

    Overwriting reducerlogs1.py



```python
!cat logfiles.log | python3 mapperlogs1.py | sort | python3 reducerlogs1.py
```

    200: 142564
    303: 142261
    304: 143337
    403: 143014
    404: 142539
    500: 142729
    502: 143556


### **Tráfico Total por IP**

En este segundo ejercicio el objetivo será identificar qué direcciones IP están consumiendo más ancho de banda.

**Mapper**:
- Extrae la IP (el primer campo).
- Extrae el tamaño de la respuesta en bytes (el número después del código de estado). Nota: a veces es un guion “-“ si es 0.
- Emite (``IP, bytes``).
  
**Reducer**: Suma los bytes para cada IP.

**Salida**: ``162.253.4.179: 5041 bytes``


```python
%%writefile mapperlogs2.py
#!/usr/bin/env python3
import sys

for line in sys.stdin:
    parts = line.strip().split()

    if len(parts) < 10:
        continue

    ip = parts[0]
    bytes_sent = parts[9]

    if bytes_sent == "-":
        bytes_sent = 0

    print(f"{ip}\t{bytes_sent}")

```

    Overwriting mapperlogs2.py



```python
%%writefile reducerlogs2.py
#!/usr/bin/env python3
import sys

current_ip = None
total_bytes = 0

for line in sys.stdin:
    ip, value = line.strip().split("\t")
    value = int(value)

    if ip == current_ip:
        total_bytes += value
    else:
        if current_ip is not None:
            print(f"{current_ip}: {total_bytes} bytes")
        current_ip = ip
        total_bytes = value

if current_ip is not None:
    print(f"{current_ip}: {total_bytes} bytes")

```

    Overwriting reducerlogs2.py



```python
cat logfiles.log | python3 mapperlogs2.py | head | sort | python3 reducerlogs2.py
```

    119.170.1.203: 5011 bytes
    137.196.118.126: 4960 bytes
    160.36.208.51: 4979 bytes
    162.253.4.179: 5041 bytes
    182.215.249.159: 4936 bytes
    233.223.117.90: 4963 bytes
    238.217.83.154: 5152 bytes
    252.156.232.172: 5028 bytes
    255.231.52.33: 5054 bytes
    59.107.116.6: 5008 bytes
    Traceback (most recent call last):
      File "/home/jovyan/MapReduce/Logs/mapperlogs2.py", line 16, in <module>
        print(f"{ip}\t{bytes_sent}")
    BrokenPipeError: [Errno 32] Broken pipe
    cat: write error: Broken pipe


## **2. Análisis de comportamiento**

### **URLs más populares***

El objetivo en este ejercicio será encontrar las las rutas (``/usr/admin``, ``/usr/register``) más solicitadas.

**Mapper**:
- Analiza la cadena de petición ``DELETE /usr/admin HTTP/1.0``.
- Extrae la URL (el segundo elemento entre las comillas).
- Emite (``url, 1``).

**Reducer**: Suma las visitas.

**Salida**: Muestra todas las URLs y el número de accesos a cada una.

**Opcional**: ¿Cómo mostrarías sólo las top 10? (Requiere un segundo paso de ordenación o un reducer inteligente).


```python
%%writefile mapperlogs3.py
#!/usr/bin/env python3
import sys

for line in sys.stdin:
    try:
        request = line.split('"')[1]  
        parts = request.split()
        url = parts[1]           
        print(f"{url}\t1")
    except:
        continue
```

    Writing mapperlogs3.py



```python
%%writefile reducerlogs3.py
#!/usr/bin/env python3
import sys

current_url = None
count = 0

for line in sys.stdin:
    url, value = line.strip().split("\t")
    value = int(value)

    if url == current_url:
        count += value
    else:
        if current_url is not None:
            print(f"{current_url}: {count}")
        current_url = url
        count = value

if current_url is not None:
    print(f"{current_url}: {count}")

```

    Writing reducerlogs3.py



```python
cat logfiles.log | python3 mapperlogs3.py | sort | python3 reducerlogs3.py
```

    /usr: 200383
    /usr/admin: 199096
    /usr/admin/developer: 200000
    /usr/login: 200225
    /usr/register: 200296


### **Distribución por Método HTTP**

Aquí queremos saber qué tipo de acciones hacen los usuarios (GET vs POST vs DELETE).

**Mapper**: Extrae el verbo HTTP (``GET``, ``POST``, ``PUT``, ``DELETE``). Emite (``método, 1``).

**Reducer**: Suma contadores.


```python
%%writefile mapperlogs7.py
#!/usr/bin/env python3
import sys

for line in sys.stdin:
    try:
        request = line.split('"')[1]   
        method = request.split()[0]    
        print(f"{method}\t1")
    except:
        continue

```

    Writing mapperlogs7.py



```python
%%writefile reducerlogs7.py
#!/usr/bin/env python3
import sys

current_method = None
count = 0

for line in sys.stdin:
    method, value = line.strip().split("\t")
    value = int(value)

    if method == current_method:
        count += value
    else:
        if current_method is not None:
            print(f"{current_method}: {count}")
        current_method = method
        count = value

if current_method is not None:
    print(f"{current_method}: {count}")

```

    Writing reducerlogs7.py



```python
cat logfiles.log | python3 mapperlogs7.py | sort | python3 reducerlogs7.py
```

    DELETE: 249768
    GET: 250515
    POST: 248931
    PUT: 250786


### **Análisis de navegadores**

El objetivo aquí es saber si los usuarios usan Chrome, Firefox, o si son bots/móviles.

**Mapper**:
- Extrae la cadena larga del final (User-Agent).
- Busca palabras clave simples: si contiene “Chrome” emite (``"Chrome", 1``), si “Firefox” emite (``"Firefox", 1``), etc.

**Reducer**: Suma totales por navegador.


```python
%%writefile mapperlogs4.py
#!/usr/bin/env python3
import sys

for line in sys.stdin:
    try:
        user_agent = line.split('"')[-2]

        if "Chrome" in user_agent:
            print("Chrome\t1")
        elif "Firefox" in user_agent:
            print("Firefox\t1")
        elif "Mobile" in user_agent or "Android" in user_agent or "iPhone" in user_agent:
            print("Mobile\t1")
        elif "bot" in user_agent.lower():
            print("Bot\t1")
        else:
            print("Other\t1")
    except:
        continue
```

    Writing mapperlogs4.py



```python
%%writefile reducerlogs4.py
#!/usr/bin/env python3
import sys

current_browser = None
count = 0

for line in sys.stdin:
    browser, value = line.strip().split("\t")
    value = int(value)

    if browser == current_browser:
        count += value
    else:
        if current_browser is not None:
            print(f"{current_browser}: {count}")
        current_browser = browser
        count = value

if current_browser is not None:
    print(f"{current_browser}: {count}")

```

    Writing reducerlogs4.py



```python
cat logfiles.log | python3 mapperlogs4.py | sort | python3 reducerlogs4.py
```

    Chrome: 599509
    Firefox: 199953
    Mobile: 100403
    Other: 100135


## **3. Análisis temporal y de sesión**

### **Picos de tráfico por hora**

Queremos descubrir a qué hora del día el servidor recibe más carga.

**Mapper**:
- Parsea el campo de fecha [``27/Dec/2037:12:00:00 +0530``].
- Extrae la hora (``12``).
- Emite (``hora, 1``).

**Reducer**: Suma las peticiones por hora.


```python
%%writefile mapperlogs5.py
#!/usr/bin/env python3
import sys
import re

pattern = re.compile(r"\[(\d{2}/\w{3}/\d{4}):(\d{2}):\d{2}:\d{2}")

for line in sys.stdin:
    match = pattern.search(line)
    if match:
        hour = match.group(2)
        print(f"{hour}\t1")
```

    Writing mapperlogs5.py



```python
%%writefile reducerlogs5.py
#!/usr/bin/env python3
import sys

current_hour = None
count = 0

for line in sys.stdin:
    hour, value = line.strip().split("\t")
    value = int(value)

    if hour == current_hour:
        count += value
    else:
        if current_hour is not None:
            print(f"{current_hour}: {count}")
        current_hour = hour
        count = value

if current_hour is not None:
    print(f"{current_hour}: {count}")
```

    Writing reducerlogs5.py



```python
cat logfiles.log | python3 mapperlogs5.py | sort | python3 reducerlogs5.py
```

    12: 1000000


### **Tasa de error por endpoint**

En este ejercicio queremos descubrir qué URLs están fallando más.

**Mapper**:
- Extrae la URL y el código de estado.
- Si el código es >= 400, emite (``url, "error"``).
- Si el código es < 400, emite (``url, "ok"``).
- O mejor: emite (``url, (1, 0)``) para éxito y (``url, (0, 1)``) para error.
  
**Reducer**: Suma totales y errores. Calcula el % de error: ``(errores / total) * 100``.


```python
%%writefile mapperlogs6.py
#!/usr/bin/env python3
import sys

for line in sys.stdin:
    parts = line.strip().split()
    if len(parts) < 9:
        continue

    url = parts[6]

    try:
        status = int(parts[8])
    except:
        continue

    if status >= 400:
        print(f"{url}\t1\t1")   # total=1, errores=1
    else:
        print(f"{url}\t1\t0")   # total=1, errores=0

```

    Overwriting mapperlogs6.py



```python
%%writefile reducerlogs6.py
#!/usr/bin/env python3
import sys

url_actual = ""
total = 0
errores = 0

for line in sys.stdin:
    url, uno, error = line.strip().split("\t")

    uno = int(uno)
    error = int(error)

    if url == url_actual:
        total = total + uno
        errores = errores + error
    else:
        if url_actual != "":
            porcentaje = (errores / total) * 100
            print(url_actual + "\t" + str(porcentaje))

        url_actual = url
        total = uno
        errores = error
        
if url_actual != "":
    porcentaje = (errores / total) * 100
    print(url_actual + "\t" + str(porcentaje))
```

    Overwriting reducerlogs6.py



```python
cat logfiles.log | python3 mapperlogs6.py | sort | python3 reducerlogs6.py
```

    /usr	57.25335981595245
    /usr/admin	57.1920078755977
    /usr/admin/developer	57.05050000000001
    /usr/login	57.30902734423773
    /usr/register	57.11397132244278



```python

```
