# Make a Tomcat project instance for EuPathDB
# usage
#
#  make install                       \
#    INSTANCE=FooDB                   \
#    HTTP_PORT=19280                  \
#    AJP13_PORT=19209                 \
#    JMX_PORT=19205                   \
#    TOMCAT_USER=tomcat_Z             \
#    ORCL_JDBC_PATH=$ORACLE_HOME/jdbc/lib/ojdbc6.jar \
#    PG_JDBC_PATH=$PG_HOME/lib/java/postgresql92-jdbc.jar
#
#  make update                        \
#    INSTANCE=FooDB                   \
#    HTTP_PORT=19280                  \
#    AJP13_PORT=19209                 \
#    JMX_PORT=19205                   \
#    TOMCAT_USER=tomcat_Z             \
#    ORCL_JDBC_PATH=$ORACLE_HOME/jdbc/lib/ojdbc6.jar \
#    PG_JDBC_PATH=$PG_HOME/lib/java/postgresql92-jdbc.jar
#
# Optionally,
#    ORCL_JDBC_PATH and PG_JDBC_PATH are optional

# Other special purppose variables
#    DEFER_USER=1  - do not do check and chown for user. Useful for RPM builds on naive servers, 
#                    assuming the RPM install process does the chown (e.g. using %attr() ).

TS := $(shell date +%y%m%d%H%M%S)
MANAGER_USER := $(shell tr -dc A-Za-z0-9 < /dev/urandom | head -c 12 )
MANAGER_PASSWD := $(shell tr -dc A-Za-z0-9 < /dev/urandom | head -c 12 )

all:
	@echo Usage:
	@echo 'make install'
	@echo 'make update'
	@echo
	@echo 'Required variables:'
	@echo '  INSTANCE=FooDB                              \
  HTTP_PORT=19280                             \
  AJP13_PORT=19209                            \
  JMX_PORT=19205                              \
  TOMCAT_USER=tomcat_Z                        \
  TEMPLATE=7.0.23'
	@echo
	@echo 'Optional variables:'
	@echo '  ORCL_JDBC_PATH=$$ORACLE_HOME/jdbc/lib/ojdbc6.jar'
	@echo '  PG_JDBC_PATH=$$PG_HOME/lib/java/postgresql92-jdbc.jar'

install : can_install copy_temp_template install_oracle_driver install_pg_driver configure fix_perms
update: can_update install_oracle_driver install_pg_driver replace_configuration configure fix_perms restart_notice

can_install:
ifneq "$(wildcard $(INSTANCE) )" ""
	@echo $(INSTANCE) already exits
	@exit 1
endif
	@if [[ "$(DEFER_USER)" -ne 1 && -z `id -u $(TOMCAT_USER)  2> /dev/null` ]]; then \
        echo user $(TOMCAT_USER) does not exist; \
        exit 1; \
	fi

can_update :
ifeq "$(wildcard $(INSTANCE) )" ""
	@echo $(INSTANCE) does not exit
	@exit 1
endif

install_oracle_driver:
	@if [[ -n "$(ORCL_JDBC_PATH)" ]]; then \
	  if [[ ! -f "$(ORCL_JDBC_PATH)" ]]; then \
        echo $(ORCL_JDBC_PATH) not found, can not install JDBC driver; \
        exit 1; \
      fi; \
    echo installing $(ORCL_JDBC_PATH); \
    cp $(ORCL_JDBC_PATH) $(INSTANCE)/shared/lib/; \
	 fi;

install_pg_driver:
	@if [[ -n "$(PG_JDBC_PATH)" ]]; then \
	  if [[ ! -f "$(PG_JDBC_PATH)" ]]; then \
        echo $(PG_JDBC_PATH) not found, can not install JDBC driver; \
        exit 1; \
      fi; \
    echo installing $(PG_JDBC_PATH); \
    cp $(PG_JDBC_PATH) $(INSTANCE)/shared/lib/; \
	 fi;

copy_temp_template:
	cp -a templates/$(TEMPLATE) $(INSTANCE)
	chmod 0644 $(INSTANCE)/conf/tomcat-users.xml
 
configure:
	@echo configure instance.env ...
	cd $(INSTANCE)/conf \
	&& \
	sed -e 's;HTTP_PORT=.*;HTTP_PORT=$(HTTP_PORT);'             \
	    -e 's;AJP13_PORT=.*;AJP13_PORT=$(AJP13_PORT);'          \
	    -e 's;JMX_PORT=.*;JMX_PORT=$(JMX_PORT);'                \
	    -e 's;TOMCAT_USER=.*;TOMCAT_USER=$(TOMCAT_USER);'       \
	    instance.env.in > instance.env

	@echo set tomcat-users.xml credentials \(not echoed to screen\) ...
	@cd $(INSTANCE)/conf \
	&& \
	sed -i -e 's;@MANAGERUSER@;$(MANAGER_USER);' \
	       -e 's;@MANAGERPASSWD@;$(MANAGER_PASSWD);' \
	    tomcat-users.xml

fix_perms:
	chmod 0644 $(INSTANCE)/conf/instance.env
	@if [[ "$(DEFER_USER)" -ne 1 && "$(USER)" != "$(TOMCAT_USER)" ]]; then \
	  chown -R $(TOMCAT_USER):tomcat $(INSTANCE); \
	fi;


# Install new configuration from Instance_Template. Original configuration
# is renamed with .${timestamp}.ori extension
replace_configuration:
	@echo 'archiving $(INSTANCE)/conf as $(INSTANCE)/conf.$(TS)'
	mv $(INSTANCE)/conf $(INSTANCE)/conf.$(TS)
	cp -a templates/$(TEMPLATE)/conf $(INSTANCE)/conf
	rm -rf $(INSTANCE)/work/*

restart_notice:
	@echo
	@echo "Restart $(INSTANCE) by running 'instance_manager restart $(INSTANCE)'"
