# deploy to heroku, after signing in
APP="learnmath-frontend"
DOCKER_IMAGE="learnmath-frontend:latest"

# build image using docker, must be in fronend 
echo "Building docker image.."
docker build -t $DOCKER_IMAGE .

# create frontend application in heroku
echo "Creating $APP app in heroku.."
heroku create $APP
heroku container:login

# push container to 
echo "Created $APP app in heroku, pushing $DOCKER_IMAGE to herku registry"
heroku container:push web --app $APP

# release image to heroku
echo "Releasing to heroku"
heroku container:release web --app $APP

echo "released $APP to heroku, run command: heroku logs --tail --app $APP to view logs"
echo "opening app on web browser.."
heroku open
