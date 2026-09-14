/**
 * VERITAS AI — Supercharged Multimodal Fact-Checking Controller
 * Includes: Speech-to-Text Mic, Tesseract OCR, Heatmap, Model Battle,
 * Fact-Check Search, Certificate Export, and Chart.js Analytics.
 */

document.addEventListener("DOMContentLoaded", () => {
    // DOM Elements - Core
    const newsInput = document.getElementById("newsInput");
    const newsUrlInput = document.getElementById("newsUrlInput");
    const analyzeBtn = document.getElementById("analyzeBtn");
    const clearBtn = document.getElementById("clearBtn");
    const wordCountSpan = document.getElementById("wordCount");
    const charCountSpan = document.getElementById("charCount");
    const scannerOverlay = document.getElementById("scannerOverlay");
    const scanStatusText = document.getElementById("scanStatusText");
    const resultSection = document.getElementById("resultSection");
    const resultCard = document.getElementById("resultCard");

    // Greeting Elements
    const greetingIcon = document.getElementById("greetingIcon");
    const greetingTitle = document.getElementById("greetingTitle");
    const greetingSubtitle = document.getElementById("greetingSubtitle");
    const liveClock = document.getElementById("liveClock");
    const voiceGreetingBtn = document.getElementById("voiceGreetingBtn");
    const voiceBtnText = document.getElementById("voiceBtnText");
    const voiceWave = document.getElementById("voiceWave");

    // Verdict Elements
    const verdictBanner = document.getElementById("verdictBanner");
    const verdictIcon = document.getElementById("verdictIcon");
    const verdictPill = document.getElementById("verdictPill");
    const verdictHeadline = document.getElementById("verdictHeadline");
    const verdictDescription = document.getElementById("verdictDescription");
    const resultModelTag = document.getElementById("resultModelTag");
    const confidenceValue = document.getElementById("confidenceValue");
    const gaugeFill = document.getElementById("gaugeFill");

    // Probability & Diagnostics
    const realProgress = document.getElementById("realProgress");
    const fakeProgress = document.getElementById("fakeProgress");
    const realProbText = document.getElementById("realProbText");
    const fakeProbText = document.getElementById("fakeProbText");
    const latencyPill = document.getElementById("latencyPill");
    const citationPill = document.getElementById("citationPill");
    const toneValue = document.getElementById("toneValue");
    const capsValue = document.getElementById("capsValue");
    const punctValue = document.getElementById("punctValue");
    const citationsValue = document.getElementById("citationsValue");
    const keywordsList = document.getElementById("keywordsList");

    // Navigation & Modals
    const langEnBtn = document.getElementById("langEnBtn");
    const langHiBtn = document.getElementById("langHiBtn");
    const tabTextBtn = document.getElementById("tabTextBtn");
    const tabUrlBtn = document.getElementById("tabUrlBtn");
    const tabOcrBtn = document.getElementById("tabOcrBtn");
    const textPanel = document.getElementById("textPanel");
    const urlPanel = document.getElementById("urlPanel");
    const ocrPanel = document.getElementById("ocrPanel");
    const themeToggleBtn = document.getElementById("themeToggleBtn");
    const historyToggleBtn = document.getElementById("historyToggleBtn");
    const historyDrawer = document.getElementById("historyDrawer");
    const drawerOverlay = document.getElementById("drawerOverlay");
    const drawerCloseBtn = document.getElementById("drawerCloseBtn");
    const historyList = document.getElementById("historyList");
    const historyCount = document.getElementById("historyCount");
    const clearHistoryBtn = document.getElementById("clearHistoryBtn");
    const infoToggleBtn = document.getElementById("infoToggleBtn");
    const infoModal = document.getElementById("infoModal");
    const modalCloseBtn = document.getElementById("modalCloseBtn");
    const copyResultBtn = document.getElementById("copyResultBtn");
    const reScanBtn = document.getElementById("reScanBtn");
    const modelBadgeText = document.getElementById("modelBadgeText");

    // Feature 1: Mic Speech-to-Text
    const micDictateBtn = document.getElementById("micDictateBtn");
    const micIcon = document.getElementById("micIcon");
    const micStatusBar = document.getElementById("micStatusBar");
    const micStatusText = document.getElementById("micStatusText");

    // Feature 2: OCR Elements
    const ocrDropzone = document.getElementById("ocrDropzone");
    const ocrFileInput = document.getElementById("ocrFileInput");
    const ocrPromptContent = document.getElementById("ocrPromptContent");
    const ocrPreviewContainer = document.getElementById("ocrPreviewContainer");
    const ocrPreviewImage = document.getElementById("ocrPreviewImage");
    const ocrProgressBox = document.getElementById("ocrProgressBox");
    const ocrProgressLabel = document.getElementById("ocrProgressLabel");
    const ocrPercent = document.getElementById("ocrPercent");
    const ocrProgressFill = document.getElementById("ocrProgressFill");
    const removeOcrImgBtn = document.getElementById("removeOcrImgBtn");

    // Feature 3: In-Text Heatmap
    const heatmapBody = document.getElementById("heatmapBody");

    // Feature 5: Battle Card Elements
    const robertaVerdictVal = document.getElementById("robertaVerdictVal");
    const robertaLatencyVal = document.getElementById("robertaLatencyVal");
    const baselineVerdictVal = document.getElementById("baselineVerdictVal");
    const baselineLatencyVal = document.getElementById("baselineLatencyVal");

    // Feature 6: Fact-Check Reference Card
    const factCheckList = document.getElementById("factCheckList");

    // Web Corroboration Elements
    const webCorroborationPill = document.getElementById("webCorroborationPill");
    const webCorrobValue = document.getElementById("webCorrobValue");
    const webCorroborationBox = document.getElementById("webCorroborationBox");
    const webCorrobList = document.getElementById("webCorrobList");
    const webCorrobBadge = document.getElementById("webCorrobBadge");

    // Feature 4: Certificate Modal Elements
    const downloadCertBtn = document.getElementById("downloadCertBtn");
    const certificateModal = document.getElementById("certificateModal");
    const certCloseBtn = document.getElementById("certCloseBtn");
    const certificateCanvas = document.getElementById("certificateCanvas");
    const certId = document.getElementById("certId");
    const certHeadline = document.getElementById("certHeadline");
    const certVerdictPill = document.getElementById("certVerdictPill");
    const certConfidenceVal = document.getElementById("certConfidenceVal");
    const certToneVal = document.getElementById("certToneVal");
    const certDateVal = document.getElementById("certDateVal");
    const saveCertPngBtn = document.getElementById("saveCertPngBtn");
    const printCertBtn = document.getElementById("printCertBtn");

    // Feature 7: Analytics Elements
    const analyticsToggleBtn = document.getElementById("analyticsToggleBtn");
    const analyticsModal = document.getElementById("analyticsModal");
    const analyticsCloseBtn = document.getElementById("analyticsCloseBtn");
    const kpiTotalScans = document.getElementById("kpiTotalScans");
    const kpiRealRate = document.getElementById("kpiRealRate");
    const kpiFakeRate = document.getElementById("kpiFakeRate");
    const kpiAvgLatency = document.getElementById("kpiAvgLatency");
    let distributionChart = null;
    let keywordsChart = null;

    let currentTab = "text";
    let currentLang = localStorage.getItem("veritas_lang") || "en";
    let sampleData = null;
    let lastAnalysisData = null;
    let isSpeaking = false;
    let isDictating = false;
    let speechRecognition = null;

    // --------------------------------------------------------------------------
    // Bilingual Translation Dictionary (English & Hindi)
    // --------------------------------------------------------------------------
    const translations = {
        en: {
            brand_tag: "Neural News Intelligence",
            model_badge: "RoBERTa Transformer Model",
            hero_badge: "Multimodal RoBERTa Deep Learning Intelligence",
            hero_title_1: "Detect Misinformation with",
            hero_title_2: "Neural Precision",
            hero_subtitle: "Inspect text articles, viral screenshots, news links, or voice dictations. Our deep RoBERTa transformer evaluates sensationalism, citation credibility, and deceitful patterns in real time.",
            listen_brief_btn: "Speak Greeting & Brief",
            tab_text: "Article Text",
            tab_url: "News URL Extractor",
            tab_ocr: "Screenshot & Image OCR",
            ocr_title: "Upload Viral Screenshot or Image",
            ocr_desc: "Drag & drop WhatsApp forwards, tweets, or headlines (PNG, JPG, WebP) or click to browse.",
            quick_samples: "Quick Samples:",
            sample_real_1: "Real: Space Research",
            sample_real_2: "Real: Fed Economy",
            sample_fake_1: "Fake: Secret Microchips",
            sample_fake_2: "Fake: Miracle Cure",
            input_placeholder: "Paste article headline or body text here for deep credibility scan (e.g. 'NASA discovers new exoplanet atmosphere...' or 'SHOCKING: Secret government conspiracy revealed...')",
            url_placeholder: "https://example.com/news/article-headline-2026",
            url_hint: "We will scrape the article title and text content on the server and evaluate its credibility automatically.",
            clear_btn: "Clear",
            scan_btn: "Scan Credibility",
            prob_title: "Class Probability Distribution",
            heatmap_title: "Interactive In-Text Credibility Heatmap",
            battle_title: "Dual-Model Intelligence Comparison (Battle Mode)",
            factcheck_title: "Cross-Referenced Fact-Check Database",
            tone_title: "Sentiment & Tone",
            caps_title: "Capitalization Ratio",
            punct_title: "Sensational Punctuation",
            citations_title: "Source Citations",
            keywords_header: "Flagged Sensationalist / Clickbait Keywords:",
            copy_report: "Copy Analysis Report",
            scan_another: "Scan Another Article",
            download_cert: "Download Fact-Check Certificate (PDF/PNG)",
            nav_analytics: "Analytics",
            analytics_title: "Session Analytics & Credibility Intelligence",
            kpi_total: "Total Articles Scanned",
            kpi_real: "Verified Credible Ratio",
            kpi_fake: "Misinformation Ratio",
            kpi_speed: "Avg Inference Speed",
            chart_pie_title: "Class Distribution (Real vs Fake)",
            chart_bar_title: "Top Detected Clickbait Keywords",
            cert_modal_title: "Veritas AI Credibility Certificate",
            download_png: "Download Certificate (High-Res PNG)",
            print_cert: "Print / Save as PDF",
            edu_badge: "Fact-Checking Academy",
            edu_title_1: "Understanding",
            edu_title_2: "Fake News vs Real News",
            edu_subtitle: "Discover how misinformation spreads, how to identify deceitful patterns, and how our neural RoBERTa model uncovers truth.",
            real_news_title: "Anatomy of Real News",
            real_news_tag: "Credible & Verified",
            real_point1_t: "Named Sources & Attribution:",
            real_point1_d: "Cites specific researchers, institutional spokespersons, and peer-reviewed journals.",
            real_point2_t: "Objective, Non-Sensational Tone:",
            real_point2_d: "Uses neutral phrasing without excessive capitalization, exclamation marks, or manufactured rage.",
            real_point3_t: "Verifiable Data & Corrections:",
            real_point3_d: "Published by accountable news outlets with editorial standards and retraction transparency.",
            fake_news_title: "Anatomy of Fake News",
            fake_news_tag: "Misleading & Fabricated",
            fake_point1_t: "Clickbait & Panic Framing:",
            fake_point1_d: "Uses urgent triggers like 'SHOCKING!', 'THEY DONT WANT YOU TO KNOW', and all-caps shouting.",
            fake_point2_t: "Unverified Miracle / Conspiracy Claims:",
            fake_point2_d: "Makes extraordinary scientific or political claims without peer review or official records.",
            fake_point3_t: "Manipulative Call-to-Action:",
            fake_point3_d: "Urges readers to 'Share before it gets deleted!' to exploit emotional algorithmic engagement.",
            how_model_title: "How This AI Model Operates",
            how_model_subtitle: "A multi-layered transformer and lexical inspection pipeline.",
            step1_title: "Deep Tokenization",
            step1_desc: "Input text is mapped into contextual subword token representations with attention masks.",
            step2_title: "RoBERTa Attention Heads",
            step2_desc: "12 bidirectional transformer layers evaluate syntax, narrative cohesion, and deceptive framing.",
            step3_title: "Explainability Radar",
            step3_desc: "Sensationalist keywords, emotional tone, and attribution density are extracted for transparent verdicts.",
            feat1_title: "RoBERTa Attention",
            feat1_desc: "Pretrained contextual embeddings capture deep semantic nuances and deceptive phrasing that simple keyword filters miss.",
            feat2_title: "Clickbait & Tone Radar",
            feat2_desc: "Lexical and sensationalist heuristic checks flag alarmist rhetoric, shouting caps, and manipulative call-to-actions.",
            feat3_title: "Sub-100ms Inference",
            feat3_desc: "Optimized PyTorch pipelines deliver lightning-fast verification for single headlines, long articles, or live URLs.",
            drawer_history_title: "Analysis History",
            clear_history: "Clear History",
            empty_history: "No scans recorded in this session yet.",
            info_title: "Model Architecture & Training",
            gauge_confidence: "Confidence",
            greetings: {
                morning: { title: "Good Morning! Welcome ☀️", sub: "Ready to inspect and verify today's headlines?", speechTime: "Good morning! Welcome to Veritas AI." },
                afternoon: { title: "Good Afternoon! Welcome 🌤️", sub: "Keep misinformation at bay with real-time AI scans.", speechTime: "Good afternoon! Welcome to Veritas AI." },
                evening: { title: "Good Evening! Welcome 🌆", sub: "Reviewing viral news? Let's verify the facts together.", speechTime: "Good evening! Welcome to Veritas AI." },
                night: { title: "Late Night Intelligence 🌌", sub: "Analyzing breaking news claims with neural precision.", speechTime: "Hello and welcome to Veritas AI Night Intelligence." }
            }
        },
        hi: {
            brand_tag: "न्यूरल न्यूज़ इंटेलिजेंस",
            model_badge: "रॉबर्टा ट्रांसफॉर्मर मॉडल",
            hero_badge: "मल्टीमॉडल रॉबर्टा डीप लर्निंग इंटेलिजेंस",
            hero_title_1: "सटीकता के साथ पहचानें",
            hero_title_2: "फर्जी और असली खबरें",
            hero_subtitle: "समाचार लेख, वायरल स्क्रीनशॉट, वेब लिंक या बोलकर खबर की जांच करें। हमारा रॉबर्टा ट्रांसफॉर्मर मॉडल सनसनीखेज शब्दों, पूर्वाग्रह और प्रामाणिकता की तुरंत जांच करता है।",
            listen_brief_btn: "बोलकर बताएं व संक्षिप्त परिचय",
            tab_text: "समाचार टेक्स्ट",
            tab_url: "वेबसाइट लिंक (URL)",
            tab_ocr: "स्क्रीनशॉट व इमेज OCR",
            ocr_title: "वायरल स्क्रीनशॉट या इमेज अपलोड करें",
            ocr_desc: "व्हाट्सएप, ट्विटर या समाचार स्क्रीनशॉट यहां ड्रैग करें या चुनें।",
            quick_samples: "त्वरित उदाहरण:",
            sample_real_1: "असली: नासा अंतरिक्ष शोध",
            sample_real_2: "असली: आर्थिक समीक्षा",
            sample_fake_1: "फेक: जासूसी माइक्रोचिप",
            sample_fake_2: "फेक: चमत्कारिक इलाज",
            input_placeholder: "सत्यता की जांच के लिए समाचार टेक्स्ट या शीर्षक यहां पेस्ट करें (जैसे: 'नासा ने नए ग्रह का वातावरण खोजा...' या 'चौंकाने वाला खुलासा: गुप्त साजिश बेनकाब...')",
            url_placeholder: "https://example.com/hindi/news-article-2026",
            url_hint: "हम सर्वर पर लेख का शीर्षक व विवरण निकाल कर स्वचालित रूप से विश्वसनीयता की जांच करेंगे।",
            clear_btn: "हटाएं",
            scan_btn: "सत्यता जांचें",
            prob_title: "संभाव्यता वितरण (Probability)",
            heatmap_title: "इंटरएक्टिव टेक्स्ट विश्वसनीयता हीटमैप",
            battle_title: "दोहरे मॉडल की तुलना (बैटल मोड)",
            factcheck_title: "सत्यापित फैक्ट-चेक डेटाबेस संदर्भ",
            tone_title: "भाव व शैली (Tone)",
            caps_title: "बड़े अक्षरों का अनुपात",
            punct_title: "सनसनीखेज विराम चिह्न",
            citations_title: "स्रोत व संदर्भ",
            keywords_header: "पहचाने गए सनसनीखेज / क्लिकबेट शब्द:",
            copy_report: "रिपोर्ट कॉपी करें",
            scan_another: "अन्य लेख जांचें",
            download_cert: "सत्यता प्रमाण पत्र डाउनलोड करें (PDF/PNG)",
            nav_analytics: "एनालिटिक्स",
            analytics_title: "सत्र विश्लेषण और सांख्यिकी",
            kpi_total: "कुल स्कैन किए गए लेख",
            kpi_real: "सत्यापित प्रामाणिक अनुपात",
            kpi_fake: "भ्रामक खबर अनुपात",
            kpi_speed: "औसत गति",
            chart_pie_title: "वर्गीकरण वितरण",
            chart_bar_title: "प्रमुख क्लिकबेट शब्द",
            cert_modal_title: "वेरिटास एआई सत्यता प्रमाण पत्र",
            download_png: "प्रमाण पत्र डाउनलोड करें (PNG)",
            print_cert: "प्रिंट करें या PDF बनाएं",
            edu_badge: "सत्य-सत्यापन अकादमी",
            edu_title_1: "समझें अंतर",
            edu_title_2: "फेक न्यूज बनाम असली न्यूज",
            edu_subtitle: "जानें कैसे भ्रामक खबरें फैलती हैं, धोखेबाज पैटर्न कैसे पहचानें और हमारा रॉबर्टा एआई मॉडल सच्चाई कैसे उजागर करता है।",
            real_news_title: "असली समाचार की पहचान",
            real_news_tag: "विश्वसनीय व सत्यापित",
            real_point1_t: "पुष्ट स्रोत और शोधकर्ता:",
            real_point1_d: "विशेष शोधकर्ताओं, सरकारी प्रवक्ताओं और मान्यता प्राप्त पत्रिकाओं के हवाले से तथ्य प्रस्तुत होते हैं।",
            real_point2_t: "संतुलित व निष्पक्ष भाषा:",
            real_point2_d: "बिना किसी सनसनी, अत्यधिक विस्मयादिबोधक चिह्नों या बनावटी गुस्से के तथ्यात्मक विवरण।",
            real_point3_t: "जवाबदेही और सुधार नीति:",
            real_point3_d: "प्रतिष्ठित संपादकीय मानकों द्वारा प्रकाशित, जहां गलती होने पर खंडन व सुधार स्पष्ट दिया जाता है।",
            fake_news_title: "फेक / फर्जी समाचार के लक्षण",
            fake_news_tag: "भ्रामक व मनगढ़ंत",
            fake_point1_t: "क्लिकबेट और भय का माहौल:",
            fake_point1_d: "'चौंकाने वाला खुलासा!', 'सरकार छुपा रही है', जैसे भड़काऊ शब्दों का प्रयोग।",
            fake_point2_t: "चमत्कारिक इलाज या गुप्त साजिश:",
            fake_point2_d: "बिना किसी वैज्ञानिक परीक्षण के 48 घंटे में बड़ी बीमारी ठीक करने या गुप्त विदेशी साज़िश के बेबुनियाद दावे।",
            fake_point3_t: "शेयर करने का अनुचित दबाव:",
            fake_point3_d: "'डिलीट होने से पहले सबको भेजें!' जैसी भावनात्मक अपील करके वायरल करने का प्रयास।",
            how_model_title: "यह AI मॉडल कैसे कार्य करता है?",
            how_model_subtitle: "मल्टी-लेयर डीप लर्निंग ट्रांसफॉर्मर और शाब्दिक विश्लेषण प्रणाली।",
            step1_title: "टोकनाइजेशन",
            step1_desc: "इनपुट टेक्स्ट को संदर्भ-जागरूक सबवर्ड टोकन में विभाजित किया जाता है।",
            step2_title: "रॉबर्टा सेल्फ-अटेंशन",
            step2_desc: "12 ट्रांसफॉर्मर लेयर्स वाक्य रचना, तार्किक सुसंगति और भ्रामक बनावट की गहरी जांच करती हैं।",
            step3_title: "पारदर्शिता व व्याख्या",
            step3_desc: "सनसनीखेज शब्दों, टोन और संदर्भ का विश्लेषण कर स्पष्ट और पारदर्शी रिपोर्ट दी जाती है।",
            feat1_title: "रॉबर्टा अटेंशन हेड",
            feat1_desc: "गहन सिमेंटिक विश्लेषण जो साधारण कीवर्ड फिल्टर से छूटने वाले जटिल झूठ को भी पकड़ता है।",
            feat2_title: "क्लिकबेट रडार",
            feat2_desc: "चेतावनी भरे शब्दों, चिल्लाहट और भ्रामक शीर्षकों की तुरंत पहचान।",
            feat3_title: "तेज गति परिणाम (Sub-100ms)",
            feat3_desc: "अनुकूलित पाईटॉर्च इंजन द्वारा पलक झपकते ही सटीक परिणाम।",
            drawer_history_title: "विश्लेषण इतिहास",
            clear_history: "इतिहास हटाएं",
            empty_history: "इस सत्र में अभी तक कोई इतिहास नहीं है।",
            info_title: "मॉडल संरचना व तकनीक",
            gauge_confidence: "सटीकता",
            greetings: {
                morning: { title: "शुभ प्रभात! स्वागत है ☀️", sub: "आज की सुर्खियों का सच जानने के लिए तैयार हैं?", speechTime: "शुभ प्रभात! वेरिटास एआई में आपका स्वागत है।" },
                afternoon: { title: "शुभ दोपहर! स्वागत है 🌤️", sub: "सोशल मीडिया के भ्रामक दावों की तुरंत जांच करें।", speechTime: "शुभ दोपहर! वेरिटास एआई में आपका स्वागत है।" },
                evening: { title: "शुभ संध्या! स्वागत है 🌆", sub: "वायरल खबरों का सच जांचने के लिए तैयार।", speechTime: "शुभ संध्या! वेरिटास एआई में आपका स्वागत है।" },
                night: { title: "रात्रि समाचार समीक्षा 🌌", sub: "न्यूरल सटीकता के साथ हर दावे का सच परखें।", speechTime: "नमस्ते और वेरिटास एआई में आपका स्वागत है।" }
            }
        }
    };

    // Hindi Pre-built Sample Articles
    const hindiSamples = {
        real: [
            {
                title: "नासा के पर्सिवियरेंस रोवर ने मंगल ग्रह के जेज़ेरो क्रेटर से प्राचीन नमूनों का अध्ययन किया",
                text: "नासा के पर्सिवियरेंस रोवर ने मंगल ग्रह के जेज़ेरो क्रेटर से एकत्र किए गए प्राचीन चट्टानों के नमूनों का वैज्ञानिक विश्लेषण प्रस्तुत किया है। शोध दल ने गुरुवार को बताया कि ये नमूने अतीत में ग्रह पर पानी की उपस्थिति और पर्यावरणीय विकास को समझने में महत्वपूर्ण भूमिका निभा रहे हैं।"
            },
            {
                title: "आरबीआई ने मुद्रास्फीति और आर्थिक स्थिरता की समीक्षा के बाद प्रमुख दरों को स्थिर रखा",
                text: "भारतीय रिजर्व बैंक (RBI) ने मौद्रिक नीति समिति की बैठक के बाद आधिकारिक बयान में कहा कि मुद्रास्फीति के रुझान और विकास दर के संतुलन को बनाए रखने के लिए नीतिगत रेपो दर को यथावत बनाए रखने का निर्णय लिया गया है।"
            }
        ],
        fake: [
            {
                title: "चौंकाने वाला खुलासा: पानी की बोतलों में गुप्त सरकारी माइक्रोचिप पाई गई!",
                text: "चौंकाने वाला खुलासा: सोशल मीडिया पर लीक दस्तावेजों में दावा किया गया है कि पीने के पानी में गुप्त चिप्स मिलाकर आम जनता के दिमाग को नियंत्रित किया जा रहा है! सरकार इस सच को दबाने की कोशिश कर रही है, डिलीट होने से पहले तुरंत शेयर करें!"
            },
            {
                title: "चमत्कार: सुबह उबला हुआ नींबू पानी पीने से 10 दिनों में सभी बीमारियां पूरी तरह खत्म!",
                text: "डॉक्टर हैरान रह गए! एक घरेलू बुजुर्ग नुस्खे ने 50 अरब डॉलर के दवा उद्योग को हिला दिया है। सिर्फ उबला नींबू का पानी पीने से किसी भी बीमारी का शत-प्रतिशत इलाज होने का चमत्कारिक दावा किया गया है, जल्दी देखें!"
            }
        ]
    };

    // --------------------------------------------------------------------------
    // Language Toggle Functionality
    // --------------------------------------------------------------------------
    function applyLanguage(lang) {
        if (typeof stopSpeaking === "function") {
            stopSpeaking();
        }

        currentLang = lang;
        localStorage.setItem("veritas_lang", lang);

        if (lang === "hi") {
            langHiBtn.classList.add("active");
            langEnBtn.classList.remove("active");
        } else {
            langEnBtn.classList.add("active");
            langHiBtn.classList.remove("active");
        }

        const dict = translations[lang] || translations.en;

        // Update all data-i18n elements
        document.querySelectorAll("[data-i18n]").forEach(el => {
            const key = el.getAttribute("data-i18n");
            if (dict[key]) {
                el.textContent = dict[key];
            }
        });

        // Placeholders & dynamic values
        if (newsInput) newsInput.placeholder = dict.input_placeholder;
        if (newsUrlInput) newsUrlInput.placeholder = dict.url_placeholder;
        if (tabTextBtn) tabTextBtn.innerHTML = `<i class="fa-solid fa-align-left"></i> ${dict.tab_text}`;
        if (tabUrlBtn) tabUrlBtn.innerHTML = `<i class="fa-solid fa-link"></i> ${dict.tab_url}`;
        if (tabOcrBtn) tabOcrBtn.innerHTML = `<i class="fa-solid fa-camera"></i> ${dict.tab_ocr}`;
        if (clearBtn) clearBtn.innerHTML = `<i class="fa-solid fa-trash-can"></i> ${dict.clear_btn}`;
        if (voiceBtnText) voiceBtnText.textContent = dict.listen_brief_btn;
        if (analyzeBtn) {
            analyzeBtn.querySelector(".btn-text").innerHTML = `<i class="fa-solid fa-microchip"></i> ${dict.scan_btn}`;
        }

        updateGreeting();
    }

    langEnBtn.addEventListener("click", () => applyLanguage("en"));
    langHiBtn.addEventListener("click", () => applyLanguage("hi"));

    // --------------------------------------------------------------------------
    // Time-Based Dynamic Greeting Engine
    // --------------------------------------------------------------------------
    function updateGreeting() {
        const now = new Date();
        const hours = now.getHours();
        const dict = (translations[currentLang] || translations.en).greetings;

        let greetingKey = "afternoon";
        let icon = "☀️";

        if (hours >= 5 && hours < 12) {
            greetingKey = "morning";
            icon = "🌅";
        } else if (hours >= 12 && hours < 17) {
            greetingKey = "afternoon";
            icon = "☀️";
        } else if (hours >= 17 && hours < 21) {
            greetingKey = "evening";
            icon = "🌆";
        } else {
            greetingKey = "night";
            icon = "🌌";
        }

        if (greetingIcon) greetingIcon.textContent = icon;
        if (greetingTitle) greetingTitle.textContent = dict[greetingKey].title;
        if (greetingSubtitle) greetingSubtitle.textContent = dict[greetingKey].sub;
    }

    function updateLiveClock() {
        if (!liveClock) return;
        const now = new Date();
        liveClock.textContent = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    }

    setInterval(updateLiveClock, 1000);
    updateLiveClock();

    // --------------------------------------------------------------------------
    // Theme Management
    // --------------------------------------------------------------------------
    const savedTheme = localStorage.getItem("veritas_theme") || "dark";
    document.documentElement.setAttribute("data-theme", savedTheme);

    themeToggleBtn.addEventListener("click", () => {
        const currentTheme = document.documentElement.getAttribute("data-theme");
        const newTheme = currentTheme === "dark" ? "light" : "dark";
        document.documentElement.setAttribute("data-theme", newTheme);
        localStorage.setItem("veritas_theme", newTheme);
    });

    // --------------------------------------------------------------------------
    // Word & Character Counter
    // --------------------------------------------------------------------------
    function updateWordCount() {
        const text = newsInput.value.trim();
        const words = text ? text.split(/\s+/).length : 0;
        const chars = newsInput.value.length;
        const wordLabel = currentLang === "hi" ? "शब्द" : (words === 1 ? "word" : "words");
        const charLabel = currentLang === "hi" ? "अक्षर" : (chars === 1 ? "character" : "characters");
        wordCountSpan.textContent = `${words} ${wordLabel}`;
        charCountSpan.textContent = `${chars} ${charLabel}`;
    }

    newsInput.addEventListener("input", updateWordCount);

    // --------------------------------------------------------------------------
    // Tab Navigation (Text, URL, OCR)
    // --------------------------------------------------------------------------
    tabTextBtn.addEventListener("click", () => {
        currentTab = "text";
        tabTextBtn.classList.add("active");
        tabUrlBtn.classList.remove("active");
        tabOcrBtn.classList.remove("active");
        textPanel.classList.add("active");
        urlPanel.classList.remove("active");
        ocrPanel.classList.remove("active");
    });

    tabUrlBtn.addEventListener("click", () => {
        currentTab = "url";
        tabUrlBtn.classList.add("active");
        tabTextBtn.classList.remove("active");
        tabOcrBtn.classList.remove("active");
        urlPanel.classList.add("active");
        textPanel.classList.remove("active");
        ocrPanel.classList.remove("active");
    });

    tabOcrBtn.addEventListener("click", () => {
        currentTab = "ocr";
        tabOcrBtn.classList.add("active");
        tabTextBtn.classList.remove("active");
        tabUrlBtn.classList.remove("active");
        ocrPanel.classList.add("active");
        textPanel.classList.remove("active");
        urlPanel.classList.remove("active");
    });

    // --------------------------------------------------------------------------
    // Feature 1: Speech-to-Text Microphone Dictation Engine
    // --------------------------------------------------------------------------
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
        speechRecognition = new SpeechRecognition();
        speechRecognition.continuous = false;
        speechRecognition.interimResults = true;

        speechRecognition.onstart = () => {
            isDictating = true;
            micDictateBtn.classList.add("listening");
            micStatusBar.classList.add("active");
            micStatusText.textContent = currentLang === "hi" ? "सुन रहे हैं... कृपया बोलें" : "Listening... Speak headline or news claim now";
        };

        speechRecognition.onresult = (event) => {
            let transcript = "";
            for (let i = event.resultIndex; i < event.results.length; ++i) {
                transcript += event.results[i][0].transcript;
            }
            if (transcript) {
                newsInput.value = transcript;
                updateWordCount();
            }
        };

        speechRecognition.onerror = (err) => {
            console.warn("Speech Recognition error:", err);
            stopDictation();
            showToast(currentLang === "hi" ? "माइक्रोफ़ोन त्रुटि हुई।" : "Microphone error or permission denied.", "error");
        };

        speechRecognition.onend = () => {
            stopDictation();
            if (newsInput.value.trim()) {
                showToast(currentLang === "hi" ? "आवाज दर्ज की गई!" : "Voice transcribed successfully!", "info");
            }
        };
    }

    function toggleDictation() {
        if (!SpeechRecognition) {
            showToast(currentLang === "hi" ? "इस ब्राउज़र में स्पीच रिकग्निशन उपलब्ध नहीं है।" : "Speech Recognition is not supported in this browser.", "error");
            return;
        }

        if (isDictating) {
            speechRecognition.stop();
            stopDictation();
        } else {
            speechRecognition.lang = currentLang === "hi" ? "hi-IN" : "en-US";
            speechRecognition.start();
        }
    }

    function stopDictation() {
        isDictating = false;
        if (micDictateBtn) micDictateBtn.classList.remove("listening");
        if (micStatusBar) micStatusBar.classList.remove("active");
    }

    if (micDictateBtn) {
        micDictateBtn.addEventListener("click", toggleDictation);
    }

    // --------------------------------------------------------------------------
    // Feature 2: Tesseract.js Client-Side OCR Engine
    // --------------------------------------------------------------------------
    if (ocrFileInput) {
        ocrFileInput.addEventListener("change", (e) => {
            const file = e.target.files[0];
            if (file) handleOcrFile(file);
        });
    }

    if (ocrDropzone) {
        ocrDropzone.addEventListener("dragover", (e) => {
            e.preventDefault();
            ocrDropzone.classList.add("dragover");
        });

        ocrDropzone.addEventListener("dragleave", () => {
            ocrDropzone.classList.remove("dragover");
        });

        ocrDropzone.addEventListener("drop", (e) => {
            e.preventDefault();
            ocrDropzone.classList.remove("dragover");
            const file = e.dataTransfer.files[0];
            if (file) handleOcrFile(file);
        });
    }

    if (removeOcrImgBtn) {
        removeOcrImgBtn.addEventListener("click", (e) => {
            e.preventDefault();
            e.stopPropagation();
            if (ocrDropzone) ocrDropzone.classList.remove("has-preview");
            ocrPreviewContainer.classList.add("hidden");
            ocrPromptContent.classList.remove("hidden");
            if (ocrProgressBox) ocrProgressBox.classList.add("hidden");
            if (ocrPreviewImage) ocrPreviewImage.src = "";
            if (ocrFileInput) ocrFileInput.value = "";
            showToast(currentLang === "hi" ? "इमेज हटाई गई। नई इमेज चुनें।" : "Image cleared. Choose or drop a new image.", "info");
            // Automatically open file picker for seamless replacement
            setTimeout(() => {
                if (ocrFileInput) ocrFileInput.click();
            }, 100);
        });
    }

    async function handleOcrFile(file) {
        if (!file.type.startsWith("image/")) {
            showToast(currentLang === "hi" ? "कृपया एक मान्य इमेज फाइल चुनें।" : "Please upload a valid image file.", "error");
            return;
        }

        // Preview image
        const reader = new FileReader();
        reader.onload = async (ev) => {
            if (ocrDropzone) ocrDropzone.classList.add("has-preview");
            ocrPreviewImage.src = ev.target.result;
            ocrPromptContent.classList.add("hidden");
            ocrPreviewContainer.classList.remove("hidden");
            ocrProgressBox.classList.remove("hidden");
            ocrProgressFill.style.width = "0%";
            ocrPercent.textContent = "0%";
            ocrProgressLabel.textContent = currentLang === "hi" ? "इमेज से टेक्स्ट निकाला जा रहा है..." : "Extracting text from image...";

            try {
                if (typeof Tesseract === "undefined") {
                    throw new Error("OCR Library loading...");
                }

                const ocrLang = currentLang === "hi" ? "hin+eng" : "eng";
                const result = await Tesseract.recognize(ev.target.result, ocrLang, {
                    logger: (m) => {
                        if (m.status === "recognizing text" && m.progress) {
                            const p = Math.round(m.progress * 100);
                            ocrProgressFill.style.width = `${p}%`;
                            ocrPercent.textContent = `${p}%`;
                        }
                    }
                });

                const extracted = result.data.text.trim();
                if (!extracted) {
                    throw new Error("No readable text found in image.");
                }

                newsInput.value = extracted;
                updateWordCount();
                showToast(currentLang === "hi" ? "इमेज से टेक्स्ट सफलतापूर्वक निकाला गया!" : "Text successfully extracted from image!", "info");

                // Switch to text tab to review & scan
                tabTextBtn.click();
            } catch (err) {
                console.warn("OCR Error:", err);
                showToast(currentLang === "hi" ? "OCR में समस्या आई।" : "OCR extraction failed. Please paste text directly.", "error");
            }
        };
        reader.readAsDataURL(file);
    }

    // --------------------------------------------------------------------------
    // Quick Samples Loader
    // --------------------------------------------------------------------------
    async function loadSamples() {
        try {
            const res = await fetch("/api/samples");
            const data = await res.json();
            if (data.status === "success") {
                sampleData = data.samples;
            }
        } catch (e) {
            console.warn("Could not preload samples:", e);
        }
    }

    document.querySelectorAll(".chip").forEach(chip => {
        chip.addEventListener("click", () => {
            const type = chip.getAttribute("data-type");
            const index = parseInt(chip.getAttribute("data-index"), 10);

            // If Hindi selected, use curated Hindi samples
            if (currentLang === "hi" && hindiSamples[type] && hindiSamples[type][index]) {
                const sample = hindiSamples[type][index];
                newsInput.value = `${sample.title}\n\n${sample.text}`;
                updateWordCount();
                if (currentTab !== "text") tabTextBtn.click();
                showToast(`उदाहरण लोड किया गया: "${sample.title.slice(0, 30)}..."`, "info");
                return;
            }

            // Otherwise English samples
            if (sampleData && sampleData[type] && sampleData[type][index]) {
                const sample = sampleData[type][index];
                newsInput.value = `${sample.title}\n\n${sample.text}`;
                updateWordCount();
                if (currentTab !== "text") tabTextBtn.click();
                showToast(`Loaded "${sample.title.slice(0, 35)}..."`, "info");
            }
        });
    });

    // --------------------------------------------------------------------------
    // Scanner Overlay Orchestration
    // --------------------------------------------------------------------------
    const scannerMessagesEn = [
        "Tokenizing input sequence...",
        "Evaluating RoBERTa multi-head self-attention...",
        "Cross-referencing trusted sources...",
        "Analyzing lexical credibility markers...",
        "Synthesizing calibrated class probabilities..."
    ];

    const scannerMessagesHi = [
        "इनपुट शब्दों का टोकनाइजेशन जारी है...",
        "रॉबर्टा ट्रांसफॉर्मर अटेंशन की गणना हो रही है...",
        "विश्वसनीय पत्रकारिता व शोध स्रोतों से मिलान जारी है...",
        "सनसनीखेज शब्दों व स्रोत की जांच...",
        "सटीक सत्यता स्कोर तैयार किया जा रहा है..."
    ];

    let scanInterval = null;

    function startScanAnimation() {
        scannerOverlay.classList.add("active");
        const messages = currentLang === "hi" ? scannerMessagesHi : scannerMessagesEn;
        let msgIndex = 0;
        scanStatusText.textContent = messages[0];
        scanInterval = setInterval(() => {
            msgIndex = (msgIndex + 1) % messages.length;
            scanStatusText.textContent = messages[msgIndex];
        }, 400);
    }

    function stopScanAnimation() {
        scannerOverlay.classList.remove("active");
        if (scanInterval) clearInterval(scanInterval);
    }

    // --------------------------------------------------------------------------
    // Predict Execution
    // --------------------------------------------------------------------------
    analyzeBtn.addEventListener("click", async () => {
        const text = newsInput.value.trim();
        const url = newsUrlInput.value.trim();

        if (currentTab === "text" && !text) {
            showToast(currentLang === "hi" ? "कृपया विश्लेषण के लिए समाचार टेक्स्ट दर्ज करें।" : "Please enter or paste an article text to analyze.", "error");
            newsInput.focus();
            return;
        }

        if (currentTab === "url" && !url) {
            showToast(currentLang === "hi" ? "कृपया एक मान्य वेब लिंक (URL) दर्ज करें।" : "Please enter a valid news URL.", "error");
            newsUrlInput.focus();
            return;
        }

        startScanAnimation();
        analyzeBtn.disabled = true;

        try {
            const payload = currentTab === "url" ? { url } : { text, source_type: currentTab };
            const response = await fetch("/api/predict", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });

            const resData = await response.json();

            if (!response.ok || resData.status === "error") {
                throw new Error(resData.message || "Failed to analyze content.");
            }

            // Render Result
            setTimeout(() => {
                stopScanAnimation();
                analyzeBtn.disabled = false;
                renderResult(resData.data);
                refreshHistory();
                // Automatically listen to verdict after scanning
                setTimeout(() => {
                    speakVerdict();
                }, 350);
            }, 600);

        } catch (err) {
            stopScanAnimation();
            analyzeBtn.disabled = false;
            showToast(err.message || "Network error occurred.", "error");
        }
    });

    clearBtn.addEventListener("click", () => {
        newsInput.value = "";
        newsUrlInput.value = "";
        updateWordCount();
        if (ocrDropzone) ocrDropzone.classList.remove("has-preview");
        if (ocrPreviewContainer) ocrPreviewContainer.classList.add("hidden");
        if (ocrPromptContent) ocrPromptContent.classList.remove("hidden");
        if (ocrProgressBox) ocrProgressBox.classList.add("hidden");
        if (ocrPreviewImage) ocrPreviewImage.src = "";
        if (ocrFileInput) ocrFileInput.value = "";
        resultSection.classList.add("hidden");
        stopSpeaking();
    });

    reScanBtn.addEventListener("click", () => {
        window.scrollTo({ top: 0, behavior: "smooth" });
        newsInput.focus();
    });

    copyResultBtn.addEventListener("click", () => {
        if (!lastAnalysisData) return;
        const report = `VERITAS AI CREDIBILITY REPORT\nVerdict: ${lastAnalysisData.label} (${lastAnalysisData.confidence}% Confidence)\nProbabilities: Real ${lastAnalysisData.probabilities.real}% | Fake ${lastAnalysisData.probabilities.fake}%\nTone: ${lastAnalysisData.linguistics?.sentiment_tone || 'N/A'}\nModel: ${lastAnalysisData.model_architecture}\nTimestamp: ${lastAnalysisData.timestamp}`;
        navigator.clipboard.writeText(report);
        showToast(currentLang === "hi" ? "रिपोर्ट क्लिपबोर्ड में कॉपी की गई!" : "Report copied to clipboard!", "info");
    });

    // --------------------------------------------------------------------------
    // Feature 3: In-Text Suspicious Word Heatmap Renderer
    // --------------------------------------------------------------------------
    function renderHeatmap(fullText, spans) {
        if (!heatmapBody) return;
        if (!fullText) {
            heatmapBody.innerHTML = "<em>No text content available for highlighting.</em>";
            return;
        }

        if (!spans || spans.length === 0) {
            heatmapBody.textContent = fullText;
            return;
        }

        // Sort spans by start index
        const sortedSpans = [...spans].sort((a, b) => a.start - b.start);
        let html = "";
        let currentIndex = 0;

        sortedSpans.forEach(span => {
            if (span.start < currentIndex) return; // Skip overlaps

            // Append text before span
            html += escapeHtml(fullText.slice(currentIndex, span.start));

            // Append highlighted span
            const matchedText = fullText.slice(span.start, span.end);
            const spanClass = span.type === "clickbait" ? "heat-clickbait" : (span.type === "credible" ? "heat-credible" : "heat-shouting");
            html += `<span class="heat-span ${spanClass}" title="${escapeHtml(span.tooltip || 'Flagged token')}">${escapeHtml(matchedText)}</span>`;

            currentIndex = span.end;
        });

        // Append remaining text
        if (currentIndex < fullText.length) {
            html += escapeHtml(fullText.slice(currentIndex));
        }

        heatmapBody.innerHTML = html;
    }

    function escapeHtml(str) {
        return str
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    // --------------------------------------------------------------------------
    // Feature 5: Dual-Model Battle Renderer (RoBERTa vs Baseline)
    // --------------------------------------------------------------------------
    function renderModelBattle(data) {
        if (robertaVerdictVal) {
            robertaVerdictVal.textContent = `${data.label} (${data.confidence}%)`;
        }
        if (robertaLatencyVal) {
            robertaLatencyVal.textContent = `${data.latency_ms || 42}ms`;
        }

        const base = data.baseline_comparison || {};
        if (baselineVerdictVal) {
            baselineVerdictVal.textContent = `${base.label || 'Real'} (${base.confidence || 50}%)`;
        }
        if (baselineLatencyVal) {
            baselineLatencyVal.textContent = `${base.latency_ms || 1.2}ms`;
        }
    }

    // --------------------------------------------------------------------------
    // Feature 6: Fact-Check Database References Renderer
    // --------------------------------------------------------------------------
    function renderFactChecks(factChecks) {
        if (!factCheckList) return;
        if (!factChecks || factChecks.length === 0) {
            factCheckList.innerHTML = `
                <div class="factcheck-item">
                    <div class="factcheck-claim">No direct viral claim matches found in archive.</div>
                    <div class="factcheck-summary">Our RoBERTa attention heads analyzed the underlying linguistic patterns directly.</div>
                </div>
            `;
            return;
        }

        factCheckList.innerHTML = "";
        factChecks.forEach(fc => {
            const div = document.createElement("div");
            div.className = "factcheck-item";
            div.innerHTML = `
                <div class="factcheck-top">
                    <strong>${fc.claimant || "Public Viral Post"}</strong>
                    <span class="factcheck-badge ${fc.rating_level || 'false'}">${fc.rating}</span>
                </div>
                <div class="factcheck-claim">"${fc.claim}"</div>
                <div class="factcheck-summary">${fc.summary}</div>
                <a href="${fc.fact_check_url}" target="_blank" rel="noopener noreferrer" class="factcheck-link">
                    <i class="fa-solid fa-arrow-up-right-from-square"></i> Read source report at ${fc.fact_checker}
                </a>
            `;
            factCheckList.appendChild(div);
        });
    }

    // --------------------------------------------------------------------------
    // Render Results & Animations
    // --------------------------------------------------------------------------
    function renderResult(data) {
        lastAnalysisData = data;
        resultSection.classList.remove("hidden");

        // Set status styling
        resultCard.className = `glass-card result-card status-${data.status_theme}`;

        const isHi = currentLang === "hi";

        // Verdict Icon & Colors
        if (data.status_theme === "real") {
            verdictIcon.className = "fa-solid fa-shield-check";
            verdictHeadline.textContent = isHi ? "सामग्री पूर्णतः प्रामाणिक व विश्वसनीय प्रतीत होती है" : "Content Appears Verified & Credible";
            verdictDescription.textContent = isHi ? "शाब्दिक संरचना, तथ्य एवं संदर्भ स्थापित पत्रकारीय मानकों के अनुरूप हैं।" : "Linguistic markers, contextual attention, and lexical flow align with established journalistic standards.";
            verdictPill.textContent = isHi ? "सत्यापित असली (REAL)" : "VERIFIED CREDIBLE";
        } else if (data.status_theme === "hoax_reference") {
            verdictIcon.className = "fa-solid fa-magnifying-glass-chart";
            verdictHeadline.textContent = isHi ? "वायरल अफवाह / फर्जी खबर का खंडन व विश्लेषण" : "Describes a Known / Reported Hoax";
            verdictDescription.textContent = isHi 
                ? "यह लेख किसी वायरल अफवाह या फर्जी दावे की रिपोर्टिंग या उसका खंडन कर रहा है, न कि उस दावे को सत्य मान रहा है।" 
                : (data.message || "This text appears to be reporting on or debunking a false claim, rather than asserting the claim as fact.");
            verdictPill.textContent = isHi ? "अफवाह का विश्लेषण (HOAX REPORT)" : "HOAX REFERENCE DETECTED";
        } else if (data.status_theme === "fake") {
            verdictIcon.className = "fa-solid fa-triangle-exclamation";
            verdictHeadline.textContent = isHi ? "फर्जी / भ्रामक खबर होने की अत्यधिक संभावना" : "High Probability of Misinformation / Fake News";
            verdictDescription.textContent = isHi ? "सनसनीखेज शब्दावली, अपुष्ट दावे अथवा भावनात्मक रूप से भड़काने वाले लक्षण पाए गए।" : "Detected sensationalism patterns, unverified claims, or emotional manipulation cues.";
            verdictPill.textContent = isHi ? "मनगढ़ंत / फेक (FAKE)" : "FABRICATED / FAKE";
        } else {
            verdictIcon.className = "fa-solid fa-circle-question";
            verdictHeadline.textContent = isHi ? "मिश्रित संकेत / अपुष्ट दावे" : "Mixed Signals / Unverified Claims";
            verdictDescription.textContent = isHi ? "लेख में अस्पष्ट दावे या अपर्याप्त संदर्भ हैं।" : "The article contains ambiguous phrasing or insufficient corroboration.";
            verdictPill.textContent = isHi ? "अपुष्ट / संदिग्ध" : "SUSPICIOUS";
        }

        resultModelTag.textContent = data.model_architecture;
        latencyPill.innerHTML = `<i class="fa-solid fa-bolt"></i> ${data.latency_ms}ms`;

        // Animate Circular Gauge
        animateGauge(data.confidence);

        // Probability Bars
        realProgress.style.width = `${data.probabilities.real}%`;
        fakeProgress.style.width = `${data.probabilities.fake}%`;
        realProbText.textContent = isHi ? `असली: ${data.probabilities.real}%` : `Real: ${data.probabilities.real}%`;
        fakeProbText.textContent = isHi ? `फेक: ${data.probabilities.fake}%` : `Fake: ${data.probabilities.fake}%`;

        // Diagnostics & Metrics
        const ling = data.linguistics || {};
        const citCount = data.citation_info?.match_count ?? ling.citation_count ?? (ling.objective_markers || []).length;
        const webInfo = data.web_corroboration || {};
        const trustedCount = webInfo.trusted_matches || 0;

        if (citationPill) {
            citationPill.innerHTML = `<i class="fa-solid fa-feather-pointed"></i> ${citCount} ${isHi ? 'प्रमाणित स्रोत' : (citCount === 1 ? 'Source Citation' : 'Source Citations')}`;
        }

        if (webCorroborationPill) {
            webCorroborationPill.innerHTML = `<i class="fa-solid fa-globe"></i> ${trustedCount} ${isHi ? 'विश्वसनीय स्रोत' : (trustedCount === 1 ? 'Trusted Source Found' : 'Trusted Sources Found')}`;
        }

        toneValue.textContent = ling.sentiment_tone || "Neutral";
        capsValue.textContent = `${ling.uppercase_ratio || 0}% ${isHi ? 'बड़े अक्षर' : 'Uppercase'}`;
        punctValue.textContent = `${ling.exclamation_count || 0} ${isHi ? 'विस्मयादिबोधक' : 'Exclamations'}`;
        citationsValue.textContent = `${citCount} ${isHi ? 'सत्यापित स्रोत / संदर्भ' : (citCount === 1 ? 'Checkable Source / Citation' : 'Checkable Sources / Citations')}`;

        if (webCorrobValue) {
            webCorrobValue.textContent = `${trustedCount} ${isHi ? 'पुष्ट स्रोत' : (trustedCount === 1 ? 'Trusted Outlet' : 'Trusted Outlets')}`;
        }

        // Render Live Web Corroboration Sources Box
        if (webCorroborationBox) {
            const sources = webInfo.matched_sources || [];
            if (sources.length > 0) {
                webCorroborationBox.classList.remove("hidden");
                if (webCorrobBadge) {
                    webCorrobBadge.textContent = `${sources.length} ${isHi ? 'पुष्ट स्रोत' : (sources.length === 1 ? 'Trusted Outlet Found' : 'Trusted Outlets Found')}`;
                }
                if (webCorrobList) {
                    webCorrobList.innerHTML = "";
                    sources.forEach(src => {
                        const item = document.createElement("div");
                        item.className = "web-corrob-item";
                        item.innerHTML = `
                            <div class="web-corrob-item-top">
                                <span class="web-corrob-domain"><i class="fa-solid fa-check"></i> ${escapeHtml(src.domain)}</span>
                                <a href="${escapeHtml(src.url)}" target="_blank" rel="noopener noreferrer" class="web-corrob-link">
                                    <i class="fa-solid fa-arrow-up-right-from-square"></i> Open
                                </a>
                            </div>
                            <a href="${escapeHtml(src.url)}" target="_blank" rel="noopener noreferrer" class="web-corrob-link">
                                <strong>${escapeHtml(src.title || src.domain)}</strong>
                            </a>
                            <p class="web-corrob-snippet">${escapeHtml(src.snippet || '')}</p>
                        `;
                        webCorrobList.appendChild(item);
                    });
                }
            } else {
                webCorroborationBox.classList.add("hidden");
            }
        }

        // Keywords
        keywordsList.innerHTML = "";
        const sens = ling.sensational_words || [];
        if (sens.length > 0) {
            sens.forEach(word => {
                const badge = document.createElement("span");
                badge.className = "keyword-badge";
                badge.textContent = `#${word.toUpperCase()}`;
                keywordsList.appendChild(badge);
            });
        } else {
            keywordsList.innerHTML = `<span class="empty-keywords">${isHi ? 'कोई आक्रामक या सनसनीखेज कीवर्ड नहीं मिला।' : 'No aggressive clickbait markers detected.'}</span>`;
        }

        // Render In-Text Heatmap (Feature 3)
        renderHeatmap(data.full_text || newsInput.value, ling.highlight_spans || []);

        // Render Attribution & Verification Advisory Note (Limitation Notice)
        const advisoryBox = document.getElementById("attributionAdvisoryBox");
        const advisoryText = document.getElementById("advisoryText");
        if (advisoryBox) {
            const hasAttribution = data.verification_advisory || data.citation_info?.has_attribution || citCount > 0 || trustedCount > 0;
            if (hasAttribution) {
                advisoryBox.classList.remove("hidden");
                if (advisoryText) {
                    advisoryText.textContent = isHi
                        ? "इस लेख में स्रोतों या संस्थानों का उल्लेख है। तंत्रिका भाषाई विश्लेषण केवल लेखन शैली का मूल्यांकन करता है, भौतिक सत्य का नहीं। वेब मिलान इंजन प्रतिष्ठित प्रकाशकों से मिलान करता है। मूल प्राथमिक स्रोतों से दावों की पुष्टि अवश्य करें।"
                        : (data.verification_advisory || "This text names a source or institution. Neural models evaluate writing style and structure, while Web Corroboration cross-checks verified outlets. Always cross-check with original primary sources.");
                }
            } else {
                advisoryBox.classList.add("hidden");
            }
        }

        // Render Model Battle (Feature 5)
        renderModelBattle(data);

        // Render Fact Checks (Feature 6)
        renderFactChecks(data.fact_checks || []);

        // Smooth scroll to result
        resultSection.scrollIntoView({ behavior: "smooth", block: "start" });
    }

    function animateGauge(targetPercent) {
        const circumference = 2 * Math.PI * 50;
        gaugeFill.style.strokeDasharray = `${circumference}`;
        gaugeFill.style.strokeDashoffset = `${circumference}`;

        // Number count-up
        let current = 0;
        const duration = 1200;
        const stepTime = 20;
        const steps = duration / stepTime;
        const increment = targetPercent / steps;

        const timer = setInterval(() => {
            current += increment;
            if (current >= targetPercent) {
                current = targetPercent;
                clearInterval(timer);
            }
            confidenceValue.textContent = Math.round(current);
        }, stepTime);

        // Animate stroke
        setTimeout(() => {
            const offset = circumference - (targetPercent / 100) * circumference;
            gaugeFill.style.strokeDashoffset = `${offset}`;
        }, 50);
    }

    // --------------------------------------------------------------------------
    // Feature 4: Fact-Check Certificate Generator & Exporter
    // --------------------------------------------------------------------------
    if (downloadCertBtn) {
        downloadCertBtn.addEventListener("click", () => {
            if (!lastAnalysisData) return;
            openCertificateModal(lastAnalysisData);
        });
    }

    if (certCloseBtn) {
        certCloseBtn.addEventListener("click", () => {
            certificateModal.classList.remove("active");
        });
    }

    function openCertificateModal(data) {
        if (!certificateModal) return;
        certId.textContent = `VERITAS-${data.id || Date.now().toString().slice(-6)}`;
        certHeadline.textContent = `"${data.title || 'Scanned News Story'}"`;
        certVerdictPill.textContent = data.verdict || (data.label === "Real" ? "VERIFIED CREDIBLE" : "FABRICATED / FAKE");
        certVerdictPill.className = `cert-stat-pill ${data.status_theme === 'real' ? 'real' : 'fake'}`;
        certConfidenceVal.textContent = `${data.confidence}%`;
        certToneVal.textContent = data.linguistics?.sentiment_tone || "Journalistic";
        certDateVal.textContent = data.timestamp || new Date().toISOString().split("T")[0];

        certificateModal.classList.add("active");
    }

    if (saveCertPngBtn) {
        saveCertPngBtn.addEventListener("click", async () => {
            if (typeof html2canvas === "undefined") {
                showToast("Image exporter loading...", "error");
                return;
            }

            try {
                showToast(currentLang === "hi" ? "प्रमाण पत्र तैयार किया जा रहा है..." : "Generating certificate image...", "info");
                const canvas = await html2canvas(certificateCanvas, {
                    scale: 2,
                    backgroundColor: "#0f172a"
                });
                const link = document.createElement("a");
                link.download = `Veritas_Credibility_Certificate_${Date.now()}.png`;
                link.href = canvas.toDataURL("image/png");
                link.click();
                showToast(currentLang === "hi" ? "प्रमाण पत्र डाउनलोड हो गया!" : "Certificate downloaded successfully!", "info");
            } catch (err) {
                console.warn("Certificate download error:", err);
                showToast("Failed to generate image.", "error");
            }
        });
    }

    if (printCertBtn) {
        printCertBtn.addEventListener("click", () => {
            window.print();
        });
    }

    // --------------------------------------------------------------------------
    // Feature 7: Analytics Dashboard & Session Trends Modal (Chart.js)
    // --------------------------------------------------------------------------
    if (analyticsToggleBtn) {
        analyticsToggleBtn.addEventListener("click", () => {
            openAnalyticsModal();
        });
    }

    if (analyticsCloseBtn) {
        analyticsCloseBtn.addEventListener("click", () => {
            analyticsModal.classList.remove("active");
        });
    }

    async function openAnalyticsModal() {
        if (!analyticsModal) return;
        analyticsModal.classList.add("active");

        try {
            const res = await fetch("/api/analytics");
            const data = await res.json();
            if (data.status === "success") {
                kpiTotalScans.textContent = data.total_scans;
                kpiRealRate.textContent = `${data.real_percentage}%`;
                kpiFakeRate.textContent = `${data.fake_percentage}%`;
                kpiAvgLatency.textContent = `${data.avg_latency_ms}ms`;

                renderAnalyticsCharts(data);
            }
        } catch (e) {
            console.warn("Could not load analytics:", e);
        }
    }

    function renderAnalyticsCharts(data) {
        if (typeof Chart === "undefined") return;

        // 1. Distribution Donut Chart
        const distCtx = document.getElementById("distributionChart");
        if (distCtx) {
            if (distributionChart) distributionChart.destroy();
            distributionChart = new Chart(distCtx, {
                type: "doughnut",
                data: {
                    labels: ["Verified Credible", "Misinformation / Fake"],
                    datasets: [{
                        data: [data.real_count || 0, data.fake_count || 0],
                        backgroundColor: ["#10b981", "#f43f5e"],
                        borderColor: ["#059669", "#e11d48"],
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { labels: { color: "#9ca3af", font: { family: "Plus Jakarta Sans" } } }
                    }
                }
            });
        }

        // 2. Keywords Bar Chart
        const keyCtx = document.getElementById("keywordsChart");
        if (keyCtx) {
            if (keywordsChart) keywordsChart.destroy();
            const topWords = data.top_keywords || [];
            keywordsChart = new Chart(keyCtx, {
                type: "bar",
                data: {
                    labels: topWords.length > 0 ? topWords.map(w => w.keyword) : ["No triggers"],
                    datasets: [{
                        label: "Detection Frequency",
                        data: topWords.length > 0 ? topWords.map(w => w.count) : [0],
                        backgroundColor: "#6366f1",
                        borderColor: "#4f46e5",
                        borderRadius: 6
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false }
                    },
                    scales: {
                        x: { ticks: { color: "#9ca3af" }, grid: { display: false } },
                        y: { ticks: { color: "#9ca3af", stepSize: 1 }, grid: { color: "rgba(255,255,255,0.05)" } }
                    }
                }
            });
        }
    }

    // --------------------------------------------------------------------------
    // History Drawer Management
    // --------------------------------------------------------------------------
    historyToggleBtn.addEventListener("click", () => {
        refreshHistory();
        openDrawer();
    });

    drawerCloseBtn.addEventListener("click", closeDrawer);
    drawerOverlay.addEventListener("click", closeDrawer);

    function openDrawer() {
        historyDrawer.classList.add("active");
        drawerOverlay.classList.add("active");
    }

    function closeDrawer() {
        historyDrawer.classList.remove("active");
        drawerOverlay.classList.remove("active");
    }

    async function refreshHistory() {
        try {
            const res = await fetch("/api/history");
            const data = await res.json();
            if (data.status === "success") {
                renderHistoryList(data.history);
            }
        } catch (e) {
            console.warn("Could not fetch history:", e);
        }
    }

    function renderHistoryList(items) {
        historyCount.textContent = items.length;
        if (!items || items.length === 0) {
            historyList.innerHTML = `
                <div class="empty-history">
                    <i class="fa-solid fa-inbox"></i>
                    <p>${currentLang === "hi" ? "इस सत्र में अभी तक कोई इतिहास नहीं है।" : "No scans recorded in this session yet."}</p>
                </div>
            `;
            return;
        }

        historyList.innerHTML = "";
        items.forEach(item => {
            const div = document.createElement("div");
            div.className = "history-item";
            div.innerHTML = `
                <div class="hist-top">
                    <span class="hist-pill ${item.status_theme}">${item.label} (${item.confidence}%)</span>
                    <span class="hist-time">${item.timestamp.split(" ")[1] || ""}</span>
                </div>
                <div class="hist-title">${item.title}</div>
            `;
            div.addEventListener("click", () => {
                closeDrawer();
                renderResult(item);
                setTimeout(() => {
                    speakVerdict();
                }, 300);
            });
            historyList.appendChild(div);
        });
    }

    clearHistoryBtn.addEventListener("click", async () => {
        try {
            await fetch("/api/history", { method: "DELETE" });
            refreshHistory();
            showToast(currentLang === "hi" ? "इतिहास साफ कर दिया गया।" : "History cleared.", "info");
        } catch (e) {
            showToast("Failed to clear history.", "error");
        }
    });

    // --------------------------------------------------------------------------
    // Info Modal
    // --------------------------------------------------------------------------
    infoToggleBtn.addEventListener("click", () => {
        infoModal.classList.add("active");
    });

    modalCloseBtn.addEventListener("click", () => {
        infoModal.classList.remove("active");
    });

    infoModal.addEventListener("click", (e) => {
        if (e.target === infoModal) infoModal.classList.remove("active");
    });

    // --------------------------------------------------------------------------
    // Health Check & Model Status
    // --------------------------------------------------------------------------
    async function checkHealth() {
        try {
            const res = await fetch("/api/health");
            const data = await res.json();
            if (data.status === "healthy") {
                modelBadgeText.textContent = data.model_architecture;
            }
        } catch (e) {
            modelBadgeText.textContent = "Offline / Error";
        }
    }

    // --------------------------------------------------------------------------
    // Web Speech API — Voice Greeting, Project Brief & Verdict Engine
    // --------------------------------------------------------------------------
    let availableVoices = [];
    window.veritasUtterances = [];
    let resumeInterval = null;

    function playAudioChime() {
        try {
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            if (!AudioContext) return;
            const ctx = new AudioContext();
            if (ctx.state === "suspended") ctx.resume();

            const osc1 = ctx.createOscillator();
            const osc2 = ctx.createOscillator();
            const gain = ctx.createGain();

            osc1.type = "sine";
            osc2.type = "triangle";
            osc1.frequency.setValueAtTime(587.33, ctx.currentTime);
            osc1.frequency.exponentialRampToValueAtTime(880, ctx.currentTime + 0.12);

            osc2.frequency.setValueAtTime(440, ctx.currentTime);
            osc2.frequency.exponentialRampToValueAtTime(659.25, ctx.currentTime + 0.12);

            gain.gain.setValueAtTime(0.08, ctx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.25);

            osc1.connect(gain);
            osc2.connect(gain);
            gain.connect(ctx.destination);

            osc1.start();
            osc2.start();
            osc1.stop(ctx.currentTime + 0.25);
            osc2.stop(ctx.currentTime + 0.25);
        } catch (e) {}
    }

    function populateVoices() {
        if ("speechSynthesis" in window) {
            availableVoices = window.speechSynthesis.getVoices();
        }
    }

    if ("speechSynthesis" in window) {
        populateVoices();
        if (window.speechSynthesis.onvoiceschanged !== undefined) {
            window.speechSynthesis.onvoiceschanged = populateVoices;
        }
    }

    function getVoiceProfile(lang) {
        if (!availableVoices || availableVoices.length === 0) {
            populateVoices();
        }

        if (lang === "hi") {
            // Target: Male Hindi Voice
            const hiVoices = availableVoices.filter(v => v.lang && (v.lang.startsWith("hi") || v.lang.includes("hi-IN") || v.lang.includes("hi_IN") || (v.name && v.name.toLowerCase().includes("hindi"))));
            
            const explicitMale = hiVoices.find(v => {
                const name = (v.name || "").toLowerCase();
                return name.includes("hemant") || 
                       name.includes("madhur") || 
                       name.includes("ravi") || 
                       name.includes("tarun") || 
                       name.includes("male") || 
                       name.includes("man");
            });

            const generalHi = hiVoices.find(v => {
                const name = (v.name || "").toLowerCase();
                return name.includes("google") || name.includes("microsoft") || name.includes("hindi");
            }) || hiVoices[0] || null;

            const selectedVoice = explicitMale || generalHi;

            return {
                voice: selectedVoice,
                rate: 0.95,
                pitch: explicitMale ? 0.96 : 0.88,
                langCode: "hi-IN"
            };
        } else {
            // Target: Female / Girl English Voice
            const enVoices = availableVoices.filter(v => v.lang && (v.lang.startsWith("en") || v.lang.includes("en-US") || v.lang.includes("en-GB") || v.lang.includes("en_IN") || v.lang.includes("en-AU")));
            
            const femaleEnVoice = enVoices.find(v => {
                const name = (v.name || "").toLowerCase();
                return name.includes("jenny") || 
                       name.includes("zira") || 
                       name.includes("aria") || 
                       name.includes("sonia") || 
                       name.includes("samantha") || 
                       name.includes("victoria") || 
                       name.includes("karen") || 
                       name.includes("moira") || 
                       name.includes("fiona") || 
                       name.includes("ava") || 
                       name.includes("emma") || 
                       name.includes("female") || 
                       name.includes("woman") ||
                       (name.includes("google us english") && !name.includes("male"));
            });

            const nonMaleVoice = enVoices.find(v => {
                const name = (v.name || "").toLowerCase();
                return !name.includes("david") && 
                       !name.includes("mark") && 
                       !name.includes("george") && 
                       !name.includes("guy") && 
                       !name.includes("male") && 
                       !name.includes("man");
            }) || enVoices[0] || availableVoices[0] || null;

            const selectedVoice = femaleEnVoice || nonMaleVoice;

            return {
                voice: selectedVoice,
                rate: 1.0,
                pitch: 1.15,
                langCode: "en-US"
            };
        }
    }

    function stopSpeaking() {
        if (resumeInterval) {
            clearInterval(resumeInterval);
            resumeInterval = null;
        }

        if ("speechSynthesis" in window) {
            window.speechSynthesis.cancel();
        }
        window.veritasUtterances = [];
        isSpeaking = false;
        
        if (voiceGreetingBtn) {
            voiceGreetingBtn.classList.remove("speaking");
            const dict = translations[currentLang] || translations.en;
            voiceBtnText.textContent = dict.listen_brief_btn;
            const icon = document.getElementById("voiceIcon");
            if (icon) icon.className = "fa-solid fa-volume-high";
        }
    }

    function getTimeOfDayString(lang) {
        const hours = new Date().getHours();
        if (lang === "hi") {
            if (hours >= 5 && hours < 12) return "प्रभात";
            if (hours >= 12 && hours < 17) return "दोपहर";
            if (hours >= 17 && hours < 21) return "संध्या";
            return "रात्रि";
        } else {
            if (hours >= 5 && hours < 12) return "morning";
            if (hours >= 12 && hours < 17) return "afternoon";
            if (hours >= 17 && hours < 21) return "evening";
            return "evening";
        }
    }

    function speakGreetingAndBrief() {
        if (!("speechSynthesis" in window)) {
            showToast(currentLang === "hi" ? "आपके ब्राउज़र में वॉइस स्पीच उपलब्ध नहीं है।" : "Speech synthesis is not supported in this browser.", "error");
            return;
        }

        if (isSpeaking || window.speechSynthesis.speaking) {
            stopSpeaking();
            showToast(currentLang === "hi" ? "ऑडियो बंद किया गया।" : "Audio stopped.", "info");
            return;
        }

        playAudioChime();
        window.speechSynthesis.cancel();
        if (window.speechSynthesis.paused) {
            window.speechSynthesis.resume();
        }

        const timeOfDay = getTimeOfDayString(currentLang);
        let sentences = [];

        if (currentLang === "hi") {
            sentences = [
                `शुभ ${timeOfDay}! वेरिटास एआई में आपका स्वागत है।`,
                `मैं आपका डिजिटल एआई सहायक हूँ।`,
                `हमारा सिस्टम डीप-लर्निंग रॉबर्टा ट्रांसफॉर्मर और एनएलपी का उपयोग करके समाचारों और वेब लिंक्स की सत्यता जांचता है।`,
                `यह भ्रामक दावों, सनसनीखेज शब्दों और स्रोत की विश्वसनीयता का गहन विश्लेषण करता है।`,
                `सत्यता जांचने के लिए ऊपर दिए गए बॉक्स में कोई भी समाचार पेस्ट करें या लिंक दर्ज करें।`
            ];
        } else {
            sentences = [
                `Good ${timeOfDay}, and welcome to Veritas AI.`,
                `I am your digital voice assistant powered by deep neural language processing.`,
                `Our RoBERTa transformer engine inspects headlines, full articles, and website links in real time.`,
                `It analyzes sensationalism, clickbait language, emotional tone, and source citations to distinguish authentic reporting from misleading claims.`,
                `Paste any news text or URL into the scanner to receive an instant, transparent credibility report.`
            ];
        }

        window.veritasUtterances = [];
        const profile = getVoiceProfile(currentLang);

        isSpeaking = true;
        voiceGreetingBtn.classList.add("speaking");
        voiceBtnText.textContent = currentLang === "hi" ? "बोलना बंद करें" : "Stop Audio";
        const icon = document.getElementById("voiceIcon");
        if (icon) icon.className = "fa-solid fa-volume-xmark";

        if (resumeInterval) clearInterval(resumeInterval);
        resumeInterval = setInterval(() => {
            if ("speechSynthesis" in window && window.speechSynthesis.paused) {
                window.speechSynthesis.resume();
            }
        }, 500);

        sentences.forEach((sentenceText, idx) => {
            const utt = new SpeechSynthesisUtterance(sentenceText);
            utt.lang = profile.langCode;
            utt.rate = profile.rate;
            utt.pitch = profile.pitch;
            if (profile.voice) utt.voice = profile.voice;

            if (idx === sentences.length - 1) {
                utt.onend = () => {
                    stopSpeaking();
                };
            }

            utt.onerror = (err) => {
                if (idx === sentences.length - 1) {
                    stopSpeaking();
                }
            };

            window.veritasUtterances.push(utt);
            window.speechSynthesis.speak(utt);
        });

        if (window.speechSynthesis.paused) {
            window.speechSynthesis.resume();
        }

        showToast(currentLang === "hi" ? "ध्वनि परिचय चल रहा है..." : "Speaking greeting & project overview...", "info");
    }

    function speakVerdict() {
        if (!lastAnalysisData) return;
        if (!("speechSynthesis" in window)) return;

        if (isSpeaking || window.speechSynthesis.speaking) {
            stopSpeaking();
        }

        playAudioChime();
        window.speechSynthesis.cancel();
        if (window.speechSynthesis.paused) {
            window.speechSynthesis.resume();
        }

        let sentences = [];
        const isHi = currentLang === "hi";
        const isReal = (lastAnalysisData.label || "").toLowerCase() === "real";

        if (isHi) {
            const labelText = isReal ? "असली और प्रामाणिक समाचार" : "फेक अथवा भ्रामक समाचार";
            sentences = [
                `वेरिटास एआई विश्लेषण परिणाम: यह सामग्री ${labelText} प्रतीत होती है।`,
                `सटीकता और विश्वास स्कोर ${lastAnalysisData.confidence} प्रतिशत है।`,
                `असली होने की संभावना ${lastAnalysisData.probabilities.real} प्रतिशत, और फेक होने की संभावना ${lastAnalysisData.probabilities.fake} प्रतिशत है।`,
                `शब्दावली का भाव ${lastAnalysisData.linguistics?.sentiment_tone || 'सामान्य'} पाया गया।`
            ];
        } else {
            const verdictLabel = isReal ? "Verified Authentic News" : "High Probability of Misinformation and Fake News";
            sentences = [
                `Veritas AI Analysis complete.`,
                `Verdict: ${verdictLabel}, with ${lastAnalysisData.confidence} percent confidence.`,
                `Calculated class probabilities are ${lastAnalysisData.probabilities.real} percent Real, and ${lastAnalysisData.probabilities.fake} percent Fake.`,
                `The tone of the content is identified as ${lastAnalysisData.linguistics?.sentiment_tone || 'Neutral'}.`
            ];
        }

        window.veritasUtterances = [];
        const profile = getVoiceProfile(currentLang);

        isSpeaking = true;
        if (resumeInterval) clearInterval(resumeInterval);
        resumeInterval = setInterval(() => {
            if ("speechSynthesis" in window && window.speechSynthesis.paused) {
                window.speechSynthesis.resume();
            }
        }, 500);

        sentences.forEach((sentenceText, idx) => {
            const utt = new SpeechSynthesisUtterance(sentenceText);
            utt.lang = profile.langCode;
            utt.rate = profile.rate;
            utt.pitch = profile.pitch;
            if (profile.voice) utt.voice = profile.voice;

            if (idx === sentences.length - 1) {
                utt.onend = () => {
                    stopSpeaking();
                };
            }

            utt.onerror = () => {
                if (idx === sentences.length - 1) {
                    stopSpeaking();
                }
            };

            window.veritasUtterances.push(utt);
            window.speechSynthesis.speak(utt);
        });

        if (window.speechSynthesis.paused) {
            window.speechSynthesis.resume();
        }
    }

    // Voice Event Listeners
    if (voiceGreetingBtn) {
        voiceGreetingBtn.addEventListener("click", speakGreetingAndBrief);
    }

    // --------------------------------------------------------------------------
    // Toast Notification System
    // --------------------------------------------------------------------------
    function showToast(message, type = "info") {
        const container = document.getElementById("toastContainer");
        if (!container) return;

        const toast = document.createElement("div");
        toast.className = `toast ${type}`;
        const icon = type === "error" ? "fa-circle-exclamation" : (type === "info" ? "fa-circle-info" : "fa-circle-check");
        toast.innerHTML = `<i class="fa-solid ${icon}"></i> <span>${message}</span>`;
        container.appendChild(toast);

        setTimeout(() => {
            toast.style.opacity = "0";
            toast.style.transform = "translateX(50px)";
            setTimeout(() => toast.remove(), 300);
        }, 3500);
    }

    // --------------------------------------------------------------------------
    // Feature: 3D Newspaper Dive Intro Animation Controller (5-8 Seconds)
    // --------------------------------------------------------------------------
    const newspaperIntroOverlay = document.getElementById("newspaperIntroOverlay");
    const newspaperSheet = document.getElementById("newspaperSheet");
    const skipIntroBtn = document.getElementById("skipIntroBtn");
    const introProgressBar = document.getElementById("introProgressBar");
    const introStatusText = document.getElementById("introStatusText");
    const replayIntroBtn = document.getElementById("replayIntroBtn");

    let introTimer = null;
    let introProgressInterval = null;
    const INTRO_DURATION_MS = 7600; // ~7.6 seconds immersive 3D dive

    function runNewspaperIntro() {
        if (!newspaperIntroOverlay) return;

        // Reset state
        newspaperIntroOverlay.style.display = "flex";
        newspaperIntroOverlay.classList.remove("dismissed");
        newspaperIntroOverlay.classList.add("active");
        if (introProgressBar) introProgressBar.style.width = "0%";
        if (introStatusText) introStatusText.textContent = "Examining The Veritas Chronicle Archives...";

        // Reset 3D sheet animation
        if (newspaperSheet) {
            newspaperSheet.style.animation = "none";
            void newspaperSheet.offsetWidth; // Force CSS reflow
            newspaperSheet.style.animation = "newspaperFlightSequence 7.8s cubic-bezier(0.22, 1, 0.36, 1) forwards";
        }

        const startTime = Date.now();
        clearInterval(introProgressInterval);
        clearTimeout(introTimer);

        // Dynamic progress & status updates
        introProgressInterval = setInterval(() => {
            const elapsed = Date.now() - startTime;
            const progress = Math.min(100, (elapsed / INTRO_DURATION_MS) * 100);
            if (introProgressBar) {
                introProgressBar.style.width = `${progress}%`;
            }

            if (introStatusText) {
                if (progress < 28) {
                    introStatusText.textContent = "Examining The Veritas Chronicle Archives...";
                } else if (progress < 55) {
                    introStatusText.textContent = "Focusing on Lead Investigation by OM Patel...";
                } else if (progress < 80) {
                    introStatusText.textContent = "Diving into Neural Fact-Checking Matrix...";
                } else {
                    introStatusText.textContent = "Launching Veritas AI Neural Intelligence...";
                }
            }

            if (elapsed >= INTRO_DURATION_MS) {
                clearInterval(introProgressInterval);
                dismissNewspaperIntro();
            }
        }, 50);

        introTimer = setTimeout(() => {
            dismissNewspaperIntro();
        }, INTRO_DURATION_MS);
    }

    function dismissNewspaperIntro() {
        if (!newspaperIntroOverlay) return;
        clearInterval(introProgressInterval);
        clearTimeout(introTimer);
        newspaperIntroOverlay.classList.add("dismissed");
        newspaperIntroOverlay.classList.remove("active");
        setTimeout(() => {
            newspaperIntroOverlay.style.display = "none";
        }, 900);
    }

    function retriggerIntro() {
        if (!newspaperIntroOverlay) return;
        newspaperIntroOverlay.style.display = "flex";
        void newspaperIntroOverlay.offsetWidth;
        runNewspaperIntro();
    }

    // Skip Intro on Click
    if (skipIntroBtn) {
        skipIntroBtn.addEventListener("click", () => {
            dismissNewspaperIntro();
            showToast("Welcome to Veritas AI Dashboard", "info");
        });
    }

    // Skip Intro on 'Escape' key
    document.addEventListener("keydown", (e) => {
        if (e.key === "Escape" && newspaperIntroOverlay && !newspaperIntroOverlay.classList.contains("dismissed")) {
            dismissNewspaperIntro();
            showToast("Welcome to Veritas AI Dashboard", "info");
        }
    });

    const playIntroBannerBtn = document.getElementById("playIntroBannerBtn");
    if (playIntroBannerBtn) {
        playIntroBannerBtn.addEventListener("click", () => {
            retriggerIntro();
        });
    }

    // Replay Intro Button in Navbar
    if (replayIntroBtn) {
        replayIntroBtn.addEventListener("click", () => {
            retriggerIntro();
        });
    }

    // Initializations
    applyLanguage(currentLang);
    loadSamples();
    checkHealth();
    refreshHistory();
    runNewspaperIntro();
});
