EXTERNSION_NAME = nautilus-open-recomendations
TARGET_FILE_NAME = $(EXTERNSION_NAME).py
SYSTEM_EXT_DIR = /usr/share/nautilus-python/extensions
USER_EXT_DIR = $(HOME)/.local/share/nautilus-python/extensions
NAUTILUS_PYTHON_SHARED_OBJECT = nautilus/extensions-4/libnautilus-python.so

.PHONY: all install uninstall check clean

all: install

check:
	@if [ ! -f "/usr/lib/$(NAUTILUS_PYTHON_SHARED_OBJECT)" ] && \
		[ ! -f "/usr/lib64/$(NAUTILUS_PYTHON_SHARED_OBJECT)" ] && \
		[ ! -f "/lib/$(NAUTILUS_PYTHON_SHARED_OBJECT)" ]; then \
		echo "Error: Nautilus Python extension not found at $(NAUTILUS_PYTHON_SHARED_OBJECT)" >&2; \
		exit 1; \
	fi

install: check
	@if [ $$(id -u) -eq 0 ]; then \
		TARGET_DIR=$(SYSTEM_EXT_DIR); \
	else \
		TARGET_DIR=$(USER_EXT_DIR); \
	fi; \
	mkdir -p $$TARGET_DIR; \
	TARGET_FILE=$$TARGET_DIR/$(TARGET_FILE_NAME); \
	rm -f $$TARGET_FILE; \
	if cp "script.py" $$TARGET_FILE; then \
		echo "Successfully installed $$TARGET_FILE"; \
		nautilus -q >/dev/null 2>&1 || true; \
		echo "Nautilus restarted"; \
	else \
		echo "Error: Failed to copy $(TARGET_FILE_NAME) to $$TARGET_DIR" >&2; \
		exit 1; \
	fi

uninstall:
	@if [ $$(id -u) -eq 0 ]; then \
		TARGET_DIR=$(SYSTEM_EXT_DIR); \
	else \
		TARGET_DIR=$(USER_EXT_DIR); \
	fi; \
	TARGET_FILE=$$TARGET_DIR/$(TARGET_FILE_NAME); \
	if [ -f $$TARGET_FILE ]; then \
		rm $$TARGET_FILE; \
		echo "Uninstalled $$TARGET_FILE"; \
		nautilus -q >/dev/null 2>&1 || true; \
		echo "Nautilus restarted"; \
	else \
		echo "$$TARGET_FILE not found in $$TARGET_DIR"; \
	fi

clean:
	@echo "Nothing to clean"