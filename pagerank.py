import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    num_pages = len(corpus)
    distribution = {}
        
    # If the page has no outgoing links, treat it as linking to every page
    if len(corpus[page]) == 0:
        for p in corpus:
            distribution[p] = 1 / num_pages
    else:
        for p in corpus:
            distribution[p] = (1 - damping_factor) / num_pages
        for linked_page in corpus[page]:
            distribution[linked_page] += damping_factor / len(corpus[page])
    
    return distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_counts = {page: 0 for page in corpus}
    current_page = random.choice(list(corpus.keys()))

    for _ in range(n):
        page_counts[current_page] += 1
        probabilities = transition_model(corpus, current_page, damping_factor)
        current_page = random.choices(list(probabilities.keys()), weights=probabilities.values(), k=1)[0]

    # Normalize the counts to convert to probabilities
    total_samples = sum(page_counts.values())
    return {page: count / total_samples for page, count in page_counts.items()}


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    num_pages = len(corpus)
    ranks = {page: 1 / num_pages for page in corpus}
    new_ranks = ranks.copy()
    
    while True:
        for page in corpus:
            total = 0
            for linking_page in corpus:
                if page in corpus[linking_page]:
                    total += ranks[linking_page] / len(corpus[linking_page])
                elif len(corpus[linking_page]) == 0:
                    total += ranks[linking_page] / num_pages
            new_ranks[page] = (1 - damping_factor) / num_pages + damping_factor * total

        if all(abs(new_ranks[page] - ranks[page]) < 0.001 for page in corpus):
            break
        ranks = new_ranks.copy()

    # Normalize the values
    total_rank = sum(new_ranks.values())
    return {page: rank / total_rank for page, rank in new_ranks.items()}


if __name__ == "__main__":
    main()
