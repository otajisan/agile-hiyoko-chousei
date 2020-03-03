#!/usr/bin/env python3

from aws_cdk import core

from agile_hiyoko_chousei.agile_hiyoko_chousei_stack import AgileHiyokoChouseiStack


app = core.App()
AgileHiyokoChouseiStack(app, "agile-hiyoko-chousei", env={
    'account': 'xxx',
    'region': 'ap-northeast-1',
})

app.synth()
