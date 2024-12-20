# Makefile for dirfetch

# Variables
NAME = dirfetch
INSTALL_DIR = /usr/local/bin
SRC_DIR = source
BIN_DIR = bin
PYTHON = python3

# Default target
all: install

# Install target
install: $(BIN_DIR)/$(NAME)
	@echo "Installing $(NAME)..."
	install -m 755 $(BIN_DIR)/$(NAME) $(INSTALL_DIR)
	@echo "$(NAME) installed successfully."

# Build the project (create the binary from the source)
$(BIN_DIR)/$(NAME): $(SRC_DIR)/*
	@echo "Building $(NAME)..."
	$(PYTHON) setup.py install

# Clean up the build
clean:
	@echo "Cleaning up..."
	rm -rf $(BIN_DIR)/$(NAME)

# Uninstall the package
uninstall:
	@echo "Uninstalling $(NAME)..."
	rm -f $(INSTALL_DIR)/$(NAME)
	@echo "$(NAME) uninstalled successfully."
