# Github_bot

A python bot that takes in a list of github users and emails me every day at 9am with a list of their commits and other activity. Deploys to AWS Lambda using CDK.
<br/>
<br/>

### To use this bot

1. Create lambda/users.py and add the following code:

```python
urls = ["https://github.com/etokatlian"]       

name_map = {"etokatlian": "Eric Tokatlian"}

```
2. Add as many users as you want to the urls list and the name_map dictionary. The name_map dictionary is used to map the github username to a name that you want to be displayed in the email.

3. Next, on lines 101, 102, and 103 of lambda/github_bot.py, add your email and password. If you're using gmail, you'll need to enable less secure apps in your account settings.

4. Run `npx cdk deploy` to deploy the bot to AWS Lambda.
