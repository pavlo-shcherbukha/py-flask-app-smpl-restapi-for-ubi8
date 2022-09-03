
echo =1===================
docker build -t pshkxml/iit2-srvc-ubi8 .

echo tag
docker tag pshkxml/iit2-srvc-ubi8:latest pshkxml/iit2-srvc-ubi8:1.0.4

echo =2==================
rem docker push pshkxml/sh-ubi8-py-app:1.0.0


rem #deployment

rem # ibmcloud fn action update appid-be/getuserprofile --docker pshkxml/icfrss:1.0.1 ./getuserprofile.js

pause