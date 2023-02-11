require('dotenv').config();
import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { BotConstruct } from './lambda_bot.construct';

export class GithubBotStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    new BotConstruct(this, 'GithubBotStack', {
      botName: 'GithubBotLambda',
      botRuleName: 'GithubBotRule',
      env: {
        EMAIL: process.env.EMAIL || '',
        PASSWORD: process.env.PASSWORD || '',
      },
      handlerPath: 'github_bot.lambda_handler',
      cron: 'cron(0 16 ? * * *)',
    });
  }
}
