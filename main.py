import requests
import json

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'authorization': 'Bearer ADAAQQAzAEYANAAyADgANQAtADYARAA3AEQALQA0ADQARQA3AC0AQgAwADgAQQAtADEAMwA1ADMAOQBEADUAMwBEADEAMgA3ADoAQQBHAEkAQQBhAFEAQgB1AEEASABRAEEAWQBRAEIAeQBBAEcAOAA9ADoAMQA2ADgANgAxADMAMQAxADkAMwAyADAAOQ==',
    'content-type': 'application/json',
    'dnt': '1',
    'origin': 'https://viewer.inqurio.id',
    'priority': 'u=1, i',
    'referer': 'https://viewer.inqurio.id/U2FsdGVkX1xMl3Jkm3YBsIWfJoYj14MS6KwePosI7SWPor21Ld5ZxlkvrtjkXeS8EYy5bTTG0SPor21Ldwq6pPor21LdP6kQj9YbZO6twrbO1zEO0fu3Por21Ld3jMLUS3NjuOas4qqqTY8TmLFZcMvI9Vh4bNTcqvVk9ihg6T4nEPyr3XDn9EPfBcPor21LdneaB5Kl60qgak2SCQMl32/ADkANwAyAEYANgBBADEAQQAtAEYANgA4ADgALQA0ADcAOQA3AC0AOABFAEMAQQAtADgANQA5AEYAMQBFAEYANQBDAEEAMgBFADoAQQBIAE0AQQBaAEEAQgBwAEEARgA4AEEAZABBAEIAbABBAEcAMABBAGMAQQBCAGYAQQBHAEUAQQBZAHcAQgBqADoAMQA3ADIANgA0ADcAMQA4ADcAOAAwADAANw==',
    'sec-ch-ua': '"Not;A=Brand";v="24", "Chromium";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
}

json_data = {
    'dashboard_id': 'dashboard:f0d3d100-0c04-11ee-acea-71edaf218382',
    'widget_id': 'visualization:bf13f1c0-0c01-11ee-acea-71edaf218382',
    'start': '',
    'end': '',
    'filter': [
        {
            'field': 'province.keyword',
            'operator': 'is',
            'keywords': [
                'DKI JAKARTA',
            ],
        },
    ],
}

response = requests.post(
    'https://viewer.inqurio.id/inqurio-api/sdi-dashboard/api/v1/workspace/widget',
    headers=headers,
    json=json_data,
)

print(json.dumps(response.json(), indent=2))