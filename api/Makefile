# Python - FastAPI

ifeq ($(OS),Windows_NT)
	VENVDIR = .venv\Scripts
else
	VENVDIR = .venv/bin
endif


help:
	@echo USAGE:
	@echo 	make [COMMAND]

	@echo COMMANDS:
	@echo 	help             this help
	@echo 	install          create virtualenv and install python dependencies
	@echo 	dev              start dev server
	@echo 	prod             start server (in background)
	@echo 	down             stop server

install:
	@echo "Creating virtualenv..."
	@python3.10 -m venv .venv
	@echo "Installing dependencies..."
	@${VENVDIR}/pip install -r requirements.txt

dev:
	@echo "Starting backend dev server..."
	${VENVDIR}/uvicorn main:app --reload

prod:
	@echo "Starting server..."
	@uvicorn main:app --daemon

down:
	@echo "Stopping server..."
	@kill `cat uvicorn.pid`
