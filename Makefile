update_bulma:
	cd ./bulma/static/bulma/sass && rm package-lock.json && npm i && npm run build && rm -rf ./node_modules
runserver:
	poetry run python test_project/manage.py runserver
