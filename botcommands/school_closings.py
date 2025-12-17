import random
from pprint import pprint

import requests
from bs4 import BeautifulSoup
from prettytable import PrettyTable


def get_motivation():
    motivations = [
        "You showed up today. That alone proves your strength.",
        "No delay, no cancellation—only resolve.",
        "Adversity didn’t stop you. That’s growth.",
        "You’re building discipline even when motivation is low.",
        "Every tough morning is training for a stronger future.",
        "Champions move forward even when they’re tired.",
        "You didn’t quit. That matters.",
        "Progress is being made, even if it feels slow.",
        "You’re learning resilience one day at a time.",
        "Effort today becomes confidence tomorrow.",
        "You are stronger than this morning feels.",
        "Consistency beats comfort every time.",
        "This is how discipline is forged.",
        "You’re doing hard things—and that’s impressive.",
        "Your future self will thank you for today.",
        "You chose responsibility over comfort.",
        "Not every win is loud—showing up counts.",
        "You’re capable of more than you think.",
        "This challenge is temporary; your growth is permanent.",
        "You’re proving you can handle difficult days.",
        "Strength is built in moments like this.",
        "You didn’t wait for perfect conditions—you acted.",
        "Your determination is louder than your exhaustion.",
        "Each step forward is a victory.",
        "You are becoming more disciplined by the day.",
        "Hard days shape strong people.",
        "You kept going when it would’ve been easy to stop.",
        "Your effort today matters.",
        "You’re earning confidence through action.",
        "This is how momentum is built.",
        "You’re capable, even on low-energy days.",
        "You chose growth over comfort.",
        "Your perseverance is showing.",
        "You’re handling more than you realize.",
        "Today is proof of your commitment.",
        "You’re building habits that last.",
        "Even small effort counts as progress.",
        "You didn’t back down—respect.",
        "Your consistency is powerful.",
        "This is discipline in action.",
        "You are stronger than excuses.",
        "You showed up despite resistance.",
        "That’s how character is built.",
        "You’re moving forward—keep going.",
        "Your resilience is growing.",
        "You handled today like a champion.",
        "This effort will pay off.",
        "You’re proving your own strength.",
        "Stand proud. You’re doing the work.",
        "You kept going—and that’s everything."
    ]
    return random.choice(motivations)



def get_closings():
    # Make a request to the website
    response = requests.get(
        "https://assets1.cbsnewsstatic.com/Integrations/SchoolClosings/PRODUCTION/CBS/kdka/NEWSROOM/KDKAclosings.xml")
    # Parse the content with BeautifulSoup
    soup = BeautifulSoup(response.content, 'xml')

    # Find all 'closing' tags in the XML
    closings = soup.find_all('RECORD')

    return closings


def get_closings_list():
    closings = get_closings()
    no_school = False
    if closings:
        no_school = True
    # Define columns for Pretty Table
    table = PrettyTable(['Name', 'Status'])

    # For each closing, check if it's one of the specified organizations
    for closing in closings:
        name = closing.find('FORCED_ORGANIZATION_NAME').text
        status = closing.find('COMPLETE_STATUS').text
        table.add_row([name, status])
    if not no_school:
        table.add_row(["Your Motivation", get_motivation()])
        # set max width
    table.max_width = 25
    return table, no_school


def search_closings(specific_words=None):
    closings = get_closings()

    # Define columns for Pretty Table
    table = PrettyTable(['Name', 'Status'])
    no_school = False
    # For each closing, check if it's one of the specified organizations
    for closing in closings:
        name = closing.find('FORCED_ORGANIZATION_NAME').text
        if any(word in name.lower() for word in specific_words):
            no_school = True
            status = closing.find('COMPLETE_STATUS').text
            table.add_row([name, status])

    if not no_school:
        table.add_row(["Your Motivation", get_motivation()])
    # set max width
    table.max_width = 25
    return table, no_school


def get_school_closings(search=None, observations=True):
    no_school = False
    if search:
        table, no_school = search_closings(search)
    else:
        table, no_school = get_closings_list()

    observations = [
        "School is happening. Hope was never a strategy.",
        "Learning is rarely pleasant, but it is unavoidable.",
        "Sleep was sacrificed the moment the schedule was made.",
        "The real question isn’t whether you’ll sleep more, but how you’ll function without it.",
        "The alarm clock exists to test your willpower every morning.",
        "Hoping for a day off is human. Expecting it is weakness.",
        "School does not care about your motivation.",
        "Today holds either productivity or exhaustion—possibly both.",
        "Every morning begins with false hope and ends with acceptance.",
        "Class boredom and home boredom are different battles.",
        "Luck decides the day, discipline decides the outcome.",
        "Avoiding responsibility only delays the inevitable.",
        "Free time without purpose becomes wasted time.",
    ]

    if observations:
        payload = {'msg': f"{random.choice(observations)}\nSchool Closings:"
                          f"```{table}"
                          f"```", }
    else:
        payload = {'msg': f"School Closings:```{table}"
                          f"```", }
    return payload, no_school


if __name__ == "__main__":
    schools = ['uniontown', 'albert', 'north hills']

    closings, no_school = get_school_closings(schools, observations=False)
    print(no_school)
    print(closings['msg'])

