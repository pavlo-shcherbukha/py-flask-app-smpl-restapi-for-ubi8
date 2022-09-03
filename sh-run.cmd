echo run simple python container  FROM python:3.9
rem docker run -e LD_LIBRARY_PATH=/opt/app-root/src/hello_app -p 8081:8080 pshkxml/iit2-srvc-ubi8 
docker run -e LD_LIBRARY_PATH=/opt/app-root/src/hello_app -p 8081:8080 --device="class/e6f1aa1c-7f3b-4473-b2e8-c97d8ac71d53" pshkxml/iit2-srvc-ubi8 
rem --device list
rem --device="class/{e6f1aa1c-7f3b-4473-b2e8-c97d8ac71d53}"

docker run -e LD_LIBRARY_PATH=/opt/app-root/src/hello_app -e GUNICORN_CMD_ARGS="--workers=3 --threads=3 --bind=0.0.0.0:$PORT --access-logfile=-" -p 8081:8080 pshkxml/iit2-srvc-ubi8 
docker run -e LD_LIBRARY_PATH=/opt/app-root/src/hello_app -e GUNICORN_CMD_ARGS="--workers=1 --bind=0.0.0.0:8080 --access-logfile=-" -p 8081:8080 pshkxml/iit2-srvc-ubi8 


docker exec  -u root -it pshkxml/iit2-srvc-ubi8   /bin/bash

show processes   ps -aux



if is_gunicorn_installed; then
  setup_py=$(find "$HOME" -maxdepth 2 -type f -name 'setup.py' -print -quit)
  # Look for wsgi module in the current directory
  if [[ -z "$APP_MODULE" && -f "./wsgi.py" ]]; then
    APP_MODULE=wsgi
  elif [[ -z "$APP_MODULE" && -f "$setup_py" ]]; then
    APP_MODULE="$(python "$setup_py" --name)"
  fi

  if [[ "$APP_MODULE" ]]; then
    export WEB_CONCURRENCY=${WEB_CONCURRENCY:-$(get_default_web_concurrency)}

    # Default settings for gunicorn if none of the custom are set
    if [ -z "$APP_CONFIG" ] && [ -z "$GUNICORN_CMD_ARGS" ]; then
      GUNICORN_CMD_ARGS="--bind=0.0.0.0:$PORT --access-logfile=-"
      gunicorn_settings_source="default"
    else
      gunicorn_settings_source="custom"
    fi

    # Gunicorn can read GUNICORN_CMD_ARGS as an env variable but because this is not
    # supported in Gunicorn < 20 we still need for Python 2, we are using arguments directly.
    echo "---> Serving application with gunicorn ($APP_MODULE) with $gunicorn_settings_source settings ..."
    exec gunicorn "$APP_MODULE" $GUNICORN_CMD_ARGS --config "$APP_CONFIG"
  fi
fi

docker run -e LD_LIBRARY_PATH=/opt/app-root/src/hello_app/lib -e GUNICORN_CMD_ARGS="--workers=1 --bind=0.0.0.0:8080 --access-logfile=-" -e APP_MODULE="hello_app.webapp" -p 8081:8080 pshkxml/iit2-srvc-ubi8 