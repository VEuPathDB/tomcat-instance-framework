%define pkg_name tomcat-instance-framework
%define instance_dir tomcat_instances
%define required_tomcat_version 6.0.35
%define required_java_version 1.7.0_25
%define required_oracle_version 11.2.0.3
%define tomcat_uid 300
%define packager Mark Heiges <mheiges@uga.edu>

Summary: EuPathDB-BRC Instance Framework for Apache Tomcat
Name: tomcat-instance-framework
# set version on CLI, e.g. rpmbuild --define 'pkg_version 1.2.3'
Version: %{pkg_version}
Release: 1
License: GPL
Group: Networking/Daemons
URL: https://www.cbil.upenn.edu/apiwiki/index.php/UGATomcatConfiguration
Packager: %{packager}

Requires: jdk >= %{required_java_version}
Requires: tomcat-%{required_tomcat_version}
Requires: perl-XML-Simple
Requires(pre): %{_sbindir}/useradd
Requires(pre): %{_sbindir}/groupadd


Source0: tomcat-instance-framework-%{version}.tar.gz

BuildRoot: %{_tmppath}/%{pkg_name}-%{version}

%description
The tomcat-instance-framework package provides the framework to create 
Tomcat instances for the EuPathDB BRC project.

%prep

%setup -q

%build
%define tc_shared_conf tomcat_instances/shared/conf/global.env
sed -i 's;^CATALINA_HOME=.*;CATALINA_HOME=/usr/local/apache-tomcat-%{required_tomcat_version};' %{tc_shared_conf}
sed -i 's;^JAVA_HOME=.*;JAVA_HOME=/usr/java/jdk%{required_java_version};' %{tc_shared_conf}
sed -i 's;^ORACLE_HOME=.*;ORACLE_HOME=/u01/app/oracle/product/%{required_oracle_version}/db_1;' %{tc_shared_conf}

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/bin
mkdir -p $RPM_BUILD_ROOT/usr/local
mkdir -p $RPM_BUILD_ROOT/etc/profile.d
mkdir -p $RPM_BUILD_ROOT/usr/share/doc/%{pkg_name}
cp -a %{instance_dir} $RPM_BUILD_ROOT/usr/local/
cp instance_manager $RPM_BUILD_ROOT/usr/bin/instance_manager
cp Changelog $RPM_BUILD_ROOT/usr/share/doc/%{pkg_name}
cp ReadMe.md $RPM_BUILD_ROOT/usr/share/doc/%{pkg_name}
cp misc/bash_tab_completion.sh $RPM_BUILD_ROOT/etc/profile.d/tcif_completion.sh

%if 0%{?rhel} >=7
mkdir -p $RPM_BUILD_ROOT/usr/lib/systemd/system
cp tomcat.service $RPM_BUILD_ROOT/usr/lib/systemd/system/tomcat.service
%else
mkdir -p $RPM_BUILD_ROOT/etc/init.d
cp tomcat $RPM_BUILD_ROOT/etc/init.d/tomcat
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%pre
# Add the "tomcat" user and group
getent group tomcat >/dev/null || %{_sbindir}/groupadd -g %{tomcat_uid} tomcat
getent passwd tomcat >/dev/null || \
    %{_sbindir}/useradd -c "Apache Tomcat" -r -u %{tomcat_uid} -g tomcat \
    -s /sbin/nologin tomcat 
exit 0

%files
%defattr(-, tomcat, tomcat)
%attr(755, root, root) /usr/bin/instance_manager

%if 0%{?rhel} >=7
%attr(0644, root, root) /usr/lib/systemd/system/tomcat.service
%else
%attr(0754, root, root) /etc/init.d/tomcat
%endif

/usr/local/%{instance_dir}/templates
/usr/local/%{instance_dir}/Makefile
/usr/local/%{instance_dir}/shared/webapps
/etc/profile.d/tcif_completion.sh

%dir /usr/local/%{instance_dir}
%dir /usr/local/%{instance_dir}/shared
%dir /usr/local/%{instance_dir}/shared/conf

%config /usr/local/%{instance_dir}/shared/conf/cacerts
%config(noreplace) /usr/local/%{instance_dir}/shared/conf/global.env
%config(noreplace) /usr/local/%{instance_dir}/shared/conf/tomcat-users.xml

%doc /usr/share/doc/%{pkg_name}/Changelog
%doc /usr/share/doc/%{pkg_name}/ReadMe.md

%changelog
* Tue Aug 14 2012 Mark Heiges <mheiges@uga.edu> 1.0-1
- update to tomcat 6.0.35

* Wed Jun 6 2012 Mark Heiges <mheiges@uga.edu>
- fix %config settings

* Tue May 22 2012 Mark Heiges <mheiges@uga.edu> 1.2-1
- rework spec to aid parameterized version builds

* Wed Oct 5 2011 Mark Heiges <mheiges@uga.edu> 1.1-3
- fix instance_manager path in init script, #5958
- added JDBC install option in Makefile, #5787
- instance_manager stops file ownership checks, #6114

* Fri Feb 18 2011 Mark Heiges <mheiges@uga.edu> 1.1-2
- fix instance_dir path

* Fri Feb 18 2011 Mark Heiges <mheiges@uga.edu> 1.1-1
- fix check for existing user in tomcat_instance Makefile
- install instance_manager to /usr/bin instead of /usr/local/bin

* Tue Nov 30 2010 Mark Heiges <mheiges@uga.edu>
- change tomcat uids to a range that doesn't conflict with system uids
- useradd script changed to follow packaging guidelines 
    https://fedoraproject.org/wiki/Packaging:UsersAndGroups

* Mon Aug 30 2010 Mark Heiges <mheiges@uga.edu>
- set default CATALINA_HOME in  Makefile

* Wed Jul 21 2010 Mark Heiges <mheiges@uga.edu>
- Initial release.


