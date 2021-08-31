# backend docker setup

## 1. for init config and directory
python3 proj_setup/setup.py

## 2. for docker building

```
docker image build -t kit_test .
```

## 3. for docker running
```
bash proj_setup/run.sh
```
