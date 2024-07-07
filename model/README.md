# ML
На данный момент эта чать кода развернута в датасфере, поэтому в проекте эта директория никак не задействуется напрямую. Но любой с легкостью может развернуть наше решение при помощи docker:
## Запуск нашего решения

```cmd
docker build -t girya_team .
```

```cmd
docker run -p 5000:5000 girya_team
```

## Запросы

### Проверка работоспособности
```
curl -H "Content-type: application/json" -X GET http://localhost:5000
```

### Запрос в модель
```
curl -H "Content-type: application/json" -X POST -d '{"text": "Текстовое сообщение."}' http://localhost:5000/generate
```
