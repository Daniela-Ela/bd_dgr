# **PR0402: Trabajando con datos del clima en MapReduce**

### **Ejercicio 1: temperatura máxima por ciudad**

Utiliza MapReduce para encontrar la temperatura máxima registrada para cada ciudad. Para ello tienes que tener en cuenta lo siguiente:
- **Lógica mapper:** lee cada línea de los datos y emite el par (ciudad, temperatura)
- **Lógica reducer:** como recibirá todas las líneas de una misma ciudad consecutivamente, emite únicamente la línea con mayor valor en temperatura.



```python
%%writefile mapperEjercicio1.py
#!/usr/bin/env python3
import sys
import os

for line in sys.stdin:
    fields = line.strip().split(',')

    # Saltar cabecera
    if fields[0] == "Region":
        continue

    key = fields[3]        # City
    value = fields[7]      # Temperature

    print(f"{key}\t{value}")
```

    Writing mapperEjercicio1.py



```python
%%writefile reducerEjercicio1.py
#!/usr/bin/env python3
import sys
import os

current_key = None
max_temp = None

for line in sys.stdin:
    key, value = line.strip().split('\t')
    value = float(value)

    # Primera clave
    if current_key is None:
        current_key = key
        max_temp = value
        continue

    # Misma ciudad → buscar máximo
    if key == current_key:
        max_temp = max(max_temp, value)

    # Cambio de ciudad → imprimir resultado
    else:
        print(f"{current_key}\t{max_temp}")
        current_key = key
        max_temp = value

# Última ciudad
print(f"{current_key}\t{max_temp}")

```

    Writing reducerEjercicio1.py



```python
!hadoop jar \
/usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.4.0.jar \
-file mapperEjercicio1.py \
-file reducerEjercicio1.py \
-mapper mapperEjercicio1.py \
-reducer reducerEjercicio1.py \
-input /city_temperature.csv \
-output /ejercicio1
```

    2025-12-03 09:11:39,812 WARN streaming.StreamJob: -file option is deprecated, please use generic option -files instead.
    packageJobJar: [mapperEjercicio1.py, reducerEjercicio1.py, /tmp/hadoop-unjar193337600427174090/] [] /tmp/streamjob9054428671395279042.jar tmpDir=null
    2025-12-03 09:11:40,903 INFO client.DefaultNoHARMFailoverProxyProvider: Connecting to ResourceManager at yarnmanager/172.18.0.2:8032
    2025-12-03 09:11:41,098 INFO client.DefaultNoHARMFailoverProxyProvider: Connecting to ResourceManager at yarnmanager/172.18.0.2:8032
    2025-12-03 09:11:41,380 INFO mapreduce.JobResourceUploader: Disabling Erasure Coding for path: /tmp/hadoop-yarn/staging/root/.staging/job_1764750906611_0002
    2025-12-03 09:11:43,899 INFO mapred.FileInputFormat: Total input files to process : 1
    2025-12-03 09:11:43,945 INFO net.NetworkTopology: Adding a new node: /default-rack/172.18.0.3:9866
    2025-12-03 09:11:44,423 INFO mapreduce.JobSubmitter: number of splits:2
    2025-12-03 09:11:44,670 INFO mapreduce.JobSubmitter: Submitting tokens for job: job_1764750906611_0002
    2025-12-03 09:11:44,671 INFO mapreduce.JobSubmitter: Executing with tokens: []
    2025-12-03 09:11:44,955 INFO conf.Configuration: resource-types.xml not found
    2025-12-03 09:11:44,956 INFO resource.ResourceUtils: Unable to find 'resource-types.xml'.
    2025-12-03 09:11:46,052 INFO impl.YarnClientImpl: Submitted application application_1764750906611_0002
    2025-12-03 09:11:46,152 INFO mapreduce.Job: The url to track the job: http://yarnmanager:8088/proxy/application_1764750906611_0002/
    2025-12-03 09:11:46,156 INFO mapreduce.Job: Running job: job_1764750906611_0002
    2025-12-03 09:11:57,639 INFO mapreduce.Job: Job job_1764750906611_0002 running in uber mode : false
    2025-12-03 09:11:57,641 INFO mapreduce.Job:  map 0% reduce 0%
    2025-12-03 09:12:09,906 INFO mapreduce.Job:  map 100% reduce 0%
    2025-12-03 09:12:20,025 INFO mapreduce.Job:  map 100% reduce 100%
    2025-12-03 09:12:22,060 INFO mapreduce.Job: Job job_1764750906611_0002 completed successfully
    2025-12-03 09:12:22,204 INFO mapreduce.Job: Counters: 55
    	File System Counters
    		FILE: Number of bytes read=47411247
    		FILE: Number of bytes written=95765030
    		FILE: Number of read operations=0
    		FILE: Number of large read operations=0
    		FILE: Number of write operations=0
    		HDFS: Number of bytes read=140605114
    		HDFS: Number of bytes written=4613
    		HDFS: Number of read operations=11
    		HDFS: Number of large read operations=0
    		HDFS: Number of write operations=2
    		HDFS: Number of bytes read erasure-coded=0
    	Job Counters 
    		Killed map tasks=1
    		Launched map tasks=2
    		Launched reduce tasks=1
    		Data-local map tasks=2
    		Total time spent by all maps in occupied slots (ms)=18495
    		Total time spent by all reduces in occupied slots (ms)=7849
    		Total time spent by all map tasks (ms)=18495
    		Total time spent by all reduce tasks (ms)=7849
    		Total vcore-milliseconds taken by all map tasks=18495
    		Total vcore-milliseconds taken by all reduce tasks=7849
    		Total megabyte-milliseconds taken by all map tasks=18938880
    		Total megabyte-milliseconds taken by all reduce tasks=8037376
    	Map-Reduce Framework
    		Map input records=2906328
    		Map output records=2906327
    		Map output bytes=41598587
    		Map output materialized bytes=47411253
    		Input split bytes=186
    		Combine input records=0
    		Combine output records=0
    		Reduce input groups=321
    		Reduce shuffle bytes=47411253
    		Reduce input records=2906327
    		Reduce output records=321
    		Spilled Records=5812654
    		Shuffled Maps =2
    		Failed Shuffles=0
    		Merged Map outputs=2
    		GC time elapsed (ms)=360
    		CPU time spent (ms)=12110
    		Physical memory (bytes) snapshot=940634112
    		Virtual memory (bytes) snapshot=7638290432
    		Total committed heap usage (bytes)=837287936
    		Peak Map Physical memory (bytes)=321605632
    		Peak Map Virtual memory (bytes)=2542878720
    		Peak Reduce Physical memory (bytes)=299671552
    		Peak Reduce Virtual memory (bytes)=2554126336
    	Shuffle Errors
    		BAD_ID=0
    		CONNECTION=0
    		IO_ERROR=0
    		WRONG_LENGTH=0
    		WRONG_MAP=0
    		WRONG_REDUCE=0
    	File Input Format Counters 
    		Bytes Read=140604928
    	File Output Format Counters 
    		Bytes Written=4613
    2025-12-03 09:12:22,204 INFO streaming.StreamJob: Output directory: /ejercicio1



```python
!head -n 20 city_temperature.csv | python3 mapperEjercicio1.py | sort |python3 reducerEjercicio1.py
```

    Algiers	64.2



```python
!hdfs dfs -cat /ejercicio1/part-00000
```

    Abidjan	88.6
    Abilene	94.2
    Abu Dhabi	107.3
    Addis Ababa	77.0
    Akron Canton	86.1
    Albany	88.0
    Albuquerque	89.4
    Algiers	96.6
    Allentown	91.1
    Almaty	90.9
    Amarillo	92.5
    Amman	95.4
    Amsterdam	85.5
    Anchorage	75.3
    Ankara	87.9
    Antananarivo	78.5
    Ashabad	102.2
    Asheville	85.1
    Athens	94.3
    Atlanta	92.8
    Atlantic City	93.3
    Auckland	75.4
    Austin	94.5
    Baltimore	91.9
    Bangkok	93.0
    Bangui	93.7
    Banjul	93.6
    Barcelona	86.6
    Baton Rouge	90.2
    Beijing	92.9
    Beirut	91.1
    Belfast	77.6
    Belgrade	91.9
    Belize City	92.9
    Bern	83.7
    Bilbao	94.6
    Billings	90.6
    Birmingham	91.0
    Bishkek	91.1
    Bismarck	91.7
    Bissau	100.1
    Bogota	66.7
    Boise	94.2
    Bombay (Mumbai)	92.6
    Bonn	86.9
    Bordeaux	88.8
    Boston	90.7
    Brasilia	87.7
    Bratislava	85.5
    Brazzaville	88.7
    Bridgeport	87.0
    Bridgetown	88.0
    Brisbane	87.3
    Brownsville	91.2
    Brussels	85.4
    Bucharest	91.4
    Budapest	88.2
    Buenos Aires	90.9
    Buffalo	84.4
    Bujumbura	89.1
    Burlington	88.8
    Cairo	100.2
    Calcutta	96.8
    Calgary	79.1
    Canberra	93.2
    Capetown	83.8
    Caracas	89.9
    Caribou	83.4
    Casper	87.1
    Charleston	91.6
    Charlotte	90.4
    Chattanooga	92.7
    Chengdu	90.6
    Chennai (Madras)	97.9
    Cheyenne	84.7
    Chicago	92.3
    Cincinnati	89.2
    Cleveland	87.2
    Colombo	88.3
    Colorado Springs	86.4
    Columbia	92.8
    Columbus	97.7
    Conakry	89.6
    Concord	90.1
    Copenhagen	77.5
    Corpus Christi	93.0
    Cotonou	88.6
    Dakar	87.0
    Dallas Ft Worth	98.2
    Damascus	95.5
    Dar Es Salaam	90.4
    Dayton	91.2
    Daytona Beach	87.8
    Delhi	103.7
    Denver	88.3
    Des Moines	93.0
    Detroit	88.6
    Dhahran	107.8
    Dhaka	91.4
    Doha	108.5
    Dubai	107.5
    Dublin	70.1
    Duluth	85.6
    Dusanbe	97.6
    Edmonton	82.8
    El Paso	98.1
    Elkins	92.5
    Erie	86.4
    Eugene	85.4
    Evansville	91.5
    Fairbanks	79.5
    Fargo	91.4
    Flagstaff	83.5
    Flint	89.4
    Fort Smith	100.7
    Fort Wayne	89.4
    Frankfurt	85.2
    Freetown	88.7
    Fresno	102.6
    Geneva	85.2
    Georgetown	90.6
    Goodland	91.8
    Grand Junction	92.3
    Grand Rapids	89.1
    Great Falls	100.1
    Green Bay	91.3
    Greensboro	90.4
    Guadalajara	88.5
    Guangzhou	94.7
    Guatemala City	79.8
    Guayaquil	90.0
    Halifax	80.5
    Hamburg	89.8
    Hamilton	85.4
    Hanoi	96.0
    Harrisburg	92.0
    Hartford Springfield	89.8
    Havana	88.3
    Helena	89.3
    Helsinki	79.8
    Hong Kong	92.4
    Honolulu	87.2
    Houston	93.0
    Huntsville	91.5
    Indianapolis	94.0
    Islamabad	102.4
    Istanbul	88.7
    Jackson	89.6
    Jacksonville	88.3
    Jakarta	90.6
    Juneau	72.0
    Kampala	82.9
    Kansas City	92.6
    Karachi	99.7
    Katmandu	86.6
    Kiev	86.9
    Knoxville	91.7
    Kuala Lumpur	89.6
    Kuwait	110.0
    La Paz	63.4
    Lagos	93.2
    Lake Charles	94.0
    Lansing	88.1
    Las Vegas	107.0
    Lexington	89.5
    Libreville	86.8
    Lilongwe	90.7
    Lima	81.8
    Lincoln	91.9
    Lisbon	96.3
    Little Rock	95.4
    Lome	90.1
    London	83.4
    Los Angeles	86.0
    Louisville	93.2
    Lubbock	94.1
    Lusaka	93.2
    Macon	91.1
    Madison	90.6
    Madrid	91.0
    Managua	93.9
    Manama	103.3
    Manila	91.9
    Maputo	95.6
    Medford	97.3
    Melbourne	92.8
    Memphis	93.6
    Mexico City	77.0
    Miami Beach	89.2
    Midland Odessa	94.6
    Milan	87.4
    Milwaukee	92.2
    Minneapolis St. Paul	92.0
    Minsk	83.5
    Mobile	88.9
    Monterrey	103.4
    Montgomery	91.2
    Montreal	84.6
    Montvideo	87.4
    Moscow	87.3
    Munich	81.8
    Muscat	105.9
    Nairobi	82.4
    Nashville	94.1
    Nassau	91.8
    New Orleans	90.1
    New York City	93.7
    Newark	95.6
    Niamey	102.8
    Nicosia	102.5
    Norfolk	93.2
    North Platte	91.1
    Nouakchott	99.5
    Oklahoma City	97.1
    Omaha	93.2
    Orlando	89.3
    Osaka	93.0
    Oslo	77.1
    Ottawa	84.9
    Paducah	91.8
    Panama City	90.6
    Paramaribo	90.5
    Paris	91.5
    Peoria	90.5
    Perth	95.2
    Philadelphia	92.9
    Phoenix	107.7
    Pittsburgh	88.4
    Pocatello	90.4
    Port au Prince	97.4
    Portland	89.4
    Prague	83.6
    Pristina	89.6
    Pueblo	94.7
    Pyongyang	89.4
    Quebec	82.9
    Quito	69.0
    Rabat	97.0
    Raleigh Durham	91.0
    Rangoon	99.3
    Rapid City	91.9
    Regina	83.2
    Reno	92.8
    Reykjavik	69.7
    Rhode Island	89.2
    Richmond	93.5
    Riga	81.2
    Rio de Janeiro	93.4
    Riyadh	105.0
    Roanoke	91.1
    Rochester	86.2
    Rockford	90.6
    Rome	85.8
    Sacramento	96.3
    Salem	90.5
    Salt Lake City	92.2
    San Angelo	96.3
    San Antonio	95.4
    San Diego	86.5
    San Francisco	82.7
    San Jose	85.6
    San Juan Puerto Rico	89.2
    Santo Domingo	87.4
    Sao Paulo	89.2
    Sapporo	82.5
    Sault Ste Marie	80.6
    Savannah	89.1
    Seattle	87.7
    Seoul	90.0
    Shanghai	96.8
    Shenyang	90.7
    Shreveport	95.4
    Singapore	88.5
    Sioux City	90.7
    Sioux Falls	94.3
    Skopje	88.0
    Sofia	86.0
    South Bend	89.4
    Spokane	93.2
    Springfield	92.8
    St Louis	96.3
    Stockholm	79.2
    Sydney	96.8
    Syracuse	87.5
    Taipei	94.0
    Tallahassee	92.8
    Tampa St. Petersburg	90.8
    Tashkent	95.4
    Tbilisi	90.6
    Tegucigalpa	88.0
    Tel Aviv	88.5
    Tirana	92.5
    Tokyo	90.6
    Toledo	89.8
    Topeka	95.6
    Toronto	88.8
    Tucson	101.6
    Tulsa	100.4
    Tunis	96.4
    Tupelo	92.8
    Ulan-bator	87.5
    Vancouver	83.1
    Vienna	86.2
    Vientiane	97.0
    Waco	96.1
    Warsaw	84.4
    Washington	92.8
    Washington DC	92.8
    West Palm Beach	89.3
    Wichita	96.1
    Wichita Falls	98.5
    Wilkes Barre	88.4
    Wilmington	89.7
    Windhoek	92.2
    Winnipeg	86.6
    Yakima	97.7
    Yerevan	91.8
    Youngstown	86.7
    Yuma	107.5
    Zagreb	87.5
    Zurich	82.4


### **Ejercicio 2: media histórica por país**

Calcula la temperatura media histórica para cada país. El proceso es similar al anterior, en el reducer debes ir recordando todos los datos que te lleguen de un mismo país y, cuando pase al siguiente país, calcular la media y emitirlos.


```python
%%writefile mapperEjercicio2.py
#!/usr/bin/env python3
import sys
import os

for line in sys.stdin:
    fields = line.strip().split(",")
    if fields[0] == "Region":
        continue

    key = fields[1]        # país
    value = fields[7]      # temperatura

    print(f"{key}\t{value}")
```

    Writing mapperEjercicio2.py



```python
%%writefile reducerEjercicio2.py
#!/usr/bin/env python3
import sys

current_key = None
acum = 0
count = 0

for line in sys.stdin:
    key, value = line.strip().split("\t")
    value = float(value)

    if current_key is None:
        current_key = key
        acum = value
        count = 1
        continue

    if key == current_key:
        acum += value
        count += 1
    else:
        print(current_key, acum/count)
        current_key = key
        acum = value
        count = 1

print(current_key, acum/count)

```

    Overwriting reducerEjercicio2.py



```python
!head -n 3 city_temperature.csv | python3 mapperEjercicio2.py | sort |python3 reducerEjercicio2.py
```

    Algeria 56.8



```python
!hadoop jar \
/usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.4.0.jar \
-file mapperEjercicio2.py \
-file reducerEjercicio2.py \
-mapper mapperEjercicio2.py \
-reducer reducerEjercicio2.py \
-input /city_temperature.csv \
-output /ejercicio2
```

    2025-12-03 09:24:15,581 WARN streaming.StreamJob: -file option is deprecated, please use generic option -files instead.
    packageJobJar: [mapperEjercicio2.py, reducerEjercicio2.py, /tmp/hadoop-unjar2056735290657385595/] [] /tmp/streamjob8675868696803414386.jar tmpDir=null
    2025-12-03 09:24:17,170 INFO client.DefaultNoHARMFailoverProxyProvider: Connecting to ResourceManager at yarnmanager/172.18.0.2:8032
    2025-12-03 09:24:17,434 INFO client.DefaultNoHARMFailoverProxyProvider: Connecting to ResourceManager at yarnmanager/172.18.0.2:8032
    2025-12-03 09:24:17,729 INFO mapreduce.JobResourceUploader: Disabling Erasure Coding for path: /tmp/hadoop-yarn/staging/root/.staging/job_1764750906611_0003
    2025-12-03 09:24:18,691 INFO mapred.FileInputFormat: Total input files to process : 1
    2025-12-03 09:24:18,718 INFO net.NetworkTopology: Adding a new node: /default-rack/172.18.0.3:9866
    2025-12-03 09:24:19,186 INFO mapreduce.JobSubmitter: number of splits:2
    2025-12-03 09:24:19,891 INFO mapreduce.JobSubmitter: Submitting tokens for job: job_1764750906611_0003
    2025-12-03 09:24:19,892 INFO mapreduce.JobSubmitter: Executing with tokens: []
    2025-12-03 09:24:20,210 INFO conf.Configuration: resource-types.xml not found
    2025-12-03 09:24:20,211 INFO resource.ResourceUtils: Unable to find 'resource-types.xml'.
    2025-12-03 09:24:20,434 INFO impl.YarnClientImpl: Submitted application application_1764750906611_0003
    2025-12-03 09:24:20,506 INFO mapreduce.Job: The url to track the job: http://yarnmanager:8088/proxy/application_1764750906611_0003/
    2025-12-03 09:24:20,510 INFO mapreduce.Job: Running job: job_1764750906611_0003
    2025-12-03 09:24:29,774 INFO mapreduce.Job: Job job_1764750906611_0003 running in uber mode : false
    2025-12-03 09:24:29,775 INFO mapreduce.Job:  map 0% reduce 0%
    2025-12-03 09:24:41,126 INFO mapreduce.Job:  map 50% reduce 0%
    2025-12-03 09:24:42,132 INFO mapreduce.Job:  map 100% reduce 0%
    2025-12-03 09:24:53,387 INFO mapreduce.Job:  map 100% reduce 100%
    2025-12-03 09:24:53,403 INFO mapreduce.Job: Job job_1764750906611_0003 completed successfully
    2025-12-03 09:24:53,523 INFO mapreduce.Job: Counters: 55
    	File System Counters
    		FILE: Number of bytes read=37383722
    		FILE: Number of bytes written=75709980
    		FILE: Number of read operations=0
    		FILE: Number of large read operations=0
    		FILE: Number of write operations=0
    		HDFS: Number of bytes read=140605114
    		HDFS: Number of bytes written=3520
    		HDFS: Number of read operations=11
    		HDFS: Number of large read operations=0
    		HDFS: Number of write operations=2
    		HDFS: Number of bytes read erasure-coded=0
    	Job Counters 
    		Killed map tasks=1
    		Launched map tasks=2
    		Launched reduce tasks=1
    		Data-local map tasks=2
    		Total time spent by all maps in occupied slots (ms)=18605
    		Total time spent by all reduces in occupied slots (ms)=9051
    		Total time spent by all map tasks (ms)=18605
    		Total time spent by all reduce tasks (ms)=9051
    		Total vcore-milliseconds taken by all map tasks=18605
    		Total vcore-milliseconds taken by all reduce tasks=9051
    		Total megabyte-milliseconds taken by all map tasks=19051520
    		Total megabyte-milliseconds taken by all reduce tasks=9268224
    	Map-Reduce Framework
    		Map input records=2906328
    		Map output records=2906327
    		Map output bytes=31571062
    		Map output materialized bytes=37383728
    		Input split bytes=186
    		Combine input records=0
    		Combine output records=0
    		Reduce input groups=125
    		Reduce shuffle bytes=37383728
    		Reduce input records=2906327
    		Reduce output records=125
    		Spilled Records=5812654
    		Shuffled Maps =2
    		Failed Shuffles=0
    		Merged Map outputs=2
    		GC time elapsed (ms)=280
    		CPU time spent (ms)=13420
    		Physical memory (bytes) snapshot=976236544
    		Virtual memory (bytes) snapshot=7639379968
    		Total committed heap usage (bytes)=833617920
    		Peak Map Physical memory (bytes)=324710400
    		Peak Map Virtual memory (bytes)=2544930816
    		Peak Reduce Physical memory (bytes)=333746176
    		Peak Reduce Virtual memory (bytes)=2551472128
    	Shuffle Errors
    		BAD_ID=0
    		CONNECTION=0
    		IO_ERROR=0
    		WRONG_LENGTH=0
    		WRONG_MAP=0
    		WRONG_REDUCE=0
    	File Input Format Counters 
    		Bytes Read=140604928
    	File Output Format Counters 
    		Bytes Written=3520
    2025-12-03 09:24:53,524 INFO streaming.StreamJob: Output directory: /ejercicio2



```python
!hdfs dfs -cat /ejercicio2/part-00000
```

    Albania 33.17292251241098	
    Algeria 63.755439240232846	
    Argentina 62.304899633067144	
    Australia 61.634293114612284	
    Austria 51.04722641916694	
    Bahamas 76.57303831624387	
    Bahrain 80.63559248866852	
    Bangladesh 10.109879518072239	
    Barbados 77.00251697494731	
    Belarus 41.82123272884303	
    Belgium 51.057047269587805	
    Belize 73.47807405808072	
    Benin 76.15212605223373	
    Bermuda 66.97127603710848	
    Bolivia 44.867148715734956	
    Brazil 70.1315249847108	
    Bulgaria 45.203345564429	
    Burundi -65.39713845476538	
    Canada 42.00524749141337	
    Central African Republic 67.01951219512186	
    China 59.98367545166168	
    Colombia 55.243956399740966	
    Congo 69.31744198596857	
    Costa Rica 70.37572846967407	
    Croatia 46.92861305990289	
    Cuba 72.64080310880813	
    Cyprus 23.77747699929234	
    Czech Republic 47.60325922728247	
    Denmark 46.96044679473335	
    Dominican Republic 65.21575822989749	
    Egypt 71.95347507014894	
    Equador 59.94560884271546	
    Ethiopia 25.45525551371703	
    Finland 42.243999568314095	
    France 54.69657349449607	
    Gabon 70.39779792746123	
    Gambia 59.66582708528549	
    Georgia 46.51603471904955	
    Germany 6.421902994108639	
    Greece 59.63387072243337	
    Guatemala 56.911353334772286	
    Guinea 49.38939132311684	
    Guinea-Bissau 2.3921217353766413	
    Guyana -22.101520236920035	
    Haiti 16.68519637462248	
    Honduras 68.53149487317835	
    Hong Kong 75.06277789769037	
    Hungary 51.09906108353103	
    Iceland 41.08276494711854	
    India 79.76246121468733	
    Indonesia 35.98840798704798	
    Ireland 49.0667817828619	
    Israel 54.020448179271845	
    Italy 57.210371249730166	
    Ivory Coast 75.13995251456927	
    Japan 55.85347147276793	
    Jordan 64.16010144614734	
    Kazakhstan 49.31983810037769	
    Kenya 23.452060975609765	
    Kuwait 79.49446363047706	
    Kyrgyzstan 51.3730000000004	
    Laos 79.96746168789139	
    Latvia 44.136423483703844	
    Lebanon 69.39838117850233	
    Macedonia 54.00780356179178	
    Madagascar 63.44589898553835	
    Malawi -20.585543650096575	
    Malaysia 78.95312972156238	
    Mauritania 73.41478705686406	
    Mexico 47.615236724602546	
    Mongolia 29.695078782646313	
    Morocco 62.73345564429088	
    Mozambique 62.783186316695556	
    Myanmar (Burma) 71.51167709907165	
    Namibia 57.99034103172874	
    Nepal 49.4923475445224	
    New Zealand 58.91374919058926	
    Nicaragua 71.85128177393172	
    Nigeria 61.991546259613074	
    North Korea 48.21019857543701	
    Norway 40.923372044794604	
    Oman 21.888976113042443	
    Pakistan 71.6510145709658	
    Panama 79.57879343837666	
    Peru 66.63344696473035	
    Philippines 81.54242391538949	
    Poland 47.77608461040342	
    Portugal 61.85777034319007	
    Qatar 82.23562486509832	
    Romania 52.36450464062175	
    Russia 44.96580211335245	
    Saudi Arabia 79.15030218001289	
    Senegal 75.55507230736012	
    Serbia-Montenegro 42.396761015465415	
    Sierra Leone -9.820260911579922	
    Singapore 81.65440319447448	
    Slovakia 51.44646017699106	
    South Africa 61.94041657673202	
    South Korea 52.87797323548463	
    Spain 59.46831786459405	
    Sri Lanka 74.24142024606074	
    Suriname 47.51491152352201	
    Sweden 45.093503129721725	
    Switzerland 49.829397798402766	
    Syria 62.8061198057204	
    Taiwan 69.33387653788024	
    Tajikistan 35.15456507662428	
    Tanzania 65.30484079173851	
    Thailand 72.4640858815876	
    The Netherlands 50.81807684006042	
    Togo 71.56976041441825	
    Tunisia 66.47864234837043	
    Turkey 55.17841031728919	
    Turkmenistan 62.04968702784378	
    US 56.122331940987806	
    Uganda 44.14252563410687	
    Ukraine 47.66315562270658	
    United Arab Emirates 82.58256529246725	
    United Kingdom 51.00676667386163	
    Uruguay 60.9748650982086	
    Uzbekistan 58.806345780272224	
    Venezuela 78.32601187263904	
    Vietnam 74.73731923159944	
    Yugoslavia 54.032840492121686	
    Zambia 55.903461648951435	


Ejercicio 3: conteo de días calurosos por ciudad

Calcula cuántos días calurosos (definidos como >30 grados) hubo en cada año en cada ciudad.


```python
%%writefile mapperEjercicio3.py
#!/usr/bin/env python3
import sys
import os

for line in sys.stdin:
    fields = line.strip().split(",")
    if fields[0] == "Region":
        continue

    temp = float(fields[7])
    if temp > 30:     # condición clave
        city = fields[3]
        year = fields[6]

        key = f"{city}-{year}"
        value = 1     # contamos días

        print(f"{key}\t1")

```

    Overwriting mapperEjercicio3.py



```python
%%writefile reducerEjercicio3.py
#!/usr/bin/env python3
import sys
import os

current_key = None
count_hot = 0

for line in sys.stdin:
    key, value = line.strip().split("\t")
    value = int(value)

    if current_key is None:
        current_key = key
        count_hot = value
        continue

    if current_key == key:
        count_hot += 1
    else:
        print(current_key, count_hot)
        current_key = key
        count_hot = value

print(current_key, count_hot)
```

    Overwriting reducerEjercicio3.py



```python
!head -n 10 city_temperature.csv | python3 mapperEjercicio3.py | sort |python3 reducerEjercicio3.py
```

    Algiers-1995 9



```python
!hadoop jar \
/usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.4.0.jar \
-file mapperEjercicio3.py \
-file reducerEjercicio3.py \
-mapper mapperEjercicio3.py \
-reducer reducerEjercicio3.py \
-input /city_temperature.csv \
-output /ejercicio3
```

    2025-12-03 09:39:36,233 WARN streaming.StreamJob: -file option is deprecated, please use generic option -files instead.
    packageJobJar: [mapperEjercicio3.py, reducerEjercicio3.py, /tmp/hadoop-unjar383009423379717422/] [] /tmp/streamjob8325791567600607406.jar tmpDir=null
    2025-12-03 09:39:37,409 INFO client.DefaultNoHARMFailoverProxyProvider: Connecting to ResourceManager at yarnmanager/172.18.0.2:8032
    2025-12-03 09:39:37,603 INFO client.DefaultNoHARMFailoverProxyProvider: Connecting to ResourceManager at yarnmanager/172.18.0.2:8032
    2025-12-03 09:39:37,897 INFO mapreduce.JobResourceUploader: Disabling Erasure Coding for path: /tmp/hadoop-yarn/staging/root/.staging/job_1764750906611_0005
    2025-12-03 09:39:39,018 INFO mapred.FileInputFormat: Total input files to process : 1
    2025-12-03 09:39:39,047 INFO net.NetworkTopology: Adding a new node: /default-rack/172.18.0.3:9866
    2025-12-03 09:39:39,532 INFO mapreduce.JobSubmitter: number of splits:2
    2025-12-03 09:39:39,734 INFO mapreduce.JobSubmitter: Submitting tokens for job: job_1764750906611_0005
    2025-12-03 09:39:39,734 INFO mapreduce.JobSubmitter: Executing with tokens: []
    2025-12-03 09:39:40,040 INFO conf.Configuration: resource-types.xml not found
    2025-12-03 09:39:40,041 INFO resource.ResourceUtils: Unable to find 'resource-types.xml'.
    2025-12-03 09:39:40,175 INFO impl.YarnClientImpl: Submitted application application_1764750906611_0005
    2025-12-03 09:39:40,289 INFO mapreduce.Job: The url to track the job: http://yarnmanager:8088/proxy/application_1764750906611_0005/
    2025-12-03 09:39:40,290 INFO mapreduce.Job: Running job: job_1764750906611_0005
    2025-12-03 09:39:48,684 INFO mapreduce.Job: Job job_1764750906611_0005 running in uber mode : false
    2025-12-03 09:39:48,686 INFO mapreduce.Job:  map 0% reduce 0%
    2025-12-03 09:39:59,961 INFO mapreduce.Job:  map 100% reduce 0%
    2025-12-03 09:40:10,084 INFO mapreduce.Job:  map 100% reduce 100%
    2025-12-03 09:40:11,102 INFO mapreduce.Job: Job job_1764750906611_0005 completed successfully
    2025-12-03 09:40:11,250 INFO mapreduce.Job: Counters: 55
    	File System Counters
    		FILE: Number of bytes read=48201793
    		FILE: Number of bytes written=97346122
    		FILE: Number of read operations=0
    		FILE: Number of large read operations=0
    		FILE: Number of write operations=0
    		HDFS: Number of bytes read=140605114
    		HDFS: Number of bytes written=153755
    		HDFS: Number of read operations=11
    		HDFS: Number of large read operations=0
    		HDFS: Number of write operations=2
    		HDFS: Number of bytes read erasure-coded=0
    	Job Counters 
    		Killed map tasks=1
    		Launched map tasks=2
    		Launched reduce tasks=1
    		Data-local map tasks=2
    		Total time spent by all maps in occupied slots (ms)=18390
    		Total time spent by all reduces in occupied slots (ms)=6873
    		Total time spent by all map tasks (ms)=18390
    		Total time spent by all reduce tasks (ms)=6873
    		Total vcore-milliseconds taken by all map tasks=18390
    		Total vcore-milliseconds taken by all reduce tasks=6873
    		Total megabyte-milliseconds taken by all map tasks=18831360
    		Total megabyte-milliseconds taken by all reduce tasks=7037952
    	Map-Reduce Framework
    		Map input records=2906328
    		Map output records=2625964
    		Map output bytes=42949859
    		Map output materialized bytes=48201799
    		Input split bytes=186
    		Combine input records=0
    		Combine output records=0
    		Reduce input groups=7964
    		Reduce shuffle bytes=48201799
    		Reduce input records=2625964
    		Reduce output records=7964
    		Spilled Records=5251928
    		Shuffled Maps =2
    		Failed Shuffles=0
    		Merged Map outputs=2
    		GC time elapsed (ms)=286
    		CPU time spent (ms)=12870
    		Physical memory (bytes) snapshot=989855744
    		Virtual memory (bytes) snapshot=7636283392
    		Total committed heap usage (bytes)=857735168
    		Peak Map Physical memory (bytes)=375504896
    		Peak Map Virtual memory (bytes)=2542862336
    		Peak Reduce Physical memory (bytes)=291622912
    		Peak Reduce Virtual memory (bytes)=2552492032
    	Shuffle Errors
    		BAD_ID=0
    		CONNECTION=0
    		IO_ERROR=0
    		WRONG_LENGTH=0
    		WRONG_MAP=0
    		WRONG_REDUCE=0
    	File Input Format Counters 
    		Bytes Read=140604928
    	File Output Format Counters 
    		Bytes Written=153755
    2025-12-03 09:40:11,250 INFO streaming.StreamJob: Output directory: /ejercicio3



```python
!hdfs dfs -cat /ejercicio3/part-00000
```

### **Ejercicio 4: rango de temperaturas por ciudad (Min/Max)**

Encuentra la temperatura mínima y máxima registrada para cada región.


```python
%%writefile mapperEjercicio4.py
#!/usr/bin/env python3
import sys
import os

for line in sys.stdin:
    fields = line.strip().split(",")
    if fields[0] == "Region":
        continue

    key = fields[1]        # región
    value = fields[7]      # temperatura

    print(f"{key}\t{value}")
```

    Overwriting mapperEjercicio4.py



```python
%%writefile reducerEjercicio4.py
#!/usr/bin/env python3
import sys
import os

current_key = None
min_temp = None
max_temp = None

for line in sys.stdin:
    key, value = line.strip().split("\t")
    value = float(value)
    
    if value == -99.0:
        continue
        
    if current_key is None:
        current_key = key
        min_temp = value
        max_temp = value
        continue

    if key == current_key:
        min_temp = min(min_temp, value)
        max_temp = max(max_temp, value)
    else:
        print(current_key, min_temp, max_temp)
        current_key = key
        min_temp = value
        max_temp = value

print(current_key, min_temp, max_temp)

```

    Overwriting reducerEjercicio4.py



```python
!head -n 200000 city_temperature.csv | python3 mapperEjercicio4.py | sort |python3 reducerEjercicio4.py
```

    Algeria 33.3 96.6
    Benin 56.4 88.6
    Burundi 48.2 89.1
    Central African Republic 59.9 93.7
    Congo 61.2 88.7
    Egypt 45.2 100.2
    Ethiopia 50.4 77.0
    Gabon 40.6 86.8
    Gambia 64.6 93.6
    Guinea 65.2 89.6
    Guinea-Bissau 65.4 100.1
    Ivory Coast 40.3 88.6
    Kenya 51.8 82.4
    Madagascar 33.8 78.5
    Malawi 50.9 90.7
    Mauritania 58.3 99.5
    Morocco 33.8 97.0
    Mozambique 53.2 95.6
    Namibia 38.8 92.2
    Nigeria 63.5 102.8
    Senegal 63.2 87.0
    Sierra Leone 57.8 88.7
    South Africa 45.4 80.4



```python
!hadoop jar \
/usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.4.0.jar \
-file mapperEjercicio4.py \
-file reducerEjercicio4.py \
-mapper mapperEjercicio4.py \
-reducer reducerEjercicio4.py \
-input /city_temperature.csv \
-output /ejercicio4
```

    2025-12-03 11:05:17,823 WARN streaming.StreamJob: -file option is deprecated, please use generic option -files instead.
    packageJobJar: [mapperEjercicio4.py, reducerEjercicio4.py, /tmp/hadoop-unjar2253260645950622960/] [] /tmp/streamjob4792298733549391356.jar tmpDir=null
    2025-12-03 11:05:19,174 INFO client.DefaultNoHARMFailoverProxyProvider: Connecting to ResourceManager at yarnmanager/172.18.0.2:8032
    2025-12-03 11:05:19,381 INFO client.DefaultNoHARMFailoverProxyProvider: Connecting to ResourceManager at yarnmanager/172.18.0.2:8032
    2025-12-03 11:05:19,708 INFO mapreduce.JobResourceUploader: Disabling Erasure Coding for path: /tmp/hadoop-yarn/staging/root/.staging/job_1764750906611_0006
    2025-12-03 11:05:21,223 INFO mapred.FileInputFormat: Total input files to process : 1
    2025-12-03 11:05:21,302 INFO net.NetworkTopology: Adding a new node: /default-rack/172.18.0.3:9866
    2025-12-03 11:05:21,522 INFO mapreduce.JobSubmitter: number of splits:2
    2025-12-03 11:05:22,287 INFO mapreduce.JobSubmitter: Submitting tokens for job: job_1764750906611_0006
    2025-12-03 11:05:22,287 INFO mapreduce.JobSubmitter: Executing with tokens: []
    2025-12-03 11:05:22,637 INFO conf.Configuration: resource-types.xml not found
    2025-12-03 11:05:22,639 INFO resource.ResourceUtils: Unable to find 'resource-types.xml'.
    2025-12-03 11:05:23,071 INFO impl.YarnClientImpl: Submitted application application_1764750906611_0006
    2025-12-03 11:05:23,167 INFO mapreduce.Job: The url to track the job: http://yarnmanager:8088/proxy/application_1764750906611_0006/
    2025-12-03 11:05:23,171 INFO mapreduce.Job: Running job: job_1764750906611_0006
    2025-12-03 11:05:31,410 INFO mapreduce.Job: Job job_1764750906611_0006 running in uber mode : false
    2025-12-03 11:05:31,412 INFO mapreduce.Job:  map 0% reduce 0%
    2025-12-03 11:05:43,879 INFO mapreduce.Job:  map 50% reduce 0%
    2025-12-03 11:05:44,891 INFO mapreduce.Job:  map 100% reduce 0%
    2025-12-03 11:05:56,134 INFO mapreduce.Job:  map 100% reduce 100%
    2025-12-03 11:05:58,172 INFO mapreduce.Job: Job job_1764750906611_0006 completed successfully
    2025-12-03 11:05:58,315 INFO mapreduce.Job: Counters: 54
    	File System Counters
    		FILE: Number of bytes read=37383722
    		FILE: Number of bytes written=75709980
    		FILE: Number of read operations=0
    		FILE: Number of large read operations=0
    		FILE: Number of write operations=0
    		HDFS: Number of bytes read=140605114
    		HDFS: Number of bytes written=2508
    		HDFS: Number of read operations=11
    		HDFS: Number of large read operations=0
    		HDFS: Number of write operations=2
    		HDFS: Number of bytes read erasure-coded=0
    	Job Counters 
    		Launched map tasks=2
    		Launched reduce tasks=1
    		Data-local map tasks=2
    		Total time spent by all maps in occupied slots (ms)=21735
    		Total time spent by all reduces in occupied slots (ms)=9559
    		Total time spent by all map tasks (ms)=21735
    		Total time spent by all reduce tasks (ms)=9559
    		Total vcore-milliseconds taken by all map tasks=21735
    		Total vcore-milliseconds taken by all reduce tasks=9559
    		Total megabyte-milliseconds taken by all map tasks=22256640
    		Total megabyte-milliseconds taken by all reduce tasks=9788416
    	Map-Reduce Framework
    		Map input records=2906328
    		Map output records=2906327
    		Map output bytes=31571062
    		Map output materialized bytes=37383728
    		Input split bytes=186
    		Combine input records=0
    		Combine output records=0
    		Reduce input groups=125
    		Reduce shuffle bytes=37383728
    		Reduce input records=2906327
    		Reduce output records=125
    		Spilled Records=5812654
    		Shuffled Maps =2
    		Failed Shuffles=0
    		Merged Map outputs=2
    		GC time elapsed (ms)=303
    		CPU time spent (ms)=15310
    		Physical memory (bytes) snapshot=977674240
    		Virtual memory (bytes) snapshot=7632949248
    		Total committed heap usage (bytes)=880803840
    		Peak Map Physical memory (bytes)=370798592
    		Peak Map Virtual memory (bytes)=2544472064
    		Peak Reduce Physical memory (bytes)=285868032
    		Peak Reduce Virtual memory (bytes)=2547949568
    	Shuffle Errors
    		BAD_ID=0
    		CONNECTION=0
    		IO_ERROR=0
    		WRONG_LENGTH=0
    		WRONG_MAP=0
    		WRONG_REDUCE=0
    	File Input Format Counters 
    		Bytes Read=140604928
    	File Output Format Counters 
    		Bytes Written=2508
    2025-12-03 11:05:58,316 INFO streaming.StreamJob: Output directory: /ejercicio4



```python
!hdfs dfs -cat /ejercicio4/part-00000
```

    Albania 24.9 92.5	
    Algeria 33.3 96.6	
    Argentina 35.3 90.9	
    Australia 30.7 96.8	
    Austria 3.8 86.2	
    Bahamas 58.7 91.8	
    Bahrain 50.5 103.3	
    Bangladesh 54.3 91.4	
    Barbados 74.2 88.0	
    Belarus -15.8 83.5	
    Belgium 8.8 85.4	
    Belize 64.6 92.9	
    Benin 56.4 88.6	
    Bermuda 51.1 85.4	
    Bolivia 32.8 63.4	
    Brazil 44.8 93.4	
    Bulgaria 2.6 86.0	
    Burundi 48.2 89.1	
    Canada -36.5 88.8	
    Central African Republic 59.9 93.7	
    China -17.0 96.8	
    Colombia 46.7 66.7	
    Congo 61.2 88.7	
    Costa Rica 63.1 85.6	
    Croatia 10.2 87.5	
    Cuba 46.9 88.3	
    Cyprus 33.9 102.5	
    Czech Republic -3.1 83.6	
    Denmark 9.3 77.5	
    Dominican Republic 65.0 87.4	
    Egypt 45.2 100.2	
    Equador 49.1 90.0	
    Ethiopia 50.4 77.0	
    Finland -13.6 79.8	
    France 13.8 91.5	
    Gabon 40.6 86.8	
    Gambia 64.6 93.6	
    Georgia 14.7 90.6	
    Germany 1.8 89.8	
    Greece 28.4 94.3	
    Guatemala 51.2 79.8	
    Guinea 65.2 89.6	
    Guinea-Bissau 65.4 100.1	
    Guyana 67.0 90.6	
    Haiti 71.4 97.4	
    Honduras 56.1 88.0	
    Hong Kong 40.2 92.4	
    Hungary 7.3 88.2	
    Iceland 10.6 69.7	
    India 43.9 103.7	
    Indonesia 71.3 90.6	
    Ireland 17.1 70.1	
    Israel 45.1 88.5	
    Italy 14.3 87.4	
    Ivory Coast 40.3 88.6	
    Japan -1.7 93.0	
    Jordan 33.3 95.4	
    Kazakhstan -14.2 90.9	
    Kenya 51.8 82.4	
    Kuwait 41.4 110.0	
    Kyrgyzstan -10.8 91.1	
    Laos 51.4 97.0	
    Latvia -12.1 81.2	
    Lebanon 44.5 91.1	
    Macedonia 0.3 88.0	
    Madagascar 33.8 78.5	
    Malawi 50.9 90.7	
    Malaysia 73.4 89.6	
    Mauritania 58.3 99.5	
    Mexico 28.6 103.4	
    Mongolia -37.2 87.5	
    Morocco 33.8 97.0	
    Mozambique 53.2 95.6	
    Myanmar (Burma) 50.9 99.3	
    Namibia 38.8 92.2	
    Nepal 36.6 86.6	
    New Zealand 41.1 75.4	
    Nicaragua 68.5 93.9	
    Nigeria 63.5 102.8	
    North Korea -4.7 89.4	
    Norway -8.7 77.1	
    Oman 60.7 105.9	
    Pakistan 36.2 102.4	
    Panama 73.4 90.6	
    Peru 57.5 81.8	
    Philippines 70.9 91.9	
    Poland -8.1 84.4	
    Portugal 39.0 96.3	
    Qatar 49.6 108.5	
    Romania 1.9 91.4	
    Russia -20.4 91.8	
    Saudi Arabia 38.0 107.8	
    Senegal 63.2 87.0	
    Serbia-Montenegro -3.3 89.6	
    Sierra Leone 57.8 88.7	
    Singapore 73.3 88.5	
    Slovakia 5.6 85.5	
    South Africa 44.9 83.8	
    South Korea -0.6 90.0	
    Spain 24.9 94.6	
    Sri Lanka 70.3 88.3	
    Suriname 71.6 90.5	
    Sweden -5.0 79.2	
    Switzerland 4.7 85.2	
    Syria 26.8 95.5	
    Taiwan 41.5 94.0	
    Tajikistan 7.5 97.6	
    Tanzania 65.0 90.4	
    Thailand 63.0 93.0	
    The Netherlands 11.0 85.5	
    Togo 69.6 90.1	
    Tunisia 36.6 96.4	
    Turkey 3.2 88.7	
    Turkmenistan 6.8 102.2	
    US -50.0 107.7	
    Uganda 64.4 82.9	
    Ukraine -11.1 86.9	
    United Arab Emirates 55.8 107.5	
    United Kingdom 12.5 83.4	
    Uruguay 35.7 87.4	
    Uzbekistan 3.8 95.4	
    Venezuela 71.5 89.9	
    Vietnam 44.7 96.0	
    Yugoslavia 1.4 91.9	
    Zambia 47.8 93.2	



```python

```
