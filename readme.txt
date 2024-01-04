========== BUILD DOCKER IMAGE ==========
docker build -t ichrak-app:latest .

========== START DOCKER COMPOSE ==========
docker compose up -d

========== OPEN THE WEB APP ==========
localhost:3000

========== CHECK DB ==========
docker exec -it mysql-server bash -l
mysql -uroot
show databases;
use tournage_paris;
describe tournage_paris_table;
select * from tournage_paris_table;
