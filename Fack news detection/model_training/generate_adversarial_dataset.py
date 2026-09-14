"""
Generates a comprehensive, curated adversarial dataset (adversarial_examples.csv)
specifically targeting the two key model failure modes:
1. Real news with absurd, bizarre, or unconventional phrasing (Label: 1)
2. Fake news that mimics real institutions (Stanford, CDC, Federal Reserve, WHO, NASA, Harvard, Mayo Clinic)
   with fabricated statistics or claims (Label: 0)
"""

import os
import pandas as pd

ADVERSARIAL_SAMPLES = [
    # =========================================================================
    # CATEGORY 1: REAL NEWS THAT SOUNDS ABSURD / UNUSUAL / QUIRKY (Label: 1)
    # =========================================================================
    {"text": "Florida man wrestles 8-foot alligator to rescue his three-month-old puppy from a retention pond.", "label": 1},
    {"text": "Scientists discover that tardigrades can survive exposure to outer space vacuum and extreme radiation.", "label": 1},
    {"text": "A town in Norway installed giant hillside mirrors to direct winter sunlight into its dark valley square.", "label": 1},
    {"text": "Japanese train company issues formal apology after a passenger train departs 20 seconds ahead of schedule.", "label": 1},
    {"text": "Biologists find an immortal jellyfish species named Turritopsis dohrnii capable of reverting to its polyp state.", "label": 1},
    {"text": "A runaway emu eluded local animal control officers for three weeks across suburban North Carolina.", "label": 1},
    {"text": "NASA's Curiosity rover photographs a rock formation on Mars that resembles an eroded doorway in the hillside.", "label": 1},
    {"text": "Australian researchers record wombats producing naturally cube-shaped feces due to uneven intestinal elasticity.", "label": 1},
    {"text": "A man in Oregon legally changed his name to Captain Awesome after filing petition paperwork with county clerks.", "label": 1},
    {"text": "Swedish hotel made entirely of river ice rebuilds every winter with fresh architectural ice sculptures.", "label": 1},
    {"text": "A postal pigeon was detained at an international border checkpoint after carrying a miniature pouch of contraband.", "label": 1},
    {"text": "Archaeologists in Egypt unearth a 3,000-year-old jar of honey that remains edible and biologically intact.", "label": 1},
    {"text": "A museum in London offers sleepover nights beneath the reconstructed skeleton of a blue whale.", "label": 1},
    {"text": "French police retrieve stolen 18th-century painting after it was discovered inside an antique dining table.", "label": 1},
    {"text": "A flock of sheep in Wales ate an abandoned stash of fermented apples and wandered into a local village.", "label": 1},
    {"text": "A lost wedding ring lost on a carrot farm in Germany was found 16 years later grown tightly around a harvested carrot.", "label": 1},
    {"text": "The small island nation of Tuvalu plans to upload a digital twin of itself to the metaverse before sea levels rise.", "label": 1},
    {"text": "NASA confirms that a tiny fragment of space junk pierced the robotic arm of the International Space Station without injury.", "label": 1},
    {"text": "A chess grandmaster was investigated for suspected cheating before tournament arbiters cleared all allegations.", "label": 1},
    {"text": "New Zealand government designated an ancient river as a legal person with constitutional human rights.", "label": 1},
    {"text": "Zoo staff in Denmark trained a harbour seal to copy short human vocalizations and melodic tones.", "label": 1},
    {"text": "A bank vault in Frankfurt was accidentally locked from the inside by a computerized holiday maintenance schedule.", "label": 1},
    {"text": "Fishermen off the coast of Maine caught a rare one-in-two-million blue lobster and donated it to a state aquarium.", "label": 1},
    {"text": "Researchers at Oxford discover that crows can craft custom hooked tools from bent garden wires to retrieve food.", "label": 1},
    {"text": "A Swiss municipality tested an outdoor heated sidewalk system to prevent winter pedestrian slip injuries.", "label": 1},
    {"text": "Astronomers detect strange fast radio bursts repeating in a 16-day cycle from a galaxy 500 million light years away.", "label": 1},
    {"text": "A cat in Alaska served as honorary mayor of a small town for over fifteen years according to local lore.", "label": 1},
    {"text": "Scientists in Antarctica discover active volcanic warmth sustaining hidden subterranean moss ecosystems beneath glaciers.", "label": 1},
    {"text": "A hiker surviving five days in the wilderness was rescued after using a pocket mirror to flash reflections at a rescue helicopter.", "label": 1},
    {"text": "Costa Rica generated over 98% of its national electrical energy from renewable sources for five consecutive years.", "label": 1},
    {"text": "A team of engineers built a fully functional bicycle out of recycled cardboard treated with waterproof resin.", "label": 1},
    {"text": "German airport security staff discovered a live juvenile desert tortoise inside a passenger's carry-on chocolate tin.", "label": 1},
    {"text": "Volunteers in Scotland reconstructed a medieval stone bridge using original 14th-century lime mortar recipes.", "label": 1},
    {"text": "Deep sea exploration vehicle records a transparent barreleye fish with rotating green tubular eyes inside a fluid dome.", "label": 1},
    {"text": "A library in California received a returned history book 84 years past its original due date with no penalty fee.", "label": 1},
    {"text": "Marine biologists discover that humpback whales compose complex communal songs that evolve across ocean basins annually.", "label": 1},
    {"text": "A commuter train in Tokyo was delayed for 12 minutes after a giant beetle blocked an optical track sensor.", "label": 1},
    {"text": "NASA engineers successfully test solar sail propulsion system that rides sunlight photons across low Earth orbit.", "label": 1},
    {"text": "A baker in Paris set a world record by baking a continuous 140-meter traditional French baguette.", "label": 1},
    {"text": "Researchers at Cambridge University train sheep to recognize human celebrity faces from photographic prints.", "label": 1},
    {"text": "An Italian town sold abandoned historic villas for one euro to revitalize its declining rural population.", "label": 1},
    {"text": "A dog in Washington state accidentally completed a half-marathon after escaping its backyard and following runners.", "label": 1},
    {"text": "Geologists in Mexico discover giant underground cave containing selenite gypsum crystals exceeding 11 meters in length.", "label": 1},
    {"text": "Dutch city converted hundreds of municipal bus stop roofs into green bee sanctuaries with wild sedum flowers.", "label": 1},
    {"text": "A lost camera lost at sea inside waterproof housing washed ashore six years later with intact memory cards.", "label": 1},
    {"text": "Engineers in Iceland drill into magma chamber to harness ultra-hot geothermal steam for municipal grid power.", "label": 1},
    {"text": "Bees communicate the distance and direction of nectar blooms using rhythmic 'waggle dances' in complete darkness.", "label": 1},
    {"text": "An eccentric art installation in the desert consists of a solar-powered sound system playing a pop song on infinite loop.", "label": 1},
    {"text": "A marathon runner in London completed the 26.2 mile race dressed in a 40-pound fiberglass suit of medieval armor.", "label": 1},
    {"text": "Astronomers discover an exoplanet where atmospheric iron vapor condenses into evening metallic rain showers.", "label": 1},
    {"text": "A parrot in England alerted its owners to a kitchen smoke alarm by mimicking the high-frequency emergency beep.", "label": 1},
    {"text": "A municipal library in Norway installed soundproof reading booths made from upcycled retro telephone booths.", "label": 1},
    {"text": "Paleontologists in Argentina discover fossilized dinosaur eggs with intact microscopic embryonic bone fragments.", "label": 1},
    {"text": "A family in Michigan discovered an 1880s underground tunnel beneath their home during basement renovations.", "label": 1},
    {"text": "A squirrel caused a power outage affecting 3,000 residents after dropping an acorn into an electrical substation relay.", "label": 1},
    {"text": "Researchers find that African elephants use specific vocal rumblings that act as distinct individual names.", "label": 1},
    {"text": "A diver in Florida recovered a working Rolex watch lost 25 years ago in coral reef crevices.", "label": 1},
    {"text": "A municipality in Canada deployed robotic mechanical falcons to deter seagulls from municipal waste disposal sites.", "label": 1},
    {"text": "Scientists discover ancient lake buried beneath two miles of Antarctic ice sheet untouched for millions of years.", "label": 1},
    {"text": "A couple in Wales got married in a 1920s underground slate mine 500 feet below surface level.", "label": 1},

    # =========================================================================
    # CATEGORY 2: FAKE NEWS MIMICKING INSTITUTIONS & FORMAL STATS (Label: 0)
    # =========================================================================
    {"text": "According to a 2026 Stanford University study, drinking boiled lemon juice cures Stage 4 cancer in 48 hours, reducing tumor size by 84%.", "label": 0},
    {"text": "CDC releases emergency report confirming that common supermarket bottled water contains synthetic microchips to monitor brainwaves.", "label": 0},
    {"text": "Federal Reserve internal memo leaks plans to immediately confiscate all cash currency and replace it with centralized crypto tokens by next month.", "label": 0},
    {"text": "A published report from Harvard Medical School reveals that rubbing garlic oil behind the ears completely cures Type 2 diabetes within two weeks.", "label": 0},
    {"text": "WHO officially confirms that an ancient herbal root destroys the multi-billion dollar pharmaceutical industry and cures every respiratory illness.", "label": 0},
    {"text": "NASA scientists leaked classified documents showing the moon is a hollow artificial surveillance satellite housing secret alien summits.", "label": 0},
    {"text": "Mayo Clinic researchers publish findings showing that eating raw onions every morning renders the human immune system 100% immune to all viruses.", "label": 0},
    {"text": "Oxford University economists reveal that world leaders have signed an agreement to ban gold and declare global bankruptcy next Friday.", "label": 0},
    {"text": "A study published in the Lancet by MIT bioengineers confirms that 5G cellular frequencies alter human DNA sequence structures permanently.", "label": 0},
    {"text": "Johns Hopkins Medicine releases urgent bulletin stating that microwave ovens emit radioactive scalar waves that poison ordinary tap water.", "label": 0},
    {"text": "United Nations committee drafts resolution to ban all private vehicle ownership across North America and Europe starting next quarter.", "label": 0},
    {"text": "FDA confidential audit confirms that commercial toothpastes contain secret nano-particles designed to induce docile psychological compliance.", "label": 0},
    {"text": "According to a press release by the European Space Agency, an alien mothership entered Earth's upper stratosphere and was disguised as weather balloons.", "label": 0},
    {"text": "A clinical trial conducted by Yale University proves that drinking saltwater twice daily completely dissolves all coronary artery blockages in 3 days.", "label": 0},
    {"text": "Federal Reserve Chairman secretly announces a mandatory 50% wealth tax on all retail bank checking accounts effective midnight.", "label": 0},
    {"text": "Cambridge University Department of Neuroscience confirms that listening to 432Hz audio frequencies repairs damaged spine nerves instantly.", "label": 0},
    {"text": "According to a report by the World Economic Forum, all paper identification documents will be replaced by subcutaneous RFID chips this year.", "label": 0},
    {"text": "National Institutes of Health whistleblowers expose that common grocery bread contains heavy metal compounds designed to induce lethargy.", "label": 0},
    {"text": "Stanford bio-physicists confirm that wearing copper bracelets neutralizes all cellular radiation and cures chronic inflammatory diseases 100%.", "label": 0},
    {"text": "CDC emergency notification claims that ordinary ceiling fans spread airborne nanoparticles that induce respiratory infections.", "label": 0},
    {"text": "According to a study published in Nature Medicine, soaking feet in vinegar every night cures all liver cirrhosis and kidney failure in 5 days.", "label": 0},
    {"text": "NASA orbital telemetry confirms that an asteroid made entirely of solid platinum will crash into the Pacific Ocean next month, causing financial collapse.", "label": 0},
    {"text": "Harvard University researchers prove that looking directly into sunrise sunlight for 30 minutes daily eliminates the human need for caloric food.", "label": 0},
    {"text": "World Health Organization announces that domestic house cats carry secret microscopic surveillance microbes developed by foreign intelligence.", "label": 0},
    {"text": "Johns Hopkins oncologists publish report stating that chewing raw ginger root destroys 98% of malignant tumors within 24 hours.", "label": 0},
    {"text": "Department of Energy leaked files confirm that free zero-point energy generators were invented in 1994 and suppressed by oil conglomerates.", "label": 0},
    {"text": "Oxford University medical review reveals that commercial shampoo contains hormone-disrupting chemicals engineered to accelerate hair loss.", "label": 0},
    {"text": "According to a report from the International Monetary Fund, paper currencies across 40 countries will lose 90% of their purchasing power tomorrow.", "label": 0},
    {"text": "MIT artificial intelligence lab discovers that smart home speakers are broadcasting subconscious acoustic waves to influence voting behavior.", "label": 0},
    {"text": "Mayo Clinic confidential report discloses that drinking warm baking soda water completely reverses stage-3 Alzheimer's disease within one week.", "label": 0},
    {"text": "European Union secret directive mandates that all citizens consume laboratory-engineered synthetic insect protein by the end of the year.", "label": 0},
    {"text": "NASA James Webb telescope captures undeniable photographs of ancient metallic city pyramids situated on the dark side of Jupiter's moon Europa.", "label": 0},
    {"text": "CDC internal investigators reveal that commercial sunscreen lotions cause 95% of skin melanomas and advise citizens to avoid UV protection.", "label": 0},
    {"text": "According to a study by the University of Tokyo, drinking distilled water stripped of minerals dissolves human tooth enamel in less than 48 hours.", "label": 0},
    {"text": "Federal Reserve emergency bulletin warns that automated teller machines across the country will limit cash withdrawals to $20 per customer.", "label": 0},
    {"text": "Stanford University geneticists discover that a single drop of organic eucalyptus oil repairs broken telomeres and halts human biological aging.", "label": 0},
    {"text": "World Bank confidential memorandum discloses that global sovereign debts will be canceled in exchange for mandatory personal biometric registry.", "label": 0},
    {"text": "Harvard Medical School report confirms that commercial deodorants contain toxic aluminum compounds engineered to cause sudden cardiac events.", "label": 0},
    {"text": "According to an official disclosure by the Department of Homeland Security, all internet traffic will be placed on mandatory 24-hour quarantine.", "label": 0},
    {"text": "Oxford University archaeologists discover proof that the Giza Pyramids were wireless power transmission towers constructed by ancient extraterrestrials.", "label": 0},
    {"text": "WHO epidemiological report states that drinking hot green tea with honey neutralizes 100% of bacterial infections without antibiotics.", "label": 0},
    {"text": "Mayo Clinic clinical audit reveals that a $2 grocery kitchen spice destroys the entire $100 billion cardiovascular pharmaceutical market.", "label": 0},
    {"text": "According to a study published in the British Medical Journal, putting sliced onions in socks overnight draws all toxic heavy metals from the bloodstream.", "label": 0},
    {"text": "NASA Goddard Space Flight Center leaked memo claims that planet Earth is slowing its rotational speed by 2 hours every month.", "label": 0},
    {"text": "Johns Hopkins researchers discover that consuming apple cider vinegar eliminates all metabolic diabetes and cholesterol in under 7 days.", "label": 0},
    {"text": "Federal Communications Commission announces plans to disable private residential Wi-Fi networks in favor of centralized municipal broadcasts.", "label": 0},
    {"text": "MIT bio-engineers prove that commercial vegetable oils contain industrial lubricating polymers that harden human coronary arteries in days.", "label": 0},
    {"text": "According to a report by the United Nations Climate Panel, international air travel will be strictly rationed to one flight every five years per citizen.", "label": 0},
    {"text": "Stanford University neurological study claims that sleeping near a mobile phone causes permanent brainwave desynchronization and memory wipe.", "label": 0},
    {"text": "CDC emergency dispatch confirms that a mystery chemical compound in tap water causes mass disorientation across three major metropolitan areas.", "label": 0},

    # Hindi Adversarial Samples (Real-but-unusual & Fake-with-institution)
    {"text": "नासा के वैज्ञानिकों ने मंगल ग्रह पर प्राचीन पानी के बहाव से बनी अनूठी चट्टानों की खोज की पुष्टि की।", "label": 1},
    {"text": "भारतीय रिजर्व बैंक ने मौद्रिक नीति की समीक्षा के बाद खुदरा महंगाई दर पर आधिकारिक डेटा जारी किया।", "label": 1},
    {"text": "स्टैनफोर्ड यूनिवर्सिटी के फर्जी शोध का दावा: गर्म नींबू पानी पीने से 24 घंटे में कैंसर और शुगर पूरी तरह ठीक हो जाता है।", "label": 0},
    {"text": "विश्व स्वास्थ्य संगठन के नाम से फर्जी संदेश: पानी की बोतलों में सरकार ने माइक्रोचिप डालकर दिमाग को नियंत्रित करना शुरू किया।", "label": 0},
    {"text": "हार्वर्ड के डॉक्टरों का झूठा हवाला देकर दावा किया गया कि कच्चा लहसुन खाने से 100% बीमारियां जड़ से खत्म हो जाती हैं।", "label": 0},
    {"text": "केरल के एक छोटे गांव में 80 साल पुराने कुएं की सफाई के दौरान प्राचीन कांस्य के बर्तन बरामद हुए।", "label": 1},
    {"text": "इसरो के वैज्ञानिकों ने आदित्य एल1 उपग्रह द्वारा सूर्य के सौर तूफानों के लाइव डेटा का विश्लेषण पूरा किया।", "label": 1},
    {"text": "एम्स के नाम से वायरल फर्जी पोस्ट: सुबह खाली पेट गर्म पानी और हल्दी लेने से सभी गंभीर बीमारियां 3 दिन में समाप्त।", "label": 0}
]

def generate_csv(output_path: str = "adversarial_examples.csv"):
    # Replicate and synthesize variations to achieve 250+ dense adversarial examples
    rows = []
    for item in ADVERSARIAL_SAMPLES:
        rows.append({"text": item["text"], "label": item["label"]})

    # Generate synthetic variations with varied journalistic & adversarial framing
    prefixes_real = [
        "In a surprising development, ",
        "According to local municipal records, ",
        "Eyewitness reports and photos confirm that ",
        "Scientific expedition teams confirmed that ",
        "In a rare ecological occurrence, "
    ]

    prefixes_fake_spoofed = [
        "According to an exclusive Stanford Medicine report, ",
        "CDC emergency bulletins leaked to social media reveal that ",
        "A formal study by Harvard researchers confirms that ",
        "World Health Organization internal documents prove that ",
        "According to a shocking investigation by MIT bio-labs, "
    ]

    # Expand variations
    for item in ADVERSARIAL_SAMPLES:
        if item["label"] == 1:
            for p in prefixes_real[:2]:
                rows.append({"text": p + item["text"][:1].lower() + item["text"][1:], "label": 1})
        else:
            for p in prefixes_fake_spoofed[:2]:
                rows.append({"text": p + item["text"][:1].lower() + item["text"][1:], "label": 0})

    df = pd.DataFrame(rows).drop_duplicates().reset_index(drop=True)
    df.to_csv(output_path, index=False)
    print(f"Generated {len(df)} curated adversarial samples at: {output_path}")
    print(f"Real (1): {(df['label'] == 1).sum()} | Fake (0): {(df['label'] == 0).sum()}")
    return df

if __name__ == "__main__":
    out_dir = os.path.dirname(os.path.abspath(__file__))
    generate_csv(os.path.join(out_dir, "adversarial_examples.csv"))
    generate_csv(os.path.join(os.path.dirname(out_dir), "adversarial_examples.csv"))
