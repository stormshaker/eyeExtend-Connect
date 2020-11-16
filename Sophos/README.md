Sophos Central endpoint discovery. Discovers endpoints from Sophos Central.

Build using the build.sh script, to create the ZIP archive that can be imported into the Forescout console. Requires that importing of unsigned apps be allowed; use the following fstool command from the Forescout command line interface:

``fstool allow_unsigned_connect_app_install true``

Supports:
  * Host Discovery (Polling)
  * Property resolution (still testing)

Properties:
  * Hostname
  * Overall Health status
  * Service Health status
  * Is a Server OS True/False
  * OS Platform (e.g. MacOS)
  * OS Name
  * Associated Person Name
  * Associated Person Login
  * Tamper Protection Enabled True/False

