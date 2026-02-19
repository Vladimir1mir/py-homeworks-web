### Сборка образа

```
docker build ./ --tag stockproducts:0.0.1
```

### Запуск контейнера

```
docker run --name my_stockproducts -d -p 8000:8000 stockproducts:0.0.1
```
