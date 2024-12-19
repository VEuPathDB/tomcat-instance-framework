#!/bin/sh
#################################################
## Copied from Jenkins job performing this task
#################################################

export WORKSPACE=/tmp
export BUILDDIR=build
export PKG_NAME=tomcat-instance-framework
export PKG_VERSION=$(cat VERSION)

# purge any previous work directories and recreate
rm -rf ${WORKSPACE}/${BUILDDIR}
mkdir -p ${WORKSPACE}/${BUILDDIR}/rpm-build/RPM/SRPM

runtimeDir=$(pwd)
sourceDir=$(dirname $(realpath $0))

cd $sourceDir

git log --date=short --pretty=format:"%h%x09%an%x09%ad%x09%s" > Changelog

cd ${WORKSPACE}/${BUILDDIR}
ln -s ${sourceDir} ${PKG_NAME}-${PKG_VERSION}
tar -czf ${WORKSPACE}/${BUILDDIR}/rpm-build/${PKG_NAME}-${PKG_VERSION}.tar.gz \
    -C ${WORKSPACE}/${BUILDDIR} \
    --exclude .git \
    --exclude .gitignore \
    --exclude ${BUILDDIR} \
    -h ${PKG_NAME}-${PKG_VERSION}

cd -

rpmbuild \
  -ba \
  --define "_topdir ${WORKSPACE}/${BUILDDIR}/rpm-build" \
  --define "_builddir %{_topdir}" \
  --define "_rpmdir %{_topdir}/RPM" \
  --define "_build_name_fmt %%{NAME}-%%{VERSION}-%%{RELEASE}.%%{ARCH}.rpm" \
  --define "_srcrpmdir %{_topdir}/RPM" \
  --define "_specdir %{_topdir}" \
  --define "_sourcedir  %{_topdir}" \
  --define "vendor EuPathDB" \
  --define "pkg_version ${PKG_VERSION}" \
  --define "debug_package %{nil}" \
  ${sourceDir}/tomcat-instance-framework.spec

# copy generated RPMs to the runtime directory
cp ${WORKSPACE}/${BUILDDIR}/rpm-build/RPM/*.rpm $runtimeDir
