<!---
This doc is written with Markdown syntax.
http://daringfireball.net/projects/markdown/
-->
## Non-root Installation of EuPathDB Tomcat Instance Framework

Typically the Tomcat Instance Framework (TcIF) is installed at the system level for shared use by a project's team members, but it can also be installed and used in by a regular, non-root user. This is useful for kicking TcIF's tires or doing sandbox development away from a production install.

While these instructions walk through installing TcIF by a regular, non-root user, they can be adapted slightly for installation by root. However, using our RPM (contact us for a copy) may be a more robust installation method for root to use.

### Planning

Java is required. Java 1.7 is supported and recommended by EuPathDB, but any version that is compatible with Apache Tomcat should work. `make` and `gcc` ars needed to compile C source code for a Tomcat binary. The installation of these dependencies is not covered in this document. We will use `wget` and `links` as command line web clients but you can substitute other clients; however, the client probably needs to be running on the same server that TcIF is on because the Tomcat network ports used will most likely be blocked to external clients by a firewall.

By following these instructions you will install Apache Tomcat and TcIF. Each of these products will be contained in their own directory. In this demonstration I will organize these two directories under a `tcif_trial` directory in my home account.

Let's make that directory.

    $ mkdir ~/tcif_trial

### Download and Install Apache Tomcat

If there is already an Apache Tomcat installed on the system then you may be able to use that one,  but let's download a new one so you can at least see the full process.

Download a tar.gz file for the desired Tomcat version. We'll use `6.0.37` for this example and I recommend that you also use this version to start with. You can try out other Tomcat versions later after you have become more familiar with the framework.

    $ cd ~/tcif_trial
    $ wget http://apache.claz.org/tomcat/tomcat-6/v6.0.37/bin/apache-tomcat-6.0.37.tar.gz

This specific download URL in this example may no longer be valid. Consult the Tomcat website, http://tomcat.apache.org/, for current download instructions. 

Extract

    $ tar zxf apache-tomcat-6.0.37.tar.gz

We don't need the tar file anymore so let's tidy up.

    $ rm apache-tomcat-6.0.37.tar.gz

The next step is to compile `jsvc`, a Java service daemon. This requires Java and you  need to have the `JAVA_HOME` environment variable set. If java is not installed, then you'll need to download and install that as well. Installing Java is beyond the scope of this document (I gotta draw the line somewhere) but it can be as simple as downloading and upacking a tar file.

Compile and install `jsvc` as follows.

    $ cd ~/tcif_trial/apache-tomcat-6.0.37/bin/
    $ tar zxf commons-daemon-native.tar.gz
    $ cd commons-daemon-*-native-src/unix
    $ ./configure --with-java=$JAVA_HOME
    $ make
    $ cp jsvc ../..

This unpacked apache-tomcat-6.0.37 directory is the installed, working directory. Aside from compiling and installing `jsvc` as we just did there are no other installation steps for Tomcat.

### Acquire the TcIF Source

    $ cd ~/tcif_trial
    $ wget https://codeload.github.com/EuPathDB/tomcat-instance-framework/zip/master -O tomcat-instance-framework.zip
    $ unzip tomcat-instance-framework.zip
    $ rm tomcat-instance-framework.zip 

### Install TcIF

To install TcIF we will need to copy a directory and some files from the `tomcat-instance-framework-master` source.

The `tomcat_instances` directory is the core of the framework. It provides the core directory structure where instance and their configurations are stored. Let's make a working copy of it in the trial directory.

    $ cp -a ~/tcif_trial/tomcat-instance-framework-master/tomcat_instances ~/tcif_trial/

The `instance_manager` script starts and stops Tomcat instances and manages webapps. You can put it anywhere. My shell's `$PATH` includes a bin directory in my home so I'll put it there.

    $ cp ~/tcif_trial/tomcat-instance-framework-master/instance_manager ~/bin/

The `tomcat` file in the source clone is an init script for root-owned system installs. We do not need it for this trial.

### Configure TcIF

By default TcIF expects installations at `/usr/local/tomcat_instances` and `/usr/local/apache-tomcat` . Let's change that expectation.

Set an environment variable for the location of the tomcat_instances directory we just copied.

    $ export TOMCAT_INSTANCES_DIR=~/tcif_trial/tomcat_instances

You may want to put this in your `.bash_profile` so you do not have to remember to set it later.

Alternatively, you can edit value of `TOMCAT_INSTANCES_DIR` at the top of the `instance_manager` script.

Edit `${TOMCAT_INSTANCES_DIR}/shared/conf/global.env` and set the install paths. *Tip: Do not just copy and paste this example, be sure to use the paths for your system.*

    CATALINA_HOME=/home/mheiges/tcif_trial/apache-tomcat-6.0.37
    INSTANCE_DIR=/home/mheiges/tcif_trial/tomcat_instances
    JAVA_HOME=/usr/java/jdk1.7.0
    PID_DIR=/home/mheiges/tcif_trial/tomcat_instances/shared

`global.env` uses the syntax of a BASH rc file. That is, `key=value` with no spaces around the `=`.

### Create an instance. 

Change to the `tomcat_instances` directory and let's look around.

    $ cd ~/tcif_trial/tomcat_instances
    $ ls
    Makefile  shared  templates

A `Makefile` is provided to aid creating an instance from a template in the `templates` directory. See '[Create an instance](TcIF-Manual.md#create-an-instance)' in the main documentation for more information.

The Makefile requires some variables set that define specifics of the desired instance. Here I set the TOMCAT_USER to me using the `$USER` environment variable. Of the templates included with TcIF, the closest one to the 6.0.37 version of Tomcat that we installed is `6.0.35` so I'll try that one and hope it is compatible (Spoiler alert: it is). This instance will be named `FooDB`. This name will be used later when starting/stopping the instance and deployng webapps.

    $ make install                                    \
        INSTANCE=FooDB                                \
        HTTP_PORT=19280                               \
        AJP13_PORT=19209                              \
        JMX_PORT=19205                                \
        TOMCAT_USER=$USER                             \
        TEMPLATE=6.0.35

*Tip: On most Linux systems, you need to root-level permissions to bind to ports lower than 1024.*

Earlier we set the default `CATALINA_HOME` in `shared/global.env`. That is sufficient for the `6.0.35` template we are using because it uses that default. Some templates override `CATALINA_HOME`. See, for example, `templates/7.0.23/conf/instance.env.in`. Therefore if you use a different template you may need to make edits there to accommodate your local installation.


### Start the instance

Recall that we copied the `instance_manager` script to a directory in my `$PATH` and set the `TOMCAT_INSTANCES_DIR` environment variable (or edited the script). We are now ready to start our new instance that we named `FooDB`.

    $ instance_manager start  FooDB 

Give it several seconds to start up, then confirm that it started.

    $ instance_manager status
    INSTANCE      PID       USER   HTTP  AJP13    JMX     UPTIME
    FooDB       17169    mheiges  19280  19209              00m 16s

If `FooDB` is not listed then check the log for startup errors.

    $ cat ~/tcif_trial/tomcat_instances/FooDB/logs/catalina.out 

The instance comes with two webapps preinstalled. The `manager` webapp is required by the `instance_manager` script to function. Do not remove this app. The root app (`/`) is a summary of instance properties. You may remove this root app or replace it with our own app.

We can check that the two apps are running by using the `list` subcommand.

    $ instance_manager manage FooDB list
    OK - Listed applications for virtual host localhost
    /manager:running:0:/home/mheiges/tcif_trial/apache-tomcat-6.0.37/webapps/manager
    /:running:0:/home/mheiges/tcif_trial/tomcat_instances/shared/webapps/ROOT

Now that the `FooDB` instance is running on `localhost` on port `19280` (as shown in the status report above), we can make an http request to the root webapp.

    $ wget -qO- http://localhost:19280/
    ...
    sun.boot.library.path=/usr/java/jdk1.7.0_25/jre/lib/amd64
    java.vm.version=23.25-b01
    shared.loader=
    ...

### Deploy a Sample Webapp

The TcIF source includes a sample<sup>1</sup> war file. Oddly, TcIF does not currently support deploying a war file. So we will unpack the war file and deploy it using a context descriptor file.

Make a new directory and unpack the war file in to it

    $ mkdir ~/tcif_trial/sample
    $ cd ~/tcif_trial/sample
    $ jar xvf  ~/tcif_trial/tomcat-instance-framework-master/docs/sample.war 

Copy the `sample.xml` file (it can go anywhere)

    $ cp ~/tcif_trial/tomcat-instance-framework-master/docs/sample.xml  ~/tcif_trial/

and set the `docBase` attribute to the full path to the `sample` directory. *Tip: Do not just copy and paste this example, be sure to use the `docBase` path for your system.*

    <Context 
      path="/sample"
      docBase="/home/mheiges/tcif_trial/sample"
    />

Now deploy the descriptor file with `instance_manager`

    $ instance_manager manage FooDB deploy ~/tcif_trial/sample.xml 
    OK - Deployed application at context path /sample

List the apps deployed in the `FooDB` instance to see that `/sample` is running. If not, check the `catalina.out` log for errors.

    $ instance_manager manage FooDB list
    OK - Listed applications for virtual host localhost
    /manager:running:0:/home/mheiges/tcif_trial/apache-tomcat-6.0.37/webapps/manager
    /:running:0:/home/mheiges/tcif_trial/tomcat_instances/shared/webapps/ROOT
    /sample:running:0:/home/mheiges/tcif_trial/sample

Point a browser at the `sample` webapp

    $ links http://localhost:19280/sample/

*Tip: Your Tomcat instance port may be blocked to remote clients by a firewall, so testing with a command line client and using `localhost` is the most assured way to interact with your webapps.*

### Conclusion

Hopefully you now have a working Tomcat Instance Framework in which you can deploy your web applications using a context descriptor file simliar to the way you deployed the sample webapp.

If you are satisfied with your installation, you may delete the `tomcat-instance-framework-master` source directory; it is no longer needed.

To delete your whole trial installation, simply delete the trial directory and copy of the `instance_manager` script.

    $ cd ~
    $ rm -rf  ~/tcif_trial/
    $ rm ~/bin/instance_manager

----
<sup>1</sup><sub><sup>The sample web app is attributed to the [Tomcat Project developer community.</sup></sub>](http://tomcat.apache.org/tomcat-6.0-doc/appdev/)

