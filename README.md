# Open recomendations - Nautilus Extension

## Description

This extension adds a list of recommended applications for opening different file types in Nautilus, making it easier to choose the right app.

## Requirements

- Nautilus file manager
- Python 3
- Nautilus Python extension (nautilus-python)

## Installation

1. Ensure you have the required dependencies installed.

2. Clone this repository or download the source files.

3. Open a terminal in the project directory.

4. To install the extension, run:

```bash
make install
```

5. Nautilus will automatically restart to apply the changes.

## Uninstallation

To remove the extension, run:

```bash
make uninstall
```

## Usage

After installation, right-click on a file in Nautilus. You should see an "Open With Recommended" option in the context menu. Clicking this option will open the file with the recommended application.