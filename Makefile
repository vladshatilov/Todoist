create:
	docker-compose up -d

remove-all:
	docker-compose down

recreate: remove-all create

test:
	docker ps -a