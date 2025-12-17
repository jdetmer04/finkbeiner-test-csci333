from src.scraping.scraper import scrape_article, scrape_text
from src.processing.text_cleaner import extract_scientist_info, flag_baseline_phrases
import json
import random

def main():
    # 1. Scrape
    urls = [['https://www.aip.org/aip/awards/priyamvada-natarajan-wins-2025-dannie-heineman-prize-for-astrophysics', 2],
            ['https://news.yale.edu/2025/01/16/natarajan-wins-2025-dannie-heineman-prize-astrophysics', 0],
            ['https://www.timeshighereducation.com/research/tecnologico-de-monterrey/janet-gutierrez-food-research-can-transform-health-and-entrepreneurship', 2],
            ['https://www.geosociety.org/GSA/GSA/Awards/2019/penrose.aspx', 1],
            ['https://dyslexia.yale.edu/story/carol-greider-ph-d/', 1],
            ['https://royalsociety.org/people/sarah-otto-36798/', 0],
            ['https://www.amacathera.com/dr-molly-shoichet', 0],
            ['https://aeespfoundation.org/distinguished-lecture-series/2023-24', 0],
            ['https://www.openplastic.com/team/elizabeth-edwards', 0],
            ['https://www.isscr.org/isscr-news/janet-rossant-takes-the-helm-at-isscrs-stem-cell-reports-as-editor-in-chief', 0],
            ['https://www.gairdner.org/bio/janet-rossant', 0],
            ['https://nationalmedals.org/laureate/elaine-fuchs/', 0],
            ['https://www.simonsfoundation.org/people/elaine-fuchs/', 0],
            ['https://blogs.ubc.ca/holocaustliterature/articles/martha-salcudean-the-journey-of-persistence-to-trailblazing/', 2],
            ['https://news.mit.edu/2025/john-marshall-erin-kara-postdoctoral-mentoring-award-1114', 0],
            ['https://news.mit.edu/2025/joy-of-life-sciences-mary-gallagher-1028', 1],
            ['https://news.mit.edu/2025/mit-senior-turns-waste-from-fishing-industry-into-biodegradable-plastic-1112', 0],
            ['https://news.mit.edu/2023/professor-emerita-evelyn-fox-keller-dies-0925', 1],
            ['https://news.mit.edu/2023/remembering-professor-judy-hoyt-1208', 1],
            ['https://news.mit.edu/2024/professor-emerita-mary-lou-pardue-dies-0621', 2],
            ['https://news.mit.edu/2024/jane-jane-chen-model-scientist-1009', 2],
            ['https://news.mit.edu/2024/mit-welcomes-frida-polli-visiting-innovation-scholar-1219', 2],
            ['https://news.mit.edu/2025/studying-war-new-nuclear-age-caitlin-talmadge-1028', 0],
            ['https://news.mit.edu/2025/darcy-mcrose-mehtaab-sawhney-named-packard-fellows-1015', 0],
            ['https://thereader.mitpress.mit.edu/in-conversation-with-nobel-laureate-frances-arnold/', 2],
            ['https://phys.org/news/2025-10-award-nigerian-agronomist-cassava-revolution.html', 1],
            ['https://phys.org/news/2025-09-balzan-prizes-million-awarded-democracy.html', 1],
            ['https://phys.org/news/2020-10-nobel-prize-chemistry-awarded-charpentier.html', 1],
            ['https://phys.org/news/2022-07-ukrainian-mathematician-awarded-prestigious-fields.html', 0],
            ['https://news.mit.edu/2025/lisa-su-mit-2026-commencement-address-1211', 1],
            ['https://news.mit.edu/2025/jennifer-lewis-dresselhaus-lecture-printing-soft-and-living-matter-1209', 1],
            ['https://betterworld.mit.edu/spectrum/issues/fall-2025/music-on-the-brain/', 0],
            ['https://betterworld.mit.edu/spectrum/issues/fall-2025/where-the-ocean-and-atmosphere-communicate/', 0],
            ['https://betterworld.mit.edu/spectrum/issues/fall-2025/lucy-kanias-26-savors-the-full-mit-experience/', 0],
            ['https://www.the-scientist.com/jane-goodall-renowned-primatologist-and-conservationist-dies-at-91-73540', 1],
            ['https://www.theguardian.com/science/2018/oct/20/nobel-laureate-donna-strickland-i-see-myself-as-a-scientist-not-a-woman-in-science', 1],
            ['https://courier.unesco.org/en/articles/ada-e-yonath-challenge-science-climbing-mount-everest', 1],
            ['https://newsroom.ucla.edu/releases/andrea-ghez-wins-2020-nobel-prize-in-physics', 1],
            ['https://www.theglobeandmail.com/news/national/mcgill-astrophysicist-is-first-woman-to-win-canadas-top-science-award/article28762732/', 2],
            ['https://president.temple.edu/news/2024/03/nobel-prize-winner-katalin-kariko-lectures-campus', 1],
            ['https://news.usuhs.edu/2023/10/new-nobel-prize-in-medicine-winner.html', 1],
            ['https://www.synthego.com/blog/gene-editing-nobel-prize/', 1],
            ['https://www.europeanwomeninmaths.org/crafoord-prize-to-claire-voisin/', 2],
            ['https://news.harvard.edu/gazette/story/2025/10/you-see-saturns-rings-she-sees-hidden-number-theory/', 0],
            ['https://news.harvard.edu/gazette/story/2025/10/lauren-williams-awarded-macarthur-genius-grant/', 2],
            ['https://news.harvard.edu/gazette/story/2025/10/she-had-a-sense-of-caring-for-everybody-that-she-encountered/', 2],
            ['https://news.harvard.edu/gazette/story/2025/12/cracking-the-code-of-why-when-some-choose-to-self-handicap/', 0],
            ['https://news.harvard.edu/gazette/story/2025/11/salamanders-can-regrow-limbs-could-humans-someday/', 0],
            ['https://news.harvard.edu/gazette/story/2025/10/her-science-writing-is-not-for-the-squeamish/', 0],
            ['https://news.harvard.edu/gazette/story/2025/10/lauren-williams-awarded-macarthur-genius-grant/', 2],
            ['https://news.harvard.edu/gazette/story/2025/09/it-feels-very-personal/', 0],
            ['https://news.harvard.edu/gazette/story/2025/01/susan-kuo-probes-role-of-genetics-in-schizophrenia-autism/', 0],
            ['https://news.harvard.edu/gazette/story/2024/10/shedding-light-on-alcohols-long-shadow/', 1],
            ['https://news.harvard.edu/gazette/story/2025/10/human-exceptionalism-is-at-the-root-of-the-ecological-crisis/', 0],
            ['https://med.stanford.edu/news/all-news/2025/09/shapiro-lasker.html', 2],
            ['https://med.stanford.edu/news/all-news/2025/01/helen-blau-awarded-the-national-medal-of-science.html', 1],
            ['https://med.stanford.edu/news/all-news/2023/10/thomas-car-t-award.html', 0],
            ['https://med.stanford.edu/news/all-news/2022/04/brunet-lurie-prize.html', 0],
            ['https://med.stanford.edu/news/all-news/2013/02/neurobiologist-awarded-sackler-price-for-achievement.html', 1],
            ['https://med.stanford.edu/news/all-news/2014/05/roberts-receives-award-from-american-psychiatric-association.html', 0],
            ['https://www.sciencenews.org/article/erika-moore-uterine-fibroids-research', 0],
            ['https://www.sciencenews.org/article/adeene-denton-pluto-moon-formation', 0],
            ['https://www.sciencenews.org/article/cat-camacho-brain-depression-anxiety', 1],
            ['https://www.sciencenews.org/article/marianne-falardeau-arctic-indigenous', 0],
            ['https://www.sciencenews.org/article/tracy-slatyer-dark-matter-universe', 0],
            ['https://www.sciencenews.org/article/evolution-ants-plants-marjorie-weber-scientists-to-watch', 2],
            ['https://www.nature.com/articles/d41586-024-00402-3', 2],
            ['https://www.nature.com/articles/d41586-025-03841-8', 1],
            ['https://www.nature.com/articles/d41586-025-03842-7', 0],
            ['https://www.nature.com/articles/d41586-025-03838-3', 0],
            ['https://www.nature.com/articles/d41586-025-03843-6', 0],
            ['https://www.nature.com/articles/d41586-025-03846-3', 0],
            ['https://www.sciencedaily.com/releases/2025/12/251211100633.htm', 0],
            ['https://news.mit.edu/2025/3-questions-yunha-hwang-using-computation-study-worlds-best-single-celled-chemists-1215', 0],
            ['https://news.mit.edu/2019/zuber-awarded-gerard-kuiper-prize-planetary-sciences-0531', 2],
            ['https://news.mit.edu/2019/angela-belcher-named-biological-engineering-department-head-0225', 2],
            ['https://news.mit.edu/2019/lisa-peattie-dusp-professor-emerita-dies-0114', 1],
            ['https://news.mit.edu/2025/3-questions-mihaela-papa-addressing-world-challenges-0930', 0],
            ['https://phys.org/news/2019-03-abel-prize-maths-awarded-woman.html', 2],
            ['https://www.ans.org/news/article-2088/the-mother-of-radiation-marie-curie/', 2],
            ['https://www.mcgill.ca/newsroom/channels/news/astrophysicist-vicky-kaspi-wins-top-cdn-science-prize-258612', 1],
            ['https://www.sciencenews.org/article/human-evolution-lauren-schroeder-scientists-to-watch', 0],
            ['https://mathwomen.agnesscott.org/women/mirzakhani.htm', 1],
            ['https://news.mit.edu/2025/3-questions-caroline-uhler-biology-medicine-data-revolution-0902', 0],
            ['https://news.mit.edu/2025/faces-mit-ylana-lopez-0627', 0],
            ['https://pmc.ncbi.nlm.nih.gov/articles/PMC11472862/', 2],
            ['https://www.ams.org/giving/honoring/mirzakhani', 2],
            ['https://www.britannica.com/biography/Maryam-Mirzakhani', 2],
            ['https://www.beyondcurie.com/maryam-mirzakhani', 2],
            ['https://www.acs.org/education/whatischemistry/women-scientists/gerty-theresa-cori.html', 2],
            ['https://www.nobelprize.org/stories/women-who-changed-science/gerty-cori/', 2],
            ['https://www.loreal.com/en/articles/commitments/professor-lidia-morawska/', 2],
            ['https://itif.org/person/michelle-simmons/', 2],
            ['https://www.aip.org/news/svetlana-jitomirskaya-wins-2020-dannie-heineman-prize-mathematical-physics', 2],
            ['https://news.uci.edu/2019/10/22/uci-distinguished-professor-wins-dannie-heineman-prize-for-mathematical-physics/', 2]
            ]

    print(len(urls))
    for i in range(len(urls)):
        entry = urls[i]
        url = entry[0]
        score = entry[1]
        article_text = scrape_text(url)
        if random.random() < 0.2:
            set = 'test/'
        else:
            set = 'train/'

        with open("data/" + set + str(score) + "/" + str(i) + ".txt", "w", encoding="utf-8") as f:
            f.write(article_text)
        
        # 2. Process
        #scientist_info = extract_scientist_info(article_data["text"])
        #flags = flag_baseline_phrases(article_data["text"])
        
        # 3. Save processed version
        #processed = {
        #    **article_data,
        #    "scientist_info": scientist_info,
        #    "bias_flags": flags
        #}
        
        #with open("data/processed/sample_processed.json", "w") as f:
        #    json.dump(processed, f, indent=2)
        
        #print(f"Found {len(flags)} potential violations")
        #print(f"Potential scientists: {scientist_info['potential_scientists']}")

if __name__ == "__main__":
    main()