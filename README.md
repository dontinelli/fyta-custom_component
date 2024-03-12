# FYTA - custom_component

This repository contains a custom integration for Home Assistant to monitor FYTA plants. The integration may eventually be implemented as core integration. Until then (or for easier adjustments to your desires), feel free to use this custom component.

> [!CAUTION]
> Please note that this integration is still in early development. Your testing is welcome, but please use at your own risk. Thank you for reporting any [issues or feature requests](https://github.com/dontinelli/fyta-custom_component/issues).

# Installation
## With HACS
While the FYTA integration is not (yet) part of the HACS repository, you can add `https://github.com/dontinelli/fyta-custom_component` as custom repository and download the integration directly into your HA installation.

## Manual Installation
Copy the files from `custom_components/fyta` to `./config/custom_components/fyta` of your Home Assistant installation.

## Setup
To access your plant data, you need the username (email address) and password of your FYTA account. The data will be accuired by the integration in course of the UI setup procedure.

# Fyta-cli
The client for the communication with the FYTA API is hosted (and documented) here:
https://github.com/dontinelli/fyta-cli
