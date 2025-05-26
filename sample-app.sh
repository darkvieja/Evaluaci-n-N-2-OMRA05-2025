#!/bin/bash

mkdir tempdir
mkdir tempdir/templates
mkdir tempdir/static

cp sample_app.py tempdir/.
cp -r templates/* tempdir/templates/.
cp -r static/* tempdir/static/.

echo "FROM python" >> tempdir/Dockerfile
echo "RUN pip install flask" >> tempdir/Dockerfile
echo "COPY  ./static /home/myapp/static/" >> tempdir/Dockerfile
echo "COPY  ./templates /home/myapp/templates/" >> tempdir/Dockerfile
echo "COPY  sample_app.py /home/myapp/" >> tempdir/Dockerfile
echo "EXPOSE 6789" >> tempdir/Dockerfile
echo "CMD python /home/myapp/sample_app.py" >> tempdir/Dockerfile

cd tempdir

echo "Construyendo imagen Docker..."
docker build -t sampleapp .

echo "Deteniendo contenedor anterior si existe..."
docker rm -f samplerunning || true

echo "Ejecutando contenedor sampleapp en el puerto 6789..."
docker run -t -d -p 6789:6789 --name samplerunning sampleapp

echo "Contenedores actuales:"
docker ps -a
 
