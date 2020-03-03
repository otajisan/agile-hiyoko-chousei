import json
from aws_cdk import (
    core,
    aws_lambda,
    aws_events,
    aws_events_targets,
    aws_ssm,
)


class AgileHiyokoChouseiStack(core.Stack):

    DEBUG = False

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Slack Webhook Url - from ssm
        slack_webhook_url = aws_ssm.StringParameter.value_from_lookup(self, 'AGILE_HIYOKO_GENERAL_SLACK_WEBHOOK_URL')

        # Lambda
        lambda_function = aws_lambda.Function(
                self, 'agile-hiyoko-chousei',
                function_name = 'agile-hiyoko-chousei',
                runtime = aws_lambda.Runtime.PYTHON_3_8,
                handler = 'chousei.lambda_handler',
                code = aws_lambda.AssetCode(path='./lambda/artifacts/'),
                timeout = core.Duration.seconds(10)
        )

        lambda_function.add_environment('SLACK_WEBHOOK_URL', slack_webhook_url)

        # crontab settings
        cron=aws_events.Schedule.cron(
            minute='00',
            hour='16',
            day='01',
            month='02/04/06/08/10/12',
            year='*',
        )

        if self.DEBUG:
            cron = aws_events.Schedule.cron(
                minute='*',
                hour='*',
                day='*',
                month='*',
                year='*',
            )

        # CloudWatchEvent
        rule = aws_events.Rule(
            self, 'agile-hiyoko-chousei-rule',
            # MEMO: 開催月の1日、JST 07:00
            schedule=cron,
        )

        rule.add_target(aws_events_targets.LambdaFunction(lambda_function))
