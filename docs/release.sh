#!/bin/bash -eux
# ./docs/release.sh [patch|minor|major]

[[ $(basename "$PWD") == docs ]] && cd ..

OLD=$(uv version --short)
NEW=$(uv version --short --bump "$1")
DATE=$(date +%Y-%m-%d)

sed -ri "/__version__ /s/[0-9.]+/$NEW/" nmdmail/__init__.py
sed -i "/^## \[Unreleased\]/a \\\n## [v$NEW] - $DATE" CHANGELOG.md
sed -i "/^\[Unreleased\]/s/$OLD/$NEW/" CHANGELOG.md
sed -i "/^\[Unreleased\]/a [v$NEW]: https://github.com/nim65s/nmdmail/compare/v$OLD...v$NEW" CHANGELOG.md

git add nmdmail/__init__.py pyproject.toml CHANGELOG.md uv.lock
git commit -m "Release v$NEW"
git tag -s "v$NEW" -m "Release v$NEW"
git push
git push --tags
