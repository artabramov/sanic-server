docker build --no-cache -t hide-server .
docker run -dit -p 80:80 -p 8081:8081 -p 5432:5432 --name hide-server hide-server
