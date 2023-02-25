require('dotenv').config();
import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { BotConstruct } from './lambda_bot.construct';

export class KeepWarmStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    new BotConstruct(this, 'KeepWarmStack', {
      botName: 'KeepWarmLambda',
      botRuleName: 'KeepWarmRule',
      env: {
        URL: process.env.GGFYIURL,
      },
      handlerPath: 'keep_warm_bot.lambda_handler',
      cron: 'cron(0/5 * * * ? *)',
    });
  }
}
