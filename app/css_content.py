css_content = """
    body {
        font-family: 'Helvetica', Arial, sans-serif;
        margin: 40px;
        background-color: #f9f9f9;
        color: #333;
    }
    h2 {
        color: #f7ed2f;
    }
    h1 {
        color: #f5f516;
        text-align: center;
        border-bottom: 2px solid #333;
        padding-bottom: 10px;
    }
    p {
        font-size: 14px;
        line-height: 1.5;
        margin: 10px 0;
    }
    .description {
        color: 66cdaa
    }
    .label {
        font-weight: bold;
        color: #32a871;
    }
    .value {
        color: #333;
        padding-left: 20px;
    }
    .section {
        margin-bottom: 20px;
    }
    .section-title {
        font-size: 16px;
        font-weight: bold;
        margin-bottom: 10px;
        color: #555;
    }
    .photo {
        text-align: center;
        margin: 20px 0;
    }
    img {
        max-width: 100%;
        height: auto;
        border: 1px solid #ddd;
        padding: 5px;
        background-color: #fff;
    }
    table {
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 20px;
    }
    th, td {
        padding: 8px;
        text-align: left;
        border-bottom: 1px solid #ddd;
    }
    th {
        background-color: #f2f2f2;
    }
    .header, .footer {
        width: 100%;
        text-align: center;
        position: fixed;
    }
    .header {
        top: 0px;
    }
    .footer {
        bottom: 0px;
        font-size: 12px;
        color: #777;
    }
    .page-number:before {
        content: counter(page);
    }
    """