deploy:
	kubectl apply -f config.yaml
	kubectl apply -f pv.yaml
	kubectl apply -f pvc.yaml
	kubectl apply -f deployment.yaml
	kubectl apply -f service.yaml

connect:
	postgres_pod := $(shell kubectl get pods | grep postgres | cut -d ' ' -f1)
	export PG_PASSWORD=password
	kubectl exec -it $(postgres_pod) -- psql -h localhost -U admin -p 5432 agile_avengers

stop:
	kubectl delete service/postgres deployment.apps/postgres