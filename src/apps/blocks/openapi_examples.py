BLOCK_CREATE_SCHEMA_EXAMPLES = {
    'Text block': {
        'value': {
            'message_text': 'string',
            'type': 'text_block',
        },
    },
    'Image block': {
        'value': {
            'image_path': 'string',
            'type': 'image_block',
        },
    },
    'Question block': {
        'value': {
            'message_text': 'string',
            'answer_type': 'any',
            'type': 'question_block',
        },
    },
    'Email block': {
        'value': {
            'subject': 'string',
            'text': 'string',
            'recipient_email': 'string',
            'type': 'email_block',
        },
    },
    'CSV block': {
        'value': {
            'file_path': 'string',
            'data': {
                'additionalProp1': 'string',
                'additionalProp2': 0,
            },
            'type': 'csv_block',
        },
    },
    'Excel block': {
        'value': {
            'file_path': 'string',
            'data': {
                'additionalProp1': 'string',
                'additionalProp2': 0,
            },
            'type': 'excel_block',
        },
    },
    'API block': {
        'value': {
            'url': 'https://example.com/api',
            'http_method': 'POST',
            'headers': {
                'additionalProp1': 'string',
                'additionalProp2': 'string',
                'additionalProp3': 'string',
            },
            'body': {
                'additionalProp1': 'string',
                'additionalProp2': 0,
            },
            'type': 'api_block',
        },
    },
}

BLOCK_UPDATE_SCHEMA_EXAMPLES = BLOCK_CREATE_SCHEMA_EXAMPLES
