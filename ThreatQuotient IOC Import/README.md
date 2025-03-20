# Forescout
eyeExtend Connect ThreatQuotient IOC Import App README.md Version: 1.0.0

## Configuration Guide
**Version 1.0.0**
- Initial Version

## Contact Information  
- Have feedback or questions? Write to us at

**[connect-app-help@forescout.com](mailto:connect-app-help@forescout.com)**

## App Support

- All eyeExtend Connect Apps posted here are community contributed and community supported. These Apps are not supported by the Forescout Customer Support team.
- See Contact Information above.

## About eyeExtend Connect ThreatQuotient IOC Import App

# About This App

The eyeExtend Connect ThreatQuotient IOC Import App provides functionality to ingest threat feeds in the form of IOCs from ThreatQuotient using their REST API. The app polls the ThreatQuotient API at configurable intervals to retrieve new indicators and syncs them into Forescout's IOC Scanner.

# What to Do  
To set up your system for using the eyeExtend Connect ThreatQuotient IOC Import App, perform the following steps:  

1. Download and install the module. See How to Install.  
2. Configure the module. See Configure the Module.  
3. Configure policy templates.  
4. Configure properties.  
5. Configure actions.  

# How to Install  
Get Forescout eyeExtend Connect plugin and ThreatQuotient IOC Import App from Forescout.  

## Ensure That the Plugin is Running  
After installing the Connect plugin, ensure that it is running.  

To verify:  

1. Select **Tools** > **Options** > **Modules**.  
2. Navigate to the component and hover over the name to view a tooltip indicating if it is running on Forescout devices in your deployment. In addition, next to the component name, you will see one of the following icons:  

- The component is stopped on all Forescout devices.  
- The component is stopped on some Forescout devices.  
- The component is running on all Forescout devices.  

3. If the component is not running, select **Start** , and then select the relevant Forescout devices.  
4. Select **OK**.

# Configure the Module
After eyeExtend Connect is installed, **Connect** is displayed under **Options**.

## Configure ThreatQuotient IOC Import App
To configure eyeExtend Connect ThreatQuotient IOC Import App, you import the ThreatQuotient IOC Import App.

Initially, the App Configuration tab of the **Connect** pane is blank. The ThreatQuotient IOC Import App has not been imported yet.

## Import an App
You can import the ThreatQuotient IOC Import App.

To import the ThreatQuotient IOC Import App:

In the App Configuration tab of the **Connect** pane, select **Import**.
Apps that can be imported are in .zip or .eca format. They can be in any folder.
	Select **Import**.  
If the app is imported successfully, a message is displayed at the bottom of the **Sending** dialog box. If the app is not imported successfully, error messages are displayed in the **Sending** dialog box.  

Select
**Close** when the import has finished.
A blank **System Description** dialog box opens. 

- If you select **Close** before the import has finished, it will fail.  

## Panels

After the app is imported, the **System Description** dialog box opens. It is initially blank and only the **Add** and **Import** buttons are enabled.  

To configure the ThreatQuotient IOC Import App, you add a system description to define a configuration.  

If a system description has not been configured and you select **OK** now, a warning message is displayed.  

Select **Add**

### ThreatQuotient IOC Import

Configure the following required settings:

- **Source Name**: A friendly name for this ThreatQuotient source
- **ThreatQuotient URL**: The base URL of your ThreatQuotient instance (must include http(s):// prefix)
- **API Key**: Your ThreatQuotient API key
- **Source ID**: The ID of the ThreatQuotient source containing indicators to import

Optional settings:

- **IOC refresh interval**: How often to poll for new indicators (default: 1440 minutes / 24 hours)
- **Severity Thresholds**: Configure score thresholds for Critical, High, and Medium severity levels
  - Critical: Score ≥ 90 (configurable)
  - High: Score ≥ 70 (configurable)
  - Medium: Score ≥ 50 (configurable)
  - Low: Score < 50

Select **Next**

### Assign Forescout Devices

- Initially, the Assign Forescout Devices panel has only one option, **Assign all devices by default** , and it is selected so that one device is added.

If you want to add a second device, the Assign Forescout Devices panel has more options.

Enter the following information:

- Connecting Forescout Device: Select Enterprise Manager or an IP address of the connecting Forescout device. This is the device which will retrieve IOCs from ThreatQuotient.  
- Assign specific devices: This Forescout Appliance is assigned to the connecting Forescout device for retrieving IOCs via this Connect App.
  - Select **Available Devices** and then select an IP address or Appliance name from the Available Devices list.  
  - Select **Add**. The selected device will send its requests to the connecting Appliance.  
- Assign all devices by default: This is the connecting Appliance to which Forescout Appliances are assigned by default if they are not explicitly assigned to another connecting Appliance. Select this option to make this connecting Appliance the appliance to retrieve IOCs for all Forescout Appliances not assigned to another connecting device.

Note the following:  

- An error message is displayed if you try to add a device that is already used.  
- If you have apps that discover 50,000 or more endpoints, distribute the apps in such a way so that only up to two of the apps share the same focal (connecting) appliance. An alternative is to split the endpoints across multiple user accounts on multiple servers.  

Select **Next**.

### Proxy Server

If required, optionally enter the Proxy Server information needed for network connectivity.  

Select **Finish**.  

## Edit a System Description  
You can edit an existing system description for the ThreatQuotient IOC Import App.  

To edit a system description:  

Select an existing system description and select **Edit**.  

There are tabs for each pane. You can edit the settings in the ThreatQuotient IOC Import, Assign Forescout Devices, and Proxy Server tabs.  

Select **OK** to save the system description edits to the Forescout Appliance.  

## Remove a System Description  
You can remove an existing system description.  

To remove a system description:  
Select an existing system description
Select **Remove**. A confirmation is displayed.  

**More** for details or **Ok**.  

## Refresh IOC Data
You can refresh *Discovery of IOC Data*, which instructs the ThreatQuotient IOC Import App to resolve IOCs from ThreatQuotient immediately. The app must be in the Running state.  

The app must be saved before selecting **Refresh**. Select **OK** in the **System Description** dialog box and then select **Apply** in the **Connect** pane to save the system description. Please wait about 5-10 seconds after clicking apply.  

To refresh IOC data:  

Select an existing system description
Select **Refresh**, then **Discovery of IOC Data** and select **OK**.

A window will appear to display the status of the refresh.

## Supported Indicator Types

The app supports the following indicator types from ThreatQuotient:

### File Indicators
- MD5 hashes
- SHA1 hashes
- SHA256 hashes
- File names

### Network Indicators
- URLs
- IP addresses
- Domain names

## Platform Support

The app maps ThreatQuotient platform information to Forescout platform types:
- Windows → Microsoft Windows
- Linux → Linux
- macOS → macOS
- Other → All

## Troubleshooting

1. Check the Forescout logs for any API communication errors
2. Verify your ThreatQuotient API key and permissions
3. Ensure the Source ID is correct and contains indicators
4. Check proxy settings if using a proxy server
5. Verify network connectivity to the ThreatQuotient instance
6. Check if the ThreatQuotient API is responding correctly

## Support

For issues or questions, please contact Forescout support or refer to the ThreatQuotient API documentation.

## License

Copyright © 2024 Forescout Technologies, Inc. All rights reserved. 