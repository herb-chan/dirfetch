# Variables
NAME = dirfetch
INSTALL_DIR = $(HOME)/.local/bin
SRC_DIR = source
BIN_DIR = bin
PYTHON = $(shell command -v python3 || command -v python)
PIP = $(shell command -v pipx || command -v pip)
VENV_DIR = .dirfetch-env

# Default target
all: install

# Create virtual environment if it doesn't exist
$(VENV_DIR):
	$(PYTHON) -m venv $(VENV_DIR)

# Install target
install: $(VENV_DIR)
	@echo "Installing $(NAME)..."
	# Install or upgrade pip in the virtual environment
	$(VENV_DIR)/bin/pip install --upgrade pip
	# Install the package into the virtual environment
	$(VENV_DIR)/bin/pip install .
	@echo "$(NAME) installed successfully."

# Build the project (create the binary from the source)
$(BIN_DIR)/$(NAME): $(SRC_DIR)/*
	@echo "Building $(NAME)..."
	$(PYTHON) setup.py install

# Clean up the build
clean:
	@echo "Cleaning up..."
	rm -rf $(BIN_DIR)/$(NAME)
	rm -rf $(VENV_DIR)

# Uninstall the package
uninstall:
	@echo "Uninstalling $(NAME)..."
	rm -f $(INSTALL_DIR)/$(NAME)
	rm -rf $(VENV_DIR)
	@echo "$(NAME) uninstalled successfully."

# Ensure that the bin directory exists
$(BIN_DIR):
	mkdir -p $(BIN_DIR)
