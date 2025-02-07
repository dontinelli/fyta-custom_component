# FYTA - custom_component

This repository contains a custom integration for Home Assistant to monitor FYTA plants. The integration may eventually be implemented as core integration. Until then (or for easier adjustments to your desires), feel free to use this custom component.

> [!CAUTION]
> In the past, the core component has received a lot of care and basically all features, that initially only were available in the custom components (such as for example the binary sensors or the image entity), have been implemented into the core component. Furthermore, the core component has (again) reached the platinum state on the new quality scale.
> Currently this custom component is not further maintained. Users are advised to migrate to the fyta core component to receive future improvements and bug fixes.

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
