import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as events from 'aws-cdk-lib/aws-events';
import * as targets from 'aws-cdk-lib/aws-events-targets';

interface BotStackProps {
  botName: string;
  botRuleName: string;
  env: any;
  handlerPath: string;
  cron: string;
}

/**
 * A construct that contains a Lambda function and a CloudWatch event rule that
 * invokes the Lambda function on a schedule.
 */
export class BotConstruct extends Construct {
  public readonly handler: lambda.Function;

  constructor(scope: Construct, id: string, props: BotStackProps) {
    super(scope, id);

    const env = props.env;
    const botName = props.botName;
    const botRuleName = props.botRuleName;
    const cron = props.cron;
    const handlerPath = props.handlerPath;

    this.handler = new lambda.Function(this, botName, {
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
      handler: handlerPath,
      memorySize: 256,
      timeout: cdk.Duration.seconds(30),
      environment: env,
    });

    new events.Rule(this, botRuleName, {
      schedule: events.Schedule.expression(cron),
      targets: [new targets.LambdaFunction(this.handler)],
    });
  }
}
