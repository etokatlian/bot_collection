require('dotenv').config();
import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { BotConstruct } from './lambda_bot.construct';

export class MovieBotStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    new BotConstruct(this, 'MovieBotStack', {
      botName: 'MovieBotLambda',
      botRuleName: 'MovieBotRule',
      env: {
        EMAIL: process.env.EMAIL || '',
        PASSWORD: process.env.PASSWORD || '',
      },
      handlerPath: 'movie_bot.lambda_handler',
      cron: 'cron(0 19 ? * FRI *)',
    });
  }
}
