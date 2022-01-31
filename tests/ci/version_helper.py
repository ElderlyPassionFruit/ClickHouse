#!/usr/bin/env python3
import datetime
import logging
import os.path as p
import subprocess
import sys
from typing import Dict, Union

from git_helper import Git
from push_to_artifactory import removeprefix

FILE_WITH_VERSION_PATH = "cmake/autogenerated_versions.txt"
CHANGELOG_IN_PATH = "debian/changelog.in"
CHANGELOG_PATH = "debian/changelog"
GENERATED_CONTRIBUTORS = "src/Storages/System/StorageSystemContributors.generated.cpp"

# It has {{{{ for plain "{" and {{ for following formatting
CONTRIBUTORS_TEMPLATE = f"""// autogenerated by {sys.argv[0]}
const char * auto_contributors[] {{{{
{{}}
    nullptr}}}};"""

VERSIONS = Dict[str, Union[int, str]]

VERSIONS_TEMPLATE = """# This variables autochanged by release_lib.sh:

# NOTE: has nothing common with DBMS_TCP_PROTOCOL_VERSION,
# only DBMS_TCP_PROTOCOL_VERSION should be incremented on protocol changes.
SET(VERSION_REVISION {revision})
SET(VERSION_MAJOR {major})
SET(VERSION_MINOR {minor})
SET(VERSION_PATCH {patch})
SET(VERSION_GITHASH {githash})
SET(VERSION_DESCRIBE {describe})
SET(VERSION_STRING {string})
# end of autochange
"""

git = Git()


class ClickHouseVersion:
    """Immutable version class. On update returns a new instance"""

    def __init__(
        self,
        major: Union[int, str],
        minor: Union[int, str],
        patch: Union[int, str],
        tweak: Union[int, str],
        revision: Union[int, str],
        git: Git,
    ):
        self._major = int(major)
        self._minor = int(minor)
        self._patch = int(patch)
        self._tweak = int(tweak)
        self._revision = int(revision)
        self._string = ".".join(
            (str(self.major), str(self.minor), str(self.patch), str(self.tweak))
        )
        self._git = git
        self._describe = ""

    def major_update(self) -> "ClickHouseVersion":
        return ClickHouseVersion(self.major + 1, 1, 1, 1, self.revision + 1, self._git)

    def minor_update(self) -> "ClickHouseVersion":
        return ClickHouseVersion(
            self.major, self.minor + 1, 1, 1, self.revision + 1, self._git
        )

    def patch_update(self) -> "ClickHouseVersion":
        return ClickHouseVersion(
            self.major, self.minor, self.patch + 1, 1, self.revision, self._git
        )

    def tweak_update(self) -> "ClickHouseVersion":
        return ClickHouseVersion(
            self.major, self.minor, self.patch, self.tweak + 1, self.revision, self._git
        )

    @property
    def major(self):
        return self._major

    @property
    def minor(self):
        return self._minor

    @property
    def patch(self):
        return self._patch

    @property
    def tweak(self):
        return self._tweak

    @property
    def revision(self):
        return self._revision

    @property
    def githash(self):
        return self._git.sha

    @property
    def describe(self):
        return self._describe

    @property
    def string(self):
        return self._string

    def as_dict(self) -> VERSIONS:
        return {
            "revision": self.revision,
            "major": self.major,
            "minor": self.minor,
            "patch": self.patch,
            "githash": self.githash,
            "describe": self.describe,
            "string": self.string,
        }

    def as_tuple(self):
        return (self.major, self.minor, self.patch, self.tweak)

    def with_description(self, version_type):
        if version_type not in VersionType.VALID:
            raise ValueError(f"version type {version_type} not in {VersionType.VALID}")
        self._describe = f"v{self.string}-{version_type}"


class VersionType:
    LTS = "lts"
    PRESTABLE = "prestable"
    STABLE = "stable"
    TESTING = "testing"
    VALID = (LTS, PRESTABLE, STABLE, TESTING)


def read_versions(filename: str) -> VERSIONS:
    versions = {}
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line.startswith("SET("):
                continue

            value = 0  # type: Union[int, str]
            name, value = line[4:-1].split(maxsplit=1)
            name = removeprefix(name, "VERSION_").lower()
            try:
                value = int(value)
            except ValueError:
                pass
            versions[name] = value

    return versions


def get_version_from_repo(
    versions_path: str = FILE_WITH_VERSION_PATH,
) -> ClickHouseVersion:
    path_to_file = p.join(git.root, versions_path)
    versions = read_versions(path_to_file)
    versions["tweak"] = git.tweak
    return ClickHouseVersion(
        versions["major"],
        versions["minor"],
        versions["patch"],
        versions["tweak"],
        versions["revision"],
        git,
    )


def update_cmake_version(
    version: ClickHouseVersion,
    version_type: str,
    versions_path: str = FILE_WITH_VERSION_PATH,
):
    path_to_file = p.join(git.root, versions_path)
    version.with_description(version_type)
    with open(path_to_file, "w", encoding="utf-8") as f:
        f.write(VERSIONS_TEMPLATE.format_map(version.as_dict()))


def _update_changelog(repo_path, version):
    cmd = """sed \
        -e "s/[@]VERSION_STRING[@]/{version_str}/g" \
        -e "s/[@]DATE[@]/{date}/g" \
        -e "s/[@]AUTHOR[@]/clickhouse-release/g" \
        -e "s/[@]EMAIL[@]/clickhouse-release@yandex-team.ru/g" \
        < {in_path} > {changelog_path}
    """.format(
        version_str=version.get_version_string(),
        date=datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S") + " +0300",
        in_path=p.join(repo_path, CHANGELOG_IN_PATH),
        changelog_path=p.join(repo_path, CHANGELOG_PATH),
    )
    subprocess.check_call(cmd, shell=True)


def update_contributors(relative_contributors_path: str = GENERATED_CONTRIBUTORS):
    contributors = git.run("git shortlog HEAD --summary")
    contributors = sorted(
        [c.split(maxsplit=1)[-1].replace('"', r"\"") for c in contributors.split("\n")],
    )
    contributors = [f'    "{c}",' for c in contributors]
    # Check if we have shallow checkout by comparing number of lines
    contributors_path = p.abspath(p.join(git.root, relative_contributors_path))
    extra_lines = len(CONTRIBUTORS_TEMPLATE.split("\n")) - 1
    with open(contributors_path, "r", encoding="utf-8") as cfd:
        existing_contributors = len(cfd.readlines()) - extra_lines
        if len(contributors) < existing_contributors:
            logging.info(
                "Refusing to update %s, given number of contributors %s "
                "is less than existing %s",
                contributors_path,
                existing_contributors,
                len(contributors),
            )
            return

    content = CONTRIBUTORS_TEMPLATE.format("\n".join(contributors))
    with open(contributors_path, "w", encoding="utf-8") as cfd:
        cfd.write(content)


def _update_dockerfile(repo_path, version):
    version_str_for_docker = ".".join(
        [str(version.major), str(version.minor), str(version.patch), "*"]
    )
    cmd = "ls -1 {path}/docker/*/Dockerfile | xargs sed -i -r -e 's/ARG version=.+$/ARG version='{ver}'/'".format(
        path=repo_path, ver=version_str_for_docker
    )
    subprocess.check_call(cmd, shell=True)


def update_version_local(repo_path, version, version_type="testing"):
    update_contributors()
    update_cmake_version(version, version_type)
    _update_changelog(repo_path, version)
    _update_dockerfile(repo_path, version)
