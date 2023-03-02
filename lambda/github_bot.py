import os
import smtplib
import time
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import asyncio
from bs4 import BeautifulSoup
import aiohttp
import requests
from users import urls, name_map


async def gather_with_concurrency(n, *tasks):
    semaphore = asyncio.Semaphore(n)

    async def sem_task(task):
        async with semaphore:
            return await task

    return await asyncio.gather(*(sem_task(task) for task in tasks))


async def get_async(url, session, results):
    async with session.get(url) as response:
        split_url = url.split("/")
        username = name_map[split_url[len(split_url) - 1]]
        obj = await response.text()
        results[username] = obj


def get_contribution_count(github_rectangle):
    val = github_rectangle[0].get_text().split(" ")[0]

    if val == "No":
        return 0
    else:
        return val


async def run():
    conn = aiohttp.TCPConnector(limit=None, ttl_dns_cache=300)
    session = aiohttp.ClientSession(connector=conn)
    results = {}

    conc_req = 40
    await gather_with_concurrency(
        conc_req, *[get_async(i, session, results) for i in urls]
    )

    output = []

    for item in results.items():
        # Convert the raw html into some beautiful soup
        soup = BeautifulSoup(item[1], "html.parser")

        # Get yesterday's date in YYYY-MM-DD format
        yesterday = datetime.now() - timedelta(1)
        yesterdays_date = datetime.strftime(yesterday, "%Y-%m-%d")

        # Get the github rectangle for yesterday
        yesterday_rect = soup.find_all("rect", {"data-date": yesterdays_date})

        # Get the number of contributions from yesterday
        yesterday_contribution_count = get_contribution_count(yesterday_rect)

        # Add to output
        output.append([item[0], yesterday_contribution_count])

    filtered_output = list(filter(lambda x: int(x[1]) > 0, output))

    date = f"{int(time.time())}"

    # this posts to GithubService API, which writes to DynamoDB
    # TODO: Add url to repo for GithubService
    for item in filtered_output:
        requests.post(
            "https://gdu7m457d3.execute-api.us-west-2.amazonaws.com/prod/checkins",
            headers={"Content-Type": "application/json"},
            json={"user": item[0], "date": date, "commits": item[1]},
        )

    # fire off email via cronjob
    generated_html = list(map(lambda x: f"<li>{x[0]} - {x[1]}</li>", filtered_output))

    joined = " ".join(generated_html)

    html_string = """\
    <html>
      <body>
      <h2>Statistics</h2>
        <ul style="display:value; list-style:none">
          {generated_html}
        </ul>
      </body>
    </html>
    """.format(
        generated_html=joined
    )

    # What to show in the email if there are no contributions
    no_results_html = """\
    <html>
      <body>
      <h2>Statistics</h2>
        <h3>No results found</h3>
      </body>
    </html>
    """

    generated_html = MIMEText(html_string, "html")

    sender_email = os.environ["EMAIL"]
    receiver_emails = [os.environ["EMAIL"]]
    password = os.environ["PASSWORD"]
    message = MIMEMultipart("alternative")
    message["Subject"] = "Daily Github Contributions"
    message["From"] = sender_email
    message["To"] = ", ".join(receiver_emails)

    if len(filtered_output) > 0:
        message.attach(generated_html)
    else:
        message.attach(MIMEText(no_results_html, "html"))

    context = ssl._create_unverified_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_emails, message.as_string())

    await session.close()


def lambda_handler(context, event):
    """
    Entrypoint for AWS Lambda
    """
    try:
        asyncio.run(run())
    except Exception as error:
        print(error)
        raise error
