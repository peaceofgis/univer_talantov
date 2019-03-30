docker build -t pyapp .
docker stop pyappcont
docker container rm pyappcont
docker run -d --restart=always --name pyappcont -e carmd_token="2f9f68cafaca4e349a4e6bc59d04839e" -ecarmd_auth="Basic ZWM0YWEzODgtZDc1Mi00OGUxLTliMDUtMjVjOTY4MzRhYjFj" -p 5000:5000 pyapp
#docker run -it --name pyappcont -e carmd_token="2f9f68cafaca4e349a4e6bc59d04839e" -ecarmd_auth="Basic ZWM0YWEzODgtZDc1Mi00OGUxLTliMDUtMjVjOTY4MzRhYjFj" -p 5000:5000 pyapp
