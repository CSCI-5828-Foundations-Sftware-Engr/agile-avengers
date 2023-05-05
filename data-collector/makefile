VERSION=v0
DOCKERUSER=ash002019

black:
	python -m black src

isort:
	python -m isort src

build:
	docker build -t agile-avengers-data-collector .

build-dev:
	docker build -t agile-avengers-data-collector:dev .

push:
	docker tag agile-avengers-data-collector $(DOCKERUSER)/agile-avengers-data-collector:$(VERSION)
	docker push $(DOCKERUSER)/agile-avengers-data-collector:$(VERSION)
	docker tag agile-avengers-data-collector $(DOCKERUSER)/agile-avengers-data-collector:latest
	docker push $(DOCKERUSER)/agile-avengers-data-collector:latest

deploy:
	kubectl apply -f deployment.yaml
	kubectl apply -f service.yaml

delete:
	kubectl delete deploy/data-collector
	kubectl delete service/data-collector-svc