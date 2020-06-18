# Current Status [![Build Status](https://dev.azure.com/solarmist-test/flask-tdd-docker/_apis/build/status/Build%20and%20Test%20Pipeline?branchName=master)](https://dev.azure.com/solarmist-test/flask-tdd-docker/_build/latest?definitionId=2&branchName=master)

# flask-tdd-docker
TDD with Python, Flask and Docker

### Running the image

```bash
docker-compose up -d  # Create the image

docker-compose up -d --build  # Update the image

docker-compose logs  # See the logs for the running image
```