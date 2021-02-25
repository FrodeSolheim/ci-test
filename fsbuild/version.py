import os
import re
import subprocess
import sys


class Version:
    def __init__(self, version):
        self.version = version
        m = re.match("([0-9.]+[0-9])(.*)", version)
        parts = m.group(1).split(".")
        assert len(parts) in [2, 3]
        self.major = int(parts[0])
        self.minor = int(parts[1])
        if len(parts) > 2:
            self.revision = int(parts[2])
        else:
            self.revision = 0
        self.tag = m.group(2)
        self.commit = ""

    def __str__(self):
        version = "{}.{}.{}".format(self.major, self.minor, self.revision)
        return version + self.tag


def shell(command):
    return subprocess.check_output(command, shell=True).decode("UTF-8")


def num_commits_since(base):
    to = "HEAD"
    return int(
        subprocess.check_output(
            ["git", "rev-list", f"{base}..{to}", "--count"]
        ).decode()
    )


def find_last_commit_for_file(path):
    commit = subprocess.check_output(
        ["git", "log", "-n", "1", "--pretty=format:%H", "--", path]
    ).decode()
    return commit


def find_last_commit():
    commit = subprocess.check_output(
        ["git", "log", "-n", "1", "--pretty=format:%H"]
    ).decode()
    return commit


def update_configure_ac(version, commit=""):
    print("Updating configure.ac")
    lines = []
    with open("configure.ac", "r", encoding="UTF-8") as f:
        for line in f:
            if line.startswith("m4_define([fsbuild_version"):
                if "_major" in line:
                    k = "FSBUILD_VERSION_MAJOR"
                    v = version.major
                    d = "Major version"
                elif "_minor" in line:
                    k = "FSBUILD_VERSION_MINOR"
                    v = version.minor
                    d = "Minor version"
                elif "_revision" in line:
                    k = "FSBUILD_VERSION_REVISION"
                    v = version.revision
                    d = "Revision"
                else:
                    k = "FSBUILD_VERSION"
                    v = str(version)
                    d = "Full version"
                line = "m4_define([{}], [{}])\n".format(k.lower(), v)
            # if line.startswith("AC_DEFINE_UNQUOTED([FSBUILD_VERSION"):
            #     if "_MAJOR" in line:
            #         k = "FSBUILD_VERSION_MAJOR"
            #         v = version.major
            #         d = "Major version"
            #     elif "_MINOR" in line:
            #         k = "FSBUILD_VERSION_MINOR"
            #         v = version.minor
            #         d = "Minor version"
            #     elif "_REVISION" in line:
            #         k = "FSBUILD_VERSION_REVISION"
            #         v = version.revision
            #         d = "Revision"
            #     else:
            #         k = "FSBUILD_VERSION"
            #         v = str(version)
            #         d = "Full version"
            #     line = "AC_DEFINE_UNQUOTED([{}], [{}], [{}])\n".format(k, v, d)
            if line.startswith("m4_define([fsbuild_commit"):
                line = "m4_define([{}], [{}])\n".format(
                    "fsbuild_commit", commit
                )
            # if line.startswith("AC_DEFINE_UNQUOTED([FSBUILD_COMMIT"):
            #     k = "FSBUILD_COMMIT"
            #     v = commit
            #     d = "Package commit"
            #     line = "AC_DEFINE_UNQUOTED([{}], [{}], [{}])\n".format(k, v, d)
            lines.append(line)
    with open("configure.ac", "w", encoding="UTF-8") as f:
        for line in lines:
            f.write(line)


def update_debian_changelog(version):
    print("Updating debian/changelog")
    lines = []
    first_line = True
    first_line_changed = False
    deb_package = "unknown"
    deb_version = str(version)
    # deb_version = deb_version.replace("alpha", "~alpha")
    # deb_version = deb_version.replace("beta", "~beta")
    # deb_version = deb_version.replace("dev", "~dev")
    with open("debian/changelog", "r", encoding="UTF-8") as f:
        for line in f:
            if first_line:
                first_line = False
                deb_package = line.split(" ", 1)[0]
                lines.append(
                    "{} ({}-0) unstable; urgency=low\n".format(
                        deb_package, deb_version
                    )
                )
                if lines[-1] != line:
                    first_line_changed = True
            elif line.startswith(" -- ") and first_line_changed:
                # Only update date if version was changed
                author, date = line.split("  ")
                date = shell(
                    "LC_TIME=C date '+%a, %e %b %Y %H:%M:%S %z'"
                ).strip()
                lines.append("{}  {}\n".format(author, date))
            else:
                lines.append(line)
    with open("debian/changelog", "w", encoding="UTF-8") as f:
        for line in lines:
            f.write(line)


def update_spec_file(path, version):
    print("Updating", path)
    lines = []
    rpm_version = str(version)
    # rpm_version = rpm_version.replace("alpha", "-0.1alpha")
    # rpm_version = rpm_version.replace("beta", "-0.1~beta")
    # rpm_version = rpm_version.replace("dev", "-0.1dev")
    # if not "-" in rpm_version:
    #     rpm_version += "-1"
    with open(path, "r", encoding="UTF-8") as f:
        for line in f:
            if line.startswith("%define fsbuild_version "):
                lines.append(
                    "%define fsbuild_version {}\n".format(rpm_version)
                )
            # elif line.startswith("%define unmangled_version "):
            #     lines.append("%define unmangled_version {0}\n".format(version))
            else:
                lines.append(line)
    with open(path, "w", newline="\n") as f:
        f.write("".join(lines))


def update_package_fs(version):
    print("Updating PACKAGE.FS")
    lines = []
    with open("PACKAGE.FS", "r", encoding="UTF-8") as f:
        for line in f:
            if line.startswith("PACKAGE_VERSION="):
                lines.append(f"PACKAGE_VERSION={str(version)}\n")
            elif line.startswith("PACKAGE_VERSION_MAJOR="):
                lines.append(f"PACKAGE_VERSION_MAJOR={str(version.major)}\n")
            elif line.startswith("PACKAGE_VERSION_MINOR="):
                lines.append(f"PACKAGE_VERSION_MINOR={str(version.minor)}\n")
            elif line.startswith("PACKAGE_VERSION_REVISION="):
                lines.append(f"PACKAGE_VERSION_REVISION={str(version.revision)}\n")
            elif line.startswith("PACKAGE_VERSION_TAG="):
                lines.append(f"PACKAGE_VERSION_TAG={str(version.tag)}\n")
            elif line.startswith("PACKAGE_COMMIT="):
                lines.append(f"PACKAGE_COMMIT={version.commit}\n")
            else:
                lines.append(line)
    with open("PACKAGE.FS", "w", newline="\n") as f:
        f.write("".join(lines))


def update_version_fs(version):
    print("Updating VERSION.FS")
    with open("VERSION.FS", "w") as f:
        f.write(str(version))
        f.write("\n")


def update_commit_fs(version):
    print("Updating COMMIT.FS")
    with open("COMMIT.FS", "w") as f:
        if version.commit:
            f.write(version.commit)
            f.write("\n")


def calculate_version(auto_revision=False, include_commit=False):
    with open("fsbuild/VERSION") as f:
        # with open("VERSION.FS") as f:
        version_str = f.read().strip()
    version = Version(version_str)
    if auto_revision:
        version_commit = find_last_commit_for_file("VERSION.FS")
        # version.revision = 1 + num_commits_since(version_commit)
        version.revision += num_commits_since(version_commit)
        # version.revision += 1 + num_commits_since(version_commit)
    if "--commit" in sys.argv:
        version.commit = find_last_commit()
    return version


def update_version(version):
    update_version_fs(version)
    update_commit_fs(version)
    if os.path.exists("configure.ac"):
        update_configure_ac(version)
    if os.path.exists("debian/changelog"):
        update_debian_changelog(version)
    if os.path.exists("PACKAGE.FS"):
        update_package_fs(version)
    for filename in os.listdir("."):
        if filename.endswith(".spec"):
            update_spec_file(filename, version)


def main():
    auto_revision = "--revision" in sys.argv
    include_commit = "--commit" in sys.argv
    version = calculate_version(
        auto_revision=auto_revision, include_commit=include_commit
    )
    print(str(version))

    if "--update" in sys.argv:
        update_version(version)


if __name__ == "__main__":
    main()
