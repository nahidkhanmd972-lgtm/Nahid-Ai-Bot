<?xml version="1.0" encoding="UTF-8"?>

<telegram_bot>

    <bot>
        <name>PROBASHI AI</name>
        <version>1.0</version>
        <language>bn</language>
        <description>
            Bangladeshi expatriates support and AI assistant
        </description>
    </bot>

    <welcome>
        <message>
            হ্যালো! 👋
            
            আমি PROBASHI AI 🤖
            আপনার যেকোনো প্রশ্নের উত্তর দিতে প্রস্তুত।

            নিচের অপশনগুলো ব্যবহার করুন অথবা সরাসরি আমাকে প্রশ্ন করুন।
        </message>
    </welcome>

    <features>

        <feature id="ai">
            <name>🤖 AI Assistant</name>
            <status>active</status>
            <description>AI দিয়ে প্রশ্নের উত্তর</description>
        </feature>

        <feature id="government">
            <name>🏛️ সরকারি সেবা</name>
            <status>active</status>
            <description>বাংলাদেশের গুরুত্বপূর্ণ সরকারি ওয়েবসাইট</description>
        </feature>

        <feature id="passport">
            <name>🛂 Passport Service</name>
            <status>active</status>
            <description>ই-পাসপোর্ট ও প্রয়োজনীয় তথ্য</description>
        </feature>

        <feature id="video_downloader">
            <name>🎬 Video Downloader</name>
            <status>coming_soon</status>
            <description>অনুমোদিত সোর্সের ভিডিও প্রসেসিং</description>
        </feature>

        <feature id="youtube_planner">
            <name>📹 YouTube Planner</name>
            <status>coming_soon</status>
            <description>ভিডিও আইডিয়া, স্ক্রিপ্ট ও AI prompt</description>
        </feature>

        <feature id="admin">
            <name>💬 Admin Support</name>
            <status>active</status>
            <description>অ্যাডমিনের সাথে যোগাযোগ</description>
        </feature>

    </features>

    <government_services>

        <service>
            <name>ই-পাসপোর্ট</name>
            <url>https://www.epassport.gov.bd/</url>
        </service>

        <service>
            <name>NID Services</name>
            <url>https://services.nidw.gov.bd/</url>
        </service>

        <service>
            <name>Bangladesh National Portal</name>
            <url>https://bangladesh.gov.bd/</url>
        </service>

        <service>
            <name>Birth Registration</name>
            <url>https://bdris.gov.bd/</url>
        </service>

    </government_services>

    <buttons>

        <button id="ai">
            <text>🤖 AI Assistant</text>
        </button>

        <button id="government">
            <text>🏛️ সরকারি সেবা</text>
        </button>

        <button id="passport">
            <text>🛂 Passport</text>
        </button>

        <button id="video">
            <text>🎬 Video Downloader</text>
        </button>

        <button id="youtube">
            <text>📹 YouTube Planner</text>
        </button>

        <button id="admin">
            <text>💬 Admin Support</text>
        </button>

    </buttons>

</telegram_bot>