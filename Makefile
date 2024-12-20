# Variables
NAME = dirfetch
INSTALL_DIR = /usr/local/bin
SRC_DIR = source
BIN_DIR = bin
PYTHON = python3

# Default target
all: install

# Install target
install:
	@echo "Installing $(NAME)..."
	$(PYTHON) -m pip install --user .
	@echo "$(NAME) installed successfully."

# Build the project (create the binary from the source)
$(BIN_DIR)/$(NAME): $(SRC_DIR)/*
	@echo "Building $(NAME)..."
	# This step is not needed since pip will handle the installation
	# $(PYTHON) setup.py install

# Clean up the build
clean:
	@echo "Cleaning up..."
	rm -rf $(BIN_DIR)/$(NAME)

# Uninstall the package
uninstall:
	@echo "Uninstalling $(NAME)..."
	# You can optionally uninstall with pip
	$(PYTHON) -m pip uninstall -y $(NAME)
	@echo "$(NAME) uninstalled successfully."
