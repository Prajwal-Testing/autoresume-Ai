"""CSS and styling utilities."""


def get_css_styles() -> str:
    return """
    <style>
        .main { max-width: 1400px; }
        .metric-card {
            background-color: #f0f2f6;
            padding: 20px;
            border-radius: 10px;
            border-left: 5px solid #1f77b4;
        }
        .agent-log {
            font-family: 'Courier New', monospace;
            background-color: #1e1e1e;
            color: #00ff88;
            padding: 12px;
            border-radius: 5px;
            font-size: 12px;
            max-height: 420px;
            overflow-y: auto;
        }
        .ats-score {
            font-size: 48px;
            font-weight: bold;
            color: #1f77b4;
            text-align: center;
        }
        .diff-viewer {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }
        .before-text {
            background-color: #ffebee;
            padding: 15px;
            border-radius: 5px;
            border: 1px solid #ef5350;
            max-height: 500px;
            overflow-y: auto;
        }
        .after-text {
            background-color: #e8f5e9;
            padding: 15px;
            border-radius: 5px;
            border: 1px solid #66bb6a;
            max-height: 500px;
            overflow-y: auto;
        }
        .header-brand {
            text-align: center;
            padding: 30px 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 10px;
            margin-bottom: 30px;
        }
        .footer-brand {
            text-align: center;
            padding: 20px;
            background-color: #f5f5f5;
            border-top: 1px solid #ddd;
            margin-top: 50px;
            font-size: 12px;
            color: #666;
        }
    </style>
    """


def get_brand_footer() -> str:
    return """
    <div class="footer-brand">
        <p><strong>AutoThink AI Career Strategist</strong></p>
        <p>Built by Prajwal Kedari</p>
        <p>
            <a href="https://github.com/prajwalkedari" target="_blank">GitHub</a> |
            <a href="https://www.linkedin.com/in/prajwalkedari/" target="_blank">LinkedIn</a> |
            <a href="https://prajwalkedari.vercel.app/" target="_blank">Portfolio</a>
        </p>
        <p style="font-size: 11px; margin-top: 10px; color: #999;">
            Powered by Gemini API &amp; LangChain
        </p>
    </div>
    """
