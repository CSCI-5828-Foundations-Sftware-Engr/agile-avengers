VERSION=v0
DOCKERUSER=ash002019

black:
	python -m black src

isort:
	python -m isort src

build:
	docker build -t agile-avengers-data-analyzer .

build-dev:
	docker build -t agile-avengers-data-analyzer:dev .

push:
	docker tag agile-avengers-data-analyzer $(DOCKERUSER)/agile-avengers-data-analyzer:$(VERSION)
	docker push $(DOCKERUSER)/agile-avengers-data-analyzer:$(VERSION)
	docker tag agile-avengers-data-analyzer $(DOCKERUSER)/agile-avengers-data-analyzer:latest
	docker push $(DOCKERUSER)/agile-avengers-data-analyzer:latest

deploy:
	kubectl apply -f deployment.yaml
	kubectl apply -f service.yaml
	kubectl apply -f ingress.yaml

delete:
	kubectl delete deploy/data-analyzer
	kubectl delete service/data-analyzer-svc