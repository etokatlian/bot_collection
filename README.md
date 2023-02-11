# Bot Collection

A collection of Python bots that run on AWS Lambda. The bots are deployed using AWS CDK. They perform some scheduled actions and send me emails with updates.

A base bot construct is defined in lambda_bot.construct.ts and implements a Python Lambda + Cloudwatch Event Rule. Custom bots can be extended from this construct.
<br/>
<br/>

- Github Bot: Sends me an email with the latest commits from the users I follow on Github.
- Movie Bot: Sends me an email with currently playing movies at my local theater.

<br/>

### To use Github Bot:

1. Create lambda/users.py and add a list of users in the following way:

```python
urls = ["https://github.com/etokatlian"]       

name_map = {"etokatlian": "Eric Tokatlian"}

```
2. Add as many users as you want to the urls list and the name_map dictionary. The name_map dictionary is used to map the github username to a name that you want to be displayed in the email.

3. Create a .env file in the root directory and add the following environment variables:

```bash
EMAIL=youremail.com
PASSWORD=yourpasswordhere
```
<br/>

### To use Movie Bot:

1. Create a .env file in the root directory and add the following environment variables:

```bash
EMAIL=youremail.com
PASSWORD=yourpasswordhere
```

<br/>

### Deploying the bots to AWS:
1. Make sure you have docker installed and are running the docker daemon. The stack uses docker to intall and package up the dependencies when deploying.

2. Run `npx cdk deploy` to deploy the bot to AWS Lambda.

3. Sit back and let the bots do their thing :)
