from flask import Flask, Response, abort


app = Flask(__name__)

@app.route('/')
def home():
    content = """
    <html>
    <head>
        <style>
            body {
                background-color: #000;
                color: #00ff00;
                font-family: 'Courier New', Courier, monospace;
                padding: 20px;
                text-align: center;
                overflow: hidden;
            }
            .terminal {
                border: 2px solid #00ff00;
                padding: 20px;
                display: inline-block;
                text-align: left;
                max-width: 600px;
                position: relative;
                z-index: 1;
                background: rgba(0, 0, 0, 0.8);
                box-shadow: 0 0 20px #00ff00;
                animation: glitch 2s infinite;
            }
            .terminal::before, .terminal::after {
                content: '';
                position: absolute;
                top: -2px;
                left: -2px;
                right: -2px;
                bottom: -2px;
                border: 2px solid #00ff00;
                mix-blend-mode: overlay;
                animation: neon 5s linear infinite;
            }
            .terminal::after {
                filter: blur(10px);
            }
            @keyframes neon {
                0%, 100% {
                    opacity: 0.5;
                }
                50% {
                    opacity: 1;
                }
            }
            @keyframes glitch {
                0% {
                    clip: rect(42px, 9999px, 44px, 0);
                    transform: skew(0.5deg);
                }
                10% {
                    clip: rect(12px, 9999px, 14px, 0);
                    transform: skew(-0.5deg);
                }
                20% {
                    clip: rect(52px, 9999px, 54px, 0);
                    transform: skew(0.5deg);
                }
                30% {
                    clip: rect(22px, 9999px, 24px, 0);
                    transform: skew(-0.5deg);
                }
                40% {
                    clip: rect(62px, 9999px, 64px, 0);
                    transform: skew(0.5deg);
                }
                50% {
                    clip: rect(32px, 9999px, 34px, 0);
                    transform: skew(-0.5deg);
                }
                60% {
                    clip: rect(72px, 9999px, 74px, 0);
                    transform: skew(0.5deg);
                }
                70% {
                    clip: rect(42px, 9999px, 44px, 0);
                    transform: skew(-0.5deg);
                }
                80% {
                    clip: rect(82px, 9999px, 84px, 0);
                    transform: skew(0.5deg);
                }
                90% {
                    clip: rect(52px, 9999px, 54px, 0);
                    transform: skew(-0.5deg);
                }
                100% {
                    clip: rect(12px, 9999px, 14px, 0);
                    transform: skew(0.5deg);
                }
            }
            .typing {
                overflow: hidden;
                border-right: .15em solid #00ff00;
                white-space: nowrap;
                margin: 0 auto;
                letter-spacing: .15em;
                animation:
                    typing 3.5s steps(40, end),
                    blink-caret .75s step-end infinite;
            }
            @keyframes typing {
                from { width: 0 }
                to { width: 100% }
            }
            @keyframes blink-caret {
                from, to { border-color: transparent }
                50% { border-color: #00ff00 }
            }
        </style>
    </head>
    <body>
        <div class="terminal">
            <p class="typing"><strong></strong></p>
            <p>-----------------------------</p>
            <p>Even chatgpt doesn't know.</p>
        </div>
    </body>
    </html>
    """
    return content

@app.route('/robots.txt')
def robots_txt():
    content = """User-agent: *
Disallow: /arctf/*

#Hint: it's too easy
"""
    return Response(content, mimetype='text/plain') 


@app.route('/arctf/')
def arctf_forbidden():
    abort(403)

@app.route('/arctf/flag.txt')
def arctf_flag():
    return "arctf{s3arch-3ng1ne}"