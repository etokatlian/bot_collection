import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from bs4 import BeautifulSoup


html = requests.get(
    "https://www.amctheatres.com/movie-theatres/phoenix/amc-ahwatukee-24")
soup = BeautifulSoup(html.text, "html.parser")
movie_titles = soup.find_all("div", class_="Slide")
all_images = list(map(lambda x: x.contents[0].contents[0], movie_titles))
all_links = list(map(
    lambda x: f"https://www.amctheatres.com{x.contents[0]['href']}", movie_titles))
all_children = list(
    map(lambda x: x.contents[1].contents[0].contents[0].get_text(), movie_titles))
filtered_movies = list(dict.fromkeys(all_children))
filtered_images = list(dict.fromkeys(all_images))
filtered_links = list(dict.fromkeys(all_links))
movie_links = []
for i in range(len(filtered_movies)):
    movie_links.append({
        'name': filtered_movies[i],
        'link': filtered_links[i],
        'image': filtered_images[i]
    })
generated_html = list(
    map(lambda x: f"<li><a href='{x['link']}'>{x['image']}</a></li>", movie_links))
joined = " ".join(generated_html)

html_string = """\
<html>
  <body>
  <h2>Here is what is in theatres this week:</h2>
    <ul style="display:value;">
      {generated_html}
    </ul>
  </body>
</html>
""".format(generated_html=joined)

generated_html = MIMEText(html_string, "html")

sender_email = os.environ['EMAIL']
receiver_emails = [os.environ['EMAIL'], "tsmith93036@gmail.com"]
password = os.environ['PASSWORD']
message = MIMEMultipart("alternative")
message["Subject"] = "This weeks movie briefing"
message["From"] = sender_email
message["To"] = ", ".join(receiver_emails)
message.attach(generated_html)

context = ssl._create_unverified_context()


def send_email():
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_emails, message.as_string()
        )


def lambda_handler(context, event):
    """
    Entrypoint for AWS Lambda
    """
    try:
        send_email()
    except Exception as error:
        print(error)
        raise error
