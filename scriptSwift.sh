#!/bin/bash
# Marianne Linhares Monteiro <mariannelinharesm@gmail.com>
# Ziping a directory and moving it to openstack swift

cd path_to_your_folder
source your_project-openrc.sh
CONTAINER="Your Container Name"

FOLDER="name of your folder"
zip -r "${FOLDER}" "${FOLDER}"
TARGET="${FOLDER}.zip"

swift upload $CONTAINER $TARGET

