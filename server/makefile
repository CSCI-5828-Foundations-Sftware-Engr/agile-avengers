build:
	docker build -t agile_avengers:dev .

deploy:
	kubectl apply -f deployment.yaml
	kubectl apply -f service.yaml
	kubectl apply -f ingress.yaml

delete:
	kubectl delete deployment/backend
	kubectl delete service/backend-svc
	kubectl delete ingress/backend

test:
	pytest -v --cov-report term --cov=. tests/test_apis.py