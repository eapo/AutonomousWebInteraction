functions = [
    {
        "name": "open_website",
        "description": "Open a website and continute the flow",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "A URL for example https://xxx.com",
                },
            },
            "required": ["url"],
            "optional": [],
        },
    },
    {
        "name": "click",
        "description": "Click any button on a website and returns the new HTML",
        "parameters": {
            "type": "object",
            "properties": {
                "html": {
                    "type": "string",
                    "description": "A HTML",
                },
                "button": {
                    "type": "string",
                    "description": "A text description of a button on the html page",
                },
            },
            "required": ["html", "button"],
            "optional": [],
        },
    },
]
