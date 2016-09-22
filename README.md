# Betabeers ODB: Yo, Bot

## Instalacion

```bash
vagrant up --provision
```

Cuando la maquina esta provisionada

```bash
vagrant ssh
cd project
```

Necesitamos modificar la envvar `FLASK_BASE_URL` en `launch.sh` para que
contenga un host público válido para que telegram tenga acceso a su webhook y podamos
recibir su mensaje vía POST.


```bash
bash launch.sh
```

## Ejecutar tests

```bash
python -m unittest discover
```
