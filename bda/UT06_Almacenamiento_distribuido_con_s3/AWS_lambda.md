# **PR0602. AWS Lambda**

## **Ejercicio 1**
Crea una función Lambda que se dispare cada vez que se suba un archivo a un bucket de S3. Debe mostrar un mensaje con el siguiente texto:

```
Se ha creado el archivo {nombre_archivo} de {tamaño_en_ks} kilobytes en el bucket {nombre_bucket}
````

![imagen.png](aa4eab7e-3f06-4d6f-9921-5035b7fc09a4.png)

![imagen.png](28c0bdbc-d36e-48bf-ac31-b4df0a409583.png)

## **Ejercicio 2**
Crea una función que se dispare cuando llegue un mensaje a la cola ``MiBuzon``. La función debe imprimir:

```
He leído el mensaje: {contenido_del_mensaje}".
```

![imagen.png](cdf2a207-cbb4-4f39-8fc9-6f1c5c34b123.png)

![imagen.png](ccf57353-5d23-4c51-9fd7-7e238a8f61fd.png)

## **Ejercicio 3**
Modifica el primer ejercicio. Ahora, en lugar de imprimir solo por pantalla, la Lambda debe enviar los datos del archivo (nombre y tamaño) como un mensaje a una cola SQS llamada ``ColaDeProcesamiento``

![imagen.png](60207d0b-0b49-48f4-ab78-7ecd0d4b18cc.png)

![imagen.png](a770f7da-28ce-4eae-9dd2-aefc518f66c9.png)

![imagen.png](e9b859aa-5ee0-4bc7-b07d-47201728a3eb.png)

## **Ejercicio 4**
Envía un JSON a una cola SQS que contenga un campo ``prioridad`` y otro ``mensaje``. Si la prioridad es ``ALTA``, la Lambda debe imprimir: ``¡PROCESANDO URGENTE: {mensaje}!``. Si es ``BAJA``, debe imprimir: ``Registro guardado para después``.

Para enviar manualmente un mensaje a una cola simplemente debes ir a ``Enviar y recibir mensajes`` de la propia cola.

![imagen.png](741abbd5-27cd-40b0-8400-cfb24c7855f5.png)

![imagen.png](62142b9c-3107-454d-884e-3e71dcff6b47.png)

![imagen.png](737d0f4d-4c2d-4989-a9fd-f09a634a41b5.png)

## **Ejercicio 5**
Rehaz el ejercicio anterior enviando el mensaje desde un script Python en tu equipo.

A continuación tienes un ejemplo de código sobre cómo enviar un mensaje a una cola.

```
import boto3

# Creamos el cliente de SQS
sqs = boto3.client('sqs')

# Definimos la URL de la cola
queue_url = 'URL_de_la_cola'

# Creamos un diccionario (JSON) con los datos
datos_archivo = {
    # Contenido del JSON
}

# Serializamos el diccionario
mensaje_serializado = json.dumps(datos_archivo)

# Enviamos el mensaje
response = sqs.send_message(
    QueueUrl=queue_url,
    MessageBody=mensaje_serializado
)
```


```python
import boto3
import json

sqs = boto3.client('sqs', region_name='us-east-1')

queue_url = 'https://sqs.us-east-1.amazonaws.com/533267236873/MiBuzon'

datos_archivo = {
    "prioridad": "ALTA",
    "mensaje": "Mensaje enviado desde Jupyter"
}

mensaje_serializado = json.dumps(datos_archivo)

response = sqs.send_message(
    QueueUrl=queue_url,
    MessageBody=mensaje_serializado
)
print("Mensaje enviado correctamente")
```

    Mensaje enviado correctamente


![imagen.png](dd1ac48d-aee5-4ce2-bec3-df2c3322286f.png)

## **Ejercicio 6**
Crea una función Lambda que se ejecute todos los días a las 08:40 h que muestre el mensaje 

``Bienvenido a un nuevo día de clase``

![imagen.png](8253ed7d-5d8d-4fe1-8f6b-9a9e82c88f8b.png)

![imagen.png](59c72398-de90-46c6-a24e-efce549520d4.png)

## **Ejercicio 7**
Crea una función Lambda que se ejecute todos los días y que imprima el número de archivos que hay en un bucket (puedes usar algún bucket que tengas creado por ahí). Recuerda que para obtener el listado de archivos de un bucket debes usar la función ``list_objects_v2``

![imagen.png](1c6216c4-d5d7-4680-9284-97a97582fad3.png)

## **Ejercicio 8**
Vamos a convertir la función Lambda del primer ejercicio en un productor de mensajes. La idea es que, cada vez que se suba un archivo a S3 ejecute esta función, la cual extraerá los datos que queremos del archivo y los enviará en un mensaje a una cola.

Las tareas que tienes que realizar son:

-  **Crear la Cola (SQS)**: crea una cola estándar llamada ``ColaDeProcesamiento``.
- **Modificar la función Lambda**: crea una Lambda que capture el nombre y el tamaño del archivo, la función debe enviar un mensaje a la cola SQS con el siguiente formato de texto: 
```
Archivo registrado: {nombre_archivo} | Tamaño: {tamaño_en_kb} KB
```
- **Prueba de integración**: sube un archivo al bucket de S3. Esto disparará la Lambda, la cual enviará el mensaje a la cola.
- **Verificación en SQS**: ve a la consola de SQS, selecciona tu cola y pulsa en ``Enviar`` y ``recibir mensajes`` y ``verifica que el mensaje`` con los datos correctos ha llegado al buzón.

![imagen.png](64f3d99a-ee47-482d-b02e-d80267cac8df.png)

![imagen.png](c2eeb07a-cc06-4bfa-b09a-d29a18d5b61a.png)


```python

```
