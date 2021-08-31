# docker build

## for init setup 
(skip if use ```docker pull littlepenguin89106/kit```)
```
docker image build -t kit .
```

```
bash proj_setup/docker.sh
```
## run docker without init setup
```
docker stop kit-container
```

```
docker commit -c "ENV PROJ_INIT=1" kit-container test_init
```

```
bash proj_setup/test_docker.sh
```