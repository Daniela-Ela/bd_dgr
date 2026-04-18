```python
!pip install redis
```

    Requirement already satisfied: redis in /opt/conda/lib/python3.11/site-packages (6.4.0)



```python
import redis
r = redis.Redis(
    host='redis',
    port=6379,
    db=0,
    decode_responses=True
)
```

### **Inserta la clave app:version con el valor 1.0**


```python
r.set('app:version', '1.0')
```




    True



### **Recupera y muestra el valor de app:version**


```python
print("Versión inicial:", r.get('app:version'))
```

    Versión inicial: 1.0


### **Modifica el valor de app:version a 1.1**


```python
r.set('app:version', '1.1')
```




    True




```python
print("Versión modificada:", r.get('app:version'))
```

    Versión modificada: 1.1


### **Crea la clave contador:descargas con valor 0**


```python
r.set('contador:descargas', 0)
```




    True



### **Incrementa en 5 el valor de contador:descargas**


```python
r.incrby('contador:descargas', 1)
```




    1




```python
r.incrby('contador:descargas', 1)
```




    2




```python
r.incrby('contador:descargas', 1)
```




    3




```python
r.incrby('contador:descargas', 1)
```




    4




```python
r.incrby('contador:descargas', 1)
```




    5




```python
print("Contador después de incrementar:", r.get('contador:descargas'))
```

    Contador después de incrementar: 5


### **Decrementa en 2 el valor de contador:descargas**


```python
r.decrby('contador:descargas', 1)
```




    4




```python
r.decrby('contador:descargas', 1)
```




    3




```python
print("Contador después de decrementar:", r.get('contador:descargas'))
```

    Contador después de decrementar: 3


### **Inserta la clave app:estado con el valor activo**


```python
r.set('app:estado', 'activo')
```




    True




```python
print("Estado actual:", r.get('app:estado'))
```

    Estado actual: activo


### **Cambia el valor a mantenimiento**


```python
r.set('app:estado', 'mantenimiento')
```




    True




```python
print("Nuevo estado:", r.get('app:estado'))
```

    Nuevo estado: mantenimiento


### **Inserta la clave mensaje:bienvenida con el texto Hola alumno**


```python
r.set('mensaje:bienvenida', 'Hola alumno')
```




    True




```python
print("Mensaje de bienvenida:", r.get('mensaje:bienvenida'))
```

    Mensaje de bienvenida: Hola alumno


### **Establece un tiempo de expiración de 30 segundos para la clave app:estado**


```python
r.expire('app:estado', 30)
```




    False




```python
print("Tiempo de expiración de app:estado establecido a 30 segundos")
```

    Tiempo de expiración de app:estado establecido a 30 segundos


### **Verifica si la clave app:estado todavía existe después de unos segundos**


```python
import time
```


```python
time.sleep(2)
```


```python
print("¿App:estado sigue existiendo después de 2 segundos?", r.ttl("app:estado"))
```

    ¿App:estado sigue existiendo después de 2 segundos? -2


### **Elimina la clave app:version y muestra un mensaje confirmando su eliminación**


```python
r.delete('app:version')
```




    0




```python
print("Clave 'app:version' eliminada correctamente")
```

    Clave 'app:version' eliminada correctamente

