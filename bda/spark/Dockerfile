# 1. Imagen base: Python 3.11 (Ligera y moderna)
FROM python:3.10-slim

# 2. Variables de versión
ENV SPARK_VERSION=3.5.7
ENV HADOOP_VERSION=3
ENV JAVA_VERSION=21

# 3. Instalación de dependencias del sistema y JAVA
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    openjdk-${JAVA_VERSION}-jre-headless \
    curl \
    procps \
    pandoc \
    texlive-xetex \
    texlive-fonts-recommended \
    texlive-plain-generic \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 4. Configurar variables de entorno JAVA_HOME
ENV JAVA_HOME=/usr/lib/jvm/java-${JAVA_VERSION}-openjdk-amd64
ENV SPARK_HOME=/opt/spark
ENV PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin

# 5. Descargar e instalar Apache Spark. Versión precompilada estándar (Scala 2.12)
RUN curl -o spark.tgz https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz && \
    tar -xf spark.tgz && \
    mv spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} /opt/spark && \
    rm spark.tgz

# 6. Instalar JupyterLab y PySpark
RUN pip install --no-cache-dir \
    jupyterlab \
    notebook \
    findspark \
    pyspark==${SPARK_VERSION}

# 7. Configuración del directorio de trabajo
WORKDIR /workspace

# 8. Exponer puertos
# 8888: Jupyter Notebook
# 4040: Spark UI (Monitorización del trabajo local)
EXPOSE 8888 4040

# 9. Comando de inicio por defecto
# Iniciamos Jupyter Lab, accesible desde cualquier IP, sin token
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token=''"]