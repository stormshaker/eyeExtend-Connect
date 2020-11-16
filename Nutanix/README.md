Nutanix Acropolis Hypervisor integration.

Build using the build.sh script, to create the ZIP archive that can be imported into the Forescout console. Requires that importing of unsigned apps be allowed; use the following fstool command from the Forescout command line interface:

``fstool allow_unsigned_connect_app_install true``


Supports:
  * Polling with the v2 API
  * Basic authentication over HTTPS
  * Host Discovery
  * Properties: UUID, Name, Description, Power State
  * Resolve script (still testing)
  
TODO:
  * Update to use newly-supported python Requests library
  * Investigate refactoring auth into a separate script

