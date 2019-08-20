update_bulma:
	cd ./bulma/static/bulma/sass && rm package-lock.json && npm i && npm run build && rm -rf ./node_modules
test:
	PYTHONPATH=`pwd` pytest bulma
build:
	test && poetry build
demosite:
	cd ./demo && pip install -r requirements.txt && python manage.py migrate && python manage.py runserver
