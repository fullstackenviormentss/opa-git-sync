#!/usr/bin/env bash

set -ex

make
make tag
make push
