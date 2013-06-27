<!---
This doc is written with Markdown syntax.
http://daringfireball.net/projects/markdown/
-->

The tomcat-instance-framework allows easy setup and management of multiple Apache Tomcat instances from one or more binary installation. It was originally developed to support WDK-based installations for the EuPathDB-BRC project but we have found it versatile enough to be used for any web application in Tomcat.

Each Tomcat instance is run in its own jvm process with its own configuration options.

### Requirements

BASH >= 4.0

### Setup

#### Yum Repositories

Add eupathdb and eupathdb-fasttrack yum prepository configuations to server. [Instructions TBA elsewhere.]

#### Install tomcat-instance-framework RPM

    yum install tomcat-instance-framework

The tomcat-instance-framework rpm depends on our Tomcat rpm but you can force install the framework rpm if you want to install Tomcat manually.

#### Install Apache Tomcat. 

The tomcat-instance-framework RPM will install Tomcat as a dependency. Alternatively you can download the binary tar file from the Apache Software Foundation and extract into /usr/local/ . 

Optional: Make a symbolic link from apache-tomcat to your installation. For example,

    /usr/local/apache-tomcat -> /usr/local/apache-tomcat-6.0.35

Extract and compile jsvc.

    cd /usr/local/apache-tomcat/bin
    tar zxf commons-daemon-native.tar.gz
    cd commons-daemon-*-native-src/unix
    ./configure --with-java=/usr/java/latest
    make
    cp jsvc ../../bin



#### Creating an instance

    $ cd /usr/local/tomcat_instances
    $ make
    Usage:
    make install
    make update
    with defined environment varialbles:
      INSTANCE=FooDB                   \
      HTTP_PORT=19280                  \
      AJP13_PORT=19209                 \
      JMX_PORT=19205                   \
      TOMCAT_USER=tomcat_Z             \
      INSTALL_ORACLE_JDBC=1

#### Global Configuration

All instances acquire default settings from /usr/local/tomcat_instances/shared/conf/global.env
Some of the settings can be overridden in a per instance configuration file (see instance.env below).
Start/stop Tomcat Instances

`AUTO_DEPLOY`

`ORACLE_HOME`

`LD_LIBRARY_PATH`

#### Instance Configuration

Each instance has an instance.env file (e.g. FooDB/conf/instance.env) where you can alter default behavior.

The following variables must be defined in `instance.env` and are set during `make install`

`HTTP_PORT`

`AJP13_PORT`

`JMX_PORT`

`TOMCAT_USER`


Variables that can be optionally defined in `global.env` or `instance.env` to override the defaults defined in the `instance_manager` script.


`JSVC_EXE`

`TMP_DIR`

`PID_DIR`

`PID_FILE`

`CATALINA_BASE`

`FRAMEWORK_PROPERTIES` - properties required for proper function tomcat_instance framework and its support scripts. You probably do not want to change this.

`CATALINA_OPTS` - This is an associative array by default. You can have zero or more elements in the array. This allows you to create groups of settings organized however you like. The key names are not important to the framwork. You can choose key names that help you distinguish logical groupings. 

    CATALINA_OPTS['MEM']="   \
        -Xms256m -Xmx1024m \
        -XX:MaxPermSize=512m \
    "

The `CATALINA_OPTS` values are concatenated to create a final option string. Alternatively, you can just override `CATALINA_OPTS` with a scalar assignment.

    CATALINA_OPTS="-Xms256m"

Escaped variables can be include in `CATALINA_OPTS` values. For example, in `global.env` you can define a jmxremote option with an embedded and escaped variable for `$JMX_PORT`.

    CATALINA_OPTS['JMX_OPTS']="\
        -Dcom.sun.management.jmxremote                     \
        -Dcom.sun.management.jmxremote.port=\$JMX_PORT     \
    "

In `instance.env` for each instance the `JMX_PORT` is defined.

    JMX_PORT=6060

At runtime, the port embedded variable is evaluated to generate a complete option string.
    
    -Dcom.sun.management.jmxremote \
    -Dcom.sun.management.jmxremote.port=6060

Each value in the `CATALINA_OPTS` array is concatenated together at runtime. When defining your values be careful that the final string will be generated with a valid value (e.g. be sure blank lines are not introduced when concatenating the values).

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


    