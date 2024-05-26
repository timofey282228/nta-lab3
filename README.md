# Реалiзацiя алгоритму дискретного логарифмування index-calculus

## Docker

```shell
docker pull timofey282228/nta-lab3
# Тепер образ контейнера доступний локально і з ним можна працювати
# Виведемо всі опції
docker run --rm -it timofey282228/nta-lab3 --help
```

> [!NOTE]
> Команда `benchmark` в Docker-контейнері __не працюватиме__,
> оскільки вимагає наявності `docker` для запуску контейнера генератора задач.

## Local

```shell
git clone https://github.com/timofey282228/nta-lab3.git
cd nta-lab3
poetry install
poetry run python -m nta_lab2 --help
```
