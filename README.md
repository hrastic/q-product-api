# Overview
This Product API has been built using Python 3, Django, Django Rest Framework, and Docker.

# Quick Start
To run the project execute from the project root
```bash
docker-compose up
```
This will run the pre-built image in the docker.
Navigate to: http://localhost:8000/api/docs/ to access the API through SWAGGER
# Tests
You can run all unit tests by executing from the project root
```bash
docker-compose run --rm app sh -c "python manage.py test"
```
You can check if code follows PEP8 coding style by executing from the project root
```bash
docker-compose run --rm app sh -c "flake8"
```
# API
| Endpoint | Description |
| --- | --- |
| POST /api/schema | Generates an API schema .YML file. |
| POST /api/user/create | Create a user. |
| GET /api/user/me | Get authenticated users' data. |
| PUT /api/user/me | Update authenticated users' data. |
| PATCH /api/user/me | Partial update authenticated users' data. |
| POST /api/user/token | Generate a token for created user. |
| GET /api/product/products | Get products. |
| POST /api/product/products | Enter a new product. |
| GET /api/product/products/{id} | Get product detail. |
| PUT /api/product/products/{id} | Update product detail. |
| PATCH /api/product/products/{id} | Partial update product detail. |
| DELETE /api/product/products/{id} | Delete product detail. |
| GET /api/product/products/{id}/store-average-rating | Retrieve and save average rating of a product on itself. |
| GET /api/product/ratings | Get ratings. |
| POST /api/product/ratings | Enter a new rating. **A user can rate a product only once.** |
| GET /api/product/ratings/{id} | Get rating detail. |
| PUT /api/product/ratings/{id} | Update rating detail. **Users can only update their ratings, but can still see others.** Updating only the rating field. |
| PATCH /api/product/ratings/{id} | Partial update rating detail.  Users can only update their ratings, but can still see others. Updating only the rating field. |
| DELETE /api/product/ratings/{id} | Delete rating. Users can only delete their ratings. |
# Action Secrets
Secrets are environment variables that are encrypted. Anyone with collaborator access to this repository can use these secrets for Actions.
