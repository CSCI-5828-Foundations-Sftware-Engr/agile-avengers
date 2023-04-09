deploy:
	kubectl create -f https://raw.githubusercontent.com/keycloak/keycloak-quickstarts/latest/kubernetes-examples/keycloak.yaml
	wget -q -O - https://raw.githubusercontent.com/keycloak/keycloak-quickstarts/latest/kubernetes-examples/keycloak-ingress.yaml | \
	sed "s/KEYCLOAK_HOST/keycloak.test.nip.io/" | \
	kubectl create -f -

delete:
	kubectl delete deployment.apps/keycloak
	kubectl delete service/keycloak
	kubectl delete ingress keycloak