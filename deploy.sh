#!/bin/bash
pip install -U -r requirements.txt
rm -fR lambda/artifacts
cp -pr lambda/src lambda/artifacts
pip install -r lambda/artifacts/requirements.txt -t lambda/artifacts
cdk deploy
