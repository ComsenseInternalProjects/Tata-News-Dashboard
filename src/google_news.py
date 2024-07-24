import http.client
import json
import sqlite3
from datetime import datetime

# Function to fetch competitors data
def fetch_competitors_data(botid, taskid):
    conn = http.client.HTTPSConnection("api.browse.ai")
    headers = {
        'Authorization': "Bearer bcc2c820-b0a5-44a5-bedc-51ccc6eaa7f8:691bdabe-7017-4ab7-bb4e-982795e45a65"
    }
    url = f"/v2/robots/{botid}/tasks/{taskid}"
    conn.request("GET", url, headers=headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")
    return json.loads(data)

# Function to extract relevant data from the JSON response and generate unique code
def extract_competitors_articles(data):
    current_date = datetime.now().strftime("%Y%m%d")
    articles = data['result']['capturedLists']['Ashok Leyland']
    return [(f"{article.get('Blog Title')}_{current_date}", 
             article.get('Blog Title'), 
             article.get('Blog URL'), 
             datetime.now()) for article in articles]

# Function to fetch data from the API
def fetch_news(botid, taskid):
    conn = http.client.HTTPSConnection("api.browse.ai")
    headers = {
        'Authorization': "Bearer bcc2c820-b0a5-44a5-bedc-51ccc6eaa7f8:691bdabe-7017-4ab7-bb4e-982795e45a65"
    }
    url = f"/v2/robots/{botid}/tasks/{taskid}"
    conn.request("GET", url, headers=headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")
    return json.loads(data)

def bulk_runs(robotId, bulkRunId):
    conn = http.client.HTTPSConnection("api.browse.ai")
    headers = {'Authorization': "Bearer be4fc9af-a23c-4f94-b3b9-c985b5571130:58c92ae2-143b-4cfa-a0c9-0b1a678847a0"}

    all_data = {
        "results": []
    }
    
    for page in range(1, 11):
        conn.request("GET", f"/v2/robots/{robotId}/bulk-runs/{bulkRunId}?page={page}", headers=headers)
        res = conn.getresponse()
        data = res.read().decode("utf-8")
        page_data = json.loads(data)
        
        if isinstance(page_data, list):
            all_data["results"].extend(page_data)
        else:
            all_data["results"].append(page_data)
    
    all_data["results"] = [item for item in all_data["results"] if item.get('statusCode') != 404]
    
    return all_data

# Function to extract relevant data from the JSON response and generate unique code
def extract_articles(data):
    current_date = datetime.now().strftime("%Y%m%d")
    all_articles = []

    for item in data["results"]:
        try:
            robot_tasks = item['result']['robotTasks']['items']
            for task in robot_tasks:
                articles = task['capturedLists']['Articles']
                for article in articles:
                    all_articles.append((
                        f"{article.get('Article Title')}_{current_date}",
                        article.get('Article Title'),
                        article.get('News Link'),
                        article.get('Source Image'),
                        article.get('When Posted'),
                        article.get('Writer'),
                        datetime.now()
                    ))
        except (KeyError, TypeError, IndexError):
            continue

    return all_articles

# Function to create a SQLite database and insert data
def save_to_database(articles, table_name):
    conn = sqlite3.connect('src/tata_news.db')
    cursor = conn.cursor()
    if table_name == 'competitors':
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                unique_code TEXT UNIQUE,
                title TEXT,
                link TEXT,
                last_updated_date TIMESTAMP
            )
        ''')
        cursor.executemany(f'''
            INSERT OR IGNORE INTO {table_name} (unique_code, title, link, last_updated_date) 
            VALUES (?, ?, ?, ?)
        ''', [(a[0], a[1], a[2], a[6]) for a in articles])
    else:
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                unique_code TEXT UNIQUE,
                title TEXT,
                link TEXT,
                source_image TEXT,
                when_posted TEXT,
                writer TEXT,
                last_updated_date TIMESTAMP
            )
        ''')
        cursor.executemany(f'''
            INSERT OR IGNORE INTO {table_name} (unique_code, title, link, source_image, when_posted, writer, last_updated_date) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', articles)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    # competitors_data = fetch_competitors_data(botid="89e62808-27ac-4fca-8f29-c3e0f3131206", taskid="daa470b9-00c8-4aea-8c8d-9129ad45bbe3")
    # print(competitors_data)
    # competitors_articles = extract_competitors_articles(competitors_data)
    # save_to_database(competitors_articles, 'competitors')

    # print(competitors_articles, "Data saved to database successfully!")
    # fetch_news(botid="89e62808-27ac-4fca-8f29-c3e0f3131206", taskid="daa470b9-00c8-4aea-8c8d-9129ad45bbe3")
    news_data = bulk_runs(robotId="77f195c0-294e-48f9-9962-1ceac580a9f7", bulkRunId="a9dd4fd4-18d2-414a-b40e-3a85a0f854fb")
    print(news_data)
    print("**************************************************************************")
    articles=extract_articles(news_data)
    print(articles)
    print("**************************************************************************")
    save_to_database(articles, "bulk_news")


