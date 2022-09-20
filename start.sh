docker build -t tide . &&
docker run -v /"$PWD":/opt -it tide