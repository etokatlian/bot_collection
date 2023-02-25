#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { GithubBotStack } from '../lib/github_bot.stack';
import { MovieBotStack } from '../lib/movie_bot.stack';
import { KeepWarmStack } from '../lib/keep_warm_bot.stack';

const app = new cdk.App();
new GithubBotStack(app, 'GithubBotStack', {});
new MovieBotStack(app, 'MovieBotStack', {});
new KeepWarmStack(app, 'KeepWarmStack', {});
