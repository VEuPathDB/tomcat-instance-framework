# Make a Tomcat project instance for EuPathDB
# usage
#
#  make install                        \
#    INSTANCE=PootieDB                \
#    HTTP_PORT=19280                  \
#    AJP13_PORT=19209                 \
#    JMX_PORT=19205                   \
#    TOMCAT_USER=tomcat_Z             \
#    INSTALL_ORACLE_JDBC=1
#
#  make update                        \
#    INSTANCE=PootieDB                \
#    HTTP_PORT=19280                  \
#    AJP13_PORT=19209                 \
#    JMX_PORT=19205                   \
#    TOMCAT_USER=tomcat_Z             \
#    INSTALL_ORACLE_JDBC=1

# Other special purppose variables
#    DEFER_USER=1  - do not do check and chown for user. Useful for RPM builds on naive servers, 
#                    assuming the RPM install process does the chown (e.g. using %attr() ).

TS=$(shell date +%y%m%d%H%M%S)

all:
	@echo Usage:
	@echo 'make install'
	@echo 'make update'
	@echo 'with defined environment varialbles:'
	@echo '  INSTANCE=PootieDB                \
  HTTP_PORT=19280                  \
  AJP13_PORT=19209                 \
  JMX_PORT=19205                   \
  TOMCAT_USER=tomcat_Z             \
  INSTALL_ORACLE_JDBC=1'


install : can_install copy_template install_oracle configure fix_perms
update: can_update install_oracle replace_configuration configure fix_perms

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

install_oracle:
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

	@if [[ "$(INSTALL_ORACLE_JDBC)" -eq "1" ]]; then \
        echo installing $(ORACLE_HOME)/jdbc/lib/ojdbc5.jar; \
        cp $(ORACLE_HOME)/jdbc/lib/ojdbc5.jar $(INSTANCE)/shared/lib/; \
     fi

copy_template:
	cp -a Instance_Template $(INSTANCE)

configure:
	@echo configure
	cd $(INSTANCE)/conf \
	&& \
	sed -e 's;HTTP_PORT=.*;HTTP_PORT=$(HTTP_PORT);'      \
	    -e 's;AJP13_PORT=.*;AJP13_PORT=$(AJP13_PORT);'   \
	    -e 's;JMX_PORT=.*;JMX_PORT=$(JMX_PORT);'         \
	    -e 's;TOMCAT_USER=.*;TOMCAT_USER=$(TOMCAT_USER);'\
	    instance.env.in > instance.env

fix_perms:
	chmod 0644 $(INSTANCE)/conf/instance.env
	@if [[ "$(DEFER_USER)" -ne 1 ]]; then \
	  chown -R $(TOMCAT_USER):tomcat $(INSTANCE); \
	fi;


# Install new configuration from Instance_Template. Original configuration
# is renamed with .${timestamp}.ori extension
replace_configuration:
	@echo 'archiving $(INSTANCE)/conf as $(INSTANCE)/conf.$(TS)'
	mv $(INSTANCE)/conf $(INSTANCE)/conf.$(TS)
	cp -a Instance_Template/conf $(INSTANCE)/conf
	rm -rf $(INSTANCE)/work/*
