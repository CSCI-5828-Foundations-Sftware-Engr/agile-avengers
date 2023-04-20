build:
	docker build -t agile-avengers-frontend -f ../dockerfile ..

deploy:
	kubectl apply -f deployment.yaml
	kubectl apply -f service.yaml
	kubectl apply -f ingress.yaml
	
delete:
	kubectl delete deployment/backend
	kubectl delete service/backend-svc
	kubectl delete ingress/backend

test:
	pytest -v --cov-report term --cov=. tests