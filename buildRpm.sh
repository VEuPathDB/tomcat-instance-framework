#!/bin/bash

export WORKSPACE=/tmp
export BUILDDIR=build
export source_dir=$(pwd)
export package_name=tomcat-instance-framework
export PKG_VERSION=$(cat VERSION)

rm    -rf ${WORKSPACE}/${BUILDDIR}
mkdir -p  ${WORKSPACE}/${BUILDDIR}
mkdir -p  ${WORKSPACE}/${BUILDDIR}/rpm-build/RPM/SRPM

cd ${source_dir}
git log --date=short --pretty=format:"%h%x09%an%x09%ad%x09%s" > Changelog

cd ${WORKSPACE}/${BUILDDIR}
ln -s ${source_dir} ${package_name}-${PKG_VERSION}
tar -czf ${WORKSPACE}/${BUILDDIR}/rpm-build/${package_name}-${PKG_VERSION}.tar.gz \
    -C ${WORKSPACE}/${BUILDDIR} \
    --exclude .git \
    --exclude .gitignore \
    --exclude ${BUILDDIR} \
    -h ${package_name}-${PKG_VERSION}
cd -

rpmbuild \
-bb \
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
${source_dir}/tomcat-instance-framework.spec
