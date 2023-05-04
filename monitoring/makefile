deploy:
	kubectl create namespace monitoring
	kubectl apply -f clusterRole.yaml
	kubectl apply -f config-map.yaml
	kubectl apply -f prometheus-deployment.yaml
	kubectl apply -f grafana-datasource-config.yaml
	kubectl apply -f grafana-deployment.yaml
	kubectl apply -f prometheus-service.yaml
	kubectl apply -f grafana-service.yaml
	kubectl apply -f daemonset.yaml
	kubectl apply -f node-exporter-service.yaml

delete:
	kubectl delete -f clusterRole.yaml
	kubectl delete -f config-map.yaml
	kubectl delete -f prometheus-deployment.yaml
	kubectl delete -f grafana-datasource-config.yaml
	kubectl delete -f grafana-deployment.yaml
	kubectl delete -f prometheus-service.yaml
	kubectl delete -f grafana-service.yaml
	kubectl delete -f daemonset.yaml
	kubectl delete -f node-exporter-service.yaml
	kubectl delete namespace monitoring