update_bulma:
	cd ./bulma/static/bulma/sass && rm -f package-lock.json && npm i && npm run build && rm -rf ./node_modules
