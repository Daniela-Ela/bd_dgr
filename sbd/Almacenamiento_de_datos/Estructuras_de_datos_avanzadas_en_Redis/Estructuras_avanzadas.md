```python
import redis
import datetime

r = redis.Redis(host='redis-server', port=6379, db=0, decode_responses=True)
```

Gestión de jugadores (Hash + Sorted Set)

Función add_player(id, name, country, score)

Crear el hash player:<id> con los campos: name, country, games_played, score

Insertar el jugador en el sorted set leaderboard con la puntuación inicial.


```python
def add_player(id, name, country, score):
    key = f"player:{id}"
    r.hset(key, mapping={
        "name": name,
        "country": country,
        "games_played": 0,
        "score": score
    })
    r.zadd("leaderboard", {id: score})
    print(f"Jugador {name} añadido con puntuación {score}.")
```


```python
add_player(101, "Ana", "España", 1200)
add_player(102, "Luis", "México", 950)
add_player(103, "Sofía", "Chile", 1850)
```

    Jugador Ana añadido con puntuación 1200.
    Jugador Luis añadido con puntuación 950.
    Jugador Sofía añadido con puntuación 1850.


Función update_score(id, points)

Incrementa el campo score del jugador, actualiza, su puntuación en el sorted set e incrementa el campo games_played.


```python
def update_score(id, points):
    r.hincrby(f"player:{id}", "score", points)
    r.hincrby(f"player:{id}", "games_played", 1)
    new_score = int(r.hget(f"player:{id}", "score"))
    r.zadd("leaderboard", {id: new_score})

```


```python
update_score(102, 300)
```

Función player_info(id)

Muestra todos los datos almacenados en el hash player:<id>.


```python
def player_info(id):
    print(r.hgetall(f"player:{id}"))
```


```python
player_info(102)
```

    {'name': 'Luis', 'country': 'México', 'games_played': '1', 'score': '1250'}


Función show_top_players(n)

Muestra los n mejores jugadores del ranking (leaderboard) con nombre, país y puntuación de cada jugador.


```python
def show_top_players(n):
    top = r.zrevrange("leaderboard", 0, n - 1, withscores=True)
    for pid, score in top:
        info = r.hgetall(f"player:{pid}")
        print(info["name"], info["country"], int(score))
```


```python
show_top_players(3)
```

    Sofía Chile 1850
    Luis México 1250
    Ana España 1200


Registro de actividad diaria (HyperLogLog)

Función register_login(player_id)

Cada vez que un jugador inicia sesión, añadir su ID al HyperLogLog diario.

Por ejemplo, para la fecha actual:   key = f"unique:players:{fecha}"
  redis_client.pfadd(key, player_id)


```python
def register_login(player_id):
    fecha = datetime.date.today().isoformat()
    r.pfadd(f"unique:players:{fecha}", player_id)
```


```python
register_login(101)
register_login(102)
register_login(103)
```

Función count_unique_logins(date)


Obtiene el número aproximado de jugadores únicos que se conectaron ese día usando: redis_client.pfcount(key)


```python
def count_unique_logins(date):
    print("Jugadores únicos:", r.pfcount(f"unique:players:{date}"))
```


```python
hoy = datetime.date.today().isoformat()
count_unique_logins(hoy)
```

    Jugadores únicos: 3


Función weekly_report(dates)

Dada una lista de fechas, calcula el total aproximado de jugadores únicos en toda la semana con:  redis_client.pfmerge("unique:players:week", *keys) redis_client.pfcount("unique:players:week")


```python
def weekly_report(dates):
    claves = [f"unique:players:{d}" for d in dates]
    r.pfmerge("unique:players:week", *claves)
    print("Total semana:", r.pfcount("unique:players:week"))
```


```python
r.pfadd("unique:players:2025-10-27", 101)
r.pfadd("unique:players:2025-10-28", 102)
r.pfadd("unique:players:2025-10-29", 103)
r.pfadd("unique:players:2025-10-30", 104)
r.pfadd("unique:players:2025-10-31", 105)

fechas = ["2025-10-27", "2025-10-28", "2025-10-29", "2025-10-30", "2025-10-31"]
weekly_report(fechas)
```

    Total semana: 5



```python

```
