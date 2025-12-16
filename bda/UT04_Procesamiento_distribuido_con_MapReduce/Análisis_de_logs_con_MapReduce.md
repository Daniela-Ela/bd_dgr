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

    status_code = parts[-2]

    print(f"{status_code}\t1")

```

    Writing mapperlogs1.py



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

    Writing reducerlogs1.py


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
    bytes_sent = parts[-1]

    if bytes_sent == "-":
        bytes_sent = 0

    print(f"{ip}\t{bytes_sent}")

```

    Writing mapperlogs2.py



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

    Writing reducerlogs2.py


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
        # El User-Agent suele ser la última cadena entre comillas
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

    Overwriting mapperlogs4.py



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

    Overwriting reducerlogs4.py


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

    Overwriting mapperlogs5.py



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

    Overwriting reducerlogs5.py


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
    try:
        parts = line.strip().split()
        url = parts[6]
        status = int(parts[-2])

        if status < 400:
            print(f"{url}\t1\t0")
        else:
            print(f"{url}\t0\t1")
    except:
        continue

```

    Writing mapperlogs6.py



```python
%%writefile reducerlogs6.py
#!/usr/bin/env python3
import sys

current_url = None
ok_total = 0
error_total = 0

for line in sys.stdin:
    url, ok, error = line.strip().split("\t")
    ok = int(ok)
    error = int(error)

    if url == current_url:
        ok_total += ok
        error_total += error
    else:
        if current_url is not None:
            total = ok_total + error_total
            error_rate = (error_total / total) * 100 if total > 0 else 0
            print(f"{current_url}: {error_rate:.2f}%")
        current_url = url
        ok_total = ok
        error_total = error

if current_url is not None:
    total = ok_total + error_total
    error_rate = (error_total / total) * 100 if total > 0 else 0
    print(f"{current_url}: {error_rate:.2f}%")
```

    Writing reducerlogs6.py



```python

```
