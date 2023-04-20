build:
	docker build -t agile-avengers-frontend -f ../dockerfile ..

deploy:
	kubectl apply -f deployment.yaml
	kubectl apply -f service.yaml
	kubectl apply -f ingress.yaml
<<<<<<< HEAD
	
=======
	sleep 60
	nohup kubectl port-forward --address 0.0.0.0 service/backend-svc 5000:5000 &

>>>>>>> 2b813ef498b716770a24d189b683f4b9a5d5786a
delete:
	kubectl delete deployment/backend
	kubectl delete service/backend-svc
	kubectl delete ingress/backend

test:
	pytest -v --cov-report term --cov=. tests
