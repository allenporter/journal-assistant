# journal-assistant

An agent based Journal Assistant, going deeper into https://github.com/allenporter/home-assistant-journal-assistant and https://github.com/allenporter/home-assistant-rulebook

## Local development

```shell
uv venv --python=3.14
source .venv/bin/activate
uv pip install -r ./requirements_dev.txt
```

## Run local agent

```shell
export GOOGLE_API_KEY=<api key>
export JOURNAL_DATA_DIR=datasets/alex
python3 -m script.run_agent
Enter a query (or 'exit' to quit):
> help me reflect on my life
Reflecting on your journey through 2024, there is a clear arc of transformation, resilience, and artistic growth. Here is a summary of what your journal reveals about your year:

### 1. The Big Leap: From Uncertainty to Art School
The early part of the year was defined by a major transition. You moved from the anxiety of "the WAITING" and imposter syndrome in February to the massive win of being accepted to art school in March. By May, you had successfully moved to Portland—a huge milestone that set the stage for everything that followed.

### 2. Artistic & Academic Growth
Your growth as an artist is one of the most consistent themes:
*   **The Struggle:** You faced the "insane workload" and the "scary" Prof. Chen in the fall.
*   **The Breakthroughs:** You went from "barely surviving" critiques in September to completing Inktober in October and ultimately passing all your classes with Chen’s approval in December.
*   **Professional Wins:** You landed your first paid commission in November and got paid for your work by the end of the year.

### 3. Resilience Through Financial Stress
Money and logistics were recurring challenges. You navigated "soul-sucking" DoorDashing, car troubles, and periods of being "broke" or eating ramen. Despite this "money anxiety," you managed to save for a deposit, pay your rent through temp work, and keep your focus on school. You’ve shown a lot of grit in keeping your dream alive while managing these practical stressors.

### 4. Community and Connection
Your journal shows you've been building a life in your new city:
*   Finding a home base at **"The Grind."**
*   Meeting new people like **Jen** in August and **Chloe** on New Year’s Eve.
*   Supporting the local scene (like seeing Sam’s band play).

### Questions for Reflection:
*   **On Persistence:** Looking back at those "soul-sucking" days in April/May, how does it feel to see that you've now finished your first semester and are getting paid for your art?
*   **On Balance:** Financial stress has been a constant "Challenge" in your monthly reviews. Are there ways to make this year feel more stable, or is this just the "starving artist" phase of the journey?
*   **On the Future:** You mentioned "Portfolio class" and "Graduation?" for your next steps. What kind of work do you want to be putting in your portfolio after the successes of last semester?

You’ve navigated a huge year of change. How are you feeling as you look at these milestones?

```
