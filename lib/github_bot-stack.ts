require('dotenv').config();
import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as events from 'aws-cdk-lib/aws-events';
import * as targets from 'aws-cdk-lib/aws-events-targets';

export class GithubBotStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const GithubBotLambda = new lambda.Function(this, 'GithubBotLambda', {
      code: lambda.Code.fromAsset('lambda', {
        bundling: {
          image: lambda.Runtime.PYTHON_3_9.bundlingImage,
          command: [
            'bash',
            '-c',
            ['pip install -r requirements.txt -t /asset-output', 'cp -au . /asset-output'].join(
              ' && '
            ),
          ],
        },
      }),
      runtime: lambda.Runtime.PYTHON_3_9,
      handler: 'github_bot.lambda_handler',
      memorySize: 256,
      timeout: cdk.Duration.seconds(30),
      environment: {
        EMAIL: process.env.EMAIL || '',
        PASSWORD: process.env.PASSWORD || '',
      },
    });

    new events.Rule(this, 'GithubBotRule', {
      schedule: events.Schedule.cron({ hour: '16', minute: '0' }),
      targets: [new targets.LambdaFunction(GithubBotLambda)],
    });
  }
}
