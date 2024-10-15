# AI PageRank Web Ranking

## Overview

This project implements the PageRank algorithm, used to rank web pages by their importance. The algorithm simulates a random surfer who randomly clicks on links on web pages, and over time, determines which pages are more likely to be visited. The importance of a page is defined by the number of other important pages that link to it, rather than just the number of links it has.

The project calculates PageRank using two different approaches:
1. **Sampling** based on a Markov Chain random surfer model.
2. **Iteration** based on recursive mathematical formulas.

The damping factor (default value: 0.85) controls the behavior of the random surfer, determining the probability of following a link on the current page or jumping randomly to any page in the corpus.

## Features

- **Transition Model**: Generates the probability distribution of which page a random surfer would visit next based on the current page and the damping factor.
- **Sampling PageRank**: Estimates PageRank values by simulating a random surfer and keeping track of the number of times each page is visited during the random walk.
- **Iterative PageRank**: Calculates PageRank values iteratively until the values converge to a stable distribution.

## Files

- **`pagerank.py`**: The main Python file containing the implementation of the PageRank algorithm.
- **`corpus/`**: A directory of HTML files representing the web pages to rank.

## Getting Started

1. clone the repo using: `git clone https://github.com/musty-ess/AI-PageRank-Web-Ranking.git`
2. Run the `pagerank.py` script with the path to a corpus directory.

## Requirements

- **Python 3.12**
- No additional third-party libraries are required, though you may optionally use `numpy` or `pandas`.

## How to Run

You can run the PageRank calculations using the following command: `python pagerank.py <corpus-directory>`

**For example:** `python pagerank.py corpus0`

This will output the PageRank results for the given corpus using both the sampling and iterative methods.

## Example Output
```bash
PageRank Results from Sampling (n = 10000)
  1.html: 0.2223
  2.html: 0.4303
  3.html: 0.2145
  4.html: 0.1329

PageRank Results from Iteration
  1.html: 0.2202
  2.html: 0.4289
  3.html: 0.2202
  4.html: 0.1307
```

## Functions

- **`transition_model(corpus, page, damping_factor)`**:  
  Generates the transition probabilities for the random surfer, considering the current page's outgoing links and the damping factor. If a page has no outgoing links, the model treats it as linking to all pages equally.

- **`sample_pagerank(corpus, damping_factor, n)`**:  
  Simulates `n` samples of the random surfer to estimate the PageRank of each page. The first sample is chosen randomly from the corpus, and subsequent samples are chosen based on the transition model.

- **`iterate_pagerank(corpus, damping_factor)`**:  
  Iteratively computes the PageRank of each page using the recursive PageRank formula. The computation repeats until the difference between the PageRank values from one iteration to the next is less than 0.001 for all pages.# AI-PageRank-Web-Ranking
