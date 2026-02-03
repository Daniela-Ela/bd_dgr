# **PR0302: Lectura avanzada de datos de archivos**

## **Objetivo de la Práctica**

Esta práctica es una revisión de la anterior donde aumentamos el nivel de dificultad ya que los archivos de origen tienen sus peculiaridades.

Nuevamente tienes que leer datos de tres fuentes diferentes (CSV, Excel y JSON) y volcar el resultado a un archivo CSV.

## **1. Norte** (``ventas_norte_v2.csv``):
- Formato CSV delimitado por punto y coma (``;``).
- El campo ``Direccion_Envio`` contiene comas reales (ej: “Calle Mayor, 12”). Debes asegurarte de que Pandas no rompa las filas al leerlo.
- El campo ``Total_Factura`` viene como texto con símbolos de moneda (ej: “$1,200.50”). Deberás limpiarlo y convertirlo a ``float``.


```python
import pandas as pd

def limpiar_moneda(x):
    return float(x.replace("$",""))

df_norte = pd.read_csv(
    "./ventas_norte_v2.csv",
    delimiter=";",
    header=0,
    parse_dates=["Fecha_Transaccion"],
    converters={"Total_Factura": limpiar_moneda}
)
```


```python
print(df_norte.head(20))
```

       ID_Pedido   Fecha_Transaccion Cliente_Nombre            Direccion_Envio  \
    0     N-1000 2023-05-10 03:00:00      Usuario_0       Gran Vía, 49, Piso 4   
    1     N-1001 2023-06-18 09:00:00      Usuario_1   Av. Libertad, 30, Piso 4   
    2     N-1002 2023-03-10 05:00:00      Usuario_2   Av. Libertad, 98, Piso 2   
    3     N-1003 2023-05-10 03:00:00      Usuario_3   Paseo Gracia, 94, Piso 7   
    4     N-1004 2023-02-25 17:00:00      Usuario_4    Calle Mayor, 80, Piso 8   
    5     N-1005 2023-06-26 06:00:00      Usuario_5  Av. Libertad, 54, Piso 10   
    6     N-1006 2023-04-18 20:00:00      Usuario_6   Av. Libertad, 48, Piso 7   
    7     N-1007 2023-05-11 00:00:00      Usuario_7   Av. Libertad, 20, Piso 8   
    8     N-1008 2023-05-21 08:00:00      Usuario_8   Av. Libertad, 73, Piso 6   
    9     N-1009 2023-01-21 07:00:00      Usuario_9    Calle Mayor, 92, Piso 9   
    10    N-1010 2023-03-21 15:00:00     Usuario_10    Calle Mayor, 61, Piso 6   
    11    N-1011 2023-01-28 05:00:00     Usuario_11        Gran Vía, 6, Piso 5   
    12    N-1012 2023-03-04 17:00:00     Usuario_12    Calle Mayor, 55, Piso 4   
    13    N-1013 2023-03-15 00:00:00     Usuario_13   Paseo Gracia, 69, Piso 2   
    14    N-1014 2023-01-22 15:00:00     Usuario_14       Gran Vía, 67, Piso 4   
    15    N-1015 2023-06-19 03:00:00     Usuario_15        Gran Vía, 7, Piso 6   
    16    N-1016 2023-01-20 22:00:00     Usuario_16   Av. Libertad, 28, Piso 3   
    17    N-1017 2023-06-04 18:00:00     Usuario_17       Gran Vía, 77, Piso 3   
    18    N-1018 2023-01-06 12:00:00     Usuario_18    Av. Libertad, 5, Piso 2   
    19    N-1019 2023-04-07 21:00:00     Usuario_19    Calle Mayor, 22, Piso 8   
    
                Producto  Unidades  Precio_Unitario  Total_Factura  
    0       Laptop Gamer         1              970          970.0  
    1   Mouse Ergonómico         4              927         3708.0  
    2         Monitor 4K         2             1410         2820.0  
    3          Webcam HD         2             1269         2538.0  
    4          Webcam HD         2              454          908.0  
    5    Docking Station         3              270          810.0  
    6   Teclado Mecánico         4              546         2184.0  
    7   Teclado Mecánico         2             1300         2600.0  
    8          Webcam HD         1              835          835.0  
    9          Webcam HD         4              645         2580.0  
    10  Teclado Mecánico         1             1185         1185.0  
    11   Docking Station         2              320          640.0  
    12         Webcam HD         2              742         1484.0  
    13  Mouse Ergonómico         1             1029         1029.0  
    14      Laptop Gamer         4              634         2536.0  
    15   Docking Station         1             1005         1005.0  
    16  Teclado Mecánico         4              752         3008.0  
    17         Webcam HD         1              794          794.0  
    18  Mouse Ergonómico         2              891         1782.0  
    19         Webcam HD         1              748          748.0  



```python
print(df_norte.dtypes)
```

    ID_Pedido                    object
    Fecha_Transaccion    datetime64[ns]
    Cliente_Nombre               object
    Direccion_Envio              object
    Producto                     object
    Unidades                     object
    Precio_Unitario              object
    Total_Factura               float64
    dtype: object


### **2. Sur (``ventas_sur.xlsx``):**
- Archivo Excel con múltiples hojas (``Q1_2023``, ``Q2_2023``).
- Contiene columnas booleanas (``Es_Cliente_Corporativo``) y de estado (``Estado_Envio``) que deben conservarse.
- Debes calcular una columna ``Total`` que no existe explícitamente ( ``Precio_Base``* ``Cantidad`` * (1 - ``Descuento_Aplicado``)).


```python
!pip install openpyxl
!pip install xlrd
```

    Requirement already satisfied: openpyxl in /opt/conda/lib/python3.11/site-packages (3.1.2)
    Requirement already satisfied: et-xmlfile in /opt/conda/lib/python3.11/site-packages (from openpyxl) (1.1.0)
    Requirement already satisfied: xlrd in /opt/conda/lib/python3.11/site-packages (2.0.1)



```python
df_sur = pd.read_excel(
    "ventas_sur_v2.xlsx",
    sheet_name=None
)

df_sur = pd.concat(df_sur.values(),ignore_index=True)
df_sur["Total"] = df_sur["Precio_Base"] * df_sur["Cantidad"] * (1 -df_sur["Descuento_Aplicado"])
df_sur
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Ref_Venta</th>
      <th>Fecha_Alta</th>
      <th>Articulo</th>
      <th>Cantidad</th>
      <th>Precio_Base</th>
      <th>Descuento_Aplicado</th>
      <th>Es_Cliente_Corporativo</th>
      <th>Estado_Envio</th>
      <th>Total</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>S-5000</td>
      <td>2023-02-11 00:00:00</td>
      <td>Webcam HD</td>
      <td>9</td>
      <td>425.12</td>
      <td>0.20</td>
      <td>False</td>
      <td>Enviado</td>
      <td>3060.864</td>
    </tr>
    <tr>
      <th>1</th>
      <td>S-5001</td>
      <td>2023-02-03 12:00:00</td>
      <td>Teclado Mecánico</td>
      <td>8</td>
      <td>599.60</td>
      <td>0.00</td>
      <td>True</td>
      <td>Devuelto</td>
      <td>4796.800</td>
    </tr>
    <tr>
      <th>2</th>
      <td>S-5002</td>
      <td>2023-04-06 07:00:00</td>
      <td>Mouse Ergonómico</td>
      <td>6</td>
      <td>971.36</td>
      <td>0.00</td>
      <td>False</td>
      <td>Completado</td>
      <td>5828.160</td>
    </tr>
    <tr>
      <th>3</th>
      <td>S-5003</td>
      <td>2023-04-02 05:00:00</td>
      <td>Monitor 4K</td>
      <td>1</td>
      <td>799.66</td>
      <td>0.10</td>
      <td>True</td>
      <td>Pendiente</td>
      <td>719.694</td>
    </tr>
    <tr>
      <th>4</th>
      <td>S-5004</td>
      <td>2023-06-17 12:00:00</td>
      <td>Mouse Ergonómico</td>
      <td>2</td>
      <td>619.99</td>
      <td>0.05</td>
      <td>True</td>
      <td>Devuelto</td>
      <td>1177.981</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>155</th>
      <td>S-5075</td>
      <td>2023-05-17 22:00:00</td>
      <td>Monitor 4K</td>
      <td>2</td>
      <td>1150.01</td>
      <td>0.10</td>
      <td>False</td>
      <td>Enviado</td>
      <td>2070.018</td>
    </tr>
    <tr>
      <th>156</th>
      <td>S-5076</td>
      <td>2023-01-29 13:00:00</td>
      <td>Webcam HD</td>
      <td>1</td>
      <td>874.12</td>
      <td>0.10</td>
      <td>True</td>
      <td>Devuelto</td>
      <td>786.708</td>
    </tr>
    <tr>
      <th>157</th>
      <td>S-5077</td>
      <td>2023-06-09 11:00:00</td>
      <td>Mouse Ergonómico</td>
      <td>1</td>
      <td>145.92</td>
      <td>0.00</td>
      <td>True</td>
      <td>Devuelto</td>
      <td>145.920</td>
    </tr>
    <tr>
      <th>158</th>
      <td>S-5078</td>
      <td>2023-02-07 13:00:00</td>
      <td>Monitor 4K</td>
      <td>2</td>
      <td>1152.24</td>
      <td>0.00</td>
      <td>False</td>
      <td>Enviado</td>
      <td>2304.480</td>
    </tr>
    <tr>
      <th>159</th>
      <td>S-5079</td>
      <td>2023-05-01 11:00:00</td>
      <td>Docking Station</td>
      <td>7</td>
      <td>261.88</td>
      <td>0.10</td>
      <td>True</td>
      <td>Enviado</td>
      <td>1649.844</td>
    </tr>
  </tbody>
</table>
<p>160 rows × 9 columns</p>
</div>



### **3. Este (``ventas_este.json``):**

- JSON de con varios niveles de anidamiento
- La información útil está sepultada bajo ``data -> payload -> transaccion``.
- Debes extraer:
- ID del registro.
    - Fecha.
    - Ciudad del comprador.
    - Nombre del producto.
    - Cantidad.
    - Precio de lista y el monto del IVA (que está en un subdiccionario).
- Debes descartar metadatos técnicos (``latency_ms``, ``source_system``).

El DataFrame final debe tener **exactamente** estas columnas estandarizadas:
- ``id_transaccion``
- ``fecha``
- ``region``
- ``producto``
- ``cantidad``
- ``total_venta``
- ``ciudad``


```python
df_este = pd.read_json("ventas_este_v2.json")
print(df_este)
```

                                              metadata  \
    0    {'source_system': 'API_v2', 'latency_ms': 34}   
    1    {'source_system': 'API_v2', 'latency_ms': 45}   
    2    {'source_system': 'API_v2', 'latency_ms': 94}   
    3    {'source_system': 'API_v2', 'latency_ms': 66}   
    4    {'source_system': 'API_v2', 'latency_ms': 30}   
    ..                                             ...   
    115  {'source_system': 'API_v2', 'latency_ms': 60}   
    116  {'source_system': 'API_v2', 'latency_ms': 21}   
    117  {'source_system': 'API_v2', 'latency_ms': 38}   
    118  {'source_system': 'API_v2', 'latency_ms': 46}   
    119  {'source_system': 'API_v2', 'latency_ms': 40}   
    
                                                      data  
    0    {'id_registro': 'E-8000', 'payload': {'fecha_e...  
    1    {'id_registro': 'E-8001', 'payload': {'fecha_e...  
    2    {'id_registro': 'E-8002', 'payload': {'fecha_e...  
    3    {'id_registro': 'E-8003', 'payload': {'fecha_e...  
    4    {'id_registro': 'E-8004', 'payload': {'fecha_e...  
    ..                                                 ...  
    115  {'id_registro': 'E-8115', 'payload': {'fecha_e...  
    116  {'id_registro': 'E-8116', 'payload': {'fecha_e...  
    117  {'id_registro': 'E-8117', 'payload': {'fecha_e...  
    118  {'id_registro': 'E-8118', 'payload': {'fecha_e...  
    119  {'id_registro': 'E-8119', 'payload': {'fecha_e...  
    
    [120 rows x 2 columns]



```python
import json
import pandas as pd

with open("ventas_este_v2.json") as f:
    data = json.load(f)

df_este = pd.json_normalize(data)


df_este = df_este[
    [
        "data.id_registro",
        "data.payload.fecha_evento",
        "data.payload.comprador.ubicacion.ciudad",
        "data.payload.transaccion.detalles_producto.nombre_comercial",
        "data.payload.transaccion.cantidad_comprada",
        "data.payload.transaccion.detalles_producto.precio_lista",
        "data.payload.transaccion.detalles_producto.impuestos.monto_iva"
    ]
]

df_este = df_este.rename(columns={
    "data.id_registro": "id_Transaccion",
    "data.payload.fecha_evento": "Fecha",
    "data.payload.comprador.ubicacion.ciudad": "Ciudad",
    "data.payload.transaccion.detalles_producto.nombre_comercial": "Producto",
    "data.payload.transaccion.cantidad_comprada": "Cantidad",
    "data.payload.transaccion.detalles_producto.precio_lista": "Total_Venta",
    "data.payload.transaccion.detalles_producto.impuestos.monto_iva": "Iva"
})

df.head(10)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id_Transaccion</th>
      <th>Fecha</th>
      <th>Ciudad</th>
      <th>Producto</th>
      <th>Cantidad</th>
      <th>Total_Venta</th>
      <th>Iva</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>E-8000</td>
      <td>2023-06-29 00:00:00</td>
      <td>Sevilla</td>
      <td>Monitor 4K</td>
      <td>1</td>
      <td>503</td>
      <td>105.63</td>
    </tr>
    <tr>
      <th>1</th>
      <td>E-8001</td>
      <td>2023-04-12 00:00:00</td>
      <td>Sevilla</td>
      <td>Webcam HD</td>
      <td>1</td>
      <td>1122</td>
      <td>235.62</td>
    </tr>
    <tr>
      <th>2</th>
      <td>E-8002</td>
      <td>2023-04-20 00:00:00</td>
      <td>Sevilla</td>
      <td>Webcam HD</td>
      <td>2</td>
      <td>994</td>
      <td>208.74</td>
    </tr>
    <tr>
      <th>3</th>
      <td>E-8003</td>
      <td>2023-04-14 00:00:00</td>
      <td>Madrid</td>
      <td>Webcam HD</td>
      <td>2</td>
      <td>1255</td>
      <td>263.55</td>
    </tr>
    <tr>
      <th>4</th>
      <td>E-8004</td>
      <td>2023-01-03 00:00:00</td>
      <td>Sevilla</td>
      <td>Monitor 4K</td>
      <td>2</td>
      <td>1458</td>
      <td>306.18</td>
    </tr>
    <tr>
      <th>5</th>
      <td>E-8005</td>
      <td>2023-02-24 00:00:00</td>
      <td>Valencia</td>
      <td>Teclado Mecánico</td>
      <td>2</td>
      <td>475</td>
      <td>99.75</td>
    </tr>
    <tr>
      <th>6</th>
      <td>E-8006</td>
      <td>2023-05-14 00:00:00</td>
      <td>Sevilla</td>
      <td>Mouse Ergonómico</td>
      <td>2</td>
      <td>498</td>
      <td>104.58</td>
    </tr>
    <tr>
      <th>7</th>
      <td>E-8007</td>
      <td>2023-02-22 00:00:00</td>
      <td>Valencia</td>
      <td>Webcam HD</td>
      <td>2</td>
      <td>1255</td>
      <td>263.55</td>
    </tr>
    <tr>
      <th>8</th>
      <td>E-8008</td>
      <td>2023-03-27 00:00:00</td>
      <td>Madrid</td>
      <td>Laptop Gamer</td>
      <td>2</td>
      <td>668</td>
      <td>140.28</td>
    </tr>
    <tr>
      <th>9</th>
      <td>E-8009</td>
      <td>2023-03-22 00:00:00</td>
      <td>Sevilla</td>
      <td>Docking Station</td>
      <td>1</td>
      <td>933</td>
      <td>195.93</td>
    </tr>
  </tbody>
</table>
</div>




```python

```
