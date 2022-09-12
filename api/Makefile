# Python - FastAPI

help:
	@echo USAGE:
	@echo 	make [COMMAND]

	@echo COMMANDS:
	@echo 	help             this help
	@echo 	install          create virtualenv and install python dependencies
	@echo 	debug            start dev server
	@echo 	prod             start server (in background)
	@echo 	down             stop server

install:
	@echo "Creating virtualenv..."
	@python3 -m venv .venv
	@echo "Installing dependencies..."
	@.venv/bin/pip install -r requirements.txt

debug:
	@echo "Starting backend dev server..."
	@uvicorn main:app --reload

prod:
	@echo "Starting server..."
	@uvicorn main:app --daemon

down:
	@echo "Stopping server..."
	@kill `cat uvicorn.pid`
