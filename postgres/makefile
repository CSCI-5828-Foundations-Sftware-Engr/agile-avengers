deploy:
	kubectl apply -f config.yaml
	kubectl apply -f pv.yaml
	kubectl apply -f pvc.yaml
	kubectl apply -f deployment.yaml
	kubectl apply -f service.yaml

createtable:
	postgres_pod = $(kubectl get pods | grep postgres | cut -d' ' -f1)
	export PG_PASSWORD=password
	kubectl exec -it ${postgres_pod} -- psql -h localhost -U admin -p 5432 agile_avengers -c "create table dataleaks (leak_id serial primary key, breach_epoch integer not null, leak_info jsonb not null);"

connect:
	postgres_pod := $(kubectl get pods | grep postgres | cut -d' ' -f1)
	export PG_PASSWORD=password
	kubectl exec -it ${postgres_pod} -- psql -h localhost -U admin -p 5432 agile_avengers

stop:
	kubectl delete service/postgres deployment.apps/postgres