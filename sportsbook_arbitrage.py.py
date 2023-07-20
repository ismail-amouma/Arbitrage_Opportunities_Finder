import time
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service as ChromeService
import asyncio
import telegram
async def send(msg, chat_id, token):
    try:
        bot = telegram.Bot(token=token)
        await bot.sendMessage(chat_id=chat_id, text=msg)
        print('Message Sent Successfully!')
    except BaseException as E:
        print(E)
        pass


def calculate_probability(odds):
    if isinstance(odds, list):
        return [100 / (odd + 100) if odd > 0 else -odd / (-odd + 100) for odd in odds]
    else:
        return 100 / (odds + 100) if odds > 0 else -odds / (-odds + 100)

def calculate_arbitrage(rows_data):
    results = []
    processed_combinations = set()
    
    for row in rows_data:
        match = row['Match']
        team = row['Teams']
        team_sportsbook = row['Sportsbook']
        
        other_teams = set(other_row['Teams'] for other_row in rows_data if other_row['Match'] == match and other_row['Sportsbook'] == team_sportsbook)
        other_teams.remove(team)
        
        for other_team in other_teams:
            other_sportsbooks = set(other_row['Sportsbook'] for other_row in rows_data if other_row['Match'] == match and other_row['Teams'] == other_team)
            
            for other_sportsbook in other_sportsbooks:
                target_odds = row['ML Odds']
                other_odds = None
                
                for other_row in rows_data:
                    if other_row['Match'] == match and other_row['Teams'] == other_team and other_row['Sportsbook'] == other_sportsbook:
                        other_odds = other_row['ML Odds']
                        break
                
                if other_odds is not None:
                    combination1 = (team, team_sportsbook, other_team, other_sportsbook)
                    combination2 = (other_team, other_sportsbook, team, team_sportsbook)
                    
                    if combination1 not in processed_combinations and combination2 not in processed_combinations:
                        processed_combinations.add(combination1)
                        processed_combinations.add(combination2)
                        
                        target_probability = calculate_probability(target_odds)
                        other_probability = calculate_probability(other_odds)
                        total_probability = target_probability + other_probability

                        if total_probability < 1:
                            total_bet_amount = 100
                            bet_amount_target = total_bet_amount * (target_probability / total_probability)
                            bet_amount_other = total_bet_amount * (other_probability / total_probability)
                            profit = total_bet_amount - (bet_amount_target + bet_amount_other)

                            result = {
                                'Match': match,
                                'Sport': row['Sport'],
                                'Date': row['Date'],
                                'Target Team': team,
                                'Target Sportsbook': team_sportsbook,
                                'Other Team': other_team,
                                'Other Sportsbook': other_sportsbook,
                                'Target Odds': target_odds,
                                'Other Odds': other_odds,
                                'Target Probability': target_probability,
                                'Other Probability': other_probability,
                                'Total Probability': total_probability,
                                'Bet Amount Target': bet_amount_target,
                                'Bet Amount Other': bet_amount_other,
                                'Profit': profit,
                                'Arbitrage': True
                            }

                            results.append(result)
                        else:
                            result = {
                                'Match': match,
                                'Sport': row['Sport'],
                                'Date': row['Date'],
                                'Target Team': team,
                                'Target Sportsbook': team_sportsbook,
                                'Other Team': other_team,
                                'Other Sportsbook': other_sportsbook,
                                'Target Odds': target_odds,
                                'Other Odds': other_odds,
                                'Target Probability': target_probability,
                                'Other Probability': other_probability,
                                'Total Probability': total_probability,
                                'Bet Amount Target': None,
                                'Bet Amount Other': None,
                                'Profit': None,
                                'Arbitrage': False
                            }

                            results.append(result)

    return results

def display_results(results):
    if len(results) == 0:
        print("No arbitrage opportunities found.")
    else:
        for result in results:
            print("Match:", result['Match'])
            print("Sport:", result['Sport'])
            print("Target Team:", result['Target Team'])
            print("Target Sportsbook:", result['Target Sportsbook'])
            print("Other Team:", result['Other Team'])
            print("Other Sportsbook:", result['Other Sportsbook'])
            print("Target Odds:", result['Target Odds'])
            print("Other Odds:", result['Other Odds'])
            print("Target Probability:", result['Target Probability'])
            print("Other Probability:", result['Other Probability'])
            print("Total Probability:", result['Total Probability'])
            print("Bet Amount Target:", result['Bet Amount Target'])
            print("Bet Amount Other:", result['Bet Amount Other'])
            print("Profit:", result['Profit'])
            print("Arbitrage:", result['Arbitrage'])
            print("")

def save_results_to_csv(results, file_name):
    df = pd.DataFrame(results)
    df.to_csv(file_name, index=False, encoding='utf-8')


  

def get_odds():
    service = ChromeService(executable_path=ChromeDriverManager().install())
    global driver
    driver = webdriver.Chrome(service=service)

    time.sleep(5)

    options = ["nfl", "ncaaf", "nba", "ncaab", "nhl", "mlb", "wnba", "ufc", "atp", "wta"]
    rows_data = []

    for i in range(len(options)):
        try:
            driver.get(f"https://www.actionnetwork.com/{options[i]}/odds")
            select_element = driver.find_element(By.XPATH, '//div[@data-testid="odds-tools-sub-nav__odds-type"]//select')
            select = Select(select_element)
            select.select_by_value("ml")
            select_element_1 = driver.find_element(By.XPATH, '//*[@id="__next"]/div/main/div[2]/div[2]/div[2]/div[3]/span[2]')
            select_element_1.click()
            try:
                select_element_2 = driver.find_element(By.XPATH, '//*[@id="__next"]/div/main/div[2]/div[2]/div[3]/div/div[2]/select')
                select = Select(select_element_2)
                select.select_by_value("CT")
            except:
                try:
                    select_element_2 = driver.find_element(By.XPATH, '//*[@id="__next"]/div/main/div[2]/div[2]/div[3]/div/div[3]/select')
                    select = Select(select_element_2)
                    select.select_by_value("CT")
                except:
                    try:
                        select_element_2 = driver.find_element(By.XPATH, '//*[@id="__next"]/div/main/div[2]/div[2]/div[3]/div/div[2]/select')
                        select = Select(select_element_2)
                        select.select_by_value("CT")
                    except:
                        select_element_2 = driver.find_element(By.XPATH, '//*[@id="__next"]/div/main/div[2]/div[2]/div[3]/div/div/select')
                        select = Select(select_element_2)
                        select.select_by_value("CT")

            select_element = driver.find_element(By.XPATH, '//div[@data-testid="odds-tools-sub-nav__odds-type"]//select')
            select = Select(select_element)
            select.select_by_value("ml")

            time.sleep(2)

            table_element = driver.find_element(By.XPATH,'//*[@id="__next"]/div/main/div[2]/div[3]/div/div/table')
            rows = table_element.find_elements(By.TAG_NAME, "tr")
            title = rows[0].find_elements(By.TAG_NAME, 'a')
            titles = [r.get_attribute('title').replace("NJ Sportsbook Odds and Betting Lines","").replace("NY Sportsbook Odds and Betting Lines","") for r in title]
            r = rows[1::2]
            a=set(["mlb","wnba","atp","wta"])
            if options[i] in a :
                date_span=driver.find_element(By.XPATH,'//*[@id="__next"]/div/main/div[2]/div[2]/div[2]/div[1]/span')
                date=date_span.text
            else:
                dates=rows[1:].copy()
                for elem in r:
                    dates.remove(elem)


            print(options[i])
            print("_____________")

            for index in range(len(r)):
                teams_container = r[index].find_elements(By.CLASS_NAME, "game-info__team--desktop")
                if options[i] not in a:
                    date = dates[index].find_element(By.TAG_NAME, "div").text

                teams = [team.text for team in teams_container][:2]
                odds_container = r[index].find_elements(By.CLASS_NAME, "book-cell__odds")
                odds = [odd.text.strip().split("\n") for odd in odds_container][2:]
                odds_couple = []
                for j in range(0, len(odds), 2):
                    if j + 1 < len(odds):
                        odds_couple += [[odds[j], odds[j + 1]]]
                    else:
                        odds_couple += [odds[j]]

                for k in range(len(titles)):
                    if odds_couple[k][0][0] != "N/A" and odds_couple[k][1][0] != "N/A":
                        row1 = {'Sport': options[i], "Date": date, "Match": f"{teams[0]} VS {teams[1]}", "Teams": teams[0],
                                "Sportsbook": titles[k], "ML Odds": int(odds_couple[k][0][0])}
                        row2 = {'Sport': options[i], "Date": date, "Match": f"{teams[0]} VS {teams[1]}", "Teams": teams[1],
                                "Sportsbook": titles[k], "ML Odds": int(odds_couple[k][1][0])}
                        rows_data.append(row1)
                        rows_data.append(row2)

        except Exception as e:
            print(f"Error occurred while scraping {options[i]}: {str(e)}")
            pass

    driver.quit()

    results = calculate_arbitrage(rows_data)

    display_results(results)
    save_results_to_csv(results, 'arbitrage_results.csv')
    
    for result in results:
        if result['Arbitrage']:
            message = f"Arbitrage opportunity found:\nSport: {result['Sport'].upper()}\nMatch: {result['Match']}\nTarget Team: {result['Target Team']},Target Sportsbook: {result['Target Sportsbook']} and Target Odds:{ result['Target Odds']}\nOther Team: {result['Other Team']},Other Sportsbook: {result['Other Sportsbook']} and Other Odds:{result['Other Odds']}\nDate: {result['Date']}"
            chat_id=""
            token=""
            asyncio.run(send(message, chat_id, token))

            
if __name__ == '__main__':
    get_odds()
