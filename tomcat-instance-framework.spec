%define pkg_name tomcat-instance-framework-%{version}
%define instance_dir tomcat_instances
%define required_tomcat_version 5.5.30
%define tomcat_uid 300
%define packager Mark Heiges <mheiges@uga.edu>

Summary: EuPathDB-BRC Instance Framework for Apache Tomcat
Name: tomcat-instance-framework
# on CLI, use  --define 'pkg_version 1.2.3'
Version: %{pkg_version}
Release: 1
License: GPL
Group: Networking/Daemons
URL: https://www.cbil.upenn.edu/apiwiki/index.php/UGATomcatConfiguration
Packager: %{packager}

#Requires: java-1.5.0-bea
#Requires: tomcat-%{required_tomcat_version}
Requires(pre): %{_sbindir}/useradd
Requires(pre): %{_sbindir}/groupadd


Source0: tomcat-instance-framework-%{version}.tar.gz

BuildRoot: %{_tmppath}/%{pkg_name}

%description
The tomcat-instance-framework package provides the framework to create 
Tomcat instances for the EuPathDB BRC project.

%prep

%setup -q

%build


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/bin
mkdir -p $RPM_BUILD_ROOT/usr/local
mkdir -p $RPM_BUILD_ROOT/etc/init.d
mkdir -p $RPM_BUILD_ROOT/usr/share/doc/%{pkg_name}-%{version}
cp -a %{instance_dir} $RPM_BUILD_ROOT/usr/local/
cp instance_manager $RPM_BUILD_ROOT/usr/bin/instance_manager
cp tomcat $RPM_BUILD_ROOT/etc/init.d/tomcat
cp Changelog $RPM_BUILD_ROOT/usr/share/doc/%{pkg_name}-%{version}

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
%attr(754, root, root) /etc/init.d/tomcat
/usr/local/%{instance_dir}/Instance_Template
/usr/local/%{instance_dir}/Makefile
/usr/local/%{instance_dir}/shared/webapps

%dir /usr/local/%{instance_dir}
%dir /usr/local/%{instance_dir}/shared
%dir /usr/local/%{instance_dir}/shared/conf

%config /usr/local/%{instance_dir}/shared/conf/cacerts
%config /usr/local/%{instance_dir}/shared/conf/global.env
%config /usr/local/%{instance_dir}/shared/conf/tomcat-users.xml

%doc
/usr/share/doc/%{pkg_name}-%{version}/Changelog

%changelog
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


