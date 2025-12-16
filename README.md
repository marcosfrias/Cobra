
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg?style=for-the-badge)](https://www.python.org/)

This repository contains a sample Kivy and KivyMD Python application, showcasing an Android APK build workflow using Buildozer. It serves as an example for **[KvDeveloper's](https://github.com/Novfensec/KvDeveloper)** build workflow, providing a streamlined process for converting Kivy and KivyMD applications into Android APKs and AABs `(Required by Google Play)`.

## Features

- A basic KivyMD `(2.0.1.dev0)` app structure.
- A ready-to-use **GitHub Actions** workflow for building APKs and AABs `(Required by Google Play)`.
- Full compatibility with **Kivy** and **KivyMD** frameworks.

## Getting Started

### Prerequisites

- Python 3.8+
- [Buildozer](https://github.com/kivy/buildozer) for APK packaging.
- Kivy & KivyMD libraries installed:

    ```bash
    pip install kivy https://github.com/kivymd/KivyMD/archive/master.zip
    ```

### Running Locally

To run the app locally, clone the repository and install the necessary dependencies:

```bash
git clone https://github.com/Novfensec/SAMPLE-KIVYMD-APP.git \
cd SAMPLE-KIVYMD-APP \
python main.py
```
