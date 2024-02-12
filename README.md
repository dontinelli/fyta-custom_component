# Fyta - custom_component

This repository contains a custom integration for Home Assistant to monitor FYTA-plants. The integration may eventually be implemented as core integration. Until then (or for easier adjustments to your desires), feel free to use this custom component.

# Installation
Copy the files to ./config/custom_components/fyta of your Home Assistant installation.

To access your plant data, you need the username (email address) and password of your FYTA account. The data will be accuired by the integration in course of the UI setup procedure.

# Fyta-cli
For the sake of easier testing and implementation, Fyta-cli, the client to access the FYTA API is included in this repository (files fyta-connector.py and client.py).
The client for the communication with the FYTA API is hosted (and documented) here:
https://github.com/dontinelli/fyta-cli
