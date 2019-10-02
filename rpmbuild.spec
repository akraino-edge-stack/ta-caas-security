# Copyright 2019 Nokia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

%define COMPONENT security
%define RPM_NAME caas-%{COMPONENT}
%define RPM_MAJOR_VERSION 1.0.0
%define RPM_MINOR_VERSION 7

Name:           %{RPM_NAME}
Version:        %{RPM_MAJOR_VERSION}
Release:        %{RPM_MINOR_VERSION}%{?dist}
Summary:        Containers as a Service security related playbooks + manifests
License:        %{_platform_license}
BuildArch:      %{_arch}
Vendor:         %{_platform_vendor}
Source0:        %{name}-%{version}.tar.gz

%description
This rpm contains the necessary security related playbooks + manifests for the caas subsystem.

%prep
%autosetup

%build

%install
mkdir -p %{buildroot}/%{_caas_rbac_manifests_path}/
rsync -av rbac_manifests/* %{buildroot}/%{_caas_rbac_manifests_path}/

mkdir -p %{buildroot}/%{_playbooks_path}/
rsync -av ansible/playbooks/* %{buildroot}/%{_playbooks_path}/

mkdir -p %{buildroot}/%{_roles_path}/
rsync -av ansible/roles/* %{buildroot}/%{_roles_path}/

%files
%{_caas_rbac_manifests_path}/*
%{_playbooks_path}/*
%{_roles_path}/*


%preun

%post
mkdir -p %{_postconfig_path}/
ln -sf %{_playbooks_path}/rbac.yaml     %{_postconfig_path}
ln -sf %{_playbooks_path}/security.yaml %{_postconfig_path}


%postun
if [ $1 -eq 0 ]; then
    rm -f %{_postconfig_path}/rbac.yaml
    rm -f %{_postconfig_path}/security.yaml
fi


%clean
rm -rf ${buildroot}
