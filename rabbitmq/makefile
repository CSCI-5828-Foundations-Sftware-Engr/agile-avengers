deploy:
	kubectl apply -f cluster-operator.yaml
	kubectl apply -f rabbitmq.yaml

createuser:
	kubectl exec -it rabbitmq-server-0 -- rabbitmqctl add_user agile_avengers password
	kubectl exec -it rabbitmq-server-0 -- rabbitmqctl set_permissions -p / agile_avengers ".*" ".*" ".*"

stop:
	kubectl delete rabbitmq.yaml
	kubectl delete cluster-operator.yaml
	kubectl delete statefulset.apps/rabbitmq-server rabbitmqcluster.rabbitmq.com/rabbitmq
	kubectl delete --all all -n rabbitmq-system