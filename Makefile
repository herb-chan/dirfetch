# Variables
NAME = dirfetch
INSTALL_DIR = /usr/local/bin
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
	@echo "Installing $(NAME) globally..."
	# Install or upgrade pip in virtual environment
	$(VENV_DIR)/bin/pip install --upgrade pip
	# Install the package globally
	$(VENV_DIR)/bin/pip install .  # This will install it into the venv but not use --user
	# Move the dirfetch binary to the INSTALL_DIR (make it globally available)
	sudo cp $(VENV_DIR)/bin/dirfetch $(INSTALL_DIR)/
	@echo "$(NAME) installed successfully."

# Clean up the build
clean:
	@echo "Cleaning up..."
	rm -rf $(VENV_DIR)

# Uninstall the package
uninstall:
	@echo "Uninstalling $(NAME)..."
	sudo rm -f $(INSTALL_DIR)/$(NAME)
	@echo "$(NAME) uninstalled successfully."

