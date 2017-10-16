Summary: A command line tool used to investigate the point of entry of malicious files.
Name: filescout
Version: 2
Release: 12
Group: mrjung
BuildArch: noarch
License: GPL
Source: %{_topdir}
BuildRoot: %{_topdir}/BUILD/%{name}-%{version}-%{release}
Requires: coreutils

%files
%{_bindir}/filescout
%{_mandir}/man1/filescout.1

%description
%{summary}

%prep
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
cd $RPM_BUILD_ROOT
install -p -m 700 %{_topdir}/usr/bin/filescout $RPM_BUILD_ROOT%{_bindir}
install -p -m 644 %{_topdir}/usr/share/man/man1/filescout.1 $RPM_BUILD_ROOT%{_mandir}/man1/filescout.1

%clean
rm -r -f "$RPM_BUILD_ROOT"

%changelog
* Mon Oct 16 2017 Matt Jung 2.12
- Encased $file, $posted_file and $abspath in quotes to work around spaces in file names
- Converted %20 in URI's to spaces when assigning the posted_file variable
- Corrected the deep dive loop prevention logic to break out of the loop if a file self-modifies itself.
- Added usage reporting 

* Sat Oct 14 2017 Matt Jung 2.11
- Added apache_domlog_result_all to no_log_results if logic

* Sun Oct 8 2017 Matt Jung 2.10
- Cleaned specfile

* Tue Oct 3 2017 Matt Jung 2.9
- Straight up skipped 2.8
- Added the -b flag to force use of file creation time.

* Tue Sep 5 2017 Matt Jung 2.7
- Removed empty string checks for each preceding section
- Apache domlog dive: look for GET requests during the same time period ONLY if no POST request returns
- Changed '! -z' logic to '-n '
- Prevent infinite loop with -r if a file modifies itself.

* Mon Aug 7 2017 Matt Jung
- Made the RPM noarch, because I probably hsould have done that right off the get-go.
- Fixed typo in man page
- Removed debugging var output from -t flag
- Fixed regex and date commands in sftp_log_dive and ftp_log_dive to account for single digit dates without leading 0's and more than 1 space between the day and month.
- Added logic in sftp_log_dive to only run if cPanel_log_result, ftp_log_result, and apache_domlog_result are empty.

* Sat Aug 5 2017 Matt Jung
- Version 2.4 added a man page

* Sat Aug 5 2017 Matt Jung
- Version 2.3 released
- Made additional formatting fixes for indentation to be uniform across the script.
- Fixed the grep in /var/log/messages* to account for single digit dates and more than one space between the month and day in the log entry

* Wed Jul 26 2017 Matt Jung
- Further cleaned up code formatting and comments
- Removed some unnecessary output for the stat
- Added -t reminder if $file is already 000
- Added note in usage output that the timestamp in -t needs to be in quotes

* Tue Jul 25 2017 Matt Jung
- Added -r flag
- Added additional checks for the -t flag checking for too few args and checking that time timestamp provided is an actual timestamp
- removed chmod 000 reminder from -t 
- Cleaned up code formatting
- Moved the timestamp_month_year function into apache_domlog_dive function

* Sat Jul 22 2017 Matt Jung
- Version 2.0 released
- Converted most functionality into functions
- Added -m -c -t -h flags
- Added logic to check for the correct number of arguments based on the flags used.
- Added usage output to error output.

* Sun Jul 16 2017 Matt Jung
- Added check for plesk environment, and added message to use the plesk version of filescout if so
- Improved wording of wp-admin compromise message

* Sat Jul 15 2017 Matt Jung
- Added warning if HTTP POST is directed to /wp-admin/theme-editor.php, which indicates wp-admin password compromise.

* Sun Jul 9 2017 Matt Jung
- Name changed from lwchmod to filescout
- Removed interactive chmod 000 to make the script not make any changes on the host its run on
- Show absolute path for HTTP POSTS if the URI is a .php file
- Add warning if the file already has 000 permissions

* Mon Jun 19 2017 Matt Jung
- Use readlink --canonicalize to generate the $abspath variable instead of realpath (CentOS 6 compatibility)

* Sat Jun 10 2017 Matt Jung
- Initial creation
