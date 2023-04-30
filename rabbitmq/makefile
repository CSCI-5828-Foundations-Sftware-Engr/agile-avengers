deploy:
	kubectl apply -f cluster-operator.yaml
	sleep 10
	kubectl apply -f rabbitmq.yaml

createuser:
	kubectl exec -it rabbitmq-server-0 -- rabbitmqctl add_user agile_avengers password
	kubectl exec -it rabbitmq-server-0 -- rabbitmqctl set_permissions -p / agile_avengers ".*" ".*" ".*"

stop:
	kubectl delete -f rabbitmq.yaml
	kubectl delete -f cluster-operator.yaml
	kubectl delete statefulset.apps/rabbitmq-server 
	kubectl delete --all all -n rabbitmq-system

port-forward:
	kubectl port-forward service/rabbitmq 5672