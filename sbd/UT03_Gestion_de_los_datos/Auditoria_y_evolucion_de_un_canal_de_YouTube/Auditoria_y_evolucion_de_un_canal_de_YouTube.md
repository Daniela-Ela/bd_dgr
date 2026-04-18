# **PR0304: Auditoría y evolución de un canal de YouTube**

## **PR0304: Auditoría y evolución de un canal de YouTube**

Vamos a seguir practicando con extración de datos de APIs. En este caso usaremos la API de YouTube para

## **2. Pasos previos**

Para esta práctica necesitarás registrarte en la API de datos de Youtube. Aunque los resumo a continuación, tienes toda la información en esta página web.

Los pasos a realizar son:

### **Habilitar la API**

Vete a la Consola de Google Developers y en Habilitar APIs y servicios busca la API YouTube Data API v3 y la activas.


### **Obtención de credenciales**

Ahora debes crear las credenciales para poder conectarte a la API, para ello busca el botón Crear credenciales donde seleccionamos Datos públicos

Tras aceptar, ya tendrás disponible tu clave de API en el apartado Credenciales.

![imagen.png](677bfb64-37e7-4404-9fe7-e850cb1436e5.png)

## **3.- Objetivo de la práctica**

El objetivo de esta práctica será, a partir de un canal de YouTube, ingerir todo el catálogo histórico de vídeos y sus métricas actuales (vistas, duración, likes).

Algunas cuestiones que tienes que tener en cuenta son:

1. Navegación por la arquitectura de una API: en esta ocasión no vas a tener todos los datos en un solo endpoint, sino que deberás: primero buscar el canal, luego su lista de videos, y luego las estadísticas de cada video.
2. Manejo la paginación: tendrás que usar tokens (nextPageToken) para extraer listas que superan el límite máximo de resultados por petición (50).
3. Peticiones por lotes (Batching): algo importante aquí también será agrupar IDs para no agotar la cuota de la API (hacer 1 petición para 50 videos en lugar de 50 peticiones individuales).
4. Limpieza de datos (Parsing): y por último, también tendrás que transformar formatos estándar (como las duraciones en ISO 8601 PT1H5M33S) a formatos numéricos útiles para el análisis (segundos).
5. 
Los endpoints que deberás usar son:


```python
import requests
import pandas as pd
import math

# CONFIGURACIÓN
API_KEY = 'AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg'
CHANNEL_ID = 'UCo4k7uMo-JgnNaP3TbKT2Zw' 
BASE_URL = 'https://www.googleapis.com/youtube/v3'
```

### **``Channels: list``**
Este endpoint lo usaremos para obtener el ID de la lista Uploads. En la página de la guía de referencia tienes una relación de todos los parámetros que puede recibir, pero los que necesitas son:

- ``part``: para indicarle qué propiedades del canal queremos obtener. El valor en tu caso debe ser ``contentDetails``.
- ``id``: con el identificador del canal del cual quieres obtener la información
- ``key``: tu API Key
- 
Fíjate que tendrás que navegar por el JSON para obtener la clave que nos interesa (``uploads``)

![imagen.png](0cf7e802-a95d-4a10-b011-2d159c666f55.png)


```python
def get_uploads_playlist_id(channel_id):
    """Paso 1: Obtener el ID de la lista de reproducción 'Uploads' del canal"""
    url = f"{BASE_URL}/channels?part=contentDetails&id={channel_id}&key={API_KEY}"
    response = requests.get(url).json()
    
    try:
        # Extrae el id del playlist (está en la clave uploads)
        playlist_id = response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
        return playlist_id
    except KeyError:
        print("Error al obtener la playlist. Revisa el ID del canal y tu API Key.")
        return None

resultado = get_uploads_playlist_id(CHANNEL_ID)
print(resultado)
```

    UUo4k7uMo-JgnNaP3TbKT2Zw


### **``PlaylistItems: list``**
Este endpoint servirá para obtener la lista de vídeos a partir del Id de la lista uploads.

Aquí lo importante es que no te mostrará todos los resultados en una misma página, sino que los resultados los mostrará de 50 en 50, por lo que deberás gestionar la paginación. Para ello tienes que comprobar la clave ``nextPageToken`` y, si existe, quiere decir que hay por lo menos otra página más de resultados.

![imagen.png](51a60be9-753a-47db-ae41-4bd9b061a965.png)

El objetivo aquí será obtener un listado de todos los Ids de los vídeos de este canal.


```python
def get_all_video_ids(playlist_id):
    """Paso 2: Obtener todos los IDs de los videos de la playlist"""
    video_ids = []
    next_page_token = None
    
    print("Extrayendo IDs de videos...")
    
    while True:
        url = f"{BASE_URL}/playlistItems?part=contentDetails&maxResults=50&playlistId={playlist_id}&key={API_KEY}"
        
        # Si existe un next_page_token, añádelo a la URL
        if next_page_token:
            url += f"&pageToken={next_page_token}"
        
        response = requests.get(url).json()
        
        for item in response.get('items', []):
        #for item in response.get['items']:
            video_ids.append(item['contentDetails']['videoId'])
            
        # Lógica de paginación
        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break
        
    print(f"Total de videos encontrados: {len(video_ids)}")
    return video_ids

playlist_id = resultado
lista_ids = get_all_video_ids(playlist_id)
print(lista_ids[:5])
print("Total:", len(lista_ids))
```

    Extrayendo IDs de videos...
    Total de videos encontrados: 5115
    ['KHoGMBbuC2I', 'UF2j6HtrTPs', 'g3Y9p-AL_Ok', 'sGd-nzPlhi0', 'N3_hNiD06D0']
    Total: 5115


### **``Videos: list``**
Una vez que ya tienes el listado de todos los identificadores de los ids de los vídeos del canal será el momento de obtener los datos de cada vídeo (título, fecha_publicación, vistas, likes, comentarios y duración ISO)


```python
def parse_duration(iso_duration):
    """Paso 4: Transformar la duración ISO 8601 (ej: PT1H2M10S) a segundos totales"""
    # TODO: Convierte la duración de ISO8601 a segundos
    if not iso_duration:
        return None

    m = re.match(r"^PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?$", iso_duration)
    if not m:
        return None

    h = int(m.group(1)) if m.group(1) else 0
    mi = int(m.group(2)) if m.group(2) else 0
    s = int(m.group(3)) if m.group(3) else 0

    return h * 3600 + mi * 60 + s

    return iso_duration 

def get_video_details(video_ids):
    """Paso 3: Obtener estadísticas de los videos en lotes de 50"""
    all_video_data = []
    
    # TODO: Agrupa la lista video_ids en sub-listas de máximo 50 elementos.
    print("Extrayendo estadisticas de los videos")

    # Este bucle simula el procesamiento por lotes (debes adaptarlo a tus sub-listas)
    for i in range(0, len(video_ids), 50):
        chunk = video_ids[i:i+50]
        
        ids_string = ','.join(chunk)
        url = f"{BASE_URL}/videos?part=snippet,statistics,contentDetails&id={ids_string}&key={API_KEY}"
        print("--")
        print(url)
        response = requests.get(url).json()
        
        # TODO: de cada vídeo, extraer: id, title, publishedAt, ViewCount, likeCount, CommentCount, duration
        # Guardar los datos en un diccionario y anexarlo a all_video_data
    for item in response.get('items', []):
            snippet = item.get("snippet", {})
            stats = item.get("statistics", {})
            content = item.get("contentDetails", {})
            
            video_dict = {
                "video_id": item.get("id"),
                "titulo": snippet.get("title"),
                "fecha_publicacion": snippet.get("publishedAt"),
                "vistas": stats.get("viewCount"),
                "likes": stats.get("likeCount"),
                "comentarios": stats.get("commentCount"),
                "duracion_iso": content.get("duration")
            }
            
            all_video_data.append(video_dict)
                        
    return all_video_data

datos_prueba = get_video_details(lista_ids[:50])
df = pd.DataFrame(datos_prueba)
df.head()
```

    Extrayendo estadisticas de los videos
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=KHoGMBbuC2I,UF2j6HtrTPs,g3Y9p-AL_Ok,sGd-nzPlhi0,N3_hNiD06D0,dsYF8R0c324,oNLCm2l2vgQ,MiyC6KrVKm8,31zCBiIK8n4,3ljv74T31kA,mQiIRS-yHfQ,JQ8pOYB55oY,L7Mcpt_s1rY,EfGpSfChYE4,Ph5eh-Wo8cc,XYfqg1S_YpU,uTyvk8filnw,4xByhaDTA3w,uhsl95AmDCM,ISWmlua5lnY,ndJa4lmoqQ0,vbTg7igr5LQ,rN8INAdtHR8,ejHSHrsG34k,UlpQXeFAbr8,L8cfR817vSE,qd7LPx4fqn4,ucZFD1lZTjQ,jnY_-B-jTd4,HLSVBQKtQhk,NscT8lrbuDo,HxLGDvL-l_8,njiHa4N9lys,fNAZBxCn870,dTRGfA83hic,FV0PwPxIVME,0Jauu5JNSqs,5F6n5LrEfB4,Pjg4-Xh8B5o,K2nLgTTGAoY,HP0GEgnup7Y,kweQ2g_ynMA,stV3JwPSukI,lqrn8DKhCPA,phyKDIryZWk,dLOFceBtX-0,_5svzNz0HV0,ptaFGOo7EO0,hiJibcC-O6s,GtCFq7f6o2k&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg





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
      <th>video_id</th>
      <th>titulo</th>
      <th>fecha_publicacion</th>
      <th>vistas</th>
      <th>likes</th>
      <th>comentarios</th>
      <th>duracion_iso</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>KHoGMBbuC2I</td>
      <td>EL MISTERIO DE RESIDENT EVIL 9 REQUIEM RESUELT...</td>
      <td>2026-03-04T20:16:48Z</td>
      <td>349594</td>
      <td>18390</td>
      <td>191</td>
      <td>PT1M23S</td>
    </tr>
    <tr>
      <th>1</th>
      <td>UF2j6HtrTPs</td>
      <td>HE JUGADO A CRIMSON DESERT Y LO DE ESTE JUEGO ...</td>
      <td>2026-03-04T14:00:44Z</td>
      <td>156597</td>
      <td>6564</td>
      <td>790</td>
      <td>PT16M33S</td>
    </tr>
    <tr>
      <th>2</th>
      <td>g3Y9p-AL_Ok</td>
      <td>RESIDENT EVIL 9 REQUIEM - EL MAYOR SECRETO DES...</td>
      <td>2026-03-03T21:15:03Z</td>
      <td>108540</td>
      <td>5047</td>
      <td>311</td>
      <td>PT14M16S</td>
    </tr>
    <tr>
      <th>3</th>
      <td>sGd-nzPlhi0</td>
      <td>RESIDENT EVIL 9 REQUIEM - MODO LOCURA (MENOS D...</td>
      <td>2026-03-03T17:01:32Z</td>
      <td>86107</td>
      <td>2987</td>
      <td>187</td>
      <td>PT2H39M35S</td>
    </tr>
    <tr>
      <th>4</th>
      <td>N3_hNiD06D0</td>
      <td>RESIDENT EVIL 9 REQUIEM - TODAS LAS MEJORES AR...</td>
      <td>2026-03-01T22:00:31Z</td>
      <td>126284</td>
      <td>5144</td>
      <td>261</td>
      <td>PT15M48S</td>
    </tr>
  </tbody>
</table>
</div>



## **4. Almacenamiento de los datos**

Por último, una vez que hayas obtenido todos los datos, deberás almacenar el dataframe en formato .parquet.


```python
# EJECUCIÓN PRINCIPAL (PIPELINE)
# ------------------------------
if __name__ == "__main__":
    print("Iniciando pipeline de ingesta...")
    
    uploads_id = get_uploads_playlist_id(CHANNEL_ID)
    
    if uploads_id:
        lista_ids = get_all_video_ids(uploads_id)
        datos_completos = get_video_details(lista_ids)
        
        df = pd.DataFrame(datos_completos)
        
        # Limpieza básica
        df['fecha_publicacion'] = pd.to_datetime(df['fecha_publicacion'])
        
        print("\nMuestra de los datos extraídos:")
        print(df.head())
        
        # 5. Guardar en un formato analítico
        # TODO: Utiliza el método de Pandas adecuado para guardar el DataFrame en formato Parquet.
        # Nombra el archivo como 'dataset_canal_youtube.parquet'.
        df.to_parquet("dataset_canal_youtube.parquet", index=False)
        
        print("\nPipeline finalizado. Revisa tus archivos locales.")
```

    Iniciando pipeline de ingesta...
    Extrayendo IDs de videos...
    Total de videos encontrados: 5115
    Extrayendo estadisticas de los videos
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=KHoGMBbuC2I,UF2j6HtrTPs,g3Y9p-AL_Ok,sGd-nzPlhi0,N3_hNiD06D0,dsYF8R0c324,oNLCm2l2vgQ,MiyC6KrVKm8,31zCBiIK8n4,3ljv74T31kA,mQiIRS-yHfQ,JQ8pOYB55oY,L7Mcpt_s1rY,EfGpSfChYE4,Ph5eh-Wo8cc,XYfqg1S_YpU,uTyvk8filnw,4xByhaDTA3w,uhsl95AmDCM,ISWmlua5lnY,ndJa4lmoqQ0,vbTg7igr5LQ,rN8INAdtHR8,ejHSHrsG34k,UlpQXeFAbr8,L8cfR817vSE,qd7LPx4fqn4,ucZFD1lZTjQ,jnY_-B-jTd4,HLSVBQKtQhk,NscT8lrbuDo,HxLGDvL-l_8,njiHa4N9lys,fNAZBxCn870,dTRGfA83hic,FV0PwPxIVME,0Jauu5JNSqs,5F6n5LrEfB4,Pjg4-Xh8B5o,K2nLgTTGAoY,HP0GEgnup7Y,kweQ2g_ynMA,stV3JwPSukI,lqrn8DKhCPA,phyKDIryZWk,dLOFceBtX-0,_5svzNz0HV0,ptaFGOo7EO0,hiJibcC-O6s,GtCFq7f6o2k&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=QuQvVymwjAU,6KEthdFDPLY,ZtfTwp-2gHM,RFPHkpmC6jE,U0y0IDTyQd8,pKsMOfG5EuY,jpOw0gc2jYY,Xv3RiKwypgs,7WsrJFSHAN4,cmYduBy4fMc,adpIcYoyg0Q,YdY1ym_Qua0,mNEqw2R4oVM,sZdTCp6d8s4,wxqcoHJfQX0,K8L-6sQcnuA,RXSIj8JJtVA,CFqpK92sST0,Ptdhhs6F-qQ,SgEy9YZZrWQ,w4Sm3asDUhk,pAPGZgcfH1M,lgwR9HtKPPk,yD-MbtqHvpM,XVLivnVC5cM,qnnOFhhnep0,fMsZBuCSIBY,IW6xfMiiC5E,klPWye7IeMQ,9pk0SHYPK5U,t5blTqR7JeA,lnfrejrsts0,L1CHeNq6zcM,dzN9OqlFcr8,a16zyOQo7ss,QY8jIlc_ycE,5SayqkF0JWc,D5ZrsdMibyA,1GuvLiTg_E4,-1za5VFLfyw,m-X8jjDq1UQ,UIJE13zutNM,cQgCiT1AhKs,I1P30F_2WE0,07BhP3xTJNE,0qCAKBHY9ec,wH1mYj5r2BE,tXIivqLQr0g,PrU34_eWo6A,Ig_fR9-tl_Q&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=q3UGe-QDly8,-vXPf1FKzFQ,it67YKAqWwI,YidluQdmdHY,pcY_vKhazMo,8VVqL9H9oZc,gOK_73EjB20,V7I6Cs19-TU,mwnI9V00SLc,fj-1u1NCFsM,GZ0unFDoyig,GFCYZcPejyY,6HBZmGdOQLo,tu3oy3zjD-M,_mlFTN9rKt0,GoPGMO3l7sE,bn3FyVXMe-k,Jm76xpEcZww,vFeYOt8FCJo,NHqzdhpvwkY,a5vak27bh2E,swuqo2Xs5Fs,rw6nuFw_Y34,nUaChYJ5xcY,qCZ7ev0x--g,wTiVm01_Npg,dSs8eHF-KVo,rWZxiytrTvg,1urQzKHyZ9Y,mM3NxxPjEyU,TANbFN93oJs,AhKEKJ4dLnY,lfHoPdqn3nI,YkT_MQLyEpQ,nrEq9kl5bvw,xx1EAFzSo38,uGpaE56B8zA,ZYfm-_3aays,XtkgOKQGkMA,SW_LEqFAPQQ,BlS_aEqUIV8,bKDrsyaKB-Y,mGYnU-bNxcs,WJpslvieYZk,JgV4cpt4nAg,DYkNW3nIkq0,mVd_rG2rNSc,22M8DmjJHlA,Q_EAZmImDAQ,2USq6fLTqT4&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=RmeOdMIbEVc,_Ft7BRj0QLI,E0rLMcWoSj8,h00yhvJRe_w,MosonCsoKbU,L4DQyW3j4U8,7mWVH9Vx6e4,wKbrzWDq1dk,IggsBOltlXk,F0cYtIeZQQE,7Y9wvAFW9H4,H3FXGkragdw,brXhOgUSuhM,TCGj4bUNziM,qgZbKcwB9v8,zM6Ss1U9uU4,C8DxWzIjIko,4GaCMqpIY2I,iWKtxgEL3og,Z-Sr1Nc3mPw,QZtT0tFhk0g,d28eL0Oma_s,3Issty2M7O8,PngEl7Utz1g,EQ83xUWPM94,JLcXB7wjYH4,eciUSKhWCE4,vCmlcftP0_w,gMcjMBBQXlk,0TjeQtOqQhE,ySRD6VL3DgY,u-V-PVeLTDU,Yo4U6Qn4BVo,HL1pAZsHFjg,oUqNCwQ0CIQ,hIAo53XaAjk,OTLG3YOgWIE,fbY1beNzmyE,849aWTRB2QE,jPbwzmKTlfw,APuYQEyK0cQ,RVvov1jNKwo,k_1mrPnMfmo,DufDUcWABt4,s6Dfs_OhO9E,VISDfNK8ttY,NGFUoXC2Bnk,jJfd2ckiipo,CybqZp9JVxw,DQXLN5_rXbA&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=d-a-_lU9Ky8,RneMy9Z5K6o,_P60o9WXG8s,o8xM3SK74yk,J7L64Y6szGg,GMZ6sLdmQAA,PmdtL0VLcbc,waRDUjbQeTA,bPeMDBgY_4A,2CA1NHZg-TY,Kkxx32Q4hWM,ahoTz8dXb0s,NzG7hkSdvQ4,LGF0pBu6YvQ,SO9j4sakfgQ,8SOf9wpS2z8,jasaFJulASk,AX7Xk9SMbOI,97e5lUSSTPU,dAyQExX4rnw,NwsSa6gx3Qc,oylxAumZK9I,6wwKUeQNXOM,-59x2T4tnRU,8n57pFtFAqY,WzbG4cBPQBQ,PH1ojvHA6Ls,d7Dq0xjtapA,r-02fZSylWE,0bILAVvRh1A,8i3Xulau7-Y,oh82A7gDlYQ,ER5hp7D7_QI,wsZFy0nmV0k,IXQesxV5L50,LIZq0tyPAjQ,ejEEPzGaoUY,gFNuxlnsCb0,1vJ8gOiC7LI,zmGdwR1gXLg,KI0l6XDffiM,ZDisbrlq8gI,WIqcR2xk9as,MM_2O5ckxH0,DWO3qsVzwC0,nzqdKvtVeAs,80OL5PUx7mQ,JXwEFHhW4yE,0n3yewMd3W8,hm22SCiV0HA&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=1GmrOOGYOhs,rksQ2Hmiy2I,4tU2HR3HXZs,r99FBcBoDWQ,ojkNBIOQadg,hHIV_RPJBKY,PSRxuDJqCnk,GWRdkJ8W29U,o70r4FoQgHA,UHzELlH9_fQ,x4P4ui42FDA,GGY-7I2na6g,8DzI00lZ_4Y,-8Er7eMuETc,GfHHten0xFs,bex8KfQ4Gws,K_H1eZ7M4Qc,-a9wRySnkPg,hNrfK8BT_GY,81NWu3u3_vE,qmZCOTQ1Ln4,GDhZlmCK7Vs,bS7-Mz4t6AQ,eNeWE_LQ57I,X8Xgi0c8Wk8,0rYmr_W_49I,Y11HUV6yCX8,-1bm1IgT5oA,rI_W7ECpt8U,4UbHhwArBFo,aA1uOJFyaZY,EuDZySgzLtI,yl8Xubet45I,B42hu8tP33s,YRi6i086FfA,wCn2E9PXPwg,iQVP_g9mGlE,LqMTaJKch3k,nwcZ5iSGxzM,PvcYtWnZxzc,vmqh63LftqI,4NlwcSRkHBA,myApAY_W3es,1Unbma2ScxU,B3q7bZSt7WQ,MEbsvCL2zrI,SyweUaIkSPQ,PItF86OjXNI,OI_LplJNATk,ri59cVxci4w&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=i3F4MAv4Yz8,FLjsg3GevuA,DZNKGr5J5-k,qiyitcSSFro,K0bM1xLFvWo,yTcJzYoAxzw,LqOj706bX3w,vGI-1kp9xE4,4NOUR9w4WuA,OL8iixOtqso,H_Qu8ZFvfMQ,bJ8OHND41BE,guvywELGUKY,9KOedq1oKFM,mMKoBBG8U_8,MIGnBur7q_Q,XcZ9UYoAGUs,sa7_jJJlmu4,yvWLtZyRdng,wo4sc1OCbyU,FzqUsCt6SfU,t7gEdctVKBg,qolHSoCwnJE,YGCICeTTj3Y,NP0_8XmumGc,-WWoFXer09E,Bqli0AVMP3M,ZPwlWuX_fXA,p8QDqPU8lc0,w-LD47P0nCE,VvGp52Z-7d4,eb9iCZIRk2w,K-ESJ8KLMvA,vT3f3tG8rdM,9MxEpIEBHoY,wWOKZnbeg9k,WjGU-SGUbsE,haI26VfqNLo,kM8rMm9OQGk,9piY7tGusyc,JJUhseuBRwU,5CIeatag7vw,1ziyeHU6Lq4,80P2aeCuZxs,l71NuYJRwgQ,QL2M15LI9Ww,5RaGi5v5X3s,lgiPnDH__KE,ogrwkWRcIGQ,5pRood_47LM&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=WwppAX71pMU,G4wWGmZ6Gck,iQ3xtxNirs0,ZZSEqceVwM0,6DOupMb_w4U,rt25DonlmZc,VgkYSbnOX6Y,uxVr7wXnjCg,tSQL9uE_40c,ALQyHxN9iCU,DFZ3yBoi9B4,_zkvv0xjdGE,DqPMnT5s9So,d43DZO_eNi0,VwSArpTqIVY,mzqfIRnCM5U,TGWhfl9MJqc,HMONk5GBLfU,dd90mICWuDs,Cmo5TgheEFE,rawFCDat_gI,noNdwKhmiaQ,ew6zc_K2-oE,aU8I_2138Mo,P5eDNloHrcY,obbOTRk6hrI,5LCTzQz43j0,1406i8mwjy4,DY4fJR6PqHA,7U4JYdpHj3Y,od-tyylb-Ng,0pHVM3AFf5o,57uC1yv6pzc,jOO6FIGP2Xk,2n8vr2PXYSY,B4_-FRIE4ro,4ZrDpkR-Hjs,48QmsHOADYc,29EtG-6IezA,ggbGoRTT0CU,8C54gejK9sY,g1-k7OAXVIs,mzdV3XKbYdM,QP1-HEZzkhE,_F88h6D2cTw,hkv_PijehnY,E9X9UZHpsuY,S0r4qQ3q0vc,00NO9T5oKw0,27L9YXibswM&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=x1cVM4R-GC4,D9nLgsS_gkA,Vgr-MdK-sXs,y5dxkVrdH7A,lC_iJyuD-10,VXDkk3hZL3g,0dKZB-zTlJg,hSKdDPBTrnI,zDYuaPdDoZ8,rTcx8TkBqXI,37NYevAOQh8,yrQKWNgnF60,u4cRZiRpGDQ,TrC9QjGrs2M,XxCTMKE7S4k,sl_l8t04p1w,X86MvXW1SwA,lpLCp-CzfS8,e2vSqfaA2BQ,0vBNqEo0oIk,uOTzpnW0Mo4,4p7Bc29aj9E,frQqcB6YUNk,vp1atDqvfGM,ahL4MSNoNhE,1HGlJlN6h5M,wiRuoDaH0rU,kqBIFtiTQgg,NjbwSGTmHNc,i3YQNeF6URc,4-JFWYwBXs4,XOifF-RQvFw,NVZpwD9uNs0,4RuYcCS-SPU,iHD20eabpHU,r16FFrWloWc,AwHPj3vWyZs,XXw3bUVoAP8,f7WFkbo8Ivg,icaPfSII3_E,X18chpWA9cY,FWIl45fWDpc,6yFwTdv9dBw,VHoNebQH_2k,EYkcdVFPLCs,xMTWejHd0_I,A-9J096XmIQ,PjLXEqeye7A,wLzRG_rUDIs,pPyQgjdXCGY&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=825fdaKSz3U,_IzXLKJ8D88,6Dcn-uqEMwY,33N2bmtQl6o,6nBXGo-ZB6E,TvrhGf4127E,g_7VLSmss6M,tJlbbyqqxZ0,laspbtEl-y8,T46J2bvTJu0,HJmHH1QemUo,nXWSPAXdEUw,Qy4Uz3gLnP8,A6UGJriaXgg,x2k3j6lv2jg,R5ym0n6NFqc,YA07Iq8wLfY,Rcj0dwzYh4w,zaDlKFcj4sU,2p5h24YwGnA,xmUOu6kWVWc,-b-BsoNSr4k,KB8RCmAX5XQ,uxw-QJAl0Xk,uncNqUunSw4,L6GA7nmqj74,rVWH7DnyERk,tk3nxXxA-yM,CeGEwMuQYFE,MS0OaK30-H0,lzrrm2iE-Hw,t_LPETH_dUE,Trj9TGleAzU,oLFlyGKYO0c,6BB1v5etbKg,pGAqCDkAk2A,uRu1m8TuU_o,MrF-sD7fLOE,UVxSFqncJG8,4FG6FbORapo,wPC4OGiMbmQ,Kx08JQTbZEg,V-DkLu7Zeug,cyvKUuD3vNw,a_B1BY4ba0s,2k47Axd3QB4,4B7j6Q2nIh8,WBZ8rEK8F0E,UEVr5jUCOpw,CvBROdMe3uY&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=Jzh75BldaW0,3i1grifrB-s,Yl8VqZhWT8Q,yf8eQiJLxAw,0MHXPc4BcBY,_-AsrvtKo_M,NFTj30ynbac,1iZSIlkMuI4,dDh4uwUPBuc,8-R75sNroKU,bXp2i4YUsZA,8RzPghWhDzI,7j2j5VupA8Q,lTEpEYqTEPM,Xw_QQGfi4PQ,G_9ukdjjYK4,Aop-WbfsUjY,m-rQtKt54r8,Zg6W-I0QZ-U,ZPmmOy4dcI8,ILdDcbux7zc,hqtdUndd6HQ,qR7a1JWwaj8,l7RWBAKuhR0,zbjrkUtkXVk,8VTl5HqpXbM,NGg_ZecafNA,HGq-gCjOLfY,PJe6AelXuy8,QOen2yusBE0,CkJZB82j1b0,x0-AGNOyelY,HBXUM0tiZXc,ISFBmnICe3A,E1oZ7iCmV6A,XutCtyeau7g,LN6ZGhISZn4,LyqMQ9lJjaA,fFmnDNaHbr0,_N7t09mSdwk,amTwApLLoPE,eqmOyieWQ30,fq93sdN7C8g,xP9zESIhn2k,Aggudyy9fL0,Gi0RKJS0yDg,Gl_GA6-ObTU,y8D0JBWPVcs,aemvN4fW3ng,DlbkDSFaBd8&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=Fz1wnABUrR8,-XXRZU4cb4o,5A9W5OxweyU,6Gd1LXasnYg,Bq-E2kzbm-8,mq83Qa8r-tI,qVtD4zpgmUA,EyprFrNtu0s,Q14VtqBWnSw,tQq7Ss8tybs,ri1Jvy9BfNQ,9EgFBjzNtRU,H_xXEtKc664,G8KRCfwlDUg,lFlT9i4zhQo,V_jJT0ejLts,CpVQ5eOQEjc,5OKZnW3vVRc,oJ5f8BK0jKg,Ey9ROL7Zjos,BzacfHYdnCw,Z32pOIx3CQc,11Ghxm6zHdA,A5xGp9XGb6U,N7-GJJa70Jo,jiSTkhjgi4s,1Mjqk1TQzHo,jcgwJ_fCamw,0I7fYU22lg8,oUKWavDWL1c,6Kk_rz2VIMw,Xv9OSaQhstw,6wvQmMGSliQ,wKnOMEvvd38,6cmo6d6khto,i3hMIUs-GXU,xpPLTxx94Wk,Q4w_iJqr1Tk,o3LnBB38Q-E,Ll_3vbUSvXs,OoHILyh_yz4,VKT3CKSA-l0,u8xj7RJW53c,g_eQn5rKrEs,luLZTKXOsK4,M1sCrwRmCO0,jwL4kmw-wiw,Nmo12g55W8Y,syCQFzvuInw,MtElg-pwEww&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=cu5NEXVuF34,6rGAp0-vVaA,nNIZmPb_iJo,poq7aiX0cr0,1k8zxwmhHfQ,VRC6UODlPVI,je8V08hT8jI,fDMMSggJ4-A,Mz8zfmuTtX0,8cBfgCpLLpA,YoWWixDLOMA,4WWCmZbRCJE,KL57jLso3Po,NrnIP-Wkrf0,ysHwjFXBI3Q,2pl728r5TgI,xKj0IoRyycI,VNtRsaIaYfs,Xzlsi3K4-ws,-RbN9pH8Ihs,iHzs1cF884w,Dcre52r3R1Q,5jxYof1v9nc,epAjo40UUag,GulW4njG5bY,qg1K5YLimko,tP0xpZcbTJ4,uvqCHbxlEA8,Xr49nCDbpiM,LjitwmjK9qM,54-4eGHI8yA,Wx4k837urBg,pgeyhwB00Nk,X1I-7bTlqlQ,m_4oQiUvIAA,4ofT8UPKH_c,x8RQm-K3mZI,84US3Le1PwU,jpiAawMBaK0,kEZishd5ebE,3OHfJuu_mG4,sqyk2S7edXg,-lVwmm9bIAk,FpUxQvgpgKs,gCMZ5keKD-k,imbPuhSbebI,7ZV_aPmcnSA,gGtOQIoTWPI,CEVMJoidjso,rAnrDZfjPzs&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=UFEovzu7-Gg,2tHB9p5G1Dc,2DUWAPBuax0,G4XF4DFktu4,Qvs64yxLcOY,5QB7EyifQFM,IsxRlDlR4to,IUTWZZ2laNk,8zsFAZVLKyY,Et-1pQV0SlM,R53n6fjACbo,IEtWiqrVKiU,kEI8nYhCnBQ,QzDkJ3THjvo,a_apMDagzg0,k6lKdbOvOLQ,QQ2QhNc-8WU,v4yT_RO7DQ4,Q5FBQq_P89c,AbUQfw_kvWk,frPDi1zGiJs,jzh2I7J75_Q,baiCTIHJpsw,qY8pDFtVgSY,S30QmRt2VFE,HSfbvjGnPM8,zozg3r72mQQ,-Eg3TjHxjps,T780BBL0FlE,jONIWIpc-j0,2t7yaMpbHMk,QecL4OGGnWo,GbwHTlyFCXE,MQMSLjf9qOc,I2iW3qdAwyg,20uzDESIObA,b5eeUxq5gr8,PPHUHEZH3DA,hTw1YUyPdsY,oX-_yKRTrNs,AD91jKsxeoE,hu4M-H8R99E,DtzRPUoITmI,HQQL8TWF72k,lP_ILtz08oE,HtBIzLcR0ww,sU0P8vl3PGg,fBWkqADz3Tc,K6CE-J8pUWs,6_xAnQpDMAw&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=XWRuy2JOMAw,7Zdd0oNdwg4,PJU2UK-EXDo,U1lmku-CV2A,fKmsKov4Pvs,od1Y7jNAJD0,woIOpkoaw70,WIzv76FfwtU,IzFqxeGHgM0,FkcN-DDnrfo,VUCTlbA0BG0,j-7-FggajGY,_4rmh_gZ5zY,V0lUGM35nPw,mp_B7MgTrgA,8Psfo1BBD0Q,NN8sdvKMSWw,weWvdPJAzOE,Ek1Ifh8Q3bk,KXjKhsL0z2o,yUTZ_0EmImc,k84ZZTrTlM8,Y6PSYhcnQss,E8MXTahu99Q,cJ43RDO91pA,bJzDzdtf8IY,PeSYmuVhgbQ,_Crwoydrh2A,EcsMWF08Ywg,j78jyCczidg,j6v1qbu5Xa0,QVz7_3Wy6mE,yooXOvtrDUs,9FXrA44mwIw,KYdjghhvAj0,RkN7PISx0qE,pYlSb8CT6Uc,_x0wN0_2zMA,PmEFUx6H444,WVj-IecBY1o,aY368iVvmfI,dPe_xN39UbE,QKPahay-yv0,Jedv7wMEBpU,kTSzylwtcsk,rWxzNk5r3g4,S8ZXG8AGEEE,U_iOkO-0Tnk,j-6ubQTSf6s,9NICJ4q18jA&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=V283MuANV_k,2WA7biDYWDY,LpQitCE6tPI,tXWClGpq4t0,4Ap2as9c390,1fhgMvyL1J4,cLv9V5PcS5E,MRHVko92IN0,rPIpvsRUkko,0fKzdXcrnbU,MNAMg_NsMho,BNMqt5v_adg,ePd8kVLTA4Y,dehhNj8YtNc,9Rgb3RszY1Q,I9J4A1mimZI,3AMXZI-nYt4,Jarpd1NpETg,CgZBYbxoM7A,ulWY6DmOYUU,P1kT_fHNdck,LgXoXpfd7m0,fKsMxgqgHSM,K_wkpJ8lcfw,iKtOMtGiCrM,Gdsbf8HraZQ,PdOrvOLIUIk,0uhZloeinJQ,x4HosI1Rtzg,HqO0ZwujLUg,HQXogyhmSKA,fEBS-2kTBd8,Tfg7krqzcrs,r6Vn6cF0lc8,nr69FjoUi3I,zX-xoIJ7-jI,sNKuBSVRZkc,Ult0qWQDxw8,ehDzHSTSXeQ,oI6PsWkxGU4,7C3Do2sxIcc,WAg965t-QUU,0VVo0en2qvU,rbUJH1eqcVI,2JiasLCRjVk,45cRN2id6x0,bfH8tfW64Jg,vdL94J40WUg,VoLj2v_gpj4,dMNrPBBsi0Y&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=wj3pz8lxDY0,35gUPQVOBtY,mBLeEl5S--Y,8QRTtYwasgw,jIAJUNmxzdQ,6vsTR6pGqpk,-lAmbpRI2vc,NfhQL9jUP64,aVHoZSIqcBY,Yd8lCml-BMI,LR8X6ecpZE4,US0_gIjokZk,ltr33BkjYvo,c8CIQ5COXxg,68MiwJvV9uI,pc4nUavYGlM,DrkujLMe1cc,y0V0-g5iQ2o,cgw2FSvhEZ0,7Lox9_CFHEc,qu7hL4oTv8o,zK9c40dPIlE,BrGkVzzDj8s,WjrbGd8Vg-0,cymZxci65mw,VG1PaALV_nQ,1qQvbYHuT5c,dzrIWJFjhqo,8Tu6qPPE1M0,JNwdwpF0Uo4,BXEbf7kwOZI,2hYHLQ_QRvk,NCxdnw-TYMw,Q1tP7BrhJ9M,sP5GMTTaGxs,-akt9lWXx7o,nGgq29XB0bQ,hKhTZFkQF5A,ZPM7dXGpylg,SqGhPf9ASAo,WOdl2ZSLcy8,6NNgpEY-lr4,7biyK1zMat0,MC1m3JIYabI,4U2gvoEVCto,KR38lIgydCk,EX5AkUCB8wk,CkeDU-IW-nA,aNjzNeCoPC4,UtZORcFSl7k&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=cjPXv1wJ460,qRxwTaXC-gE,IXcnRU1_ZTc,JrAgRdKIMjo,FlSBrdIgeoo,QMOQFjcl9S8,zM2dxXXSSCY,N0HLkHced54,WK1xHmzvmxk,IraqebqevOE,FwAzIOG17Ro,D_RE_asyFO4,KQ301kCwi0g,uTc0xCnGLQM,dyZ2nLUdNeM,czuvBy5eDn0,uXXVCwIy32U,m5MmUK6WdwQ,AlbMhB2LfYI,qvE5cZwWTc4,Sd9TIPHtrlE,YaLhg_vbCk0,MJeFsmIrv6c,q023oeqg0Wk,NbdLlN9Ln-8,Kh-7aH7TOcM,ufZB9DYJWI0,hJTh9NaVLpU,MySqdbkVYUk,wN1Pabxpn0Q,FUOVNymzNA4,UXR-gm2Pjtg,cjPguJS9Z7Q,nn8XXkpmtYA,dnfYNS4-FSg,IG_HYaLvFqA,AMx6AOTaPDA,k0eCdxleFs4,8mbTmBAgHHA,EzEpuQNdDeE,p1O_wDNp9AU,HHzZgDvx4Xk,tL05_ONW1ws,jztg9tRVEm4,Gs66u62Nyms,tU9uEh_tr-o,dV3spwsylSY,sjqqIp6wWz4,ZmTW3XZGSNQ,WYXDgYDr3yk&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=J9MQuOgZX50,Bh-T7-zqyrs,-tGwp0KpkYU,H9hSOELizfI,6fLMKQNTD2g,mcoE-qLQNqI,lY5QtkNd8NY,_IQL-MGRQbc,tBqjtXEndFM,hylQ3JSJvzk,dKgTHUIjUtI,ybsIF99r2H0,YIdP_Ir7c8g,bX62Ldl8Erg,fcRUMm4KaYw,TBmWz2uuJew,Fq5hRx9cATM,ypq6UARcmJs,YN9R7xqzrqk,wsl0RQVsVlc,8NaP9quUYpY,eMomqrT0cqA,yw8JHo8ex7s,2t9yyyUURL0,H4tuIScE5bg,IhRjLalGRQQ,SUE41bWolKc,kQGiJchJu44,YJln-bAvoME,k1m_MY3UTJ8,wwmLuiDkRzQ,FaSOiPYpvpA,a_HtBLbLSKM,KQcbHl7-0h0,cGnlgyDsl9A,p91YhkzwMuA,_OClUbD2eMo,BEkMyZPLrn0,MRsGud888U4,TFWyTXMad84,6Er-tFdLYgo,GETcjeoedGY,zRGD3r4UMSU,0im0Dpjx11s,fRPW4t088XI,fisL0MCPRI4,0RbYkq4h1I0,Tmbd2HLfi_g,jArvr4jr_Cs,Bs8lsdqI6Fs&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=2cMhPZNsmg0,XIIj6EZtPCs,4s5krKsh9RA,t3g7b3UMU2E,uqkjZ5ck73s,x5VWUMQdxb4,C7BTb7Pgxc4,1RsdSRT3Mas,XzlqmtfrUhc,-PSMeX9ICpo,GPx5SK05TRY,sm4DFytMArw,sOdAHRPtSnM,8E6-oGl06lc,0bGmacYBfpg,nxgAVwv2yeI,rMd267lYxJw,RLsyCp1bbgI,Du2J7ObkidI,1z5O3H9exEU,4zAnZlIeFmc,ZVzSsj1lUnE,SZAgjXkRyD8,O8POFR6cwKw,aoU-0ORyGZ8,Dc9rRC7mMT4,ipG2nw6wRYY,QNwc03gBpcw,08Bux9yC2sQ,_CgVmN414kw,bWd6gJHyOzA,36svsr8yK2k,6bd5ItbVXiE,LvqJDPra2K8,1YZ5_Pne2UY,Y-mh4yjlVbo,CQXY6o30zt0,vg4vO-UziGY,dbrO5lT5ZyM,OCOt7Vg2GPE,KODeCgZfFWM,pE98CYdiR8o,fU2eRXHjZWo,LZwzUlN2w2o,YeMyoBaIVIw,qSskPg6jo04,nezT6xR9dFM,iPP5B5nwXww,Tno5EsfFEg8,lrmIGoxiWL0&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=pGOXSMfru50,W3Dv-atYDqg,Up0S1ihxXGY,herat_BkwlA,o8Gkcutg-xE,uM6SRXcmaU8,DFFs0O_-Poc,OWKHtRFfO54,TJGhUiWQ_G4,L3bUvbRcm0Q,JEi3rvbn_n4,O-LTOPZJ6Zo,DpnBCdNyEUk,SEbKp1bTMTQ,mYKyykIBSm4,QAvarWq8jkA,NV1KGUjYwpk,H7gxdlMwFdY,cyE6KL8SW-4,CiSTju6Tzso,qcr1ImEEPEs,H3-sDc4OqNA,Nc8QfjTDFdg,Jm5YOLvr7aU,zf4ZzjobAQg,20D3Sbx3vKY,wx9zN7-3ZTE,RxEY8ZixHP8,5gVZ1Nps4OM,-_mgKMVx-Cs,j1AQDQ9VfAA,uC0TwjHzNYQ,vdPZNR2ELhs,17uie95Z0Mo,mtOhZKtzhKM,l2ImJLfdtUg,8uzeKyqxilU,Zt5fJYngHg0,P9eyF0tv8dQ,VQLp50jlm-g,FAJOXqN2_IM,rRkYP2_Hsk8,ze8DpxwUCu8,mlWpzqCeIrU,3wjZldzSB4U,zus4R3DXalA,em_ZH8pzF-k,m2mCPL7iIG8,RWhwKALclfg,-_VuYtB4R7Q&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=4Mami5k7MBA,Cmv_lWcab38,z9_ZrLA8CRE,OCn15HubxFM,ahajVd_0J6k,tQVrRaXE_xc,6ai0FL7gwFA,HkGKIitBscg,n6Elz7JBPEE,1DiDelUkrMs,cE4n6jdmgJc,_JQtWXmOGMI,cAUf9a-fNek,pg0mmfPLf3s,UzZqRbYCP-Y,x_-Ubd2xDis,w54z3FzzNjM,qP7S7Ob_InQ,iXSGHb85N3M,l8QeI6kzgHc,qdBISYy6SPc,x-0IeYlFah8,qtiXVhCcy0M,otrvQ-rnkyw,M49DlwRAPsM,xfB-82Xpfpc,erZwT7tyb_M,NPUua0Vk9Wg,i-xKctcw6eY,G7kQZIhDhpk,PpEeAMC1Ec8,xbYVygV54QI,fzzvbpe7n-k,VOmj4K6WJ5E,QUZXJ8_Xc-A,CGas5XDIlZg,DqDaK7hjtKY,n4VNnvP-P0w,mIakU_ahxEw,KqSbwMBLIR8,OYIVXKw5Z_Y,NR1VGz9FeFo,Za748NA4MGQ,wp5xjaEs5sU,8b5aThId02U,Wxcb6pca24U,YLq44EOXTas,NQKeYTROYOE,8cQBwiHj6ic,PEGW36KO16E&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=QaIT-Mc6Fp8,lImOCw5ikZU,I_EUbUzkZKk,5Mn3fSZq0Ng,cCq1pwa_0Us,wanW4MT29vQ,FX593TYobDU,WIoQyH-gy7s,pzdjEPqqtww,a5Pu0PRG95U,hoYUfaslgrM,-gk2OH3kvME,ACSHNzraLcc,7mC2DT6gH2o,s7bTzdSH9hQ,AaiVI8JoRA4,1d6BEhZXOQo,I53uqce3Cdw,m0WAe9vCErg,WLPHXPiKaiY,0J7nMdNQLE4,ciomL3E0owk,WiNyracbhTI,psInWfkWHZc,BkXyMOYgpXA,u0kEVfmmvWM,IiVB0D7M4CU,3tiYfZV69uQ,d5bl7mtcoeY,-GJOAWQRHis,mNohNa6tdX4,ZorvboNPz8U,cpHlk_mItzI,SUfrEs7LPlw,Li6JsCJOtdY,BZN88kEBJHY,toCAvhwTV0E,eRp0djqXwk8,7frkGDg0ZQw,WxoAlTo8TFk,kYomrlV8Zmg,r0QKYG7il3s,T4iPzE3o784,GvYEG_w95E8,Pa2wDqAmW1E,26NgTXH9-74,Jnh-6XCsRnM,xWWB9yf-2L4,my7PoyzEthA,0TnAXXATL2I&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=ghNIy2J-wRw,79Ks9-JvuFE,6e2mn_uPySA,JCmJ5JvJk38,xSjYWa9qSqw,za5c43CcJSA,GlUuGXuHzcg,A_zJOlIn1NA,rw1wBomAo_4,5nLrbklrkAQ,viw7OtxDtAk,bTqgt_o7Z9E,XpAVthaYyyM,4r_Py8_93TA,p6be17uxwew,OAozgK2TpvE,yg1ddnMQJeM,RO9bV3VaCLc,hE2yVl-ks-w,EhjZ4AWh5FU,g0JSNaRCj4I,EjSz0cbo3FA,PDoA96E0xQU,KCjIoZmZONs,gT4vF93tqNg,d98tgyoQn40,TcR5ZgXGh0g,vI3g3I8qy44,RXiknhtuM5c,LDO5gnbfams,Wi5sUYKWKLo,_5GKcHUfSVI,yHZ4_ei2lkg,6F809RcfwFk,ueh24KHkrhE,KmTa1cVOLiI,0H7JzAo903Y,ZI6qXHopnAo,tb1PvyTOiX8,Yuer-1tJrsI,X6NYyXhfiio,v9-pJkDy0JQ,m2mxiqxpRP0,QpgyyLTRZK0,ZUC52LCkJAc,xNNE5BV2WgA,EMsA6oSjza0,2tOOLcpeJXc,IGgfrxI6t5Q,ww7WMn9yMPY&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=Nx4jaFeL5AM,kl670n3bmoI,1TJE1ppAW-0,TTs_5C79Vdo,d3ijsFFDJ-M,Xlqc9Z93rjY,XKdKSAI29mE,-nTsN9ONORA,aWhBVWMza00,Z-k1XkLvUFA,SATEVitYWDs,eSOKFxhjBIk,oFAaO2piKeU,mS5oE01aOJk,kcYBiShOPOY,JYWYorpaYZI,gXzqD2faJGw,k11-qBpnz0M,X4wbBcPBRFU,7zm1eYxwxik,b77vVzWOPFs,y-9DlojrsJs,sIQeEhf3z70,KDjIx8Y-r64,CospNrGE5ac,07ZgQ0P39bI,6wr_sqONUs4,27HpvOawT40,7Zn_1MrZk0E,0Qld-4koCcM,g2ZVZprs4VE,1CEc0n_HYAM,zt6VZTpN0sU,liPAyuh8D88,RfDzwW6-I_w,xCfXccl-JyU,i9kutLPCraU,m529FPfqj2k,nN7B5QkWM-E,zS-f6EFHZHw,Mm3OYpye_jI,gxVXSMe8r_A,zYqCahvFK0s,mCWTGHFFMdY,Z2tv2E91rK0,TkAPS5Sm78g,NAXVNDmR7h4,VHRkiCliK3w,HwNgsxARyzI,MOxP9_lNZEU&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=Muu_lVhsHtk,FGjWt6Wd1UI,Q5kDtR397rs,uF0Me8aJBkk,HQdGPjyQ2c4,QNUjRavEnOM,t9Oy-4QSTdQ,Kj3KyDupJ18,LnZHosT7mtk,8hB2D20KUiI,IijayjbkhZM,1omLZhrE4gw,BBaA8m8biXs,YOgcZvKA1Ls,zSgahHdwd5o,vJx6Ej-n8kQ,c5ej5poRjSw,SQBijnl76iA,MO96C8h9w6Q,5VvDOsRqkdM,pTh6xKuMo-M,a36R8CU6BFI,c179DNc1xKo,OA2twmo96RE,2s9rEo9ghPc,gIFe7WFjfX0,yucVQPvGcTA,aMhi4LT6y1Y,H5yO9AEabUU,27JbVa2MMhY,5Q9ot_BoQK0,XuI9oZpgjbQ,t03xzgvNIxQ,LGkeZkgfReA,PcXARbWONKI,i0XPNQ-z63Y,2aPrG2vN7hE,7X644yVl6Xw,38tXeza3mo8,zcztet-5Auc,1XPJ2DQVxuw,JnTPObMpxcM,DF7WpqFyvSE,tXTsa5AueQA,fGMOf2DCXSc,VosPVONUcrQ,H-Ss-ZPMN_I,Pgsq4brIUCI,tammvQ9O59o,ReSX0bHQUvM&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=Py-9ZmLqTtI,kNC8ZDuxv8U,jTI31fEzHOw,jC44cFMmR8s,xtRl5UeKMAU,vkl2X4hKHPE,v6ztJe6e14s,u2h8ua4VImA,NOmjWnjbabs,3iz0oLM4ba0,EdtNtbp3E8Y,f_9barKrT8s,66nBpHNExa8,179dTI7eomg,kYG6C6uTY50,YU5kSMwTKYI,4Gi_9N9CB7A,rf7feztqmxU,WaoOg4F5eTw,js9_7JK38cM,h6AA7lVA-p4,V-O7PYgbMjA,TuqZMrait_g,KJj4Afr8rIU,DQgLwIgO6Y8,7u2NYUPDjyI,j3lIFcyqs-Q,tRGLmghY8oQ,itTmKKb4q-c,WAcPWCJqnaA,qUGHzuOlPek,aV-UbJrF9nk,6WtIIB2sftg,Yd_hlQ_9v0k,9COLqWtxUtA,u6r2hiF4IyI,SMAn8us2ymk,CbYhBZxrbY8,Ot7ca4ysmH8,sKjUmHsAy_A,KtkQQFao-qw,Qz1FfXnkJIA,RCqpBA9EMNQ,IdNVTAjKqFw,ZVmW0Fz_7cI,JXXc37loE04,Qmd5SaB7WZc,_xOU2FoZdPM,9FBGder61Vc,TSHUtr5hIWU&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=WSr8IpsXN3g,oVGVYLx9sug,jcgTTiPD2L8,6fFYBT_3Ky0,e1BHETMuFXQ,kW_7xrY7FgE,LmSr1x4IGBM,GhEjQMxYfVE,gsiN5UK-cK0,1o9fPR0Ka0s,n-X6eFxJYPo,sr8SdHTsle4,kdj9h6VrjlE,izLCFETMlD4,1MMvnhNk4NU,VoftFNAyMV0,IJ_Lt7vm-Pk,bDjgaVCW-BU,CUtyfVoIosY,6sI-oa0xgK4,5xyUu2cn-oM,3iBzP3VIT4k,lZHOvXVeB1I,DANTCuyZNDc,Imm1xDmt3SQ,ThEeCPDO6Gw,sl4oj_h0u3Q,ypqFSEzx6EY,VHWRTNjxkIU,8_Czkn7EhNw,UFDrZWaAev4,AUPBeIv6UKg,KQoUWKEEmlA,Sy_hWHg3gnY,Q_OA0wtVDAg,91YtJRh0fpw,7g2EmHa38q0,ZbocFyp19FU,RYGi18SxdIc,lZoC8Zd0mig,rfyD9heNIsE,_zZp9-vAIno,Me_1nuNkVog,XHWqFCHNZ9Q,7nvVOOc6_m4,-bq8qLSoh0w,64fBVnMME_U,fG1Pzejrs3Y,y0GiP_u52CI,cCNL5u2nBsA&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=1BtNZLMNsQ8,Fb25MfaXc7Y,ICkskaS_eZY,fXOMypUxSCs,scmGmb-1NpY,Be2qroFGcSM,RSw58_KnhhU,FOX12vD9ri8,Hu8YwBboP1A,Rof6Vk94PQg,E40YZyRudoA,gF8EAmzohZE,lxxamyBrTeQ,p8HFtdhZSyg,cgeuDTojbdg,lkCyLLc5Pk4,VL94K0hQHPI,7qiedeyTWAA,DKjCNL0_Ki8,o4RqshqXAY0,I-YIV8VY01g,ATWRYd1L0BA,YVdbPtN_n2g,vpxzVb0iXSs,LKJ-TnMNNZ0,DXQyyLFeJdQ,cp5jxY94Prw,1iV7v6jDnuY,Z3nFJGzH_BU,nm16r71Ozcw,0jt2G-4LPOQ,Fpc0ACQ64ac,ZNxTx8htuuc,Qj9rGy5Mxqc,-Gn1DN6R_jw,cSzvm2u94uc,emOUu1h3i64,DNe6DYIskww,H7AVm7ftabc,KyvDPR2PsVk,BR0JfVbG5VE,gjWy3q-WX18,T1gLUaITrbM,0zz4ofs7miQ,RWiB8NtfAM4,Fm24mRJ6Gts,od9mRhReaNw,S4BukTgUKug,SfaRelyLW3w,Yw8LwcYRW6M&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=Mf4an04IYWI,VZdcyRVb3Po,pzRPtnamuUM,xbRjR7dX5lA,5gTINBSG-d0,BZV9_ooxABU,RoVSus9VMYU,8bL50X5Xm7E,MjP903bOt8I,oxUlRfph2k4,pzMDtd0uGMc,AS6UQHzwTNc,O05zmaQA59Y,GbuwUzqsxyo,Sirz24DuvLE,tE0Ltscl-ZM,CdGDR9J3Klw,FEejdObqzjs,uL_BHD4yj_U,yY5bXxNSw_k,tSq1ZaXJzeU,fegnHVl2W08,2rlp1Kfc0nU,yW35LX6aFcc,t9PmxPdxlYs,9M7f6LDOspI,KLNkeeecr2s,p__eAq6g6Ro,FJGaZhFFYK4,3ttPvRiE-p0,fohPC1YK8Lo,snMw2nztG8A,9hx9gOpMCg0,ZhzqQ-CBZrI,rAYLO1rJkiM,YXUl0MJ3CWM,zOttrmSQqB0,YAiIwVQayhQ,keCOC2rIG9s,4Inytt5DSNs,5gVap_28okQ,DG79xc9Y9qg,01qFMK0tYH8,X8OXaPW6Oos,trmzkZpKeVI,z9wo-F_uBi4,svXWoMj7JhU,6EsrstKqMp4,UxhMN3odcms,E5Or3hdojsE&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=uM08TY1e0-Y,7yuq_4FgTmo,pxg4QUG7nEg,iM_fc3tU5aE,LlgTEPP6-oM,RcdaW7ML9GE,YcrtwIVF3Sc,CC7zjdyGe9o,3Tnwj86Nrgo,DzIFptOcfYE,DTuflB3OyXo,i3QaVYWcfP8,rymRXM0zynE,F_oVjcO4znM,f_4vI49KqpQ,0gtqyJ6YYJs,PObDWJfjOqk,18qIs1ijSxQ,XM6H2fWFhVk,vXzzAbd1Tq4,gNZJUOeOmxU,G6UIsaGg3bE,O0T_ktiKlXk,RxRdxkg0WLo,Q1VjD1eEvvw,ep4odOh7hIw,c9E1G2BQRKs,aKCqrtWPZOM,eo7mKGUJZpQ,tz1zxGfokbA,_fhvUJP8gkU,K7doCu7lkMI,coplL7kYo_o,7l2s6E1x_FM,bXUsu4EndQc,iXOEBfvRHY4,qA04etnyTWg,4PoxPGzNmUc,gN85MidDQGQ,NhxKzxR35ps,eCillIWmqRs,M5SsXCqvZg0,3pwbQQqE4Hk,AT_USm0en-w,6cx5ZIZIR6w,Iu4WKVhDrJg,m_Y2DRwBhaI,weOgtjapef4,-31uRswSky4,xcmNHn3CV9o&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=uRPgYlxL918,tLgPe22VQIo,xa6-OYbjwe4,29-F6HpozGQ,6YWDTjFw3-c,kQKci8lEMak,8SHgk5sM7NU,CEYcB1rdi-E,XAnFxmsAKTA,LLR2iFOvO4c,5wo4mFk4c1E,p5KpJQjSK-A,fea-S21Diao,TQU7uyyaSxg,bnEqkY7JgU8,zNIhtIkfHE4,0NSwUyJXLio,9EdEQmsR4YQ,3IUbRZtAQ_w,JpBJs6Cz9cg,S4YHYJAuTfY,SVY3Y3zYYP8,4cadeAfa1Hw,AYVDOlmapQ4,SXVadqit4fQ,g0trP9ON5OM,HVSOUAyZwGU,3uH8MTlrrSY,MA6Um5tM81M,O3Wnsk5KtrA,jsXKqLhMiZw,mRmWagiy8iQ,GBKFMk2LdUA,8EvHyLTNqpI,qafhIIoWzxM,LWf1w7I3beM,GgoNa8RENqQ,mH-ki325U5E,XmmROXJVzkU,BhBlbKKQ028,Zn2H96b2qx0,Kr2ooqzs2wo,9t9o-qnhh18,reOq-1LJ12c,Rs6UDxHRTxw,YzkBxcDQi9U,4moqpwBUjfA,X2L7ldU4qt4,WjN5FN-sSAQ,xBDH1g9scBg&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=0Eo63OxJHh4,DNtDpg7lKgM,qUHA2e4NsoE,nVoq9Sz7eyM,wiM7l1_3GFc,N2SlTwVfprM,TlBixJvaAu0,hFTk84OF8lo,tyKENhKBxFA,-5j5PMLTq4U,k5NaVBTbURY,wpsfg3i8Ldk,N6zK7R9yvlo,rC-yPq-03hU,y_N-6sQfno8,-pcmnk1wn6A,uW7-ZciD8Ho,yVgGjwzjktc,2M5c52pTJyw,8_jHLErFcMY,zyTkoVbP4II,qZ_fpz-G6Dk,NKKzGbNwOVw,UMuZZvjPbTk,TtVj14XL5r0,VYJSimUNXao,ZmCcDcxXxQY,hTgDWE7KEko,aIoYQWoIpqE,2_vrp6JSUjE,w7RdDnpJlzE,W1bTv3OYAsk,1aWpZLnAFA0,9pO75qE3jNo,l3wkWrWZ2cY,ToYCTiDqPfw,PdYmC9RCIig,uwOri5703U4,_FcHzDKfxw0,4R47lq2rI3I,6TLjqLczZqY,8lvG6mMs79s,OkaajIgOKF4,WB7gyY8mskE,JmFDRlgYqDg,LLoD79VdCDg,BsiBhwHqxrk,scMTGN-8j_c,zD8zcSt33jA,KdLEGSqxI2w&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=m4pcZb7qEZ0,OG-1-GP2Z5w,IuggNYlx2rY,83xHv85xyuY,z9GwgDa5yAg,4XWJ_RveHrQ,ox3Vfh8T98s,528u2BgO1Wo,jwYjOJjaCjY,EctlHhW1Yc4,TvV_cR0Pumw,B5m_IMta1wQ,44qzhCD1dLc,J6x1N2HN8jU,ptcyQ0iPUco,HTs99YSA0Is,59liQ8iahBA,V1oSUOn1uAE,Q77Ss4Jl0mw,4Iq4LYaH8_I,3TR0-UgUBeg,-KY9C1PfEog,neMufJx9CjI,O6hApMOIBZg,pAmYUu3JqJI,S3ZeLOvj9_I,fapSZ9pbvHU,aUD7292cOHY,CGDdTHaiUEs,WM9FlDW3EDY,BTj1hbYu_So,Uu3NT7glfl8,60p_GGFYZTY,_6nQhJGrIG8,FPkyJ83jnnU,KGk9GJgDo3k,e0M9ldR9IwE,nMZOz09zKnY,A-fQpy3rKTY,OWgKcoJVn6I,ovl6vuFOXKc,CJFOiS31BGM,peWgObGPa3s,P7M9aFiv44U,tDtVTsqfLXA,1kfLM88iFTc,nf7BPPe4O4k,zo1R6vNtrpQ,PngQ0PGefTM,A_FN7Kds3KA&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=jf_fdRegJWA,O62ujwBhhPo,hfd0zz5q5XE,HZtVZEXgHqU,_vGeQY-8uB4,ksdB_tRQhyU,gzlTBcs3-18,Idx6Jy2_-2Q,JKS4Ux5W8qY,EBBQWXaA4II,iJSooX0Lr3M,QsKIyjJ8hVc,dA_pgkmoYDA,sSvEWsx_TVY,-BNgKpJL-cE,IeZhkHbdLLM,F-f6eX6sRUk,yO3MCSyjoJU,pMLJIP1sViw,Hf19el18Y4w,RBgsaaeRs-k,lJOb0Rlsufk,1OjBPyMYiaQ,NYOXmF_HHRA,2JrQs93fKMY,jDfJVyEiMM0,qkpBrVp2ImI,yONz5F5pHP0,uA3Z_y3f1jw,B3LfjwkFTFk,ag7Azkj7xOE,8Lp0gF2uRN4,lWvJuvQObhM,I-R7hJe9sak,kc4oDYU3HNU,3FVo3VMHnBY,GeNiuZdSAR4,1M7Y0_RzrRg,DgyzdjmDK-Q,Y8HZOtl8avk,ANCn9kCyieg,ABll5-VBIQ4,XBzR-yrbxK8,0vDuW9vNQcM,DHJoVceaINc,yrPxXksaehw,xQj2faSrvhc,25xW23O12Uw,NFCwn1fpOhc,ZbEdHiSJwF8&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=QnxDL7FVYc0,cyAdwR_4Qb0,5x3Tpy-EHGY,pP6KUok96gM,Gdv-uPNUEp4,JSTT9S2_6OY,wKXmhf4yyWk,ECq90fng8q8,yb1jHfw7Wn4,gpdvbeV3wv4,wLDh1JFv-Nk,VYrupzaNUdk,kYunTV0PIWY,_2af-7iPwAM,nRoupD5L9Yk,NpGxfK1niPg,k4mNSiYPP7w,3ELdz-0eU7M,8YmH5IeWmO0,c7V6AupuTZY,P4Hdf1zuaOc,zB2qYpg5scI,5M7d1FMuDWU,D5NTks6XDkI,idxyngDM8ec,H2jcIltOQ0A,lTqvpR8f6-c,lH0bSv3xhD4,_KT6RAdY_I0,JOx6u5xrBJE,PI2MuYkN05A,zYy0CAFIhAY,8h4PY0Apx18,9yvl4RXbbI8,24746vvI4A4,HWP4TyfxDQg,jrfxdlxNZIw,4GHs31VR3Zc,XM9rIXeLbuw,twT98AwoJWQ,cPdYKW4xHlU,reen55aPHh8,abHKgKjoWBA,IwOxdIt3KBE,CrwK_R3Ptlc,pvr3o8eKpqQ,XKqUf2HeQNk,FGq9AY_bFvs,WknBFTBBDwY,2_ygDMwZHuw&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=x7F54WXcaA4,isIklLJceE0,Pcr4bewKXRE,n-dXlQLhdx8,3zVr5xJlpCc,O9Y1CLRUCJQ,aFlkttT4ZxY,dRKkzpRUEsw,GOSw9yEyIi8,_QWqgplXYs4,KZiZ-EkZpqI,HaM_D7mI39w,WvIgpv8-96s,a4KyyHmDA6Y,LCDIRskNhP4,wj3T2xJO6os,YQ-F_DmDStk,TLkUWaEcbj0,x8nd_spNkwI,ut9n1Rk-jtk,2bcOxa15J6M,3YpIYMU_gW0,UuUMolFQfF8,8dYAPjaOZj0,zwzpILaJwpU,483Dp0PqJJ4,ApJsLovU7qY,oRyn_pv3HKs,dmMoUk6TVBs,pfkB6UYjYBY,SMlKqNnXNB4,Y6yx5MxARbg,DoryeUQA5V4,D_ORdJW11gk,n8G5owJZqOA,g3SHth6GeBU,_HLRheGkeP8,3bmfwSH3oY4,DOeS5EMhXDw,7uhXsNsbgXs,HKjzryri-UI,2pdJJERv56s,qK9tKECADdM,XsZu2P7k_vc,orLBNg2LHN0,sttx1b_TbpM,OAFo-0bky-8,Ab0HJARqqYE,-U8DPGgBogg,VJUwt9-8_mA&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=MWK7En65zgg,jxTuMb-hdYM,lFDLbGvc_8o,cbOu1bDQzxE,H_He_Kul3fg,hwWFDe2Gm8Y,RZwify2YnG8,GvWuEarYu0k,r6uBnVv6Gvk,t_EN64UPi5s,Wp6RGupHHTg,i5tOgN2xEd4,cNHrTe9d6Lg,RHmOKQ9SYTA,MU5jLW4AHPE,SXzzCQbTKEs,g1p3SHJTZMQ,dSLeSXNgHUQ,JrmZqe-q3fM,KtJ6oTZwIYo,Xv9nmWWnDvU,UxttE08WRgE,HEJR4AlEies,-1sCAfrUWdo,X97eZB0ZS_g,E-uFN7LYLYo,SozZB9eaVYI,3SCHAdpnPA4,amkiCP3iBok,HT2UkoQVp34,iXumiLPUZPg,-gkW32tWsdM,dRB4DVXvMYc,aOMMPr05ZAw,pKBn3Ul5MEM,ZvWnoBvS_vw,jKsmkLK279g,2ziVjJu1fKA,HvlN9oux93g,1h_9W0PeZLY,1uVksAA_JZI,J50TUhO5mq8,H4fFgQnXUqY,V36oZQgICf4,BxuRvZm9RDI,qNxlE0Yqjf8,fI7V7-4FCW0,nprLARHpdio,8NhlUlpDIGk,f_vl0YgOzr4&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=1d_nK-KlP9k,UMYvMpJea2g,i4p-NKJU0l8,q9CdUsSOXfc,ESFoVSEk2f4,DpsBQCTquBg,MdlP4l0tMkk,_8wKOjc8QSM,Be1JmWjOaBo,diU9Lnsk6o0,ZuF5gVaKnv0,c937As5TluE,rJVdU0HRbA8,jNN0XMQzjIY,gkPeW63Xxbc,hqZMBK1kKl4,--ivBy_OaFk,lZhOp2mheBQ,igbFgi0R8XQ,Yocct-3tMXk,NNtbivmq5_E,hWeuwccjWWA,_wo62U9HdrU,VA5ld6l2ckA,rW5OhWHScdI,TeUuG4fjBaM,wBfGS0InZGM,emjHITzM3lo,3p4XLlsHFNE,0peLr_R8KvQ,KK24DwQeMZQ,772lQEtmSUQ,mXMaepepl5E,Vig2cCdYhh0,bEHkAz-SNzA,oqZ-oPAbyTU,XWcADk5sJaw,wEuBhpdqikY,tKgKzXQ5vjw,6kiKLeMQsUE,h7ARuxs-rxI,JUG-t1ks9TQ,txQ3M4UlI6g,FhFQObyQ0yg,ppjIDaUY-sM,rvqtImTL5P8,mmKD-VGZco0,2jUjF5doV-g,IEpM9V6ag6s,wkunIWCh_Iw&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=reb-VHggKAs,9eOpCOYtOoU,g7bsmj-22eA,yFnN7fW5OXU,YKI1N7p-VxA,Ao-PAnkPRYc,g-rd-mfbF-8,jr80INs6A7w,yiDcM6DfWvQ,kW-DjxIl4fM,Fr7HjR4uehA,8JeAZmLa7gU,KTs0ezQoMjI,-oWullCC4S0,pyMrXPinoM0,QsHu19e6KdM,8xc7H_t2lJ0,wj5mNrpoFSY,ss9opAIlD9w,CVWjA6qtivg,cNsk6i8WlvI,f-zQ-MIbC8A,5oNhhaE1uoM,P2fS0LuC1iM,TMsRzwZmpb4,mhB9fNTu4yk,XQ9l3t0ap54,40sg7mcjaFM,rAwaqNyG9a8,-zVG5Vk2Og4,aegJDI4PYs8,5624DBKktjg,Wz910TCFLCY,6MzEu8t4JVU,UzjROVJHFKM,acihTFSWmPQ,o7O16uN7wUo,V_9aTK3qJK8,1KdsaYTnDEE,e9niqdeoqWQ,hIqh4qesRG4,nX9HqxD9gFU,2Z_4Ac31Feg,DvftZ6jtSP0,fHUbsKddFeM,RCQmG0bBd4Y,FkLR2DqAp5g,xShe_X_uq3o,BKTkiB0Tbco,HmYcGtMUwY0&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=86QbQDsQDAQ,V-40vhJRWKI,nFnjN_SMqEQ,ubXLwdTodFg,L2h21t3N1nE,KniJPa_qfFw,-pSmNCDjlHo,8_-xXq0fEnk,kOjv-hMQ0qY,ixC7afwkDcQ,Z3Xq9aAlQe4,cBxsmu0xqGE,WrQbo-3QSN4,wJq_ddaJ4TE,3XISsgc1rVI,Dqm4BDFY7Aw,OM7KdEIzI3A,DuZVToTRgmI,h9HZEH-GthY,cmPQvcgpZJc,aAH0KKs6O20,PAl-8Yl9tiE,_vijzU4AHN4,c0PABgP8w0o,cuJMd0S2xIw,b-yqfSn9_4k,u7_3roN-2Zg,S9Pz5nVrAvA,NZjvewTj2G4,3MOjUwQVEUs,zAzaJqqhQyc,6GrOcHIf4HU,SmgsA-AvBlg,NH2LQ1H-j1w,VBLcEmdzlSw,vjothel2Bjg,_U-goB2q0Dg,6r2jwi4qZ9c,_j6HuBllEN4,Vm_cVgaDj84,o2SfRvYRtZk,S7iIFbx2KA8,0RXijhkK3jo,KaJOa7IC1lQ,4yoS2N5AD_4,cddzWLyK69c,oT4Yuzd2j48,_B-To1RrAns,BwVdfpHKW0I,X8RNPOvwQA8&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=M_5QgXIlmR0,U7s--W_-Y_w,yNJ95JfWfgg,gpjpSXz0qDk,8xQrB62wVMg,ExGFydG8Wt0,EPZusa1gPPM,o7THjRNTP8w,p2jPAm2zsEM,WackFaN-rjo,dFUj5B8ywOE,yNusuujxP4M,g8zroklRzXQ,v9Jv52Dy874,t3XSOywOyYU,dEeSGHhiYhc,uYj6F0ouCpk,HN5810KJq3c,Lqw1HQFlNas,LMCFdbbTcuQ,Ah0pWplKvrs,ox2ybLt_EiE,jXh2BpJ45wg,4Zq2frPXFaI,oVqeGAaM-os,ocv_KBgRTuE,QuwbcB-PXLY,cKN774PBOKY,ugU0EOklJAs,Ht9Y7mR6myI,SNlnpAeLo-Y,FGTskFjZvBA,KRBtQ36enlc,LYUSnVSLBbI,2GXluJ-UdQs,s2F1lXL3Elw,pQmxRLNmnbU,SGACWubxLJw,EnJBdOk_uLM,0BjHLh1D0S0,HnJmYUXjn4M,1KP24-SsiBU,XXBy763aZxo,NBoY0CypxwM,z63AYjknbTI,PezQav6S3GI,SCSBEu5JG_g,gRgSD1xtvqQ,j8eA8YbCJ4M,7FEYkKMDK2o&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=pMgOl2vRwPM,5VglYcqahTY,wS13BkndKzY,uBoO3wwllJQ,nDah1cioYIE,MojGK5KW5h4,YxDRECetRno,yFxHpZWRdSE,qTHQ8t2LvSI,YrBaBgHmovw,hOZL50TlGWg,mUluzZXz1as,2rjPLHi_3to,SLSI-JZrQhA,k-QhdkHbZH0,dUYyDj1JV5g,6G6c9nPRI38,f37tNYLIpmc,uRTLm6az5Vk,wb1MtKWLay8,ctsrcBswBxQ,IBRVb31Ulls,CyqtvkwpP34,lb2wF-M_Ytw,4ZvCkflnMVA,TKEmao7Wrew,D9vXxX863Xg,diRPogf1jMQ,7Bz9ibmTQco,bGktZsvfimk,7IQsLRX67I4,j5K_k5gq6YQ,TE7UaFgPoUg,vUpRQz872vw,a2yrAm7iYyA,1zWsI7weTSA,xOzgzk_4uXc,s6PBm0esLS8,nhp_OEQq2B0,v9oKy9XXCBk,89dbu294zOk,gTUFzMeMghE,7bZeWEN-z-U,kUzkEFCj1Io,EW0rpON6urI,cAkgGdH-HMY,NPLdyVuhnM8,RYx0D4cIurc,AwfsHiDN138,fZuQSI7NUUw&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=-W8v3xrKI7c,Hb92SwNxAzQ,xZp8oekxYs4,tFyUU16cAow,JYqUHFzrvNI,Bw0XrXqNuVI,5wLMmyMuC8U,PyMgQr9Z3rc,K_L7SRBwx5o,jz6-CTq53uY,J0ZZENv7OpI,IxvzJ0cHbvQ,paPPS-iams4,QVgqfwQpVDo,EnEDVEnm6z8,CgjKtFaHbE0,GLBnjLgN4GY,62_Z9k0FqN4,A6YyD1CuYyE,EIlUYdErBKA,oyDB75WDm6M,RKKyraPbwpI,oo-5zav6Ulg,xdY9E32GYPY,ACCi-hWnLGE,h_sNLeWPlE4,O1rN1nWsZ_4,-O3xC-Zq8U4,lTCSajJBQZI,FYUNwXhyr_Q,lT29qP9Ck9M,r-QAH1Im6yw,FUdDE2450pc,FkBHZi6GBl8,75lfyB2Sg8E,yG8yJwYmpsE,qGMv1A3PXn4,4HgJprL3X0A,c22uyrCdyjQ,6UG_LXIo13s,2wKD67YzATs,QHtnWEftWd0,CDy-5xBgCVo,3vEMiGVIEQw,kz1AbHyMnBY,M5n7O4QRCms,FoSEV8Klvjg,ohpxZJZFL3w,p-At0kVg6J0,meLxJJ07Hp8&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=Wdg5m0yYcCU,4U16T_hgFKM,EJzlcTgZLg4,FFKP2RDA2ks,m7COMvN-m6k,b4ifVTSBEBA,1JEZ76OMPW8,4O5kUHeclFU,KFGCZ22evtU,iRJ9y5lSWB8,rf3d9YSFIGc,hoLgozohTq8,Nhjfy-E5tTY,94DFYd0333w,4klybsjpJMc,glXw4ABya1k,WGCfkcIjrF4,0aq3tfrdOvo,zbzbaFJTA4s,18p06_vT-7c,RR9rJOdqSNQ,tTNggh890YE,zgkn76fM_cA,TU1qzSj0kZo,ufS-G3NabNA,kPNdHpT9Hpc,v_i9oAmvBIM,gX95U9bQi8A,p2Ojs9mh4-U,v3I_RAw_Ue4,-TqpMYn8eBQ,FPCw4SjpE_o,rBpRI8uI0dA,6UxI99XAz98,Wo2jyItSwVA,WLtZBy8aluY,MSeD0RvS73k,jI88a7Mn78E,PxEQs6jxN84,BZghpMGahOY,qNJsysKT688,XUXYU_aR90Y,L6qXg4D3OyA,nFuP_WAdFY4,4Op8fDoY6W8,WjPzsqZRI0E,88-zNoNjauY,ZuAiEmshKL4,MPjJ5oGvwG8,yfxy6PBgYKM&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=VW12zhT5_DU,vRqJUNAz1Vg,QSgKYaURKEs,MvaxR7wb6bY,Id4mAO2Mlf8,uAFzXVPNfK4,qQ3R6MWbKdg,RUEqvBWAmHc,vuHQqviEPoo,4zdcvDa_flc,NQGKkU8svm0,FnCuQNMB5rQ,0QLu8NHpb6U,HlD-I4FdE18,NPXNotEiaKg,Xr7ilXlmNNw,f2lZKcFSjus,y17h9YJ5DWc,ackB1eJdJ4k,EuHkXSpiS9U,j-ZpiUPJ1Mk,bI2yccuwYBg,1reQpE9opyM,B0176-CNTCY,AHxsAuGUIr0,7bYha0x8G7Q,BM3no07gvBQ,n7pOEVBKsqA,pF5pmeuKd-s,pvCH3s9hroo,1YzHgoFpsaQ,A-epLRieg14,p0QstXlaok0,z87NfjYWV8Y,D5s0BUDSBBU,351IRac8Q-s,bnMso86j2wQ,4pJGY9KNVhc,HuaI4PggAVM,nbm2zO5QrwE,iJF75rqvtmQ,sERUYdTQ2xE,_BaesO8Y-x0,Z5EL0OmJeGM,dPcTDKecpjY,zqyH3YC-WeE,i-wvdcOc8Dw,1xqDxirjwkk,TjYJiIvcujI,WamypeDZRi4&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=NxdfvJ6St6o,19xZnQ9YySc,SLaiX7cB80g,fKSwBHkH3Zg,MWbA0LvFfC0,6Q32qNuOBBs,vFTpO6uB_AA,3oGXRSn4XHQ,9vAYGkOshfc,YGm6YsfE6ws,5LWX5fw5QJM,gI-2EbGwN9w,ABfONaVV8k8,Eu88g502E7s,nN7CnsBqA-0,xrjAYKkTDKw,cfgKtXMsI6A,r1yugqwNbX4,ivSNNEeFKvA,Jk_Dmw-iamY,nw-lMBcag6s,ZPd2rrArnfI,OZ5GMGPWW0g,3ktXUhDXQFQ,Xu0jCp3RLe0,fw4wK2k0U18,ELZDwXvsDGo,Mnmkn48NvfE,ejv2RyQu5QQ,jUwPvYb1n-0,vby5a3zvsqg,Q5sFzpIbif0,KwBB40oo9r4,tqZKXVX66O0,BuYhTW543bk,Uv5wLCQt8AA,etb-ivhBPPo,uxcy6mkM65g,6WnsEwTE7-8,qdgtqKx8iKs,jKg-96oTBTA,oJcRImmT5Uw,wYaBgnfqCQI,HFbfu0GHYDo,oPYEMuz9i0k,6qbETLzThko,5ENkLHQbQRA,12aBvw2PdtI,NkOtB-37Sho,FTwb9ReXK-A&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=OckhoH70-qQ,RY4hBRN8Vcc,w4zwgrhQCPM,Y3duFav37gg,8orE0LM7JEo,3whRgQTpzNU,z0SdKXk8bNY,2BbCXkMyP_o,pQWyZBoE6-0,jhFgVcdelJY,e29WzPI1R8U,ZkhmBBtkv2s,dgwif0ruscc,EBC01S9qwlM,4kjoECCHjJc,7V-zX31IkmI,Z8w-ey6zcBc,_O15HF8o4Sg,6tZLYeQsSHs,C-yv-kLt_l4,cOQRwQluDN0,FODYY-ytwvA,TNYOEUMUAqE,MwQwycs3dv8,SD2v5tLBsVc,1trSnsjQoik,xEOA7w0poRs,Fcco6kuyjwA,q1p3ocFeLGM,2kNVw9vt2po,ImSTdaZi3vE,MdnUq_gkoCo,m3sVp-b2bYY,5U4DYnJc0gY,pf9Y9ab0hPg,c0AEKEepevg,wVRySd0sBcM,Exk-THEBGlY,GwTvij_eV5o,O-KZfU9Sj-4,jIX8aTfRjbk,nx3oAtqZ5vc,qY3Vp6lYp-0,Ni2Za22D6k4,kvbcku8Twj8,LdHkjREoxRc,5EFtHequLc8,AorWRvNEWvQ,DanPC50dpkA,g3xJEx-891w&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=H4-T0clVg_A,T_ogUZRu2K4,hloKK9r472c,vitU3-eak-4,TpTDNgnADl0,SA3C_kBtzIs,WJhnwrasWn0,O-fhPgyrJQg,tSbc8UueXmw,kjYiJbe2BEI,nz9RbJ3g-sA,1smgKzxiDVk,SySJhLndIkw,0mrNEojCs94,Q5dXCDcDRqE,95FHjR9SqXs,5SodW7mTYAI,TL4RchKYI3I,-eKKBR41S_k,ldcLKoFj3Es,cJgYbyYksJ8,ZtR0ptHJVpo,HGMZw9VummQ,ytifNU-VsIk,SS8Lzigr6Zw,U7uqoUdfGUI,aX4VSLErk68,La3Ss4uVpBA,-l_goVely2A,TfosGl8NfP4,1iPEU6s-DxE,Byt1iYulH_o,HKWoCfS6cz4,QA0xV1YVQdQ,Y3ByWF2d-ZQ,Ma2WjBlRS2I,uKm6KOONd08,xDNQvDkSq1I,o5Difl5XTx4,idtexw4w3rw,1mQPYHTkmko,bGUIJr9ZHsg,xpslV__5Zoc,65bqU2bS56Q,hT8wTdNSY1s,SOQmv-kQixg,eKj1ydI11WE,OEh-fOtIb58,RquyXf0G7p4,nLWX_dcVTPg&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=it26LTjo4Ac,KJpimu8nQRM,XzJ4S_29aMg,Q7BBJpD_7GA,ouk6jRfPr_Q,SQEywe3K74U,uszfclUp34E,MOfvhKeVJt8,_4QDfmsH5qg,5yWIcBJQIic,t252pNMce6Y,j0NqUiaURtM,ki46gz4rKVc,axpHMWFtofo,DTkScoknn4g,RPcOO2OlxU0,wU9qd-Wbljc,d9GDH4pQZ_8,2-nVOZXeSzQ,2GlLs-6VPZs,62iVB2gB_sA,yWtkibcwyg4,HIHTkr2y3zo,g951HUuJzCM,fIS04Tx_xbA,_gC6S46ZdvU,cM2Pu69dIHU,PPOhD4LXPBs,fz7oBhGo9_g,mRM47EcCIik,KtFzOBmsZuQ,xfvG5URs0P0,z1e-E_BcvUI,IxU3kogYdEM,i66u-8tHpBk,BMdi-_hlt6w,DU7pqnhu44A,ZPMVYH8gzPk,Lr8_Fod069s,C-vVxcRDOgo,TYdKBMJZRz8,EljS5n5fgV4,4jGtDNW0MM8,3J4ZsijOaAw,ooudPm7jB9Q,kuz_WtjdYxs,vndqdp6sbFE,l7zEOArxxTA,LBjdPqmfSr4,DFD-ETfx8AY&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=2uM4bFezDuQ,tb-FpyZEPJ0,GZ6YL-MIViU,Qpyur3OfPjk,7wbAdXNcCB0,Qp-g0SLG-CA,RlHXusONwN4,793JkHFTKhA,uNekiWcuHlI,Kh56ACYF6I8,Wduq5kmFi78,XJw3KZZveHY,YJrUYnprSeQ,_vYAzy4yYMI,SGFW4cSkQjk,J5pBxapsG8Q,8loxdpPc6Rc,dwS7jQ8EBIA,4rkNqQYzqk0,L8qs2b_A5HE,-VGCD1ii8Wc,FbWX-w2x9M0,SMLjVI66kQw,yv7CPxvLCpw,ynJu9dYQ9YM,WzeeCHh-e2o,lhmpeoz_Vuo,mYQ3VO87n54,mTE2-F35tzI,TrKqEi4oBWM,KA3lcXsZ270,5-0n6YWCkg4,WSQR44HT9eM,xqwmYqUsygM,HgwTHcndQP4,VY0MnBp2Jeo,E6DhgdEy7-E,W2HJ3gYT0YE,EUqBiWYl7Y4,IpPlnX4iohI,OIs08ilUJsE,Qn_zqNtwy_w,FZE_4l5IUyw,4Ocrx8vKjog,hitqS9tUU7Y,OHwvkQ01KcY,qsBheVauF14,E7EzHoYDBNg,ufSBj_7SxzA,rZOv1QPKiVk&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=I6y9-GOMG7w,1ybRGy83fJo,qRu7VUJLjzc,z7cmhEY6tns,umJbcBpjVmM,PWEnfrb09iw,Z5Hf-1gUAIs,uppZR-5pWoA,z_OTw0TgER4,aSQlwOrWM1Q,fs4dWM2k7OQ,0UDx6nCttv4,UJHD9OnUggk,1XUljH-sW9I,Uzw6mN3Fse0,cbDsrtPwj5w,fL0TUNyweH0,7FMZ4pDy074,O1ApAo6vB-o,DQGOyjaIIko,dO802IW-FjI,kx6n1LQjOik,MeEzIRGiPRU,CPJFz9kExcw,D8QBT9wXMwU,umkslYWJKP4,Y0Py9i8fpLY,4-Zs55z8yGc,3F6El1WaHTk,wtb80SG-ZTo,9k427pQaAIk,exWeRxX7cNY,q2BkzgXOkxw,NCa83PX12dc,5k_tWEDh1sI,bWpiJ7p2CwE,WoZVlosiPJY,DCCVvSD0x5w,jAqjTe0n5V4,SLEF-vsQLeI,IVKZRj1mlxU,0-zsYVnbRGo,S5MLVsBAeGE,Hc1B7hYZIaQ,HRqD-YgKRCI,6XucTCMjMcw,sq25yhpAIiE,KNkiUqmlIfc,-puHigA4j1Q,Nr-kGAL68HM&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=zD3mbCkjiMw,BJ37wZA44S8,ZyzACNbWgOI,EJgupUrILHc,9i9ZcbqIgd0,rXkhUP2Di1U,diZ4mqu_SVU,26ME3S7qfWg,yilGy4YowmQ,lfBflNxi8AQ,OfHYMJzd0iE,RzJhX9cH7A0,EfOhZMqvi7k,NSleQO8TySg,qCD0ZtDf7F4,CmKj4va9Yts,CjC6JLST_WQ,KDU6V5vcu-U,m9FKj75tKhI,xRtXtPtRssg,n6Sa6QVqssk,TknihdSoqjc,BvBpOC5sGMU,8QZqVv6mtmQ,3Pht192GWaU,gl_tBasdY9A,36JKVOlbgaM,2nwdkYZeB_4,DFCuw5sLk9A,NHmFQ5HflaY,2y67SrkYklY,q5oDKBEHmHM,iGsyt0QzxIc,HKIIGaJaDG0,XWcID9BpOwc,JFuvwgjX2So,m7I6Z5Mv3Ts,McqTdYLbPOM,Gd1AXlEUymQ,Gt5brIzNUgs,-k_-GN9Buhc,Ml8SIjRbBmo,TiI2T_JT5V4,N4dNT_ScBUc,QxakB0m7iG8,YvXodsBUOoY,RA8KiLvqqVg,QTUmLx15dI0,9lQpLmpoZgw,C7DCuwOZ6Zw&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=sNXGzVES04Q,WUqSqOFTAGo,cBdvwAzqX30,KRW8DCzH1eI,UF5-6k5QA8g,oa8qrSWCpBY,hbSbpFyxZbE,SNYvP3zcgV4,U1VPfJn-K4Y,XpA_H92Wv7c,mZBkd6uApv0,zYLYAQCl2EM,rVGrjrOvN6k,-yJPjgrOKCs,-xr-nCO6jn4,ZCe7lnehMH4,IRmGEUxPrD0,ZmPn2eFKtqs,qpyurX9uazA,Ot5BrKUGM7M,J0fMhGKpkt0,hZb3BGQWfGQ,yfrj7UmMENM,dALbl6xmln8,FK9jEd9ZFOU,9koCCtfsuik,k76EurK9LR4,vO3iLCc6szk,slgd_NDIIwA,f5JsdPMlD7s,XPRNk8Avzg8,9enqaz8Rhjc,5NlaWep0DBc,9RtRsY5i7HE,NJ-u46noErA,ueZqmlCESRg,VCfbsn4kL2M,6eMN4rx_VWw,T5m-_LXqW6A,Ga0HMB6GZqw,lFgL-ReydAQ,5FPwG8nSmKM,iPKeFY3FTCY,YsWiWd3wfkM,24sx15rcSzs,SvbOd_XoiME,bPokTiG38ZA,xUNFcaa7TRI,_AxcpGukg9A,VUUUCXunAMA&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=JIJnjSmb61s,_jC-B8euAyw,la8SG3qgplU,8fTFYm-c43c,xSIRjfImZy4,dHb9DjRFLC0,6d4fugO6mUw,TG_5rJeppPs,rz5TlhN2blQ,mr-4bZm5VMU,ARwY1HVl7DY,wd8BUCL2lEM,oHjV56qH7t0,tXzq1nQx-6Q,RQ-KWhffOP0,R-7baLDGKnY,AVj8yXzUN-g,LVJRv_clAp0,V8G-4odw1B4,GALyarDowuc,TLhzDeXWB2g,hGfHhwLvIEo,OEZZPpCkt6c,N_QRtUehX-Q,3L8ky8IhOrk,JxApo_pRtQM,9jAHoxNdv9E,fcEZuxCxFtk,42XqTvgmZ5I,OHZ9faDO0Ew,iS9AgQSkNe0,B0VkJiJzL0A,vD7-iDa6TBc,IrPnu4R6jiM,1tfVDCMCPAY,-ysYglZCcEA,B8A76bR1E-c,ZRkG6xT1YGc,U5fT5hKOaaY,N94arh-0dNc,ejJuWdjG5Zs,MRYwIPmpRjY,N5Fmy4zg-gg,xoVxPzST4fY,0WjidPAPFTo,bvUsTddoP0w,5JZf2D_7eyc,2K_gjmLWHYg,Zp8CHoRxtEc,aRfByHC4pao&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=zTn7DIG2Nfw,jQIfqgVCZkY,wpENakUGoko,89EQDORYNtI,pA7WzggcoaU,9ZIscbogw_s,wLjDnW_LXVU,mquwwkHSV7I,b3iHG1NEHts,rC66il5L440,lgIEPXeOwXs,KItW4bsdkO8,lDZ7sLLC5eE,hqpBaLC9QRs,UrNrlURn-o4,lE9zx4-osZU,dUIUtwJ15Ew,plbb51d4_a8,tStF5rs7pVg,1ErPoeIjHyo,bPE4Qrzc55I,11EMf0qStGE,9-QWVfWed9g,BA5qgJdflks,2QimjDmlp-o,uAETA2IKXbU,phZesQLq2Lg,wbTB__WK5PM,emxGN0aM8SY,OXzfPG2clU4,pp60VndVOkU,Y-NhS50baN8,Q4LM3liMR2Q,Tdd-zDlMRHQ,ITuiKXsqihM,GYWzBT0zgBU,Pq1-K5ojAL0,00jIcl_jbf8,7kLZ8cuyvDU,MbIh1h2dwWA,xv72dq-fyDQ,qAOH3fqRk6Q,4iotHZQKf5Q,qoiUVwfiiVU,sH9kLBGIrkY,KmoOEMECRXU,UhQBR8OKXOE,FXH_go2k-bk,v0CAD1Cig3w,4cKMIzxdFW4&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=Sgjp0MsirGY,UJKFk3jMqsw,GuthXhcNaws,OlQmwO8PFHw,t8tq6mJh9wA,SZr4rf44ND4,FVVGM5xS4Ag,4BIkgYk8GnY,EWmw6d32oNc,zG8e7SgJiqs,HVE3t_MUTxs,eWI936QJLF4,C3DxqMQKRiI,abJ4FULrB8M,22VBiAVJ6ww,uYB8STaOu9M,PuHkCpOSdpM,cj1p_f9nMlI,Ncbwp2IvWWk,BrLUk8e6KB4,zAv_ZucO77o,eo0bslrSgnQ,hGOOzx5fC30,Csmp7ZEK74I,hdk077dJuWg,hAScVVMckjs,0w-jm9XqBbc,XPjn68HGGK0,AFJGg2gBiig,SQZkqdFQ578,iRHkU7BkR58,QUv-7okWBoQ,rntiU8rdBLg,uU1WULpX-bE,gnZFtIBaBpA,uN7k02RbB2M,MdqjaAzrYcc,6MdgOwAwbH0,3Z3QDVEKB48,YfS9Bwi8PAA,W0fAmTkDgkI,fI5BqzEsqtE,3gwnsE50vas,n3vXxJssHPI,c370tW7spMg,lstfqP2Alpg,hm5oAhCvPHA,oErahb9JmqE,or_NTwVOdow,svkq7ULXN4w&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=ISzLX_zXYYo,jKIrmxknG1Y,heAMXJafWpI,IKvfKMNdUv0,2Qz116oqWtw,tdD1IcwBahI,UdDpqJsf4So,IbzGoKYf5Fo,ePTygwyI49k,SVH4zosT7CA,7yMfv9ddZyk,HoSL1HvPFZE,dflf7Sw7nt4,Cnd1zysWNhw,m-B2Dm_8FdU,qlJ_AX9ta5s,ezQE45QzLg0,NEWSI3GkCe4,6WY9VYW8JvA,sfPDNoRlQY4,YoOs4Jq3PCU,Av4r8Fw9TSI,TJMnmpT_kqs,m7Zo6iaRQ8g,hkojcHH0KC4,97Euwpg28Uo,maPAoK-Nbjc,p4wLarg623Q,01BEJe8LCqs,MK-DxYWSqww,GrMpTRfKwEQ,AzCH_vjPpUk,QJguXOua2b8,D2_vxVPwHM8,alep8mqkDtA,V6r6b0BsEfU,gsMjQ-fnaZ8,8Nv05zAQ0iQ,80K5qLpLNL0,wZFy8GG4Fx0,YCkFhLoqONA,DUYk98QgCT0,mvHSsZLKD9c,fjSYA8IksXc,Ap9M0i43pqo,pBcvkxJFDHQ,Plplu4rxleo,WXghtyXu4Sc,ct-LFukNbFI,Mzxupj6i9tI&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=7_FxZKAbDcw,AQiwz9VGN4c,BmfeB9hAZpc,B-iIdivc1xg,GEYXRwG5wYo,m7sYK8Hb3N4,ns_2qRsMj-M,E3L4cmpOyhA,fW_M5UHLbaQ,0us02nQPIwg,doVRuw2TesA,38Y00G_zxdI,6hxK3qQR8Gc,ULXwSd6orAE,RkBE868PzRc,pXje90K-vxA,xIczw_H6gT4,N2W58CSKlyk,aU-tjceD8ls,dTH0wWoc5FA,kb80sq2b6fE,Af3oVHMCEio,VHnubZaU20c,cReJmdjSoOI,XmB50W3IewI,a1tL-rEZFtk,yZuFRn9Z7q4,A6qXnXLYKRs,r-ELJZBDUgA,ewzr3JnIv7U,G_bth2mSunA,oCwlaqhGQP8,pFn_HTIE2Lw,T6bGtJPUT_c,x5b0NDGfShs,uIVdLO-9bhc,HbxXGW0YceI,1m-WhrVniFs,hSZ3-eHczSg,jRy-AKZPGX0,14spx_7J28U,XPJ7Cue_hL8,phxDPiKMrcA,AkriZQ7-rQ8,utZPVBdPsto,rRDLzJWcXgw,Bu5QurvrceU,o6bUreedJPE,izJHYaFvvGc,JQJYI5c1fRk&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=oHv59LGaTWk,QY1N23fGOTw,ZJKZA7MRciI,KpY6JP2UxlM,n0BuBkp96SI,0YltFxR07HI,02-utKo8xDQ,4MZR4r_RhVo,P7jT4q2hQNc,4MMbxyIZl08,xWyBsCivptQ,9hv3ttRZQ0g,BR8vUeqBNpE,fskPtSQFtQQ,MWUA2zD0RL4,g9q8rmglvZc,jeNUyOtjHHc,5Zlzm7KGkxs,vT7YEtHsCY0,KnkJMCZdsYM,1-8zN2R_G_U,a7XmWMw9PX8,bU7oO_sNEH0,9lt1w72FdZQ,L5Jn1s6hXmI,gxcRo7UkAvI,F5ykljpQSs0,xigF5-OgMUg,AdcYuATMEO0,X6c5xbdpUQI,3hfM5ALKz6k,UIfttcKMrGE,rpIsp_CgHYo,KgA2Ajzux_E,5OMjTFTM254,_rYtfDGmPDU,Fn9VgJTRz44,y_6BmvTS2Vs,d2UkMs6PWtI,hN_UOpdmDlM,qbDn3vx5n2w,rOAGTB0b0TY,BEilMpu0JUU,TnzD7pdPt-k,4AZGrhbWa7Q,sdtzhzO4Az0,DkxDkjzUUcg,3xU_T1cHKes,ldtXE5GC4-k,h5zuidDs0XY&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=tiSuF_18A3w,LYG6kkaZ_C4,P7bCBgFir4E,7q6oj2SDL9k,KabSnkLgsA0,-EJbYliXBtc,S6SmGPlrZ1g,eRRu8j6F668,-WwMUlNS_W0,XIdTz6fCuCw,6U2qzpPP5jU,hSean94kCVE,IyipWy4lN1A,NhuJb7ZG2nw,YEEfuwV8UNo,Bn5OlXoi9-g,7K9uG6ITl-o,kSkNsLMhNFU,V_PjwlmW-z0,brm5LdWbVlE,LV1soaukDRk,UUrrt3Ywx0Q,mk71MWQtgC4,nyHAJUgEgJI,fpJoDke3b2c,HnaLy7qLi8Q,q1DICxYuyyw,doGgpGTB7ew,5tKGMs-Bf_M,wo98WuSj-_8,_SmdE8sCPJg,GTBMa2KzZuM,2WU6qjvf2_o,KFH-W0m9Hmc,VfNylUqjHkc,Y1cO6Vz-T8U,GizX4sd4z38,rkNRPumAVmU,WPzJmQSa0mM,-W_fJMTg_m8,PIqgN3xEqVk,4vpIaZQofJo,IBfi2eJXw2M,NrqIfPNcu70,ZPl4D_nbwDc,FZ2Aq1wshIw,ncUvtf8KlxI,pLvJQdgfw1s,yhzzfpNqh4U,OCVjifaAA4Y&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=kPEbcoTCA3o,VdiRv8ENPKQ,QZQJTvXrI5o,vx3ZVMrJFPM,zvfhin7jYvw,5WsWObWL9SI,eb_FDeAkTBQ,xQ5XmnnpJ8A,1gArLb3TB3Q,JVW-_ru3BNo,qVcIkkUd_o4,NLkhWV-U5a4,MjyNml6pm_o,RYesAsQIr40,gFCFnobitcE,_DiMQYCUMvc,q8A-ui8o7HY,xNT0YHyW6Ns,-jMBqBG-kKM,Py-gN3gyBPY,5aCDLwUnnjM,cihOJqzDSpU,P1gAe20zzxI,xSMMKQLyOII,UUoLJN7SLiY,oiAGkMClFdA,pBZoUJZYQ2Y,rxn7VWd4nag,R_A_1aqcj64,okO2euCDNhw,0HQ-dFfaAwA,nWCqsz7ZOdk,RVEcKxYK5yk,zuHMAXkWdgg,nlIqM0hADkc,f7k_Spe9u-w,3_zlVkpwV0Y,8O7aFbCKzxA,FmvB7YWc3XM,WkGKFQorAQ8,c7O80tS-vDw,bTJhJrnZEAs,b4RRLql5P5I,Wq5XLOVbuP0,M9LvZgAwkqk,28Wjb_f7CUA,SKtrKmfIPUw,Cb1NEjuB6Fw,cjrAW4pGqgU,4bg3A1vG_AU&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=2XwKISBcLCk,2vNuAGc-WOg,C-AALR4KDnM,48MZyt8le0Y,7C_DDxxD378,Y-2Eu_7sFr8,syRVIWQHitA,aZAQdfaAEUk,8sPdINB0mjg,jwsaaecQ4fY,H3TQHbiQ4ec,2yx5imVlCCY,0YGAomqnVu8,Abp8Kwn8u28,CsC3oGGl0Xw,LEjrZAJP3oc,uPmP_LkZWSo,_j9LakROgvE,xSgvgLEJ1bI,_Gz_PFqlKUM,Ut3Vh2OP2sM,A12JjevF0h0,Ehnfr01RHkA,5X0ktz5UMbY,XqFFHJpLn2Q,Db4bJ7hwXW8,7gvUo49xi3s,S0Q8lIjdQdk,9qFwdb3uhys,HKsD9brruTQ,QDsAVjHGBuc,VNuqRxB7xZ0,e7JqbN2vEho,BPp62hol8gI,q3fu57MASBg,sxk1JvJRBRI,aJcr4jwb8d8,gp6JVVUUl9Q,K9TPiWuJzrM,GvG9l61b-Bs,FBm0aehdv1k,Y26e6xQL694,iKVRsSr-B04,oCCbUjt5XfM,bcDq56l_XtU,AWdOCTAhVpo,MopYswPQUUw,ieI-7Vwe6nU,A95MJ5bTdPA,M9Ziz-rcKFY&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=f-g8nsdvv08,iEfModZtmWk,wtpxkNHJXxA,xpTMPBsWq38,_SCWHdiAn-c,wHKixoeuVGQ,d2zynSFOCm4,U8f3NCwH5J4,WA1hmo7Suas,4iHYoO0YAl0,7ZabLFwHGfI,x2skV8LH5qg,kAFx4Wmojok,FL41NoldNWs,qUyuKSPbwVg,-dMmb0vbWag,GLu0bDHuM5s,lOb5ArtT7X0,_HFJsDV_O2k,hHPyl0Rm4xQ,TlfviRJy7Es,Bc5oavID1wA,G2t3n7lP3oo,WeZAbCzFSUw,mfi_B36WdBY,g9xgr_k_PtU,6yEyIK4FYHY,ZHmNF4EbTu8,R3jPyE_PbXo,kW4LOPBvJAk,2BH2kAbEq_M,_2EaE5qPRhE,64D2iZBMaPQ,MjhiaIaZQEY,mpX14S9sPWY,q7z0vPvN3XM,JknF90ukHH8,KZl8CSqCn-M,GFUYztee_a8,MfJgDlsqiFQ,KHx171az73g,QwYo_mVo1q0,tv6xZyBKQFs,JC5UQ9s2cg8,c9lo7gJzVho,IttOe8DqoCE,zsYsnlBsSic,tZvRp4svbSc,nFJDYFRwE5g,-65NWd-GVig&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=xVUtnv8Y_6w,dWa4tyzrwwo,S_Gfw5WbzgI,ZP-bOTVM14c,NFNrPEJa5P0,aLmIC7f_7RM,YdRvM6qpb_Q,K36rYJ18tPc,qoFY2ewXHSo,i3tiQlcq7sY,eaIDoaLwlRA,54szGTZpmvk,EmjnVJ1fZQ4,4POxXwv-5qg,hstL0z5BKAU,UEHp84NjaLs,YRsvI1wJrWU,51KbSEGgDKw,OgrKXE9lGq4,bPh1nxt9mjQ,lkI_LMxI5Fw,5D0E1W_Eiss,pFeIA03abAs,eJUdfSydKO0,b_7OlMSCQJc,i0jI4-swGZM,Ovdo8zxeCpI,dgyWxKC2mJU,g5IxrFUPGhk,PJX4Awh6iBo,Nu4uMt37TKA,V_b6ImD1J1w,Kwb1w2jIIFg,Vn5Bi_cVSAc,GZrNs1q_VUE,b11fB4psA9w,KHeMZI9H_tk,XCJ4qSXuSng,bBGMx8J-Ku0,LwYgeufLyb0,E_g8BLCQdYI,E1S2_lcaUuY,Z1jhABefM8w,sWGT8Wztnbk,YfMafX96oa4,RkesRV6_eQo,1--R7uGpTTY,Zi0M2FrXjZw,_rh6qYYsSXg,7a-pxRTsuJE&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=UhcNFT6RpMg,WOu0w0wqMkk,cIX3OZen_VU,pKlZpq-hU7c,jYHp6PQwgFM,zPL3T_qI1lg,9tcl6aMN9Rk,bKEIgM5eWJY,0FWVr_3lyo8,PJgrB7VCDZo,6HsPH-em_1o,UpfgdrTshzE,6YTzuOHzJB0,SUnA0HUg25Y,Etcs5JB-p-o,I-GwrpYWdgk,RANVIwOGmSs,9R7sM6euUbQ,h-ajHStvz7w,ri_O5YLg3Rg,X3Xwxbq66uQ,tXHQJvCFXmg,lwRkleQzn50,ILKrSK2yKQc,_3Cn5sU_VBY,Op_CPXGJuEo,wDieCuxQdZ8,c9aVSOy9Y_w,-im-ZdPxXoI,1dz_xQCb-1k,p-DevXm9iEY,OGlt_7mLvC4,UOt07xvBd_Y,DKSRoKfdiT0,wYnmjMzRm3U,LZTbOvdMloo,J2N11BKO9OM,vULFUlMs24c,hQY2sc0GrLc,ERkoTqg2vL4,QYQ-adeoElM,S7X6CuaH-GU,JIkXT3p6IsA,lsYydu0wNqY,eyI0gmO6mUM,6-1ArFG7q34,cWkhLJJnxNc,pHdpSQhPEY4,5ksl1QnutaE,2ejRQdcMfXQ&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=OgtWUgKLF20,eZm_hwdBrcM,_c-pJzSYuXY,fl53lA0I9aw,cM07bpz4ZKg,dF7QQWEP0vY,x9EChAzGhhw,PLyg8egkPOw,CALJ8ZdXSZ0,F0GE9nd-w58,yAqMyo7RhWQ,CltvtAuVJKQ,BAaw2iGDbio,Ws7ylGgGOBE,hg_TCxeTiHg,Ga01F4CcL7s,7RjXCxC79JA,sxWIy3pdMeo,4jK6UFP5Wbk,rrKoxNs7av0,_Me9DrVXOak,QG9MdyWUSds,HaiwffMZv8M,-wG2Lh4wFsc,YMjc7O0p5Oo,7Uu08O3ygWY,47oshRiDwN4,ouCeqOvqdWk,thB0AWj818o,d8LSdjJknF0,-HsjddnaZUk,A2AUh9CD0ec,xay_n9eezO0,7YQmmdHCPcM,XRn1YKg4OFc,5sXs3lzB1kI,gTuTOoRXDm4,lgQExS4A14c,9t4XEqhQ5IA,F1JFeIXGC7A,0Zr7Y1091BM,NRCSTnZrvcU,Wst-ciOUDLQ,K-emGDnvFpE,TTwXTCdO-U4,-y4-D-EUdkQ,9VHJrihwu78,gPQGf00eM6o,ECsIHz7gyD0,e8jHDK88-NM&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=6kaHSS-ZW-s,9ns2NbciddE,x6Yuls-wyeE,p8LjuzkAd8A,N8LEzk0ugOA,1CMbax2ZABA,PJLFiLkJTWU,Lm43vGfu1SA,IloArHAOdC4,m3HeamstkEY,srRtpKGK5zw,KljiQMLTpxk,LNQk2pe2bpk,B08Daydxea8,6bWTrEl7rgw,HnDTNubH28U,EkdpC4wtdQA,CtFmeMtgHi4,j6VDOD-NcU4,UbS5sPjZ5jw,nMuyKavg40A,jbRmkkBjl4k,XOMi3L1NGnk,2b3TEpoXlyw,GWA12aQCJW8,yQj2HPCwQ4E,AGXPzs0GH1E,y-DG-xIWSJA,BBR_VE48xcg,GAbpL_WD_zI,84Tb_iFe07w,YZ1nmjww4zk,jpEyAtDwA-s,0vUUWGQRIxA,Aw9HHsp4ZG0,tmqcPIoRZiA,gAcIAxD-CqE,0ju1yY9fdv0,c5KPQJTBbR8,gmD1cHtBlG0,AoyVsiQv4kI,hOR7ia4dODA,IlUW-dnYJmg,ItydvXbvL3g,a0ErFAUmIP8,jq0K4nZoEgs,JzTVsgfUAzA,_ZG7CUwY4H8,mzxPg3kSmks,x3mrupYSLpc&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=UTn4p8RpAz0,KglpUhfl7kQ,BcwIJI3iZ0w,_cmyDY-78c8,I6IdWc0kKOw,y0atCzvin3I,7zbhKh_12MM,lZkypJDy2ck,Ospx1GuWwwU,rBMxBdWjlWY,R9m9jtMI9F4,Hn6zSpqp65c,ghlJzPxfZIc,aff6tDuHjE4,azkxFQ0g6UE,M7EKsgAN9yQ,QcU_MHb42BQ,TC1zVh6_564,xe93rYyM7Zk,yLndKnoSZe0,Ul_nLTzP-ZE,09qOjq_9QPI,4aM65xcTTDE,S9VujYxJnXo,-Wr__whHRoM,tQT7NA-caxM,mKsOd0lCb44,OT1uDRxKPUA,9WAWmaXHpoQ,4w2mJ8DmENA,GgoV5QjQeDQ,m32AwjdG7k0,TFLmse69IGE,7oqjK03C584,BSIcOBPOMeY,VDV3g77Ak6o,pVnB14Z0Ymk,bwv-G7QsY54,jhhbb8RL3PM,_tMy8up1fOA,Hjb3gLaRIqY,0rkkvSoGvMQ,ZqxzMLD_faM,I6JWcy7B6zE,j48B3lrJ5Uw,73MpSrc2pEk,wY-Lch617fY,GFZzx9R3zEU,fqBf7RWpIQc,x5KFK8_gDIc&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=ehwTy5tCUGU,i3gdClhZxjA,sp0WDN0QlFI,Y2COmVezJPA,eUcXJ3Y0R4Y,dKWvRhaJYIc,sy-BGJRzwbI,-ODZqSdFCRs,CWS0umyHybE,i9lLmx-cR1o,7iSoqQEhsvc,xDkSbIm2Woo,e4wN7a0DHOU,YlfJfc0CjSk,qG4o_Tb-aJI,JCDPnOgX3OU,UONLNRXCIS4,dqOg0bCP-Nc,uXnz9cDYCnY,_Q5sr_BDki4,BMami2WFdL0,szU-ewPTloU,o-rUjUitZZM,ofjJvJN7Hfg,btg356g0nX8,Pp3aSFIR0Hc,URU9EGibja0,u77HxB8ZaJA,LL7hofKa2n0,RmMcCpa42oI,q5PQXajwjQ4,U6ye6QchKMA,HNAx5eNdZFE,HAc5FPXftEo,W0K5Y3tyz74,0XICDeO6GI8,BggvY0u3lQI,ksJUVVd6noU,oBa7nWCkte0,AbsP73GXWSY,BEUqHi4nd_M,vYkP103KYRg,aZVDC9Gza6o,FM65JwZOGGg,18J85x_xdWw,WCJea636xv4,9mrScVFknes,sTyGr0eLt2s,Ec2aVvk999Q,4_cGdBzIW_A&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=sFu7-m5sgRQ,cePbN4gR1O8,aZOOSMrOsvI,7f2WLLJdZiI,wMu9iU-yy60,9lC3TZeeSbg,Hwcb13matWw,7kUW4wxDBos,EAHtjZKpXyw,UafVvihBkdE,lH3hGabw9c4,tDmBxoGQk5s,9UgTRviOZhk,dTLLgI1-3es,vT3WOuJn-p0,ykeirDq08I4,xnu7MiO2f1Y,1FyXpmdYYu4,6T0Hy38uttE,fqkSR4uOx3w,2jt-kR-3xoc,EsSj9bgOx2I,w-GiusKqD_A,6ucVbBBaS90,buK5rx3fnBk,S5Ze-J1nfgU,GNcSeFhQNnM,o_lvx8cVi1s,eOG9x5XW59A,swVxaFPnZUs,DZdZ2o6zx88,pGjPw7AiL98,JhsxXwOefKo,9Bz70dGwuZ0,qLIURKpQ9_c,3m7xRDGJBc0,VRyaJ2Rwo5g,fobWTm2hmW8,gsLTjvHdzvg,mHRzLBa08YI,nNIpfSMxkcU,-SyXWA0fFKY,VRuGxevtLGo,GWGF55D0tFM,JEdd0HzWCf4,wHsV_ZH_pLM,wePLTZ9fKL0,zeytw6W8VaI,ifwnJR3xBmA,5p38yGRXXRo&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=0UiieHugWPU,vEG3XWS6Cw4,ELeMLcmP394,eZrRs8BrsYo,DTWmdBgIGV8,EPoU8iQarLw,V_4ys-aHTmQ,uRpW6JPmC20,Fr35eDF4Hj8,JaDBv8CXOIM,5sl6xLVR6F8,WUPUQ6bBGmQ,Mu9NEE1Xgi8,q5wZ29AnWAU,X8O3ufCeL8M,mnfeQNEMhjQ,EQ-kis0L5ws,Umm_dm1WBTU,XgpRmAFoDmM,xXwKstmGGeU,CoMA51fIQmw,4Gpe7iNVSFU,XCUHU7errpI,-_OGY7BcAnk,yCmTghOdrxQ,QggIA2Xn9JM,ULVFdckFJp8,1SKYC000lO4,Q6u1O_W5Y8Y,mfpjVcB9KLM,_r9mi0k51fE,Dsw0ME_QuM8,o3YAivsZ3sg,MrHShHJJIhc,fT1Zzdok9qI,jZgVZR8gBZw,3XWcgMVGm4A,9T6JrWJSlGY,X2LHmXnl1cc,C5PRNfs_S7A,3dsqzNOP76Q,-PhZPjuB8Bk,Mr-uTyWS194,N_emY1YuDuI,MSGUidGqBp8,HSR8hpSNs44,FQq5yLGlkxU,HpcroRYJ2hw,DeJbQJjjv5k,QBwtukyPKr4&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=IQl3ueLWg5E,IoXhbt3ynAw,8gg4auwH8XU,aE4DdX_NDd0,NElVq4ILiKQ,YLtRYcKZ9-A,35tpvNdBKFI,1EEYzLde6eI,pAVDsONNYMg,bee7bDD18go,msBR3LVcBT8,tbJnHDU_LLc,u8yoUfwthpg,zZi5vHkpAC0,tUvfwaE6tgg,UkP4RavteVY,SSYHBfePhRA,0Gr1-iMIRf4,dazfA89Wu8s,tOKQUVahlwo,eL5AycCDG7E,B9DVf5KK1kU,E5sKHsnjvIg,v1tzxDf__S4,G0KKZ_lj0v4,yQQzGph6E4s,bOoM2LmLFb8,D9rCaH-9TWE,QKiq1oaloA8,NyGXNl22Dgw,bk1Oq_gPtmg,GqYn6N5OoTE,IpGhKOzXHms,MIttUMKPq5s,IpOUcN6zAug,Gv6LPUaZiF0,072cbCkUcSk,xGSYmbrb_co,oGUtRvChmnk,Wtl5OWQ28pg,vYaliNU-thQ,VzM3xzYcSsQ,1-a6e8H7w2c,0OtZ1KmxgdM,WfOiUS_cltQ,7FA1r1JdPB8,tEEzZ7RqcFQ,lA7ZMXrlpF0,NsyHMZEXyFc,-3d9CNmaKtU&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=jGjG3j3d0n8,79FFDs_1_XA,z9Ob2gF4VzU,9w6jYU4Fn68,AKic1i8W8vA,MFXTFHnlHpQ,2Ka6xu6JfQw,drvqHKg3Gu4,RhQTfo77Bjk,vzQOXLgh0zc,8gUiVrC4PNo,I-D3ITjuNCU,d2WaqjQng8M,jUfHvU4hrxU,FO-4EmnsInQ,TGk-O7TrGT4,ACoxyXImBoc,S46BXiCo2l4,-qowCg2kcD8,WO7GewSBf-U,xWYNMtjfp3A,k2QBwkSvNxs,oyCzKEeW_h4,APaLQlTCepY,_Ddf61taqDU,NePSXIIDui8,MYcpVYR-mk0,wLj45ITEFtI,gN1wri5D9GI,VgO9EFo8bHc,yJMldpzLQl0,bOSmcdTSbgA,uWQAO20pQZk,MjsSfzEhQjQ,Q5F5YZ_qgTw,r7HhgBJ5f-o,0ZdJ1sVrCUg,eYcxD8GjcS8,pLt5AfcG51M,ldq3sotaH9g,LB2Gw6EPuXk,vaFZBoDRNSo,aBRYWXT7WlM,SrWM0NofKVw,2T1BDfbOFR0,7bdqMOPiXnw,LPfP0WDIeOw,l_nHdi03fOA,k5OBjliN2OI,hUuBF6VOh7o&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=pYRzPPWFsRo,Od5mwPZh3Ro,u7njez5Yq7Y,oGhEgptMAB4,4v2KAXLRKR8,b5je8tgICfg,fL41pNEUHy0,fm_syaVUWg8,iR_gvxLEER0,IYRmDYzESq0,qK7_MeukbhQ,SsFangiSZms,3PhccueJgXM,3uDsgmsXpxk,Q9G9_DUmq5g,FXzUpTqRax0,YDiolDthsYM,PsFE8IcY60w,MN5-eA3siEk,DIQ-u0GzTnY,P39UO8kQoZ8,9KmZrWWIXX4,SwoATIhioSg,AWQnbTSJHY8,4n4svBZyrNM,_5IvLHEWOoI,9b3OK-9nrJA,iT_nVVxkFQw,uHju7_40GTc,ywGjuwAua2o,vRI-TA-Fb60,LhSDyg_hIaw,f14gw389i2Y,hxhGWD3o9QQ,luKgwniRBj8,ZVXfx3lxHnM,mDRklKTrN6s,8toTSYhTSxU,nDoswY4SKfc,WX72wR1oNJE,sOh4_u9RFpM,Ji1g2HCT1jI,z7gV00Y0DZA,Gu_Jps6BxdM,HRJFkoVKjI0,LYKkQQfvSIw,RPEwh3TsTxQ,EMyskArHG5w,6qxEY4bpz4A,KFTomPjyzf0&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=Ei-TUZJDKBQ,GYlXgHGexSo,HV5ESvHmP0A,cIZK3t3FF1Q,8uqD6PtROuo,mAIXuWQtRnk,-6lWx8_9ZR4,IAoaxf6uDKk,SGsIGXh8KJk,C0wpgd9izX4,EnVnho6X898,CeieJVzeGNk,xPS6XrSrVtU,784UYMRy1d4,Y39cR0lhSS0,e1zmDEExwN0,QWOW_gAT7LY,EiBuuNuwTPg,DIhwssel-kc,8aF5X3nwBTM,D-dtLQgoKmE,7bpdwskv8S0,Q_h5zD-lln0,gkjzN4BXKJc,Y888EZvZSoQ,Z2ZI0aJ6Z-w,rOtHW_l6EIE,-hCtwYY-Yfc,NfGD1Z3YGVw,dHDmp2OzGHQ,qO_ZPkddHhw,252j3hPVfx0,jFpeEqz6cQI,WHnu_ZjcdzY,0Q_b-Pqo_f4,G_qvulslt3s,uco4pETOTL8,sEcQ85MWbFo,B93nAnTaB-4,yqHoHaNKvhg,wFXKmkOVBmw,mLvAZqGt-J8,w-2vKiq2zvI,NhzjUctSv1A,PSiA5oluVeY,EwpOfEok6xg,OI0srYj2dwE,LXheIbX4n60,x52tNVTutig,wB1AgYtNRV4&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=Oy_v7lLYo2Q,z_lVZjhlnvM,BPczX_dKfdQ,iD2Szr6cAgA,6cUzS55JaAc,N96ajILIY04,9tOCLy9CKRk,oh2u4XT7jZM,ktpaa6MAJd8,her6VVWpm_E,XK1E8-HGn78,vaTG3IGP_pA,FY9fprSkBJY,KxIPdCoEaEY,uosfGnIHLy0,6RU849k_ykc,zi20Lo0rKrw,-uUhRvs_i-A,hpR8BbtjX90,c-4Z5W95AnQ,0klnRR27Ie8,CtzS9w8l7aw,usyJ66dX3nk,-nccD1UwflE,BY-G7SJCUkE,PRWZhtaru8M,3BhKaeN17IA,NiSlrDy5uiA,AYZ8wQ08ptI,AhjxqnzrLww,cer7cpcCEXg,2G_J_x-jfg8,QRzILfw8nEw,NVWx2Sruf_0,DfSsWo4iB1g,dsExJkCYi0s,muMhvuMv2uE,_-_nkw6zp2M,vLQ1OOJ7Vts,tEmREJz5GOs,x6-riDmv6cE,8WIJTVcENAw,NX0-qmGqTsI,5_JtEklP6ZA,FfJ9KppcYwU,njucomOm_mE,MOQvvOvvL5c,VMAjMTP_r6U,abU4-ghznYI,HJKrHZSR3OU&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=-BUlSWo0SbY,EjH1aIbVkJs,1ZhA6GF6r6g,Sc_sr1g8SEA,IKS7Rs06y6E,Y1jTpkdXVRc,yAwzWTysovw,HPzSX4fSJT8,6eR9D_3bOak,fZwURLLKPwk,hXI0hUM9q6o,jCvt5pCFRoo,zDHB9n8XYuo,Lil46GUmerw,UIJPko2qV1Q,IgmOxrLvPfM,4RbEY7X_N58,qtULRqK5b1c,kW8zxi8_p6s,L0MJ5TW9ucI,stcZXOZ3ENw,-DKPim_OoRs,CapweGKq9Vw,dawKH6uNXBU,9BL33KScRyA,LKgCiZcwXg0,HGEckBo1vQo,M1qj2WnDOXI,QReYu4j9q8A,bLIhwYsfWtE,PrLsYE6FYeo,376b5WDjUkU,Liy8_IKKIQk,7QsqkEMO1BA,HM-D0PQ4RAU,3BEdoQ9jrAY,_ZCc4AuiwMg,FX-jgZ9krjw,9NBED0ke-Bw,8Ct4FsJr2f8,gQ6UDsPfQik,B880EYAQibk,MpTJ_84s2wU,1Yr4QeiF9EM,GSFQZmGoIJs,1i33vSgD4PI,A2eg03zCtw0,G1OaYTnv5Cg,SSbPTBEUT3s,cFzjMuxMPlk&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=YHlBJfmh55Y,cd2D96Tb5Rg,tRWYwblhSvU,9Pt-VEh3J0o,ZJ8WUzN21gs,g85y2eMMYas,Ikflm4Zlw7E,mjry0jDaa94,aVMVD9_zaZg,Xqi8MooImv0,7WEpEVDW3Z4,3FB3nbbimQI,WFrR09CYAMY,0MSHnz7F5QY,o5GSCocJ-RQ,HZHUUJfKJhQ,583L73PQ9Ag,b-mRCSLfxOk,sepE5WqWoJQ,EnzBJkwCka4,Wa_Dv1Az8xM,2I6liRG3eD4,scp9PiT_b6s,SnYbKWqQKU4,mNl69_6n0DU,Do5RRvhCvCs,Dgxo0Cm3Ks0,U9dPEMQHdr8,m1QYyK0LncY,1WaM_MOcy7s,GO1Ddg0tXOA,Q_kuEkazZ8Q,_rOXMLf1jCw,Hlmdnf8n8RI,ky1ENOn1eG4,eh2254NeB_U,aHd2WNCEiIk,6bBiq-Lpw-E,YCqIsuBINN8,g_2XZMJhrVg,iySwjh4q20Y,88i2fhC-s3A,pJ4FRqy3h5Q,IS6kKdiWYyc,DQRe51mPe2w,HJ7fXKkOwGA,tp4kOK-Rksg,N0KREEO1jpk,ev02lkLYgp4,4HAgwBSCzUI&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=Qb-KKQzmMCs,OjZbbhQBd3s,pqLTrvDnMDk,utA0RngO8Tg,3li2heolmP8,CjEbD9g1AOI,4t1JfPfnCcY,iGLISkY7Y6A,MDARzQte4F0,LtV1q46ZYPk,qMV2JuyVJSY,KxBFF58Xj5U,gPrvRHWqyc0,VuUDJ__Tc7g,5gGTgsml7KI,6h7bqM_neMw,3qWlIZl2gZg,7ExjGf1ezEM,o27XywugB6g,XsQnOK90COo,EOd03fb9h9U,f8mvXsBY89w,k2-PtjyxLgM,fxeTG3oOljk,-sCNXiUcZ-I,yB_UEyeEfHs,NVHqJRK79dQ,qmwCnQwWrYQ,x7EQmXlnSUE,azm4xF_EcDU,L9OlD62QjPA,Xow4kr1dlqg,f4liNQoiYDI,IpceTqRDYh8,vjCt8fLHpKI,vtTMyafNsVY,rghhnWbqa9Q,MN9CKzDXLxI,5h1nNDInEm0,6n3LZc8kX9Y,WZrp_OT7Gb0,a-s7psNmC9c,5du0Q6168Aw,arNX4A6JJPo,ZKd6xVvktKU,Hh2xJXBYulI,ykRwxi05PWU,IYdAeRJZAn0,x0zWQJ2eneM,Mxf2ZF3RRgk&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=2FTu96B9Tdc,C2yNSq84Y18,lL6qTeHSMD0,Btl8zbTqp44,s8XB_ZccuZU,UT2JOwzS8C8,b2aLQBnR3kE,TR4quLfF3sU,t54uix5ZeZ4,LDFhECsgHMM,S_fEpa2ZEAE,0Wg8LWdZPMA,9p3o2x3WnKg,NiUp_TUTG0Y,HPRBpCUrrr0,OZfQTplMNz4,aLKlgoMpSu0,42-B8WMWN10,KhRES44j3-o,ClK6K9SeG2c,a-vlyvj2__o,2vyMOKlHR3g,jq8mha0bmxU,PMoJWVuavb4,MIkroB6GiXs,LJYEcrv9umY,s-W9je9YCVQ,ydwIuXCIusE,j7O1kzrhuds,lkQcOO1kSnU,ih3LZD7mYSI,AyBsp4kSiH0,-AL2S3ECTqI,AW5jAoSN1Sg,txtSup6Hu8Q,30GoiLManLs,PAXf7dGYR-A,O1i5mk8njhI,FqSxAvgK7R0,SXUAW1zh7QU,VSO0pCyl4hI,mtkXUS8EAMU,izA14ehnwuo,SwoSVrz6hTM,0dSjnoFV0RU,vvfK2tbrPOs,SW7-8MG0Tbg,KwpoGEEti30,Gef_Mxuxh1U,dph_DpYs-Hc&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=Hb7idI1Bvo4,v6_Ik53Ue-8,_IOdEemPzro,_L9uSnrAiCw,XROBKuNWnb0,15uJt3S1hLI,JSTJCVYUe0k,fmbuy2NHQ1Y,V19j5txzFGg,W5GvjPN7Ux4,JMNPC7Ifv9k,yJxR-Jl9FdY,DLh-hexhgtU,_xPXzg-2958,xpWkCfxtQ-4,BKvrXG9RSsI,g1Ww5X4dDNA,ibZ8QfGan5Q,kJ4vEOZsjuQ,JuHdWQIQLRQ,w779B7BrdBQ,QaMLwKGqrrg,5KYBhIzWKFA,H_DMGa5Jx_M,6-JKXfITfhE,Rvnm1m73KJ4,19vVEbN1KCY,1c7-A4Gg8dA,LWZdKxthECo,4gX7oql4xhY,Cj2qiKruKGc,I5M2jCIHyxI,bYqJGcSgDcM,-RBJsdyF6mw,hwiwda_rbvA,SzIvSafPsPs,qO-NaktZInI,pr4FdPt-Q_s,iVCTG3oQX_E,JyOaNAY8BgA,F3uwqAfzvOc,5WGTpE-v4NY,RWxaucCYNz0,JMjhNS9CSrg,th5JDy28bdw,NCoSn2An9OM,TIKaUQ5crkY,aCDnGqaEdzM,dMi-l877Uhc,A8K3emrsyw4&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=TZcpTsBxKsg,NBf0POxJJP4,ILUXgXama5s,6YDXGk2LnWo,RHMq5RxqzW8,bOmkKagTphI,tjI5ko-Csb4,Koee6BgNM68,fp_kxC74TIk,mISzjN5F-GA,djZf115rrvo,0c3vwxcwkkk,7RPF_C-7BvU,kOaCqtFmRsM,FxAUmyow0LQ,8BGEfOT-dRU,KHj3Sku_Ug4,2rWe2-V90ig,hyU60SMv6Ts,NCCSkL1FMXY,u02obJZKpZ4,G8PnBYXWFlg,vJ1h1d5P5vQ,N6VIbd7N4qY,JDaVrJX-4xc,kjMGVNSk1sE,eTwW_LfXVKA,wXwn33dlw6M,gMzB8pFDnDk,-waSz2D7uxI,qCxRJXUQtfI,tdI0VxL16Z0,fBAPy9ViQKg,KtW4RPD-I94,dFjl8ALqTE0,x8f_mONlnPc,uzTPp8SSpNs,dgiqXNdD6eU,C8cS_M4S3_I,bp2sOvr_XKk,WOMR0a56JjE,UVEuQe1mJis,-HvLxMqbygg,5gMQg1uP85U,4GzZ6AABAn0,l2QgaBlFn88,hbsl2a6_5kM,g9RIoEQCiwg,UI8SDXfXyKE,-0-V4wH-FwY&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=J-3_e7Q1KxY,okv6ZM-d9hg,cmuSHd_DhKA,FsReUsHESE0,EdGMYAaoOFE,G0kCqqVipNM,QmRFJJR3d4w,lYNNPeTFarQ,f3svAi5HXLE,A1fYzWbHIzU,vyzhYvCelBk,xnqSSQKn9dU,9_hKvfD86RA,3rsReUIm0FY,5lVN4LsdCf8,s1Dkho0WeTE,GG6zEIOjens,DeXONaOnVBc,guqhL6DdT68,ST_oPjm4ymc,W7RWJrlHnz8,0r68wUJx40o,gm3l4HywTHU,TUhticoy0kc,fVYlx5ZX9dU,macyQ_Fa7AQ,ifl4VQrmdGk,zszA-MxM_2c,xF_3vHiJhu8,l8VBXP07Kqo,wJcreXDhrcM,QkbiAHMZwWU,qZYJSE0aipE,kUm5D3QNmHQ,s704Xu-4twk,hklbxfLu96A,lSFNJOPDr-o,C3aW-NR2HXQ,bJE9KrYbbyQ,CBkDzYoc8fQ,PELHtA9GDAI,Fyl7LVpqxhw,3joCBh5WfS4,qTPUyz3ywK8,wse4BVECSCU,5hPKB7H3dCc,aL0bChkFV7Y,y65byTUuajE,q1GcWs4ZnN0,IN8HpkKJ6y8&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=YAoHSSfIj3I,hX7lS4pvgoU,Ngyq9NDA80k,xkr4V6y1Zk8,HPWauOm8nwo,52ra-IXg_tE,sG_pVbMQSb0,JFOInXj9ZUE,7V74Z6Gtjgc,VKbWkVTWvaY,tnc_KO3tnFc,i5reNCUGcWM,ToaBPq0Bg9I,euDab6XCjjM,KafKPfRrk8U,vKPiGfQMP-M,obAeHt5_PBk,7ARR8F9zyKE,LG4yImYHbnk,EOrIHWdhheg,nZNI2FpAfjc,WWdVPZk3r44,1pDRLlvi_2w,IwIJMd3_ZM8,G91efAYNzG8,hPhn9w_ZjIg,35J-er1upf4,Kfjf2qCG0Rg,1QmlslfiJmQ,DzwWjL8TkCs,Q_MTwe-Cqz0,jZjPM-EADpw,31-DfQOIkpA,67dGePpXwLU,y9uKgFeMiJk,6rIcdmAwKhc,U1rMTzoxgEU,um54qfdz-Fo,O9H9dpyFLJA,e-d8qJhQFrc,4Pj4qO5rL8s,MQZ8xgjzyw0,8pWyjiFO3ss,A7M1theNtT0,3e8OjPaFkzM,BuVApem--Y8,rWaDOKJbRaY,olsiopz0yAs,lAzCQn_de_Q,InAjCWLTGHQ&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=_hKhIX5rHk8,41K9LlIskr8,3_jOohgPmKU,WYBbXcxauio,tnZxll3XYws,TqfNS-Uke7Q,Xz8J2mIw2AE,xBFR_GnJ7Gs,RYJAtJwWBSw,OSuYRcZ9-ls,bytahCf_KPc,TOatfbsfqOc,V2lL2JGJX0k,Jd961bfbVBE,RobLDraRCjc,pRXpoqfebPA,u1nidCCy-bc,bj-k1oss8L0,HPSagA6w6CI,HkFekwbXCJ0,P_Ol0V31dDU,cXrI2dMxHPk,wxNacjqfgC8,azEPss1V5H8,yIdbppqT1lY,zhRMIOmi7n0,7ki8Keo6kKI,VSkPgMzbhpI,sO39NFFb4gQ,Uft1XXavO-c,EW521hWWauY,YnhzfNnQDN0,OM0frxs0jOw,D4UqLP0Zvfo,utxmhnTVfHU,xAQ7_FJMQsc,I2xqjPtwYZI,1D4mfI1xsPE,rJ9b_Vfldco,NbQ9v9DhSus,x7FOt1NhAgw,otFuBd6ilPQ,ywEsDv4jUNw,w0EOCyLSLa0,tmEIKPfukY0,BG4bikRq7K0,CnUtpeNoOK0,lfyNcbqCKWA,BdjgcqaIRRo,jjef1xNanqg&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=cHWSiXKZBgg,ecXMfcYpDFs,eSlHgOujLvM,mFbcV2zaSeA,D1ENz8MQrSU,Y4qxz0uPZXA,RQVXEegT4Ts,QrAp9A2lTms,DCSAFSaOoQg,wrfveWjBSt0,-X5OncoadFA,mvSj0bv-_QM,CUCUHieoDj4,aikHqWFoGAM,ZT9xvY8RUMU,wifu4o-kc0U,iEL-f0yKaPI,RUQyUFvSdvk,JqbtHr1pZlQ,6qLqL18h_Og,mF4ysQNLxXU,p11JPPT86fc,pEQVwFdg-PI,VM2rV0bv_Fc,hmrvX1vbTcI,OB7QAAyb6mU,66vSjnX3S5c,fJXkGKw0zMo,UNH2i_l2mFM,bttfHTvlaKg,-9CyDBmmQ5c,zNbZIdG0Ukc,nGofkhwYKcg,af0kjR-5txg,T21DY_yJxF8,l9J9aB7zQ-4,5s2rR2E_8DI,XCUauzbcFCM,Ulu_8GNqdhg,d0A2kzJ4MOY,4tgxjc9Okg8,6WT2grjFjoc,1WjFVoXnrTw,O_HwzBq09gE,8wkUh0R6J5g,2Tx2ieWdK5g,9SQzhoNlE0w,Ig4KjdGHCMI,UUdv9V0pB_A,VQp9pKPuGIE&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=cf1e0-5BLas,1IZ5TZnDaQQ,0eZNaiI3VLY,rY_fjAgqwI4,YKVE1RU_83Y,YjsnufTy79I,nMpdW2lBknE,VmKhGVcWXlU,m72XSkcCAMI,Xrb9R3tfvjk,qVPD1Vm3B-w,UC5xz0iZpYI,zn4YAXOZnWI,Bxu1R7cq74Y,bw9MOzYl7c4,7s8db1S__tY,ENmh8GDGBDE,HNL83cM-c_o,U2stSQK6tL0,bpV0SMSznPI,vySoDDeDhrs,Y6A8BkKT-lc,0moHFd9KdsU,vgrvBDGbZ_U,WWhyF2u16AA,a86e8Nd7Udo,zKJxIcP9peI,IpSWXes1aXI,SunuthY1pEw,Q49pVbMu8eQ,veFrjAZxs3k,QzrC4FePSpQ,8GXTcFiF7O4,14YHmzMVtNg,z3JyZQXqWGM,eR7rw_-4GA4,Ph6cgde-Vc0,aV0V4cIY6gA,ZMMEx8o-2aM,oolgOLhr9dU,ov-VrWHo6vg,6_vS3iAPiCQ,9-HLSxr_WkU,K2Xn08399es,Sa6ZZ3EVKoo,E3XBl_38SZA,i7zwnKHb_a8,x4YnLTXRhCg,vLUsvrPJ5BA,100Qktu6BjA&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=3onBGJ1SSJI,WdieShUazWk,n_ypt3O4R1A,tBc6fzCpQfE,BuDMCHLl-TU,PPtshznHTLc,aWDOXKUPkbc,lZO2-GO7W6Q,HiEv5VNmR40,T4CehVn747U,4KxyH2a8Xx4,lUIQ8n3Lihk,IEwv6efv5NM,iOUgkP08ve4,5gYCF7DNmFI,oKxGrrkU02I,0lk9cVCFtpw,2ii2jPbTDkc,3es2rC-Xk5E,Q7zygGTHDeo,N55L0oYdY4s,5mbnmbSunOA,GNAq47plgLM,N-3TWp7mC9I,FjMScriGz8I,Y4aVtmnXcLI,gXqTt2ixBdg,wX16HHZtpik,fqtP4_A6F78,2XmjSiH1-4c,arIPrRexGpk,RAoKtWsgUdU,KcaToUSD6vg,cpoVj4zanL0,jDcKFWaJGrM,7Az4I9zOzv0,MZASaWlmZXw,gW2KQid34_c,H9AC2s3UmBk,NDuke07EpFc,2xNeP5JPZNs,ZX9mli5EOKU,CjdajfTjmz8,5gRCqLubVM4,M4pSx7TwnZU,3P5o7e7YmKA,_UMFzHxNBiQ,OBxjseojriA,8sBBqliHfso,CzGZZguY2ec&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=LP8qKb3laqM,winj3q0__gE,yDGV4HxDVRE,b06bwtACQ0o,-ABBFTanWNI,Q_y1MSyiOD4,FjMRcxQiZuk,Uq_kuH6GnLw,LdBKvKm1AQ8,MDF1QU2mwYU,yOxeZf4QjTc,uMRS9pmg1dI,IYJVHa1zBOM,3RKhyP0TFoI,WWKRLAx_V9Y,sLAFUzHOLZI,Aqea__ZhHOo,JF8_sy6VX-w,UVK3P4Iq0Hg,_puiOeTsx2U,6eh9FrTT73I,mZ2T9ZeA09w,1MP-JY6uI5E,WT0dAA8IdNw,FAPM0vowZ24,1UrGZYQY_zQ,Kl9KiZy41P0,v1FTJuH9WKs,0IjGkFp26uo,Rxmiyc0VXAU,pmHrM23hj38,7aBHPEIIy4E,TXf_wEH9vmA,Lfquv4kgc38,NRxtPTGEGUA,hcGwkBj1-4M,I5mgMQyuJLg,ROephR_7O-g,6sLpoxvuKYc,H020Rydsmok,2wTrVGpAwVU,0wEKu_msjhg,DhAZUj-knC0,m3rXs1kmrJ4,HK_rQDAeolk,XdO8Jbh_yEY,4OXz6hX7rm4,Ab975kkhOfI,N9qumu0iIe4,439RuK_PH4M&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=zRchZ36psI0,bftzNAI80pU,hNNdVGbBvCk,-eO2UUSFXhs,ofaemDQCrMc,O-cYVqK1mqA,VjyvnTRJxFY,jbV8jR2OlpQ,bQP0KNa8dO0,lB0vOh2Qc_8,7r_ZaFlY4Os,xufnYYahCmU,K5ROMrfariI,R0buuB0M7a8,2VZtsA7jdPI,ZPCT0P5iysA,YhffYU1G0Ok,bpgSnuybmyw,FUlMJ_E3Vos,51tB8kX3eSo,-TZqHKbh8rw,6r0FNgigK5g,dC2lvtL9PS0,GZ4SJMtH1cw,1yL4Pg050UE,hlN_1nI84os,M-gPTqj1dpQ,K8D6E0thH9g,0jWjz80W_Ow,od7P_XI47BE,MVczLitygIo,8GI4JzXfZnI,a9l6q21MT5o,L0uvsjb4oOg,WT6C6bkZ50A,mzpGYRtYiA8,niJT3fx_87w,jLWe7EnTd70,yUDpSg-Nzqo,eTNhAlbpEZw,fbZT9428zno,0vGvXcj__jw,bBmsIClNTEA,cIekdDScwis,OnvJmNAwAm8,UQAAwYLzOsE,iU8PqpCKHNk,7eVXTl8hswI,zOT7SmObukw,VGoOON4ZeIk&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=t2TfPQUSVAU,0KHSo5p-nmM,sMyfjR072Iw,LveacVI75ps,qce-cuh4cg4,EQkDle_GozY,Zx3rNEoouyk,4RHTkndl_Tw,i9k1DfdQ-H8,wK1Sywdm8GQ,Xu4sHhk9i-s,j7KqYTf6WZM,1g3JT0Fy-5s,w55CJPIc0Ho,0IN-ZK6nw68,MqaIW6KUpyY,-1TOUnELm80,aSorsQqbr8Y,N1Wh9jM9Tsg,fd4BDbz2tWE,oS3gP0aeCCw,eWlGNdAWZFE,_K82dE0Fe24,-ePBp7G9FBE,GqaWTCaZZGk,mZ3JFqK9uYE,yBRop2wK0Aw,qLQ9eZaBl7s,hTs_tgSgbsI,KcUGyVorb_8,1wyDkTIbf9M,c43ORKzv90k,0v668T833x8,uAO20FAr5z8,n68ELqWKTR0,wpOXDYIdvi8,MQ2geDHSY2g,aAzR5xIXbiI,Mqft3fmKNDU,NTZ0x8LtNEQ,BcgngDueI8A,_LWtyBUBgIY,-zctxhO0gCw,QGIAv9OdpRk,F0r3oBgtGns,3F8lg7QLe0E,Zp3WSMCZvwk,hlfMComKyGw,z70di3My5AA,79c4MLdWvwE&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=MnHxSWovXoY,8R1f5bNKH3Q,BsweRckBC_E,lbEaIrP7uMU,kAf-Q_1W52M,3C5q0gSd_j8,V4jFyKiD5pc,AgaUSkyJsS0,8k9pBfNmKwQ,Njc4ItAFJgo,fBKSl8dhFH8,Y3s5TtIo5SA,W9iinoYRN30,yIxgwdikGAs,Qs3gP2IvyO0,P8vgObUFV14,gtAdYKJ78LE,Dk10Z5zIxhg,g1uusls6EGA,KwfvQqiMsk0,fJmU__X6wF0,GSN1V9uRGGY,2Vw_-SsnKrw,1phDBH-ejNQ,LXX6lcYZwo4,UgsLL2fkuNU,4oG8FV1wFpM,ElxH20ZHTng,8LpNmnA6EPk,u9FlvTrrBHo,2R9iNX6CJHo,5H7G11zgqHU,TxhAXs7MelE,WfIWGclS9KY,mPWo0j1VLyc,3M6DB1A9YBo,DIK42zMH9EE,RzTnnwUNJLM,GuGxSjEjUcw,wfTd5kay0nU,axaBD8axyGs,7UMSYMcJyaU,aT4gN3YRdqM,Qu5Xyu3kyyM,WgmAdVZhWgE,MON22NhcqLk,ohxiVMaQpPw,_iTt74Mwp_4,3PJu_hnEvJ4,fkuXwHjO3SU&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=TNcu_GSTaRI,Zcl6jmeOQio,_vA8q6Mrdfo,uwNGi6ekWyA,ZwEQI3NbxYU,maIi04LHJHQ,4EcB6aVScC8,DjOGMu2pGQM,3jCozTd2Wqc,zkTElkQc8wI,BlO4hXufPOE,ZxIJSiBhh8A,_xZc81gZg-g,pUHMLXvY27s,HIB-Cils7JM,Shkp8g6osS8,IYN8jiuzOtY,Zsm_7dAnyM4,3El8qsHcZko,xcU1eN91g8k,i94HmJ3i-XM,TT9M9T-AzGc,Lwwcb1rwOQ8,Zcbh-5a1gIo,LHQx3ARdiOE,F6m_JOjaeP4,IVu32pgpUaM,O8MS6oxLR5Q,qlNxeWkYYMA,n1KjIVE87zA,6yaaAZj_7iw,5nz9q_9ur_8,y5twb4-vCsA,Az4OcMdPw4U,Vjnd4H4o-18,-s3Lyqwl_KA,VNWI5ut6MEE,f8s_J8FVJzY,LIAfM8B-xcw,ZJa_quDOsPc,0ADT57LtTRM,XjUMmmYMrbk,tw965yvU7ys,jj-ZS8SkZs4,1BBHUVjwY70,EUobGKsqYrw,jcGTWng6cOY,2FafgcjNHTk,bEYnvvBvAJA,IhDuOf91clE&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=R3PEg1lZhnM,9Lrfn7z2t2Y,rl2JEKHJaCY,W4h0EyRIUM8,XvIeHNS8x3w,gFfWEJFlOU4,3anBchzvWt8,0zdYRM5yX2o,2bO-ZtxmtVk,ia3bWWg9dlA,OVDSR4lT150,AsGVPQFqwMY,r32t_zp4Y3I,M1yftPmywVw,m4gLdSe0sts,dEpaQvopPl0,pwRSZve1U3U,4OqsSnhL2Cg,W1g8hyWcIxw,HhMbVIObDs0,BRP1-dz_Jv0,32_JOsYTy7M,Litikrzq4d0,RaCPalT0K7I,C7ePHQlqmCo,rszcVV-6oAg,chXYUFeUvD0,P0aRhEBTdIc,jMGswfpoO_g,n1XKoxaNXxE,x7jJ1jHwI1o,ia93HIovVSk,BSzmaLMV1Jw,logbXXHyJOI,NZbRW_EqwYg,83vlgTXfxLc,weX6eLQSLEw,HT5jmV3vgsg,ZOvSW0wCRQc,bxraF1Sp9AE,7MvOI-757kg,rZxHnWQNJl4,adrL6zDMp_c,YVGMz2iPyLA,uWngFhbZVzE,QnjpoCzkMZ8,LbipmAzBhYA,Fl_a7uPD_xQ,zfW9opqKS2Q,h0DgQzd9rok&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=SOtXugvjCT0,0qySPHGciCU,IFkgo3Ux-0Q,uHwDujbK8hg,QUQlHUv92Nc,DkG_YTczM8M,T_J66JqbAQM,z6l70LMGw5w,rQqs3QTnYPc,1ZuqqP6JFqo,hX9Ms_8cvSM,hXhUeMFquEA,LE0J3ZPJ2HQ,9B_ZC_9Txy4,nw5XD-fX_6I,YL9SPRuAkVY,0SDA0WEvj3o,GqpKClp_T-4,2CzTrMMeQXg,yJ4Cte8vwDU,Asy9WFtLxJQ,DVMBVhOpH10,IdHoiQRktv4,LvBmOYpcuds,Thfn54QxETE,P8uX0KHyzDM,JSFFEpeUVhU,4X4lfI4LFEs,n7WImmLn9MI,XzkT1aCnahk,-oKB_qz9A_M,XQ5YTijNQBA,2URtJbj8Vq4,5wVh4X8mh6s,3CAPBb76ioE,ip-QWHKObr8,Dfj95S1vi44,qrKvzEpcY3Y,SX_48XOL5KM,4VML89TOB5A,qPaMP8wQUaA,VFM0gn42t24,J120q9G9ctY,NFhUsDhGubo,oqsQioUlTg4,0u1VEKqcK-4,ZWrVavpc34Y,4-Hz2pF3XeM,hESucBk9tjU,Ijq0B6g-lNU&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=zrKWtwJHcGs,n84kiHzZih4,jeTFv1GPmow,6XLVwjw7G3o,XhV8xPk5f7s,vNYn6rLyUuM,gJLPpdG1JXo,isItG9VAUlA,St4LvLxnSyU,fmToGfDqU7Q,8qbgSw9hwE8,Y7vONic0EQg,UYjfQFsXn18,lg92AO7SvIg,a6yLnuXxyUc,BBfH9l7X9Xc,DNoNvyza2Jg,Lts7cW1I9fQ,QSx5K59Meu4,g2Uw8QjPBks,rLgBsXCmMDk,pvuDJ3ewn9E,IUngWruU2XM,8ttay6A7WHw,MJ1hlJeLt44,dSuftHnW0KE,BCBW4VFHb0c,Ou-hg3uh79s,OE5Ue5lT8o0,aPkhTSefs-Y,X5BYlJTWRxQ,-c5Yn4TrEXo,cHPGS2sb9PI,2Faq6_O_3dU,N2Y4bsPXyZg,gXzqZRM--30,Z9pjezym-bA,7HkSoMZKoMM,Ih3USoalcBo,PNKhs0GKAII,X7RGKkKdo1Q,DTB_IOeTPJo,XVcMUprGZIk,7VNm-OOo96Y,vwk_U_RfANo,via4X3XdJcQ,OzEUpkaMV38,VQnHPImp010,0tPNgVtbo0o,8X46vKQQkz0&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=x0lFcqyaBQg,JylItI-Z0bc,WgO7RBgOA5U,Mp0xiitmAmg,7IzKF6Bxg30,5rys4smpw10,5ZeY29f1n8k,06lY_mjNIu8,6PPu7LDc-nY,OqvjizYauEs,EakXQlz-xho,lrReQ7s_d7M,9u2benGmUtU,Gl-M52n1l_k,ne0sd45hD3s,me2V_JvrWNw,XhKJzQu5-30,jraKkQFsYAc,JZmv1GKI0Ag,chqmQIltpBI,zDpdThBs_x4,UAA_-OK1adM,QBtVIya-6CM,E2zxNhKXeOY,zhsARB1ENiI,EXyZvXDzKaQ,MoXJnX1sx88,vjNlCmShLaQ,w-WfpRclqRA,0DS71CBEF0c,8W2AO8jtRxg,qgd-r5qsTnI,LlfSqjUD2mY,3IfKIx1lw94,-pwWENxmz6U,5gkD8WN8lz0,K6XOKl4emxk,-IZuHZFmjyM,4Smev97sLfM,Anjo8Sef1wo,OeiYkZ95JCY,_WnFFXuONtU,lXIaybe-8g4,nVlIDPEuMRs,f9vKuGkBTJI,hMizvxRn120,0i4YuJVAAIA,0jh-qZt9A_M,jK7JAiXmzuY,sQWI9hSxipY&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=A-0CxV27_XQ,Pl2Ym1jUN64,vJztxeWLiWo,KQKSxwwDJh4,ILJwRbby4ww,I4l6WSzeoMg,LbJhoSPjwBo,DhGLDIEdx8U,UgU3GJXlo6k,_fxaGlXrroc,kgKCCyXYxRE,StmhoNyXvcE,y0xs0pyhPZY,P2b8GzZg7p8,e98sNN6sX2Q,MBtgKcI5J_o,jnPug7I2OSM,C4pl0TrOvLU,38PGW7hS_Wc,SekzGcE1ugM,TeRq7RvGvN0,qQblNpq-Q70,_SScN9DkyGA,4h9dqHwYL4Q,ktjtwbDaTWQ,cmvHmWCkbQk,HtD5zJrzlvw,EOoawoE8x2c,G-KBZ4X39AA,rYhEK6uCgdQ,15MeZ5H-lR0,FhJFHREXvvY,fglwP3Cof8k,oOB6kme094Y,7Id-mqVsJ2s,IcQmxaM4PzA,30O6_zaejjM,vBDT8og-24M,53Ya7r0HmKA,JsTQeW6jT3w,I_urnAadEx8,7cXNurGAwCQ,zV1vIX69Iw4,YBR40Xx5LXo,rGLAOXuM6dU,zPdeyMr95wo,p7XJqFUYrVc,kM-D821DqCE,C1GZuMkn-yE,OKHrEA5GW8k&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=YkrXi_uiRjU,eDEo5vHyrmQ,bWJJaEgGABw,NJd6rQAUp90,FD7WergQNxE,3vkwOWy8Ynk,THvFO11BEXQ,adK3A1UlfEk,GuvCvJg7mfs,tKa9wHlZnMs,TFD6LYX4i4g,B8IGiCigkC4,QWO6QXADgYA,GBsJDcgpiCM,T6odJgyaTKs,Mn4QP6yR2cM,Ub1e2mtRkNg,IrieRBV877I,Jbl4opCiVI0,ec6EQ0MRRoM,OwUX89bXjv4,MYn53sDJfVk,z_Pt_wqmqlQ,JV2HqHJWeXI,AhwXDtT-Ats,TFAwEk_PyFg,3884AGxQMoE,_2c5Psky0uY,cQGYWufdYA0,bDOv18tOsVE,t7ktBnAIaEI,YXbsSLB8lts,uc3ulmDQzpQ,7jX47QyQClU,3rJNO_5Y07U,3-NSs3QkK_0,R6RoCubrvYE,rzSNDaGUXb4,OuTxmUvMnsA,ZSJmK1cWJVY,A1oSDAGNXek,MQqDicIfpZg,JGygso4mcq0,ADrzufs0lJQ,ggpjAe3-Xzc,pEpLBPuG8_Y,Vi5pvdXTc3k,EBSEcN4GlOc,ZkC-AP0q51U,6ez0Lg-DTN4&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=Gbds16Fj9gA,bp86Av6ZkM8,6mOfEQ3z1J4,bnADdrXhqFo,o-FT5t7XFao,zMCYGo9kAJc,Erxknh7JGHw,5ySpqqLNPLY,t6WE5pRe2aw,9gr170Ec4zk,BqQtAyIxo2E,O7Y-S2c6Gnc,1E03BeijBJg,sbtBS7sP-Rg,4t4YweYlpeM,u02PJv2n1bM,ytNXFr48lq8,__hbuok-rEo,N-KPbF9XR5Q,Xgfr1BgakTY,Qyo-5UfIpaY,p1R4unAL31k,M9j1QtZPTWY,Ys_wWWwgDQg,A4zxqSD35GU,BpTSuwYqAvU,4i6eldJYWAI,UQlnqvbN-cU,iEZGtc2tVjs,uU1KIYVGenU,1b4nD43f7YY,BeupGqgob0g,rEM5GDvcFeU,xKy6r9vGC1k,Rd3OreiVUC0,omLf7T1qETc,X9yJwiOKboI,HxnooFYz-yY,eeUH5yzPVj0,a1P-LVM1sLw,aX-8wWoFH_0,vzEXt7SO3dA,SXXu67zMTG4,cYh-8KDdEZM,37oP4LFaHl8,RrG2Xw-2ry4,osjWnY-5jls,UJ_LSxyFCEM,KA4twPLkvZQ,5a8V65mQh4w&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=IwB6Aec_vKE,cIYUMdmisFQ,imYWPNFIWrU,0E39qDglvvw,G93tPDQUmIA,99HONmPuGDc,sXwy8Vs38sU,BGl3YSBmgzM,zWdp6uwQWfc,lpk3BE-zji4,vdRfKSwEDxc,_dkPmYr8SQg,R1j5X8k2YuQ,48E3Hr0plXM,lDiojT4q2gA,Gnaa2v1dM_I,0oxfUuuUypk,H5Y5vs3o7m8,iR4rf23RPb4,CUFmAOa6MQY,lSz7uRtq-1Q,RZDsef0llrI,lDgzDE4ED0Y,jf7L2QQzf2Y,tpThX5Z3Q48,5qxrHf7Ul1c,SnwKuywb0yk,KczYwhjTx3g,7WQ5p17KT2w,HFSgnIN67kQ,csFLOOqvodM,Pq6kf1x5TOM,ain9Aqk8TnA,VHERgVeBMAs,8cYQfo_hQtk,8udskq0xzpY,NP44QN2wdiY,1bEHTqp3d0U,SkiJWNF08_8,Hr6XxA52ju0,zDofiErwsdc,dLESL4ZFTh4,0kssT-oEo34,QV_l9yZE97M,bB6a5TI_VhM,dka3AzVJxHk,riLc-amj_Sg,_tpxusdUIhw,N0Su97ejnN0,kzP9xpIgzJQ&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    --
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=m7ALVFrgsPM,FctXTuExZlA,mUAXyuyK57Q,9BBHBlih8js,1_nYSkoJqcA,Dn4fpLJ3l14,LiDMmXpFQuA,Q5x7bskPQQ0,4MXefaEPejM,egFHOosOvk4,bhRAozVlu_A,cHEXL7_prDw,_UVIJDU1exA,28dshtEH2xM,IHgwXdZnynQ&key=AIzaSyBXzmJNls0YAYMNF6O2KAqljxgXZFiJrcg
    
    Muestra de los datos extraídos:
          video_id                                             titulo  \
    0  m7ALVFrgsPM  Assassin's Creed 2 | Walkthrough Español | Sec...   
    1  FctXTuExZlA  Assassin's Creed 2 | Walkthrough Español | Sec...   
    2  mUAXyuyK57Q  Assassin's Creed 2 | Walkthrough Español | Sec...   
    3  9BBHBlih8js  Assassin's Creed 2 | Walkthrough Español | Sec...   
    4  1_nYSkoJqcA  Assassin's Creed 2 | Walkthrough Español | Sec...   
    
              fecha_publicacion vistas likes comentarios duracion_iso  
    0 2011-10-09 01:37:18+00:00   9823   129          10      PT8M16S  
    1 2011-10-08 04:53:44+00:00  11688   141          14      PT2M52S  
    2 2011-10-08 03:44:20+00:00  10928   157          12      PT4M25S  
    3 2011-10-08 01:19:45+00:00  10966   147           6      PT4M18S  
    4 2011-10-07 23:15:10+00:00   7043   103           8      PT3M48S  
    
    Pipeline finalizado. Revisa tus archivos locales.


## **5. Plantilla**


```python
A continuación tienes una plantilla del código para que te puedas centrar en las funciones propias de la consulta a la API.

import requests
import pandas as pd
import math

# CONFIGURACIÓN
API_KEY = 'TU_API_KEY_AQUI'
CHANNEL_ID = 'ID_DEL_CANAL' 
BASE_URL = 'https://www.googleapis.com/youtube/v3'


# FUNCIONES DE INGESTA
# --------------------
def get_uploads_playlist_id(channel_id):
    """Paso 1: Obtener el ID de la lista de reproducción 'Uploads' del canal"""
    url = f"{BASE_URL}/channels?part=contentDetails&id={channel_id}&key={API_KEY}"
    response = requests.get(url).json()
    
    try:
        # TODO: Extrae el id del playlist (está en la clave uploads)
        # ...
        
        return playlist_id
    except KeyError:
        print("Error al obtener la playlist. Revisa el ID del canal y tu API Key.")
        return None

def get_all_video_ids(playlist_id):
    """Paso 2: Obtener todos los IDs de los videos de la playlist"""
    video_ids = []
    next_page_token = None
    
    print("Extrayendo IDs de videos...")
    
    while True:
        url = f"{BASE_URL}/playlistItems?part=contentDetails&maxResults=50&playlistId={playlist_id}&key={API_KEY}"
        
        # TODO: Si existe un next_page_token, añádelo a la URL (&pageToken=...)
        # ...
        
        response = requests.get(url).json()
        
        for item in response.get('items', []):
            video_ids.append(item['contentDetails']['videoId'])
            
        # TODO: Lógica de paginación. 
        # Busca 'nextPageToken' en la respuesta. Si existe, actualiza la variable. Si no, rompe el bucle.
        # ...
        break # BORRAR ESTE BREAK CUANDO IMPLEMENTES LA PAGINACIÓN
        
    print(f"Total de videos encontrados: {len(video_ids)}")
    return video_ids


def get_video_details(video_ids):
    """Paso 3: Obtener estadísticas de los videos en lotes de 50"""
    all_video_data = []
    
    # TODO: Agrupa la lista video_ids en sub-listas de máximo 50 elementos.
    # ...
    
    # Este bucle simula el procesamiento por lotes (debes adaptarlo a tus sub-listas)
    for i in range(0, len(video_ids), 50):
        chunk = video_ids[i:i+50]
        
        ids_string = ','.join(chunk)
        url = f"{BASE_URL}/videos?part=snippet,statistics,contentDetails&id={ids_string}&key={API_KEY}"
        
        response = requests.get(url).json()
        
        # TODO: de cada vídeo, extraer: id, title, publishedAt, ViewCount, likeCount, CommentCount, duration
        # Guardar los datos en un diccionario y anexarlo a all_video_data
        # ...
            
    return all_video_data

def parse_duration(iso_duration):
    """Paso 4: Transformar la duración ISO 8601 (ej: PT1H2M10S) a segundos totales"""
    # TODO: Convierte la duración de ISO8601 a segundos
    # ...

    return iso_duration 


# EJECUCIÓN PRINCIPAL (PIPELINE)
# ------------------------------
if __name__ == "__main__":
    print("Iniciando pipeline de ingesta...")
    
    uploads_id = get_uploads_playlist_id(CHANNEL_ID)
    
    if uploads_id:
        lista_ids = get_all_video_ids(uploads_id)
        datos_completos = get_video_details(lista_ids)
        
        df = pd.DataFrame(datos_completos)
        
        # Limpieza básica
        df['fecha_publicacion'] = pd.to_datetime(df['fecha_publicacion'])
        
        print("\nMuestra de los datos extraídos:")
        print(df.head())
        
        # 5. Guardar en un formato analítico
        # TODO: Utiliza el método de Pandas adecuado para guardar el DataFrame en formato Parquet.
        # Nombra el archivo como 'dataset_canal_youtube.parquet'.
        # ...
        
        print("\nPipeline finalizado. Revisa tus archivos locales.")
```
