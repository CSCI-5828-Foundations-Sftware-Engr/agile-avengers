VERSION=v0
DOCKERUSER=ash002019

build:
	docker build -t agile-avengers-frontend -f ../dockerfile ..

deploy:
	kubectl apply -f deployment.yaml
	kubectl apply -f service.yaml
	kubectl apply -f ingress.yaml

deploy-dev:
	kubectl apply -f deployment-dev.yaml
	kubectl apply -f service.yaml
	kubectl apply -f ingress.yaml

push:
	docker tag agile-avengers-frontend $(DOCKERUSER)/agile-avengers-frontend:$(VERSION)
	docker push $(DOCKERUSER)/agile-avengers-frontend:$(VERSION)
	docker tag agile-avengers-frontend $(DOCKERUSER)/agile-avengers-frontend:latest
	docker push $(DOCKERUSER)/agile-avengers-frontend:latest
	
delete:
	kubectl delete deployment/backend
	kubectl delete service/backend-svc
	kubectl delete ingress/backend

test:
	pytest -v --cov-report term --cov=. tests
	