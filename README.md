# Github_bot

A python bot that takes in a list of github users and emails me every day at 9am with a list of their commits and other activity. Deploys to AWS Lambda using CDK.
<br/>
<br/>

### To use this bot

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
4. Make sure you have docker installed and are running the docker daemon. The stack uses docker to intall and package up the dependencies when deploying.

5. Run `npx cdk deploy` to deploy the bot to AWS Lambda.

6. Enjoy your daily emails!
