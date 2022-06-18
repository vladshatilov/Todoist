create:
	docker-compose up -d

remove-all:
	docker-compose down

recreate: remove-all create

create_bot:
	docker-compose up --build --force-recreate --no-deps -d bot

remove-all_bot:
	docker-compose rm -f bot

recreate_bot: remove-all_bot create_bot


test:
	docker ps -a
	#https://api.telegram.org/bot5263235054:AAEO5IwBS78-niSzn5VgknROYab80VSqZFY/sendMessage?chat_id=204580903&text=hello