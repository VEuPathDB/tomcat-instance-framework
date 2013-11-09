<!---
This doc is written with Markdown syntax.
http://daringfireball.net/projects/markdown/
-->
![logo](/doc/catherder_branded.png) 

## EuPathDB Tomcat Instance Framework

### Background

The EuPathDB tomcat-instance-framework allows easy setup and management of multiple Apache Tomcat instances from one or more binary installation. It was originally developed to support WDK-based installations for the EuPathDB-BRC project but we have found it versatile enough to be used for any web application in Tomcat.

Features include

- Each Tomcat instance is run in its own jvm process with its own configuration options. For example instance `A` may be Java 6 + Tomcat 6 with a 1024MB memory heap, whereas instance `B` can be configured to use Java 7 + Tomcat 7 with a 512MB memory heap.  Each instance can host multiple webapps.
- Each Tomcat instance is named for easy identifcation and management.
- Management script permits non-root users to manage webapp deployments and permits `sudo` users to start/stop instances.

See the [TcIF Manual](/docs/TcIF-Manual.md) for more information.