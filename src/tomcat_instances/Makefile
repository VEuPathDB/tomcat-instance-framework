# Make a Tomcat project instance for EuPathDB
# usage
#
#  make INSTANCE=PootieDB                                \
#       JAVA_HOME=/usr/lib/jvm/jre-1.5.0-bea            \
#       JSVC_EXE=/usr/local/apache-tomcat/bin/jsvc      \
#       CATALINA_HOME=/usr/local/apache-tomcat          \
#       HTTP_PORT=19280                                 \
#       AJP13_PORT=19209                                \
#       SHUTDOWN_PORT=19205                             \
#       TOMCAT_USER=tomcat_Z                            \
#       INSTALL_ORACLE_JDBC=1


INSTANCE=PootieDB
JAVA_HOME=/usr/lib/jvm/jre-1.5.0-bea
JSVC_EXE=/usr/local/apache-tomcat/bin/jsvc
CATALINA_HOME=/usr/local/apache-tomcat
HTTP_PORT=19280
AJP13_PORT=19209
SHUTDOWN_PORT=19205
TOMCAT_USER=tomcat_Z


all :
ifneq "$(wildcard $(INSTANCE) )" ""
	@echo $(INSTANCE) already exits
	@exit 1
endif
	@if [ -z `id -u $(TOMCAT_USER)  2> /dev/null` ]; then \
        echo user $(TOMCAT_USER) does not exist; \
        exit 1; \
	fi
	@if [[ "$(INSTALL_ORACLE_JDBC)" -eq "1" ]]; then \
	  if [[ -z "$(ORACLE_HOME)" ]]; then \
        echo ORACLE_HOME is not set, can not install JDBC driver; \
        exit 1; \
      fi; \
	  if [[ ! -f "$(ORACLE_HOME)/jdbc/lib/ojdbc5.jar" ]]; then \
        echo ojdbc5.jar is not found at $(ORACLE_HOME)/jdbc/lib/ojdbc5.jar, can not install JDBC driver; \
        exit 1; \
      fi; \
	 fi;

	cp -a Instance_Template $(INSTANCE)

	cd $(INSTANCE)/conf && \
	sed -e 's;JAVA_HOME=.*;JAVA_HOME=$(JAVA_HOME);'                 \
	    -e 's;JSVC_EXE=.*;JSVC_EXE=$(JSVC_EXE);'                    \
	    -e 's;CATALINA_HOME=.*;CATALINA_HOME=$(CATALINA_HOME);'     \
	    -e 's;HTTP_PORT=.*;HTTP_PORT=$(HTTP_PORT);'                 \
	    -e 's;AJP13_PORT=.*;AJP13_PORT=$(AJP13_PORT);'              \
	    -e 's;SHUTDOWN_PORT=.*;SHUTDOWN_PORT=$(SHUTDOWN_PORT);'     \
	    -e 's;TOMCAT_USER=.*;TOMCAT_USER=$(TOMCAT_USER);'           \
	    instance.env.in > instance.env

	@if [[ "$(INSTALL_ORACLE_JDBC)" -eq "1" ]]; then \
        echo installing $(ORACLE_HOME)/jdbc/lib/ojdbc5.jar; \
        cp $(ORACLE_HOME)/jdbc/lib/ojdbc5.jar $(INSTANCE)/shared/lib/; \
     fi

	chown -R $(TOMCAT_USER):tomcat $(INSTANCE)
