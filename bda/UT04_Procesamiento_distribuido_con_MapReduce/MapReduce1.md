```python
ls /
```

    [0m[01;36mbin[0m@   [01;34mdev[0m/  [01;34mhdfs[0m/  [01;36mlib[0m@    [01;36mlib64[0m@   [01;34mmedia[0m/  [01;34mopt[0m/   [01;34mroot[0m/  [01;36msbin[0m@  [01;34msys[0m/  [01;34musr[0m/
    [01;34mboot[0m/  [01;34metc[0m/  [01;34mhome[0m/  [01;36mlib32[0m@  [01;36mlibx32[0m@  [01;34mmnt[0m/    [01;34mproc[0m/  [01;34mrun[0m/   [01;34msrv[0m/   [30;42mtmp[0m/  [01;34mvar[0m/



```python
!hdfs dfs -put /media/notebooks/quijote.txt /
```

    put: `/quijote.txt': File exists



```python
!hdfs dfs -ls /
```

    Found 2 items
    -rw-r--r--   3 root supergroup    2178972 2025-12-02 09:47 /quijote.txt
    drwxrwx---   - root supergroup          0 2025-12-02 09:43 /tmp



```python
%%writefile mapperquijote.py
#!/usr/bin/env python3
import sys, re

regex = re.compile(r"[^a-záéíóúüñ0-9]+")

for line in sys.stdin:
    line = line.lower()
    line = regex.sub(" ", line)
    words = line.split()

    for word in words:
        print(f"{word}\t1")
```

    Overwriting mapperquijote.py



```python
%%writefile quijote.py
#!/usr/bin/env python3
import sys

current = None
suma = 0

for line in sys.stdin:
    key, val = line.strip().split("\t")
    val = int(val)

    if key == current:
        suma += val
    else:
        if current is not None:
            print(f"{current},{suma}")
        current = key
        suma = val

print(f"{current},{suma}")

```

    Overwriting quijote.py



```python
!head -n 10 quijote.txt | python3 mapperquijote.py | sort |python3 reducerquijote.py
```

    a,1
    andrada,1
    cada,1
    certifico,1
    cervantes,1
    compuesto,1
    consejo,1
    cual,1
    cámara,1
    de,6
    del,2
    dicho,1
    don,1
    doy,1
    dél,1
    el,3
    en,1
    escribano,1
    fe,1
    gallo,1
    habiendo,1
    hidalgo,2
    ingenioso,2
    intitulado,1
    juan,1
    la,2
    libro,2
    los,2
    mancha,2
    maravedís,1
    medio,1
    miguel,1
    nuestro,1
    ochenta,1
    pliego,1
    pliegos,1
    por,2
    que,3
    quijote,1
    residen,1
    rey,1
    saavedra,1
    señor,1
    señores,1
    su,1
    tasa,1
    tasaron,1
    tiene,1
    tres,2
    un,1
    visto,1
    y,3
    yo,1



```python
!hadoop jar \
/usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.4.0.jar \
-file mapperquijote.py \
-file reducerquijote.py \
-mapper mapperquijote.py \
-reducer reducerquijote.py \
-input /quijote.txt \
-output /salida1
```

    2025-12-02 10:12:49,603 WARN streaming.StreamJob: -file option is deprecated, please use generic option -files instead.
    packageJobJar: [mapperquijote.py, reducerquijote.py, /tmp/hadoop-unjar2226146373486368984/] [] /tmp/streamjob3838069656381623848.jar tmpDir=null
    2025-12-02 10:12:50,600 INFO client.DefaultNoHARMFailoverProxyProvider: Connecting to ResourceManager at yarnmanager/172.18.0.3:8032
    2025-12-02 10:12:50,797 INFO client.DefaultNoHARMFailoverProxyProvider: Connecting to ResourceManager at yarnmanager/172.18.0.3:8032
    2025-12-02 10:12:50,953 ERROR streaming.StreamJob: Error Launching job : Output directory hdfs://namenode:9000/salida1 already exists
    Streaming Command Failed!



```python
!hdfs dfs -ls /
```

    Found 5 items
    -rw-r--r--   3 root supergroup    2178972 2025-12-02 09:47 /quijote.txt
    drwxr-xr-x   - root supergroup          0 2025-12-02 09:59 /salida1
    drwxrwx---   - root supergroup          0 2025-12-02 09:43 /tmp
    drwxr-xr-x   - root supergroup          0 2025-12-02 09:58 /user
    drwxrwxrwt   - root root                0 2025-12-02 09:59 /yarn



```python
!hdfs dfs -ls /salida1
```

    Found 2 items
    -rw-r--r--   3 root supergroup          0 2025-12-02 09:59 /salida1/_SUCCESS
    -rw-r--r--   3 root supergroup     280624 2025-12-02 09:59 /salida1/part-00000



```python
!hdfs dfs -cat /salida1/part-00000
```


```python
%%writefile mapperquijote1.py
#!/usr/bin/env python3
import sys, re

stopwords = {"de","la","el","y","en","que","a","los","del","se"}
regex = re.compile(r"[^a-záéíóúüñ0-9]+")

for line in sys.stdin:
    line = line.lower()
    line = regex.sub(" ", line)
    words = line.split()

    for word in words:
        if word in stopwords:
            continue
        print(f"{word}\t1")

```

    Writing mapperquijote1.py



```python
%%writefile reducerquijote1.py
#!/usr/bin/env python3
import sys

current = None
suma = 0

for line in sys.stdin:
    key, val = line.strip().split("\t")
    val = int(val)

    if key == current:
        suma += val
    else:
        if current is not None:
            print(f"{current},{suma}")
        current = key
        suma = val

print(f"{current},{suma}")
```

    Writing reducerquijote1.py



```python
!head -n 10 quijote.txt | python3 mapperquijote1.py | sort |python3 reducerquijote1.py
```

    andrada,1
    cada,1
    certifico,1
    cervantes,1
    compuesto,1
    consejo,1
    cual,1
    cámara,1
    dicho,1
    don,1
    doy,1
    dél,1
    escribano,1
    fe,1
    gallo,1
    habiendo,1
    hidalgo,2
    ingenioso,2
    intitulado,1
    juan,1
    libro,2
    mancha,2
    maravedís,1
    medio,1
    miguel,1
    nuestro,1
    ochenta,1
    pliego,1
    pliegos,1
    por,2
    quijote,1
    residen,1
    rey,1
    saavedra,1
    señor,1
    señores,1
    su,1
    tasa,1
    tasaron,1
    tiene,1
    tres,2
    un,1
    visto,1
    yo,1



```python
!hadoop jar \
/usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.4.0.jar \
-file mapperquijote1.py \
-file reducerquijote1.py \
-mapper mapperquijote1.py \
-reducer reducerquijote1.py \
-input /quijote.txt \
-output /salida2
```

    2025-12-02 10:15:28,066 WARN streaming.StreamJob: -file option is deprecated, please use generic option -files instead.
    packageJobJar: [mapperquijote1.py, reducerquijote1.py, /tmp/hadoop-unjar8664733315377394603/] [] /tmp/streamjob7066642834906902590.jar tmpDir=null
    2025-12-02 10:15:29,614 INFO client.DefaultNoHARMFailoverProxyProvider: Connecting to ResourceManager at yarnmanager/172.18.0.3:8032
    2025-12-02 10:15:29,819 INFO client.DefaultNoHARMFailoverProxyProvider: Connecting to ResourceManager at yarnmanager/172.18.0.3:8032
    2025-12-02 10:15:30,119 INFO mapreduce.JobResourceUploader: Disabling Erasure Coding for path: /tmp/hadoop-yarn/staging/root/.staging/job_1764668628422_0004
    2025-12-02 10:15:31,026 INFO mapred.FileInputFormat: Total input files to process : 1
    2025-12-02 10:15:31,934 INFO mapreduce.JobSubmitter: number of splits:2
    2025-12-02 10:15:32,202 INFO mapreduce.JobSubmitter: Submitting tokens for job: job_1764668628422_0004
    2025-12-02 10:15:32,203 INFO mapreduce.JobSubmitter: Executing with tokens: []
    2025-12-02 10:15:32,497 INFO conf.Configuration: resource-types.xml not found
    2025-12-02 10:15:32,497 INFO resource.ResourceUtils: Unable to find 'resource-types.xml'.
    2025-12-02 10:15:32,659 INFO impl.YarnClientImpl: Submitted application application_1764668628422_0004
    2025-12-02 10:15:32,715 INFO mapreduce.Job: The url to track the job: http://yarnmanager:8088/proxy/application_1764668628422_0004/
    2025-12-02 10:15:32,717 INFO mapreduce.Job: Running job: job_1764668628422_0004
    2025-12-02 10:15:41,991 INFO mapreduce.Job: Job job_1764668628422_0004 running in uber mode : false
    2025-12-02 10:15:41,996 INFO mapreduce.Job:  map 0% reduce 0%
    2025-12-02 10:15:49,165 INFO mapreduce.Job:  map 50% reduce 0%
    2025-12-02 10:15:50,210 INFO mapreduce.Job:  map 100% reduce 0%
    2025-12-02 10:15:56,362 INFO mapreduce.Job:  map 100% reduce 100%
    2025-12-02 10:15:57,381 INFO mapreduce.Job: Job job_1764668628422_0004 completed successfully
    2025-12-02 10:15:57,492 INFO mapreduce.Job: Counters: 54
    	File System Counters
    		FILE: Number of bytes read=2849298
    		FILE: Number of bytes written=6641048
    		FILE: Number of read operations=0
    		FILE: Number of large read operations=0
    		FILE: Number of write operations=0
    		HDFS: Number of bytes read=2183236
    		HDFS: Number of bytes written=280529
    		HDFS: Number of read operations=11
    		HDFS: Number of large read operations=0
    		HDFS: Number of write operations=2
    		HDFS: Number of bytes read erasure-coded=0
    	Job Counters 
    		Launched map tasks=2
    		Launched reduce tasks=1
    		Data-local map tasks=2
    		Total time spent by all maps in occupied slots (ms)=11707
    		Total time spent by all reduces in occupied slots (ms)=4440
    		Total time spent by all map tasks (ms)=11707
    		Total time spent by all reduce tasks (ms)=4440
    		Total vcore-milliseconds taken by all map tasks=11707
    		Total vcore-milliseconds taken by all reduce tasks=4440
    		Total megabyte-milliseconds taken by all map tasks=11987968
    		Total megabyte-milliseconds taken by all reduce tasks=4546560
    	Map-Reduce Framework
    		Map input records=37453
    		Map output records=275628
    		Map output bytes=2298036
    		Map output materialized bytes=2849304
    		Input split bytes=168
    		Combine input records=0
    		Combine output records=0
    		Reduce input groups=22933
    		Reduce shuffle bytes=2849304
    		Reduce input records=275628
    		Reduce output records=22933
    		Spilled Records=551256
    		Shuffled Maps =2
    		Failed Shuffles=0
    		Merged Map outputs=2
    		GC time elapsed (ms)=256
    		CPU time spent (ms)=6100
    		Physical memory (bytes) snapshot=908726272
    		Virtual memory (bytes) snapshot=7637164032
    		Total committed heap usage (bytes)=773849088
    		Peak Map Physical memory (bytes)=321241088
    		Peak Map Virtual memory (bytes)=2543632384
    		Peak Reduce Physical memory (bytes)=270204928
    		Peak Reduce Virtual memory (bytes)=2550595584
    	Shuffle Errors
    		BAD_ID=0
    		CONNECTION=0
    		IO_ERROR=0
    		WRONG_LENGTH=0
    		WRONG_MAP=0
    		WRONG_REDUCE=0
    	File Input Format Counters 
    		Bytes Read=2183068
    	File Output Format Counters 
    		Bytes Written=280529
    2025-12-02 10:15:57,492 INFO streaming.StreamJob: Output directory: /salida2



```python
!hdfs dfs -ls /salida2
```

    Found 2 items
    -rw-r--r--   3 root supergroup          0 2025-12-02 10:15 /salida2/_SUCCESS
    -rw-r--r--   3 root supergroup     280529 2025-12-02 10:15 /salida2/part-00000



```python
%%writefile mapperQuijote21.py
#!/usr/bin/env python3
import sys

for line in sys.stdin:
    for word in line.strip().split():
        clean_word = ""
        for char in word:
            if char.isalpha():
                clean_word += char

        if clean_word:
            print(f"{clean_word}\t1")

```

    Writing mapperQuijote21.py



```python
!head -n 10 quijote.txt | python3 mapperQuijote21.py
```

    El	1
    ingenioso	1
    hidalgo	1
    don	1
    Quijote	1
    de	1
    la	1
    Mancha	1
    TASA	1
    Yo	1
    Juan	1
    Gallo	1
    de	1
    Andrada	1
    escribano	1
    de	1
    Cámara	1
    del	1
    Rey	1
    nuestro	1
    señor	1
    de	1
    los	1
    que	1
    residen	1
    en	1
    su	1
    Consejo	1
    certifico	1
    y	1
    doy	1
    fe	1
    que	1
    habiendo	1
    visto	1
    por	1
    los	1
    señores	1
    dél	1
    un	1
    libro	1
    intitulado	1
    El	1
    ingenioso	1
    hidalgo	1
    de	1
    la	1
    Mancha	1
    compuesto	1
    por	1
    Miguel	1
    de	1
    Cervantes	1
    Saavedra	1
    tasaron	1
    cada	1
    pliego	1
    del	1
    dicho	1
    libro	1
    a	1
    tres	1
    maravedís	1
    y	1
    medio	1
    el	1
    cual	1
    tiene	1
    ochenta	1
    y	1
    tres	1
    pliegos	1
    que	1



```python
%%writefile mapperQuijote22.py
#!/usr/bin/env python3
import sys

word_dict = {}

for line in sys.stdin:
    line = line.strip()
    clave, valor = line.split("\t")
    valor = int(valor)

    if clave not in word_dict:
        word_dict[clave] = valor
    else:
        word_dict[clave] += valor

for key, value in sorted(word_dict.items(), key=lambda x: x[1], reverse=True):
    print(f"{value}\t{key}")
```

    Writing mapperQuijote22.py



```python
!head -n 30 quijote.txt | python3 mapperQuijote21.py  | python3 mapperQuijote22.py
```

    19	de
    10	y
    8	que
    6	la
    6	en
    5	libro
    4	del
    4	dicho
    4	a
    4	se
    3	El
    3	los
    3	el
    3	vender
    3	no
    2	ingenioso
    2	hidalgo
    2	Mancha
    2	Juan
    2	Gallo
    2	Andrada
    2	su
    2	por
    2	tres
    2	maravedís
    2	medio
    2	tiene
    2	al
    2	precio
    2	para
    2	pueda
    2	esta
    2	di
    2	años
    1	don
    1	Quijote
    1	TASA
    1	Yo
    1	escribano
    1	Cámara
    1	Rey
    1	nuestro
    1	señor
    1	residen
    1	Consejo
    1	certifico
    1	doy
    1	fe
    1	habiendo
    1	visto
    1	señores
    1	dél
    1	un
    1	intitulado
    1	compuesto
    1	Miguel
    1	Cervantes
    1	Saavedra
    1	tasaron
    1	cada
    1	pliego
    1	cual
    1	ochenta
    1	pliegos
    1	monta
    1	docientos
    1	noventa
    1	ha
    1	papel
    1	dieron
    1	licencia
    1	este
    1	mandaron
    1	tasa
    1	ponga
    1	principio
    1	sin
    1	ella
    1	Y
    1	dello
    1	conste
    1	presente
    1	Valladolid
    1	veinte
    1	días
    1	mes
    1	deciembre
    1	mil
    1	seiscientos
    1	cuatro
    1	TESTIMONIO
    1	DE
    1	LAS
    1	ERRATAS
    1	Este
    1	cosa
    1	digna
    1	corresponda
    1	original
    1	testimonio
    1	lo
    1	haber
    1	correcto
    1	fee
    1	En
    1	Colegio
    1	Madre
    1	Dios
    1	Teólogos
    1	Universidad
    1	Alcalá
    1	primero
    1	diciembre
    1	licenciado
    1	Francisco
    1	Murcia
    1	Llana
    1	EL
    1	REY



```python
!hadoop jar \
/usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.4.0.jar \
-D mapreduce.job.reduces=0 \
-file mapperQuijote21.py \
-mapper mapperQuijote21.py \
-input /quijote.txt \
-output 
```

    2025-12-02 12:06:03,618 WARN streaming.StreamJob: -file option is deprecated, please use generic option -files instead.
    packageJobJar: [mapperQuijote21.py, /tmp/hadoop-unjar8482244212917780704/] [] /tmp/streamjob7912066664121140811.jar tmpDir=null
    2025-12-02 12:06:04,863 INFO client.DefaultNoHARMFailoverProxyProvider: Connecting to ResourceManager at yarnmanager/172.18.0.3:8032
    2025-12-02 12:06:05,103 INFO client.DefaultNoHARMFailoverProxyProvider: Connecting to ResourceManager at yarnmanager/172.18.0.3:8032
    2025-12-02 12:06:05,529 INFO mapreduce.JobResourceUploader: Disabling Erasure Coding for path: /tmp/hadoop-yarn/staging/root/.staging/job_1764668628422_0005
    2025-12-02 12:06:07,024 INFO mapred.FileInputFormat: Total input files to process : 1
    2025-12-02 12:06:07,137 INFO mapreduce.JobSubmitter: number of splits:2
    2025-12-02 12:06:07,376 INFO mapreduce.JobSubmitter: Submitting tokens for job: job_1764668628422_0005
    2025-12-02 12:06:07,376 INFO mapreduce.JobSubmitter: Executing with tokens: []
    2025-12-02 12:06:07,686 INFO conf.Configuration: resource-types.xml not found
    2025-12-02 12:06:07,686 INFO resource.ResourceUtils: Unable to find 'resource-types.xml'.
    2025-12-02 12:06:07,893 INFO impl.YarnClientImpl: Submitted application application_1764668628422_0005
    2025-12-02 12:06:07,955 INFO mapreduce.Job: The url to track the job: http://yarnmanager:8088/proxy/application_1764668628422_0005/
    2025-12-02 12:06:07,958 INFO mapreduce.Job: Running job: job_1764668628422_0005
    2025-12-02 12:06:16,246 INFO mapreduce.Job: Job job_1764668628422_0005 running in uber mode : false
    2025-12-02 12:06:16,247 INFO mapreduce.Job:  map 0% reduce 0%
    2025-12-02 12:06:26,510 INFO mapreduce.Job:  map 100% reduce 0%
    2025-12-02 12:06:27,556 INFO mapreduce.Job: Job job_1764668628422_0005 completed successfully
    2025-12-02 12:06:27,701 INFO mapreduce.Job: Counters: 33
    	File System Counters
    		FILE: Number of bytes read=0
    		FILE: Number of bytes written=626958
    		FILE: Number of read operations=0
    		FILE: Number of large read operations=0
    		FILE: Number of write operations=0
    		HDFS: Number of bytes read=2183236
    		HDFS: Number of bytes written=2825828
    		HDFS: Number of read operations=14
    		HDFS: Number of large read operations=0
    		HDFS: Number of write operations=4
    		HDFS: Number of bytes read erasure-coded=0
    	Job Counters 
    		Launched map tasks=2
    		Data-local map tasks=2
    		Total time spent by all maps in occupied slots (ms)=14040
    		Total time spent by all reduces in occupied slots (ms)=0
    		Total time spent by all map tasks (ms)=14040
    		Total vcore-milliseconds taken by all map tasks=14040
    		Total megabyte-milliseconds taken by all map tasks=14376960
    	Map-Reduce Framework
    		Map input records=37453
    		Map output records=381208
    		Input split bytes=168
    		Spilled Records=0
    		Failed Shuffles=0
    		Merged Map outputs=0
    		GC time elapsed (ms)=271
    		CPU time spent (ms)=4080
    		Physical memory (bytes) snapshot=506859520
    		Virtual memory (bytes) snapshot=5089853440
    		Total committed heap usage (bytes)=386924544
    		Peak Map Physical memory (bytes)=254676992
    		Peak Map Virtual memory (bytes)=2545364992
    	File Input Format Counters 
    		Bytes Read=2183068
    	File Output Format Counters 
    		Bytes Written=2825828
    2025-12-02 12:06:27,701 INFO streaming.StreamJob: Output directory: /salida3



```python
!hadoop jar \
/usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.4.0.jar \
-D mapreduce.job.reduces=0 \
-file mapperQuijote22.py \
-mapper mapperQuijote22.py \
-input /salida3/part-00000\
-output /salida4
```

    2025-12-02 12:08:59,744 WARN streaming.StreamJob: -file option is deprecated, please use generic option -files instead.
    packageJobJar: [mapperQuijote22.py, /tmp/hadoop-unjar5770700518938515305/] [] /tmp/streamjob7750292854817217096.jar tmpDir=null
    2025-12-02 12:09:01,435 INFO client.DefaultNoHARMFailoverProxyProvider: Connecting to ResourceManager at yarnmanager/172.18.0.3:8032
    2025-12-02 12:09:02,034 INFO client.DefaultNoHARMFailoverProxyProvider: Connecting to ResourceManager at yarnmanager/172.18.0.3:8032
    2025-12-02 12:09:02,524 INFO mapreduce.JobResourceUploader: Disabling Erasure Coding for path: /tmp/hadoop-yarn/staging/root/.staging/job_1764668628422_0006
    2025-12-02 12:09:03,151 INFO mapred.FileInputFormat: Total input files to process : 1
    2025-12-02 12:09:03,647 INFO mapreduce.JobSubmitter: number of splits:2
    2025-12-02 12:09:03,981 INFO mapreduce.JobSubmitter: Submitting tokens for job: job_1764668628422_0006
    2025-12-02 12:09:03,987 INFO mapreduce.JobSubmitter: Executing with tokens: []
    2025-12-02 12:09:04,356 INFO conf.Configuration: resource-types.xml not found
    2025-12-02 12:09:04,358 INFO resource.ResourceUtils: Unable to find 'resource-types.xml'.
    2025-12-02 12:09:04,629 INFO impl.YarnClientImpl: Submitted application application_1764668628422_0006
    2025-12-02 12:09:04,763 INFO mapreduce.Job: The url to track the job: http://yarnmanager:8088/proxy/application_1764668628422_0006/
    2025-12-02 12:09:04,774 INFO mapreduce.Job: Running job: job_1764668628422_0006
    2025-12-02 12:09:13,050 INFO mapreduce.Job: Job job_1764668628422_0006 running in uber mode : false
    2025-12-02 12:09:13,052 INFO mapreduce.Job:  map 0% reduce 0%
    2025-12-02 12:09:20,191 INFO mapreduce.Job:  map 50% reduce 0%
    2025-12-02 12:09:21,204 INFO mapreduce.Job:  map 100% reduce 0%
    2025-12-02 12:09:21,222 INFO mapreduce.Job: Job job_1764668628422_0006 completed successfully
    2025-12-02 12:09:21,443 INFO mapreduce.Job: Counters: 33
    	File System Counters
    		FILE: Number of bytes read=0
    		FILE: Number of bytes written=626972
    		FILE: Number of read operations=0
    		FILE: Number of large read operations=0
    		FILE: Number of write operations=0
    		HDFS: Number of bytes read=1420062
    		HDFS: Number of bytes written=229994
    		HDFS: Number of read operations=14
    		HDFS: Number of large read operations=0
    		HDFS: Number of write operations=4
    		HDFS: Number of bytes read erasure-coded=0
    	Job Counters 
    		Launched map tasks=2
    		Data-local map tasks=2
    		Total time spent by all maps in occupied slots (ms)=10745
    		Total time spent by all reduces in occupied slots (ms)=0
    		Total time spent by all map tasks (ms)=10745
    		Total vcore-milliseconds taken by all map tasks=10745
    		Total megabyte-milliseconds taken by all map tasks=11002880
    	Map-Reduce Framework
    		Map input records=191170
    		Map output records=21479
    		Input split bytes=182
    		Spilled Records=0
    		Failed Shuffles=0
    		Merged Map outputs=0
    		GC time elapsed (ms)=148
    		CPU time spent (ms)=2600
    		Physical memory (bytes) snapshot=481951744
    		Virtual memory (bytes) snapshot=5090009088
    		Total committed heap usage (bytes)=363855872
    		Peak Map Physical memory (bytes)=244490240
    		Peak Map Virtual memory (bytes)=2545139712
    	File Input Format Counters 
    		Bytes Read=1419880
    	File Output Format Counters 
    		Bytes Written=229994
    2025-12-02 12:09:21,443 INFO streaming.StreamJob: Output directory: /salida4



```python
!hdfs dfs -head /salida4/part-00000
```

    5318	que
    4570	de
    4041	y
    2398	la
    2313	a
    1982	en
    1937	el
    1454	no
    1204	se
    1073	los
    994	por
    972	con
    929	su
    919	le
    876	lo
    806	las
    641	del
    632	me
    585	don
    563	como
    520	Quijote
    512	es
    511	más
    478	un
    451	Sancho
    447	al
    434	yo
    428	si
    419	dijo
    402	mi
    375	para
    374	tan
    370	él
    357	ni
    343	porque
    340	sin
    332	una
    307	Y
    296	había
    276	bien
    271	o
    271	todo
    270	sus
    262	era
    258	vuestra
    247	respondió
    237	ser
    233	merced
    225	esto
    215	así
    213	cual
    212	ha
    205	caballero
    197	muy
    197	cuando
    196	fue
    179	señor
    175	donde
    174	ya
    170	sino
    166	todos
    165	quien
    163	otra
    162	pues
    159	dos
    157	qué
    156	aquel
    154	hacer
    150	cosa
    148	te
    144	ella
    140	aunque
    135	pero
    133	este
    133	esta
    128	otro
    128	No
    126	os
    126	mí
    123	poco
    122	mal
    121	estaba
    119	decir
    117	he
    114	aquí
    112	manera
    112	allí
    108	Dios
    108	sé
    107	parte
    106	alguna
    105	sobre
    104	tenía
    104	tal
    104	señora
    103	mis
    103	tengo
    101	hasta
    101	luego
    101	aquella
    98	buen
    97	amo
    93	tanto
    92	hay
    91	dicho
    91	está
    90	nos
    90	lugar
    90	ahora
    90	ver
    90	vida
    89	mucho
    89	Rocinante
    88	son
    88	les
    87	menos
    86
