deploy:
	kubectl apply -f config.yaml
	kubectl apply -f pv.yaml
	kubectl apply -f pvc.yaml
	kubectl apply -f deployment.yaml
	kubectl apply -f service.yaml

connect:
	export PG_PASSWORD=password
	kubectl exec -it service/postgres -- psql -h localhost -U admin -p 5432 agile_avengers

stop:
	kubectl delete service/postgres deployment.apps/postgres
