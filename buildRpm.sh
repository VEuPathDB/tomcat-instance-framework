#!/bin/sh

pkgName=tomcat-instance-framework
pkgVersion=$(cat VERSION)

runtimeDir=$(pwd)
sourceDir=$(dirname $(realpath $0))
cd $sourceDir

workspace=/tmp/rpmbuild-$(openssl rand -hex 12)
buildDirName=build
buildDirPath=${workspace}/${buildDirName}

git log --date=short --pretty=format:"%h%x09%an%x09%ad%x09%s" > Changelog


# purge any previous work directories and recreate
rm -rf ${buildDirPath}
mkdir -p ${buildDirPath}/rpm-build
cd ${buildDirPath}
$(cd rpm-build; mkdir -p BUILD RPMS SOURCES SPECS SRPMS)

ln -s ${sourceDir} ${pkgName}-${pkgVersion}
tar -czf ${buildDirPath}/rpm-build/${pkgName}-${pkgVersion}.tar.gz \
    -C ${buildDirPath} \
    --exclude .git \
    --exclude .gitignore \
    --exclude ${buildDirName} \
    -h ${pkgName}-${pkgVersion}

cd -

rpmbuild \
  -ba \
  --define "_topdir ${buildDirPath}/rpm-build" \
  --define "_builddir %{_topdir}" \
  --define "_rpmdir %{_topdir}/RPM" \
  --define "_build_name_fmt %%{NAME}-%%{VERSION}-%%{RELEASE}.%%{ARCH}.rpm" \
  --define "_srcrpmdir %{_topdir}/RPM" \
  --define "_specdir %{_topdir}" \
  --define "_sourcedir  %{_topdir}" \
  --define "vendor EuPathDB" \
  --define "pkg_version ${pkgVersion}" \
  --define "debug_package %{nil}" \
  ${sourceDir}/tomcat-instance-framework.spec

# copy generated RPMs to the runtime directory
cp ${buildDirPath}/rpm-build/RPM/*.rpm $runtimeDir
