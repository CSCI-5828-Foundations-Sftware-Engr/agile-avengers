build:
	docker build -t agile-avengers-frontend -f ../Dockerfile ..

deploy:
	kubectl apply -f deployment.yaml
	kubectl apply -f service.yaml
	kubectl apply -f ingress.yaml
	sleep 60
	nohup kubectl port-forward --address 0.0.0.0 service/backend-svc 5000:5005 &

delete:
	kubectl delete deployment/backend
	kubectl delete service/backend-svc
	kubectl delete ingress/backend

test:
	pytest -v --cov-report term --cov=. tests