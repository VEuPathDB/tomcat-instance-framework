<!---
This doc is written with Markdown syntax.
http://daringfireball.net/projects/markdown/
-->
## EuPathDB Tomcat Instance Framework (TcIF) Manual

### Background

The EuPathDB tomcat-instance-framework (TcIF) allows easy setup and management of multiple Apache Tomcat instances from one or more binary installation. It was originally developed to support WDK-based installations for the EuPathDB-BRC project but we have found it versatile enough to be used for any web application in Tomcat.

Features include

- Each Tomcat instance is run in its own jvm process with its own configuration options. For example instance `A` may be Java 6 + Tomcat 6 with a 1024MB memory heap, whereas instance `B` can be configured to use Java 7 + Tomcat 7 with a 512MB memory heap.  Each instance can host multiple webapps.
- Each Tomcat instance is named for easy identifcation and management.
- Management script permits non-root users to manage webapp deployments and permits `sudo` users to start/stop instances.

### Security Warning

The `tomcat-users.xml` installed by this framework is world readable and includes a clear-text password for the Tomcat Manager. This is designed so the `instance_manager` script can get the login credentials it needs to work. This of course means that any user on your server will be able to obtain the credentials needed to execute any Manager command. If this is a security concern for you then this framework may not be suitable in your environment. The access to the Manager is limited to clients from 127.0.0.1 by virtue of the RemoteAddrValve defined in `manager.xml`, so this should prevent remote connections. The assumption is that only trusted team members have access to your server and that if your server is compromised by a malicious intruder then you have more important things to worry about than Tomcat.

The default framework also enables JMX Remote accessible without authentication on a port on localhost. For more information about JMX Remoting see [http://tomcat.apache.org/tomcat-7.0-doc/monitoring.html](http://tomcat.apache.org/tomcat-7.0-doc/monitoring.html)

### Requirements

This document assumes the reader has prior experience with Apache Tomcat. Our framework is largely an implementation of what is describe in '_Advanced Configuration - Multiple Tomcat Instances_' at [http://tomcat.apache.org/tomcat-7.0-doc/RUNNING.txt](http://tomcat.apache.org/tomcat-7.0-doc/RUNNING.txt) using a set of deployment conventions. You may need to refer to the official Tomcat documentation at [http://tomcat.apache.org/](http://tomcat.apache.org/) for additional information and troubleshooting tips.

#### Software Requirements

- RedHat-based Linux (including CentOS). Others will probably work with a little code tweaking but we have not tested.
- BASH >= 4.0
- make
- perl
- XML::Simple Perl module
- Apache Tomcat >= 5.0.28 (earlier versions may work but we have not tested). The framework relies on the script `$CATALINA_HOME/bin/version.sh` that should be included with Tomcat but there have been reports that some vendors repackage Tomcat without this script. We recommend using one of EuPathDB's Tomcat rpms.
- jsvc (included as an optional installation with Tomcat). This is precompiled and installed if you are using one of EuPathDB's Tomcat rpms.
- Java
- Three network ports for each Tomcat instance to be used for HTTP, AJP and JMX. Technically only need the HTTP port if you are hosting Tomcat without a proxy server in front. If you are using a proxy webserver such as Apache HTTP Server or Nginx in front of Tomcat then these three ports can be (should be) firewalled and only accessible to localhost and proxy server.

### Installation

#### Manual Non-root Install; Quick Start

TcIF can be installed without root privileges. The [Non-root Installation of EuPathDB Tomcat Instance Framework](install_nonroot.md) document can show you how. It is also a good 'quick start' guide to install TcIF for evaluation.

#### Yum Repositories

*Skip this section if doing a non-root install*

Most of the required software is available as RPMs from RedHat/CentOS and EPEL yum repositories. The remaining requirements are availble from EuPathDB's internal yum repoitories. Currently EuPathDB's yum repos are not publicly accessible. If you need access to our repository, contact help@eupathdb.org for arrangements.


#### Install tomcat-instance-framework RPM

*Skip this section if doing a non-root install*

    yum install tomcat-instance-framework

The tomcat-instance-framework rpm depends on one of our Tomcat RPMs but you can install the framework using `rpm --nodeps` if you want to install Tomcat manually.

The three main items of interest installed by the RPM are

- `/usr/local/tomcat_instances` directory where you will create your Tomcat instances. The directory contains templates and a Makefile for creating the instances.
- `/usr/bin/instance_manager` script used to manage the Tomcat instances and webapps.
- `/etc/init.d/tomcat`  System V  init script. Use this to start/stop all your Tomcat instances at boot and shutdown. You may want to run `chkconfig --level <levels> tomcat on` to enable the script for the desired runlevels.

Run `rpm -ql tomcat-instance-framework` for the complete list of files installed by the RPM.

The RPM creates the user `tomcat` and group `tomcat` if these do not already exist.

#### Install Apache Tomcat from EuPathDB RPM 

*Skip this section if you want to install from a different source such as the bundle provided by the Apache Software Foundation.*

*Skip this section if doing a non-root install*

You can install Tomcat from an RPM or from the tar file downloaded from the Apache Foundation. EuPathDB has RPM packages for some versions of Tomcat. The EuPathDB Tomcat RPMs are designed to allow multiple versions of Tomcat to be installed and you can configure different instances to use the different Tomcat versions. As of this writing we have `tomcat-6.0.35.x86_64` and `tomcat-7.0.23.x86_64` RPMs available. Check our YUM repo for current availability.

The tomcat-instance-framework RPM has a EuPathDB Tomcat rpm as a dependency unless you install with `rpm --nodeps`. It's recommened that you just install the dependency. You can still add other Tomcat versions later.

The EuPathDB Tomcat RPMs are simple. The Apache Foundation's tar bundle is unpacked at `/usr/local/apache-tomcat-N.M.O` and a `jsvc` binary is installed to `/usr/local/apache-tomcat-N.M.O/bin`. No other modifications to the original distribution are made.


#### Add `sudo` permissions

*Skip this section if doing a non-root install*

Individual webapps can be managed using the `instance_manager` script without elevated user privileges. There is no technical restriction on which system user can manage which webapp (see caution about world-readable tomcat-users.xml above) so you should consider establishing a policy on your team on who is responsible for individual webapps.

An instance is started as a root-owned `jsvc` process ([http://commons.apache.org/proper/commons-daemon/jsvc.html](http://commons.apache.org/proper/commons-daemon/jsvc.html)). Jsvc is a daemon process so started as root and then downgraded to an unprivilegded user. Therefore starting and stopping a Tomcat instance requires root-level permissions, which can be granted to users through `sudo`.

Allowing users to restart tomcat instances is optional. You may omit the `sudo` configuration and only allow `root` to peform the action. However, there is little point in having that restriction because our framework lets any user undeploy any webapp so blocking users from restarting Tomcat offers little protection against someone maliciously distrupting the webapps.

Configuring `sudo` for your specific environment is beyond the scope of this document but basically you need to grant execution for `/usr/bin/instance_manager`. For example,

    User_Alias DEV_TEAM = joeuser, %devgroup
    Cmnd_Alias INSTANCE_MANAGER = /usr/bin/instance_manager
    DEV_TEAM ALL = NOPASSWD:INSTANCE_MANAGER

We typically allow execution with `NOPASSWD` but you may require that users enter their password.

### Usage

#### Create an instance

Before you can launch a Tomcat process using the framework you must create an instance directory structure and configuration files.

An instance is created by copying a template and editing an instance.env file. A Makefile is available to execute the necessary steps. It requires root privileges. `cd` to the `tomcat_instances` directory and run `make` with defined variables (run `make` alone to see list of required and optional variables). For example,

    $ cd /usr/local/tomcat_instances
    $ make install                                  \
      INSTANCE=FooDB                                \
      HTTP_PORT=19280                               \
      AJP13_PORT=19209                              \
      JMX_PORT=19205                                \
      TOMCAT_USER=tomcat_Z                          \
      OJDBC_PATH=$ORACLE_HOME/jdbc/lib/ojdbc6.jar   \
      TEMPLATE=7.0.23

The `make` variables are:

`INSTANCE` - All instances must have a name, such as `FooDB` in this example, that is unique to the server. The first letter of the name can not be an underscore, '`_`' (see below for why).  For legibility, it is recommended that you capitalize the first letter of the name.  A directory will be created with the instance name in `/usr/local/tomcat_instances`. 

`HTTP_PORT` - The port for the HTTP/1.1 protocol when Tomcat functions as a stand-alone web server. For more information see [http://tomcat.apache.org/tomcat-7.0-doc/config/http.html](http://tomcat.apache.org/tomcat-7.0-doc/config/http.html)

`AJP13_PORT` - the port for the AJP connector for connecting Apache HTTP with Tomcat using the mod_jk module. For more information see [http://tomcat.apache.org/tomcat-7.0-doc/config/ajp.html](http://tomcat.apache.org/tomcat-7.0-doc/config/ajp.html)

`JMX_PORT` - This is the localhost port on which JMX remote listens. It is required by default, but can be disabled by undefining `CATALINA_OPTS['JMX_OPTS']` in `global.env` or `instance.env`. For more information on JMX remote see [http://tomcat.apache.org/tomcat-7.0-doc/monitoring.html](http://tomcat.apache.org/tomcat-7.0-doc/monitoring.html)


`TOMCAT_USER` - the user that will own the Tomcat process. This framework uses `jsvc` to control the java processes. `jsvc` is a daemon process that is started as root and then downgraded to this  unprivilegded `TOMCAT_USER`. It is recommended that each instance have a unique user dedicated to it so Java subprocesses spawned from the instance can be more easily identified in output from the `ps` command.

`OJDBC_PATH` - (optional) The path to the desired ojdbc jar file for Oracle.

`PG_JDBC_PATH` - (optional) The path to the desired ojdbc jar file for PostgreSQL.

`TEMPLATE` - the name of a template in `/usr/local/tomcat_instances/templates` to use as the basis for the new instance.

After running `make ...` should then have a directory for your new instance, `/user/local/tomcat_instances/FooDB`, in this example. This directory is known as `CATALINA_BASE`. You will notice that term used in configurations and will probably see that term used in other documentation about multi-instance Tomcat configurations. The counterpart is `CATALINA_HOME` which is the Tomcat binary distibution, e.g. `/usr/local/apache-tomcat-N.M.O`.

You should now be able to start your new instance by its name. As stated above, we need to use `sudo` when starting or stopping an instance.

    $ sudo instance_manager start FooDB
    starting FooDB...

Then confirm that the instance is running (`sudo` not required).

    $ instance_manager status
    INSTANCE      PID       USER   HTTP  AJP13    JMX     UPTIME
    FooDB       20902   tomcat_1  19280  19209  19205       00m 25s

If the instance is not listed then something has prevented it from starting. Check the `catalina.out` file in the instance's `logs` directory for errors. The `catalina.out` is probably only readable by the `TOMCAT_USER`. We typically `chmod` the file so everyone on the team can read it, otherwise you'll need to get your `root` out.

    $ cat /usr/local/tomcat_instances/Foo/logs/catalina.out

Once you have the instance running, you can list the deployed webapps. The newly created instance will come with two webapps already deployed: the Manager and the root app.

    $ instance_manager manage FooDB list
    OK - Listed applications for virtual host localhost
    /manager:running:0:/usr/local/apache-tomcat-7.0.23/webapps/manager
    /:running:0:/usr/local/tomcat_instances/shared/webapps/ROOT

You can now deploy additional webapps using a context xml descriptor file. There is currently no support in the `instance_manager` for deploying war files.

More information on `instance_manager` is described in a later section.

### Configuration

You have all the usual Tomcat configuations at your disposal - `server.xml`, `web.xml`, various property files -  but this framework is designed to need only two configuration files. There is one global configuration file that defines default values for all instances. For each instance, there is an instance-specific configuration file.

#### Global Configuration

All instances acquire default settings from `/usr/local/tomcat_instances/shared/conf/global.env`. Review and edit this file as needed for your environment.

Most of the settings can be overridden for a single instance in the `instance.env` configuration file (see below). 

The `global.env` file is a BASH source file so has the format of `VAR=value`. 

You may customize this file for your environment. The following are a required minimum. Please consult the `global.env` included with the `instance-manager-framework` for a definitive list as your installed version may be older or newer than this document.

`CATALINA_OPTS` - This is an associative array by default. You can have zero or more elements in the array. This allows you to create groups of settings organized however you like. The key names are not important to the framwork. You can choose key names that help you distinguish logical groupings. 

`AUTO_DEPLOY` - `true` or `false`. This flag value indicates if Tomcat should check periodically for new or updated web applications while Tomcat is running. For details see, [http://tomcat.apache.org/tomcat-6.0-doc/config/host.html#Automatic\_Application\_Deployment](http://tomcat.apache.org/tomcat-6.0-doc/config/host.html#Automatic_Application_Deployment)

`ORACLE_HOME` - path to ORACLE_HOME. If you are not using Oracle then you can probably leave this empty.

`LD_LIBRARY_PATH` - path for shared libraries. It may be optional for your environment but we frequently need to add a path to Oracle's libraries.

#### Instance Configuration

Each instance has an `instance.env` file (e.g. `FooDB/conf/instance.env`) where you can alter the defaults set in `global.env` and where you add instance-only values like network ports.

The following variables must be defined in `instance.env` and are set during `make install`

`HTTP_PORT` - The port for the HTTP/1.1 protocol when Tomcat functions as a stand-alone web server. For more information see [http://tomcat.apache.org/tomcat-7.0-doc/config/http.html](http://tomcat.apache.org/tomcat-7.0-doc/config/http.html)

`AJP13_PORT` - the port for the AJP connector for connecting Apache HTTP with Tomcat using the mod_jk module. For more information see [http://tomcat.apache.org/tomcat-7.0-doc/config/ajp.html](http://tomcat.apache.org/tomcat-7.0-doc/config/ajp.html)

`JMX_PORT` - This is the localhost port on which JMX remote listens. It is required by default, but can be disabled by undefining `CATALINA_OPTS['JMX_OPTS']` in `global.env` or `instance.env`. For more information on JMX remote see [http://tomcat.apache.org/tomcat-7.0-doc/monitoring.html](http://tomcat.apache.org/tomcat-7.0-doc/monitoring.html)


`TOMCAT_USER` - the user that will own the Tomcat process. This framework uses `jsvc` to control the java processes. The `jsvc` is a daemon process that is started as root and then downgraded to this  unprivilegded `TOMCAT_USER`. It is recommended that each instance have a unique user dedicated to it so Java subprocesses spawned from the instance can be more easily identified.


Variables that can be optionally defined in `global.env` or `instance.env` to override the defaults defined in the `instance_manager` script.


`JSVC_EXE` - The path to the `jsvc` executable. Typically `${CATALINA_HOME}/bin/jsvc`.

`TMP_DIR`

`PID_DIR`

`PID_FILE`

`CATALINA_BASE` - The path to the instance directory, for example `/usr/local/tomcat_instances/FooDB`.

`FRAMEWORK_PROPERTIES` - properties required for proper function tomcat_instance framework and its support scripts. You probably do not want to change this.

`CATALINA_OPTS` - This is an associative array by default. You can have zero or more elements in the array. This allows you to create groups of settings organized however you like. The key names are not important to the framwork. You can choose key names that help you distinguish logical groupings. 

    CATALINA_OPTS['MEM']="   \
        -Xms256m -Xmx1024m \
        -XX:MaxPermSize=512m \
    "

The `CATALINA_OPTS` values are concatenated to create a final option string. Alternatively, you can just override `CATALINA_OPTS` with a scalar assignment.

    CATALINA_OPTS="-Xms256m"

Each value in the `CATALINA_OPTS` array is concatenated together at runtime. When defining your values be careful that the final string will be generated with a valid value (e.g. be sure blank lines are not introduced when concatenating the values). Debug with the `verbose` option with `instance_manager` to see the final compiled command.

The `instance_manager` script assembles a full startup command, something like

    $JSVC_EXE \
    -user $TOMCAT_USER \
    -home $JAVA_HOME \
    -Dcatalina.home=$CATALINA_HOME \
    -Dcatalina.base=$CATALINA_BASE \
    -Djava.io.tmpdir=$TMP_DIR \
    -wait 10 \
    -pidfile $PID_FILE \
    -outfile $CATALINA_BASE/logs/catalina.out \
    -errfile '&1' \
    $FRAMEWORK_PROPERTIES \
    $CATALINA_OPTS_E \
    -DautoDeploy=$AUTO_DEPLOY        \
    -cp $CLASSPATH \
    org.apache.catalina.startup.Bootstrap
    
See the `instance_manager` script for the current specifics.

#### `global.env` and `instance.env` interactions

Recall that `global.env` and `instance.env` are simply files with VAR=value pairs that are `source`d by the `instance_manager` BASH script. `global.env` is read first, followed by `instance.env`.  This allows variables defined in `global.env` to be overridden by `instance.env`. The value can be a predefined variable (`FOO=bar; VAR=$FOO`). The value can also be an escaped variable that is defined later (`VAR=\$FOO; FOO=bar;`) A precusor command line string is generated from the values and then that string is given a final parsing with `eval` to expand any embedded escaped variables (`eval VAR`). 

Let's use `CATALINA_OPTS` as an example. In `global.env` you can define a jmxremote option with an embedded and escaped variable for `$JMX_PORT`.

    CATALINA_OPTS['JMX_OPTS']="\
        -Dcom.sun.management.jmxremote                     \
        -Dcom.sun.management.jmxremote.port=\$JMX_PORT     \
    "

In `instance.env` for each instance the `JMX_PORT` is defined.

    JMX_PORT=6060

At runtime, the port embedded variable is evaluated to generate a complete option string.
    
    -Dcom.sun.management.jmxremote \
    -Dcom.sun.management.jmxremote.port=6060


### Creating New Templates

Additional templates can be added to the `templates` directory. This may be necessary to support versions of Tomcat that are incompatible with the templates bundled with our framework or if you have particular settings you want to routinely include when making new instances.

The Tomcat instance will use the stock files `$CATALINA_HOME/config` by default but each instance  requires that some of the configurations be customized. Copy and edit the following files into your custom template.

In `server.xml`, define ports using Java system properties

    <Server port="${shutdown.port}" shutdown="SHUTDOWN"
    <Connector port="${http.port}" protocol="HTTP/1.1"
    <Connector port="${ajp13.port}" protocol="AJP/1.3"

and define autoDeploy using a Java system property

    unpackWARs="true" autoDeploy="${autoDeploy}"

In `catalina.properties`append 

    ${catalina.base}/shared/lib/*.jar

to `common.loader`


in `tomcat-users.xml`, add a role for the Manager. The username and password can be anything.

    <?xml version='1.0' encoding='utf-8'?>
    <tomcat-users>
      <user username="839da325" password="71bd242d57ba" roles="manager-script"/>
    </tomcat-users>
    
You can have more than one user but at least one user must have one and only one role of manager or manager-script, otherwise the simple XML parser in `instance_manager` will fail.

Changes to `web.xml` are optional. If the default values in `$CATALINA_HOME/config/web.xml` are fine for you then you don't need to include a copy in the template. We typically change the `session-timeout` so the templates bundled with the tomcat-instance-framework reflect this.

`conf/Catalina` directory tree copied from one of the other templates. This tree includes context descriptors for ROOT and manager webapps. The manager.xml defines the Manager app and is required for `instance_manager` function. The ROOT.xml defines what is served when the root, `'/'`, path is requested. When using the bundled ROOT.xml, the root context serves a JSP that summarizes information about the Tomcat server. The ROOT.xml is optional and can be redefined to reference a different webapp.

You'll need a copy of `instance.env.in` in your custom template. Copy it from one of the bundled templates. You will need to override `CATALINA_HOME` in `instance.env.in` if it different from the definition in the framework's `global.env`. `instance.env.in` is copied and edited to `instance.env` by the make process when you create a new instance. 


### Managing Instances

The `instance_manager` script included with the framework handles most of the management tasks for the tomcat instances. This script is developed by EuPathDB and is unique to framework so please report any problems or related questions to help@eupathdb.org. Running `instance_manager` without any options will print a brief usage text.

      $ instance_manager 
      
      Manage Tomcat instances and webapps.
      
      Usage: sudo instance_manager <start|stop|restart> <instance> [force]
             instance_manager manage <instance> list
             instance_manager manage <instance> <start|stop|reload|undeploy|redeploy> <webapp>
             instance_manager manage <instance> deploy </path/to/context.xml>
             instance_manager status
      
      Use 'instance_manager help' for expanded information.


#### Start/stop Tomcat Instances

Start, stop and restart of an instance requires sudo or root permissions, as explained above.

    $ sudo instance_manager start FooDB
    starting FooDB...


    $ sudo instance_manager stop FooDB
    stopping FooDB...

The start and stop actions are effected using the `jsvc -stop` command. See [http://commons.apache.org/proper/commons-daemon/jsvc.html](http://commons.apache.org/proper/commons-daemon/jsvc.html) for details. Stopping an instance an take several minutes, especially if it has been running for a long time and is low on memory.

Sometimes the instance will be in such a degraded state that `jsvc`is unable to stop the instance. It's even possible for `jsvc` confuse `instance_manager` into thinking the process has stopped but in fact it is still running and visible only through a `ps` listing. In such situations the only resolution is to kill the jsvc processes. Appending the `force` option to `instance_manager` will invoke a `kill -9` on the PIDs (there will usually be two: one for the root-owned parent and one for the spawned process owned by `TOMCAT_USER`).

    $ sudo instance_manager stop FooDB force
    killing PIDs 1280 1279...

#### Managing Individual Webapps

Individual instances are managed with the `manage` subcommand and some action command. Each action makes an HTTP request to the Tomcat Manager application at localhost (append `verbose` to the `instance_manager` command to see the manager url used). For more information about the Manager's actions, see [http://tomcat.apache.org/tomcat-7.0-doc/manager-howto.html](http://tomcat.apache.org/tomcat-7.0-doc/manager-howto.html).

##### list

The `list` command will list webapps deployed in the instance.

    $ instance_manager manage FooDB list
    OK - Listed applications for virtual host localhost
    /manager:running:0:/usr/local/apache-tomcat-7.0.23/webapps/manager
    /:running:0:/usr/local/tomcat_instances/shared/webapps/ROOT
    /fooapp:stopped:0:/usr/local/tomcat_instances/shared/webapps/ROOT

##### start, stop, reload

See [http://tomcat.apache.org/tomcat-7.0-doc/manager-howto.html](http://tomcat.apache.org/tomcat-7.0-doc/manager-howto.html)

##### deploy

`instance_manager` only deploys webapps from a Context configuration xml file. There is currently no support in the `instance_manager` for deploying war files. 

An example Context configuration xml file, based on EuPathDB's typical usage, is

    <Context path="/release1"
        docBase="/var/www/FooDB/release1/webapp"
        privileged="false"
        swallowOutput="true"
        allowLinking="true">
        <Parameter name="model" value="FooDB"
             override="false"/>
    </Context>

See also [http://tomcat.apache.org/tomcat-7.0-doc/manager-howto.html#Deploy\_A\_New\_Application\_from\_a\_Local\_Path](http://tomcat.apache.org/tomcat-7.0-doc/manager-howto.html#Deploy_A_New_Application_from_a_Local_Path)

The workaround for deploying war files is to use the Tomcat manager API as documented in the Tomcat Manager documentation. The `conf/tomcat-users.xml` in your instance's directory will have the necessary manager login credentials.

##### undeploy

See [http://tomcat.apache.org/tomcat-7.0-doc/manager-howto.html#Undeploy\_an\_Existing_Application](http://tomcat.apache.org/tomcat-7.0-doc/manager-howto.html#Undeploy_an_Existing_Application)


##### redeploy

The `redeploy` action does not have an exact Tomcat Manager counterpart but is a series of `deploy` and `undeploy`. It first makes a copy of the app's existing context xml file, undeploys the app and then deploys that same xml file back in. The primary use case for redeploy is to clear the webapp's cache of compiled JSP. If you want to change the context configuration then you must first undeploy   the webapp and then deploy a new, edited copy of the context xml file.


#### Show Running Instances

The `status` subcommand lists the running tomcat instances along with some summary information. 

The PID isfor the jsvc process owned by `TOMCAT_USER`. This process is the one spawned by the root-owned `jsvc` parent process. The root-owned parent jsvc processes will be shown if you run `ps` on your system.

    $ instance_manager status
    INSTANCE      PID       USER   HTTP  AJP13    JMX     UPTIME
    FooDB       31265   tomcat_1  19280  19209  19205       02m 39s

Append `all` to include instances that are not running.

    $ instance_manager status all
    INSTANCE      PID       USER   HTTP  AJP13    JMX     UPTIME
    FooDB       13683   tomcat_1  19280  19209  19205       23m 54s
    Not running:
    BarDB


### Temporarily Disabling an Instance

If you have an instance configured but want to temporarily exclude it from the `instance_manager` script you can stop it and rename the instance directory in `/usr/local/tomcat_instances` with a leading underscore. For example,

    sudo instance_manager stop FooDB
    mv /usr/local/tomcat_instances/FooDB /usr/local/tomcat_instances/_FooDB

`FooDB` will now be excluded from `instance_manager` reports and actions. The `tomcat` service script will also not start the instance.

Remove the underscore from the directory name to put the instance back in service.

### Troubleshooting Tips

- Monitor `${INSTANCE}/log/catalina.out` and your application's logs for errors.

- Using `verbose` mode with `instance_manager` will print additional information to the terminal.
    
    `$ instance_manager restart  FooDB verbose`



### Known Bugs

When starting multiple instances at the same time the ports may get scrambled. For example, instance A may use port 1010 that is defined for instance B, preventing instance B from starting correctly because port 1010 is already in use. To prevent this, give several seconds for one instance to start before starting another.



