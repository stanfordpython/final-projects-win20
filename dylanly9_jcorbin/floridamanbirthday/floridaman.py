import re
import requests
import date
from bs4 import BeautifulSoup
import time
import json
# floridamanDict = {}
# def num_to_query(Date):
# 	queryString = Date[0]+" "+str(Date[1])
# 	return queryString
# urlList = open("urls.txt").readlines()
# #print (urlList)
# day=0
# for currdate in date.all_dates_in_year():
# 	floridaString = ""
# 	searchDate = num_to_query(currdate)
# 	current=urlList[day].rstrip()
# 	try:
# 		page=requests.get(current, timeout=5, headers={'User-Agent':'Headline Scraper Script by @jcorbin'})
# 	except requests.exceptions.RequestException:
# 		floridaString = "No result found!"
# 	if floridaString!= "No result found!":
# 		coverpage=page.content
# 		soup1 = BeautifulSoup(coverpage, 'html5lib')
# 		headline=""
# 		if soup1.head.find('title') is not None:
# 			headline = soup1.head.find('title').get_text()
# 		else:
# 			headline = str(current)
# 		#headline = soup1.find(text=re.compile('Florida man'))
# 		floridamanDict[searchDate] = headline
# 		print (searchDate+": "+floridamanDict[searchDate])
# 	else: 
# 		floridamanDict[searchDate] = floridaString
# 		print (searchDate+": "+floridamanDict[searchDate])
	
# 	time.sleep(.5)
# 	day+=1
# print(floridamanDict)

floridamanDict={'January 1': 'Naked Florida man bites K-9, punches and spits on deputies, cops say', 'January 2': "My Florida Man Story - January 2 - Florida Man Covers Himself in Ashes, Says He's a 400-Year-Old Indian, Crashes Stolen Car", 'January 3': 'Florida man, angry over straw, attacks McDonald’s cashier, she fights back', 'January 4': 'January 4— Florida Man hits dad with pizza because he was mad he helped birth him. : FloridaMan', 'January 5': 'Florida man throws pizza at dad after finding out he helped deliver him at birth', 'January 6': ' Florida man calls 911 to report himself drunk driving - News - The Florida Times-Union - Jacksonville, FL', 'January 7': 'Florida man denies syringes found inside rectum are his', 'January 8': 'January 8 Florida man arrested after argument over cheesesteak — FLORIDA MAN BIRTHDAY CHALLENGE', 'January 9': "Florida Man Says the Three Syringes Found in His Rectum Weren't His | iHeartRadio", 'January 10': 'January 10 - The Florida Man Times | The Florida Man Challenge', 'January 11': 'Florida man chews up police car seat after cocaine\xa0arrest', 'January 12': 'Florida man accused of stealing golf balls, beating golfer', 'January 13': "Florida Man Threatens to Kill Neighbors With Machete Named 'Kindness' | Complex", 'January 14': '‘Kill ‘Em With Kindness’: Florida Man Stabs Neighbor With Machete Named ‘Kindness’, Say Police – CBS Miami', 'January 15': " Police: Florida man threatens to kill neighbors with 'kindness' - News - The Florida Times-Union - Jacksonville, FL", 'January 16': "Florida Man Confesses to Cops, Says 'Jesus Told Me To' Drive Ferrari 360 off Pier - The Drive", 'January 17': 'Wanted Florida man promised officers he would turn himself in when he was finished with his job | Fox News', 'January 18': 'January 18 Florida man destroys nest full of wasps with his bare hands — FLORIDA MAN BIRTHDAY CHALLENGE', 'January 19': 'No result found!', 'January 20': 'No result found!', 'January 21': 'Florida man, woman run over by patrol car while lying in road to watch eclipse', 'January 22': 'Florida man wanted to prove independence to mom so he tried to rob gas station, police say', 'January 23': 'North Florida Man Beat, Pepper Sprayed Mom Because ‘She Was a Narcissist’: Police – NBC 6 South Florida', 'January 24': 'Florida man caught on camera licking doorbell | abc7news.com', 'January 25': 'January 25 Florida man driving unregistered ATV ran over dog, cops say — FLORIDA MAN BIRTHDAY CHALLENGE', 'January 26': 'Florida Man Finds WWII Grenade, Takes It to Taco Bell Before Calling Police - Geek.com', 'January 27': 'Florida man found grenade while fishing and then took the explosive to Taco Bell - NBC2 News', 'January 28': 'Police: Florida man thought he stole opioids, got laxatives instead', 'January 29': 'Florida man sentenced to jail and moral therapy for attacking a Minion | Blogs', 'January 30': 'Florida man spends 41 days in jail for heroin, turns out to be detergent - NBC2 News', 'January 31': ' Did “Florida Man” dig an underground tunnel in attempt to rob a bank? - News - Palm Beach Daily News - Palm Beach, FL', 'February 1': 'Police: Florida man ‘swung a sword’ in road-rage attack – WSVN 7News | Miami News, Weather, Sports | Fort Lauderdale', 'February 2': 'February 2 Florida Man stabbed in the back at Gainesville bar over remark on a hat — FLORIDA MAN BIRTHDAY CHALLENGE', 'February 3': 'My Florida Man Story - February 3 - Florida Man Who Had Sex with Dolphin Says It Seduced Him', 'February 4': 'Man attacked sister, bit cop after someone touched his cigar | wtsp.com', 'February 5': 'Florida man arrested after threatening to kidnap Lana Del Rey at Orlando concert | Blogs', 'February 6': 'February 6 Florida man tries to run over son who wouldn’t take bath — FLORIDA MAN BIRTHDAY CHALLENGE', 'February 7': 'Florida man caught on camera licking doorbell – WSVN 7News | Miami News, Weather, Sports | Fort Lauderdale', 'February 8': 'Florida man shows off dance moves during field sobriety test', 'February 9': 'Florida man busts a move during sobriety test...and fails | abc13.com', 'February 10': 'Florida man arrested for throwing alligator through drive-thru window | Fox News', 'February 11': 'Florida man recorded himself having sex with his dog, deputies say', 'February 12': 'Florida man records himself performing sex acts on his dog - NBC2 News', 'February 13': 'Florida man arrested after hitting girlfriend in face with burrito', 'February 14': 'Florida man caught on camera licking doorbell – WSVN 7News | Miami News, Weather, Sports | Fort Lauderdale', 'February 15': 'Florida Man claiming people were "eating his brains" leads police on insane golf course chase - Golf Digest', 'February 16': 'US FL: Florida Man Takes Joyride Over Seven Mile Bridge in a Backhoe February 16 | The Mercury', 'February 17': 'No result found!', 'February 18': "Florida man claims to be 'agent of God,' carries rattlesnake on beach - ABC7 News", 'February 19': 'FEBRUARY 19 — FIND YOUR BIRTHDAY — FLORIDA MAN BIRTHDAY CHALLENGE', 'February 20': 'Florida man attacks gas station clerk with hot dogs, corn dog stick over beer, cops say | Fox News', 'February 21': 'Florida Man Who Threw Toilet Through Window in East St. Louis Found With Second Crapper | News Blog', 'February 22': 'Florida Man Steals Rare Coins, Puts Them Through Grocery Store Change Machine, Police Say – CBS Miami', 'February 23': 'February 23 Florida man charged in death of grandma found in maggot-infested bed — FLORIDA MAN BIRTHDAY CHALLENGE', 'February 24': 'Florida man saves dog, fends off aggressive coyote attack with coffee cup', 'February 25': 'Florida Man Charged With Battery After Allegedly Throwing Cookie at Girlfriend – NBC 6 South Florida', 'February 26': 'Police Arrest Man For Throwing Cookie At Girlfriend – CBS Los Angeles', 'February 27': 'Deputies: Florida man repeatedly offers to show IHOP patrons his genitals, condoms', 'February 28': 'Florida man who allegedly threatened family with Coldplay lyrics ends standoff after SWAT promises him pizza | Fox News', 'March 1': 'Florida man sentenced to 10 days for dragging shark behind boat - UPI.com', 'March 2': 'Police: Florida man hits 2 women with van in dispute, killing 1 – WSVN 7News | Miami News, Weather, Sports | Fort Lauderdale', 'March 3': 'No result found!', 'March 4': 'No result found!', 'March 5': 'No result found!', 'March 6': 'No result found!', 'March 7': 'http://kutv.com/news/nation-world/police-florida-man-jailed-after-trying-to-barbecue-all-the-child-molesters', 'March 8': 'Best Florida Man Headlines 2019 - The Most Outrageous Florida Man Stories', 'March 9': 'Best Florida Man Headlines 2019 - The Most Outrageous Florida Man Stories', 'March 10': "Florida man who attacked McDonald's worker over straw sentenced to jail | Fox News", 'March 11': 'Florida man whips restaurant worker with rope - NBC2 News', 'March 12': "Thong-wearing Florida man arrested while building shed with garbage on stranger's property", 'March 13': 'Florida man in Spider-Man mask steals bottles from liquor store, deputies say', 'March 14': "Florida man hits pregnant girlfriend with bag of tortilla chips over baby's paternity, SRSO says", 'March 15': 'Florida man finds bright green iguana in toilet, calls 911', 'March 16': 'Florida man breaks into store, flips off security camera, deputies say', 'March 17': '17 Fun Birthday Facts About March 17, 1919 You Must Know', 'March 18': 'Florida man accused of throwing pancake batter faces battery charge - NBC2 News', 'March 19': 'Hot sauce saves Florida man after car crashes into Taco Bell', 'March 20': 'Florida Man Attacked By Neighborhood Squirrel Who Has Residents On High Alert – CBS Miami', 'March 21': 'Florida men, one dressed in bull onesie, attempt to burn down house with Ragu sauce, police say | Fox News', 'March 22': 'The Point, March 22, 2019: Florida Man Pleads Guilty In 2018 Pipe Bomb Case – WUFT News', 'March 23': 'My Florida Man Story - March 23 - Florida Man on Bath Salts Head-Butts Car, Slaps Fire Chief', 'March 24': 'Florida man ticketed after eating pancakes in middle of intersection | Blogs', 'March 25': 'No result found!', 'March 26': 'No result found!', 'March 27': 'No result found!', 'March 28': 'No result found!', 'March 29': 'No result found!', 'March 30': 'No result found!', 'March 31': 'No result found!', 'April 1': 'No result found!', 'April 2': "My Florida Man Story - April 2 - Florida Man Who Killed Ex-Wife, 2 Children Called It 'Cleansing Act'", 'April 3': 'April 3 - The Florida Man Times | The Florida Man Challenge', 'April 4': 'Florida Man arrested after police find five bottles of Fireball in his golf cart - Golf Digest', 'April 5': 'Thong-wearing Florida man arrested while building shed with garbage on stranger’s property', 'April 6': "Thong-wearing Florida man arrested while building shed with garbage on stranger's property", 'April 7': 'Florida Man Threatens To Destroy Everyone With Army Of Turtles, Police Say – CBS Miami', 'April 8': 'Florida Man Is Re-Arrested Just Minutes After His Release : NPR', 'April 9': 'Access Denied', 'April 10': 'Florida man arrested after dining on spaghetti with his bare hands', 'April 11': 'Police: Florida man threatens to destroy everyone with army of turtles', 'April 12': 'Florida Man Arrested Outside Olive Garden After Eating Pasta Belligerently', 'April 13': "April 13 Florida man's own dashboard camera lands him in jail : FloridaMan", 'April 14': 'Florida Man Shoveling Spaghetti in Mouth Arrested at Olive Garden – NBC 6 South Florida', 'April 15': 'Florida man arrested in Naples Olive Garden while intoxicated and shoveling spaghetti into his mouth', 'April 16': 'Florida Man Tried to Pull Over an Undercover Cop While Pretending to be an Officer | Complex', 'April 17': 'April 17 Pajama-Wearing Florida Man Reportedly Wanted to Flirt with Waffle House Waitress, Pulls a Knife Out — FLORIDA MAN BIRTHDAY CHALLENGE', 'April 18': 'Mad Minute stories from Wednesday, April 18th | News | khq.com', 'April 19': 'Half-Nude Florida Man Wearing Underwear Marked "Breathalyzer, Blow Here" Arrested for DUI - The Drive', 'April 20': 'Police: Man Found Asleep In Taylor Swift’s Bed Charged With Stalking – CBS New York', 'April 21': 'My Florida Man Story - April 21 - Florida man sues for right to marry his laptop in same-sex marriage protest', 'April 22': 'Florida man pretending to be cop tries to pull over undercover detective, police say | Fox News', 'April 23': 'Florida Man In Easter Bunny Brawl Is A Fugitive & Talks About His Furry Fist Fight – CBS Miami', 'April 24': 'Cops: Florida man stabbed nephew for hogging bathroom', 'April 25': 'Florida man said he stalked family to ‘make friends,’ deputies...', 'April 26': 'Meth smoking Florida man attacks mattress in jealous rage', 'April 27': 'Florida man arrested after witnesses said he practiced karate on swans', 'April 28': 'Florida man on meth attacks mattress looking for girlfriend’s lover ‘hiding inside,’ police say | Fox News', 'April 29': 'April 29 Florida Man Falls Asleep at Stop Sign in Pickup Truck with Meth Pipe on Lap — FLORIDA MAN BIRTHDAY CHALLENGE', 'April 30': 'Florida Man Threatens To “Shoot All The Employees” At Pet Store Over Sick Puppies – CBS Miami', 'May 1': 'No result found!', 'May 2': 'Florida man wearing bonnet, dress steals baby formula from Publix - NBC2 News', 'May 3': '‘You Gotta Smoke A Bowl With Me Please’: Florida Man Invites Police To Smoke Pot While Showing Off His Marijuana Plant – CBS Miami', 'May 4': 'Florida man charged with battery after slapping girlfriend with cheeseburger, deputies say', 'May 5': "Fugitive Florida man on bike hoped 'hideous' blonde wig disguise would help him evade deputies, police say | Fox News", 'May 6': "Floridaman punches Jimmy John's employee because his sandwich took too long, wasn't 'Freaky Fast' enough | Blogs", 'May 7': '‘F*** It, I’m Drunk, Take Me To Jail’: Florida Man Crashes Lawn Mower Into Police Car – CBS Miami', 'May 8': 'Florida man blames demons after beating pregnant girlfriend for playing Xbox, police say | Fox News', 'May 9': 'Florida man cited after authorities found an illegally poached gator foot stuck in his dashboard | Blogs', 'May 10': 'No result found!', 'May 11': "Florida man arrested after hiding legless, fugitive girlfriend in stor | Atlanta's News & Talk ", 'May 12': 'Florida Man Arrested After Praising the Lord While Highway-Surfing His Cadillac - The Drive', 'May 13': 'em on Twitter: "May 13- Florida man turns himself in for murdering his imaginary friend… "', 'May 14': 'Florida man reportedly tells cops he thought playing basketball naked would ‘enhance his skill level’ | Fox News', 'May 15': 'Florida man slapped girlfriend with cheeseburger, kicked her down stairs: police | Fox News', 'May 16': 'Police Arrest Man Who Claims Playing Basketball Naked ‘Enhances His Skill Level’ – CBS Miami', 'May 17': 'Florida Man Arrested For Standing In Sunroof While Driving Down Interstate | Free Beer and Hot Wings', 'May 18': 'Florida man bit on tongue by rattlesnake he tried to kiss - UPI.com', 'May 19': 'Florida man tasered after walking naked around neighborhood', 'May 20': ' NEW: Florida man with 20 tattoos wearing hot pink bra arrested\xa0 - News - The Palm Beach Post - West Palm Beach, FL', 'May 21': 'Florida man climbs atop playground equipment at Clearwater park, tells kids where babies come from', 'May 22': 'Florida man climbs on playground equipment to tell children where babies come from', 'May 23': 'A Florida Man Was Arrested After Telling A Playground Full Of Kids Where Babies Come From', 'May 24': "Report: Armed Florida man yells 'get out of my country' to 2 McDonald's customers", 'May 25': 'Florida man takes a test drive, pulls gun on salesman, picks up buddy, runs car into palm tree', 'May 26': 'Florida man attacks his mom with spaghetti because "demons were in his head"', 'May 27': 'Florida News Stories May 27: Naked Attacker Shot', 'May 28': 'Florida man arrested, accused of hitting mom on the head with corn cob | fox8.com', 'May 29': "Florida man arrested for allegedly throwing corn cob at mom's head | Fox News", 'May 30': 'Florida man arrested after driving off from deputy, calling 911 to rub it in | myfox8.com', 'May 31': 'Florida man accidentally kills roommate, dog while committing suicide', 'June 1': 'June 1, 2019 – The Only Florida Man', 'June 2': 'My Florida Man Story - June 2 - Cops: Florida Man arrested after being found with decapitated shark', 'June 3': 'Florida man arrested after being caught on camera intentionally running over dog | Q13 FOX News', 'June 4': "Florida man caught on video dancing atop deputy's cruiser", 'June 5': 'Florida man arrested after allegedly pouring ketchup on sleeping girlfriend: report | Fox News', 'June 6': 'Florida man charged with pouring ketchup on girlfriend', 'June 7': 'Florida man gets head-butted, knocked out by alligator - WRCBtv.com | Chattanooga News, Weather & Sports', 'June 8': 'My Florida Man Story - June 8 - Florida Man Covered in Pizza Arrested for Pizza Battery After Pizza Dispute', 'June 9': 'Naked Florida man arrested after urinating on convenience store doors - NBC2 News', 'June 10': "Deputies: Florida man said cocaine on his nose wasn't his", 'June 11': 'JUNE 11 — FIND YOUR BIRTHDAY — FLORIDA MAN BIRTHDAY CHALLENGE', 'June 12': 'Florida man charged in naked rake attack', 'June 13': 'June 13 He had a ‘bad reaction’ to meth — so he asked cops for their help — FLORIDA MAN BIRTHDAY CHALLENGE', 'June 14': 'Florida man arrested for beating up Uber driver with antenna and bystander’s cane | Fox 59', 'June 15': 'Florida man arrested for beating up Uber driver with antenna and bystander’s cane | myfox8.com', 'June 16': "Florida man throws samurai sword at sheriff's deputies", 'June 17': ' Florida Man, 62, Strips, Performs "Strange Dance" At McDonald\'s. Then Tries To Impregnate A Railing. | The Smoking Gun', 'June 18': 'June 18, 2019 – The Only Florida Man', 'June 19': 'No result found!', 'June 20': 'June 20, 2019 – The Only Florida Man', 'June 21': 'Odd news from around the world, June 21', 'June 22': "Nude Florida man burns himself while dancing in flames, chanting 'gibberish'", 'June 23': 'Florida man gets 15 years for dismembering father', 'June 24': 'June 24 Florida man kills grandmother in nudist colony, drives around with her body for five hours — FLORIDA MAN BIRTHDAY CHALLENGE', 'June 25': 'FOX 5 Atlanta - Florida man clings to hood of car speeding down highway | Facebook', 'June 26': 'Florida man accused of killing dancing flamingo is hit by truck and killed before trial', 'June 27': 'June 27 Naked Florida man stood in a fire and chanted ‘gibberish.’ Mushrooms did it, cops say — FLORIDA MAN BIRTHDAY CHALLENGE', 'June 28': 'Florida man back in jail after not paying for taxi that picked him up from jail - New York Daily News', 'June 29': "Florida man robs Wendy's after grilling burger", 'June 30': "Florida Man's Penis Shot Could Land Him In Jail: Report | Jacksonville, FL Patch", 'July 1': "Florida man arrested after pelting girlfriend with McDonald's sweet and sour packets: police | Fox News", 'July 2': 'Florida man arrested for pelting girlfriend with McDonald’s sweet and sour packets', 'July 3': 'July 3, 2019 – The Only Florida Man', 'July 4': 'Florida man hit by celebratory gunfire during Fourth of July fireworks', 'July 5': "Florida man pretending to be a cop pulls over real deputy, sheriff's office says", 'July 6': 'July 6 Florida Man Arrested for Urinating on Car, Running Away from Police — FLORIDA MAN BIRTHDAY CHALLENGE', 'July 7': 'Florida man found dead with more than 100 dog bites - UPI.com', 'July 8': 'Florida Man July 8th News Story | FM 101.9', 'July 9': 'Florida Man July 9th News Story | FM 101.9', 'July 10': 'Florida Man July 10th News Story | FM 101.9', 'July 11': 'July 11 - Florida man with no arms charged with stabbing man with scissors : FloridaMan', 'July 12': 'July 12 Armless Florida man charged after allegedly using feet to stab tourist with scissors — FLORIDA MAN BIRTHDAY CHALLENGE', 'July 13': 'Florida man with no arms charged with stabbing Chicago tourist | abc13.com', 'July 14': 'Florida Man Arrested For Luring Robbery Victims From Dating Site – CBS Miami', 'July 15': 'JULY 15 — FIND YOUR BIRTHDAY — FLORIDA MAN BIRTHDAY CHALLENGE', 'July 16': '(July 16) Florida man faked his murder using a gun and a weather balloon : FloridaMan', 'July 17': 'JULY 17 — FIND YOUR BIRTHDAY — FLORIDA MAN BIRTHDAY CHALLENGE', 'July 18': 'Florida man’s murder was really elaborate suicide by balloon, police say | fox8.com', 'July 19': "Florida man, 33, posed as housewife to lure men into home where he'd secretly film sex acts for web, cops say | Fox News", 'July 20': 'Florida Man Says He Went ‘Bananas,’ Shot Out Utility Workers’ Tires – CBS Miami', 'July 21': 'Florida man shot and killed over parking space | 6abc.com', 'July 22': 'JULY 22 — FIND YOUR BIRTHDAY — FLORIDA MAN BIRTHDAY CHALLENGE', 'July 23': "Man won't be charged in deadly shooting over handicapped parking spot due to Florida's 'stand your ground' law | abc13.com", 'July 24': 'Florida man feeds alligators hot dogs. (July 24) : FloridaMan', 'July 25': "Florida Man's Family Values Appear Shaky | The Smoking Gun", 'July 26': 'JULY 26 — FIND YOUR BIRTHDAY — FLORIDA MAN BIRTHDAY CHALLENGE', 'July 27': 'July 27 Authorities: Man robs bank, then gets naked and throws money — FLORIDA MAN BIRTHDAY CHALLENGE', 'July 28': 'Florida man makes beer run with gator in hand | FOX6Now.com', 'July 29': 'Florida Man Makes Beer Run With Large Gator In Hand – CBS Miami', 'July 30': 'Watch: Florida man carries alligator into convenience store - UPI.com', 'July 31': "Florida man hit by car during failed 'In My Feelings' challenge", 'August 1': 'WATCH: Florida man makes beer run with gator in hand | fox61.com', 'August 2': 'Watch: Florida man goes on a beer run, with alligator in hand - FYI News', 'August 3': 'AUGUST 3 — FIND YOUR BIRTHDAY — FLORIDA MAN BIRTHDAY CHALLENGE', 'August 4': "Florida man who carried alligator into liquor store doesn't remember the incident", 'August 5': 'Florida man arrested for attempted striptease at restaurant', 'August 6': 'Drunk Florida Man Goes on Beer Run with Gator', 'August 7': "Florida man said he smoked THC 'because Jesus was returning,' cops say | Fox News", 'August 8': 'Florida Man Asks Walmart Employee For ‘Anything That Would Kill 200 People’ – CBS Miami', 'August 9': 'Police: Florida man drives golf cart into Walmart, attempts to run over people | abc7news.com', 'August 10': 'Florida Man Arrested for DUI Says He Smoked Pot to Prepare for Jesus to Return | David Gee | Friendly Atheist | Patheos', 'August 11': 'August 11, 2019 – The Only Florida Man', 'August 12': 'Florida man sprays women with roach spray, break out nunchucks over loud music, cops say', 'August 13': 'Florida man arrested for intentionally running over ducklings playing in a puddle', 'August 14': '\nFlorida man claiming to be Alice in Wonderland says ‘hookah-smoking caterpillar’ told him to destroy liquor store with forklift: Cops | Toronto Sun', 'August 15': "Police: Florida man wrecks liquor shop, blames 'caterpillar' | abc13.com", 'August 16': 'Florida man arrested after chugging $7 bottle of wine in Walmart bathroom: report | Fox News', 'August 17': 'FL man arrested with two cans of fart spray | WGNO', 'August 18': 'Police: Florida man, 88, burns raccoon over eating mangoes | FOX2now.com', 'August 19': 'Florida man arrested after allegedly shoving steaks worth more than $50 down his pants | Fox News', 'August 20': 'Florida Man August 20 Challenge | FM 101.9', 'August 21': 'Florida Man Caught Posing As Middle School Student To Play In Youth Football League | Hot 96.3', 'August 22': 'Florida Man August 22 Headline | FM 101.9', 'August 23': 'Florida Man August 23 Headline | FM 101.9', 'August 24': 'Florida man, drunk and naked, allegedly set house on fire in failed cookie baking attempt | ktvb.com', 'August 25': 'August 25 - The Florida Man Times | The Florida Man Challenge', 'August 26': 'https://spacecoastdaily.com/2018/08/florida-man-arrested-by-police-after-demanding-cash-and-donuts-from-krispy-kreme/', 'August 27': 'Florida man, drunk and naked, allegedly set house on fire in failed cookie baking attempt | wltx.com', 'August 28': 'August 28th: Half-naked Florida Man walks goat in the rain : FloridaMan', 'August 29': 'Florida Man Tells Cop ‘That’s What She Said’ After Being Pulled Over and Questioned About Bulge - The Drive', 'August 30': 'Florida man accused of grabbing his genitals and giving the finger to a man and his 8-year-old son - NBC2 News', 'August 31': "Florida man arrested for giving girlfriend 'wet willy' - NBC2 News", 'September 1': "Florida man accused of shooting at home after woman leaves negative re | Atlanta's News & Talk ", 'September 2': "'Wet Willy' Attack puts Florida Man in Jail", 'September 3': 'Florida man charged with battery for giving girlfriend ‘Wet Willy’', 'September 4': 'Florida man parks Smart car in kitchen so it won’t blow away – WSVN 7News | Miami News, Weather, Sports | Fort Lauderdale', 'September 5': 'Florida Man Caught With Nearly 200 Illegal Lobsters – CBS Miami', 'September 6': ' Naked Florida man starts house fire while baking cookies on George Foreman grill - News - The Florida Times-Union - Jacksonville, FL', 'September 7': 'Florida man, drunk and naked, allegedly set house on fire', 'September 8': ' Arrest made in Sept. 8 death of Jacksonville man who staggered into Burger King; another man wanted - News - The Florida Times-Union - Jacksonville, FL', 'September 9': ' Naked Florida man starts house fire while baking cookies on George Foreman grill - News - The Florida Times-Union - Jacksonville, FL', 'September 10': 'Naked Florida man causes fire while baking cookies on George Foreman Grill', 'September 11': "Florida man spots 'firefighter running toward angel' in clouds on September 11 | FOX 29 News Philadelphia", 'September 12': 'Sep. 12 - Florida Man shoots cousin to test bulletproof vest : FloridaMan', 'September 13': ' Naked Florida man starts house fire while baking cookies on George Foreman grill - News - The Florida Times-Union - Jacksonville, FL', 'September 14': 'Shirtless Florida man travels to Myrtle Beach to head bang during Hurricane Florence | Blogs', 'September 15': "Florida man suspected of smelling woman's feet at library leads police on scooter chase - Chicago Tribune", 'September 16': 'Florida Man September 16 | FM 101.9', 'September 17': 'Florida Man September 17 | FM 101.9', 'September 18': 'Florida Man September 18 | FM 101.9', 'September 19': 'Naked Florida man starts house fire after baking cookies on George Foreman grill', 'September 20': 'Neighbors complain about Florida man doing yardwork naked – WSVN 7News | Miami News, Weather, Sports | Fort Lauderdale', 'September 21': 'Video: Florida man charged with setting woman on fire after dispute 12pm September 21, 2018 - YouTube', 'September 22': '\n    Have you tried the "Florida Man Challenge" yet? | Big Country 92.5\n', 'September 23': 'Florida Man September 23 | FM 101.9', 'September 24': 'Naked Florida man chases couple around Chick-fil-A parking lot, deputies say', 'September 25': 'Florida Man September 25 | FM 101.9', 'September 26': 'Florida Man September 26 | FM 101.9', 'September 27': 'Florida Man September 27 | FM 101.9', 'September 28': 'Florida man allegedly neglected grandmother to point of death, buried her, tried to flee\xa0country', 'September 29': 'Florida Grandma Tries Scaring Off Naked Florida Man by Pulling her Dentures Out', 'September 30': 'Florida Man September 30 | FM 101.9', 'October 1': 'Florida Man October 1 | FM 101.9', 'October 2': 'Florida Man October 2 | FM 101.9', 'October 3': 'Florida Man October 3 | FM 101.9', 'October 4': 'Florida Man October 4 | FM 101.9', 'October 5': 'Florida Man Mistakenly Shoots and Kills Son-in-Law in Birthday Surprise Gone Wrong', 'October 6': 'Florida Man Busted After Bizarre Hurricane Irma 3-Way Sex Romp Ends In Gory Slaying, Body Stuffed In Closet', 'October 7': "Florida man accused of pouring beer in gator's mouth after enticing reptile to bite his arm", 'October 8': 'Florida suspect, 22, allegedly attacked mother with sausages | Fox News', 'October 9': 'A Florida Man Is Arrested For Trying To Get A Caiman Drunk | Maritime Herald', 'October 10': 'October 10, 2019 – The Only Florida Man', 'October 11': 'Florida man accused of forcing small alligator to drink beer | Boston.com', 'October 12': 'Police: Man shot after refusing shot at Ocoee bar', 'October 13': 'Florida man accused of forcing small alligator to drink beer | KECI', 'October 14': 'Man run over by lawn mower while trying to kill son with chainsaw', 'October 15': 'Deputies ask Florida man to quit calling about his stolen marijuana – WSVN 7News | Miami News, Weather, Sports | Fort Lauderdale', 'October 16': 'Police: Florida man commits murder over imaginary girlfriend | 6abc.com', 'October 17': 'October 17 - Florida Man Who Plotted to Bomb Target Stores Gets 40 Years : FloridaMan', 'October 18': 'Florida man shot outside bar after rejecting shot inside bar, officials say | Fox News', 'October 19': 'OCTOBER 19 — FIND YOUR BIRTHDAY — FLORIDA MAN BIRTHDAY CHALLENGE', 'October 20': 'My Florida Man Story - October 20 - Florida man surprised by snake while driving', 'October 21': 'My Florida Man Story - October 21 - Shot For Shot: Florida Man Shot In The Foot After Refusing To Take A Shot Of Alcohol At A Bar', 'October 22': 'Florida Man October 22nd stabbed a man to death while high on LSD : FloridaMan', 'October 23': 'Florida man faces 10 years in prison for cruise assault', 'October 24': 'Florida Man Arrested For Sexually Assaulting Stuffed Olaf In Target Store - spacedoutradio', 'October 25': 'FL man arrested for throwing sausages at his Mom | WGNO', 'October 26': 'REPORT: Florida man allegedly slaps woman with a bowl of chili | WBMA', 'October 27': "Florida man accused of having sex with 'Frozen' toy at Target | WPEC", 'October 28': 'Florida man sentenced for plot to blow up Target stores', 'October 29': 'OCTOBER 29 — FIND YOUR BIRTHDAY — FLORIDA MAN BIRTHDAY CHALLENGE', 'October 30': 'Florida Man Arrested For Throwing An Adult Toy On Field Last Night In Buffalo', 'October 31': "Florida man gets stuck after climbing down 30-foot well 'for bragging rights'", 'November 1': 'NOVEMBER 1 — FIND YOUR BIRTHDAY — FLORIDA MAN BIRTHDAY CHALLENGE', 'November 2': 'NOVEMBER 2 — FIND YOUR BIRTHDAY — FLORIDA MAN BIRTHDAY CHALLENGE', 'November 3': 'Police: Naked Florida man drove with wires on penis', 'November 4': 'No result found!', 'November 5': 'A Florida man says his pregnant wife saved his life in home invasion – with an AR-15 – WSVN 7News | Miami News, Weather, Sports | Fort Lauderdale', 'November 6': 'Florida Man Wearing ‘Crocs’ Jumps Into Crocodile Pit, Gets Bitten | The Cairns Post', 'November 7': 'WATCH | Florida man jumps into crocodile pit, gets bit, claims he was held captive', 'November 8': 'Florida man asks police to remove mugshot from Facebook after theft, only for them to replace it with booking photo | Fox News', 'November 9': 'November 9 - The Florida Man Times | The Florida Man Challenge', 'November 10': 'NOVEMBER 10 — FIND YOUR BIRTHDAY — FLORIDA MAN BIRTHDAY CHALLENGE', 'November 11': 'NOVEMBER 11 — FIND YOUR BIRTHDAY — FLORIDA MAN BIRTHDAY CHALLENGE', 'November 12': 'Naked Florida man revealed on video sneaking into restaurant and munching on ramen', 'November 13': 'Florida man accused of killing man after losing card game', 'November 14': 'Florida man arrested for ‘Mother of Satan’ bomb materials, sheriff says', 'November 15': 'Florida Man Makes Himself A Snack While Robbing Taco Bell | Miami, FL Patch', 'November 16': 'No result found!', 'November 17': 'Florida man tried to steal vending machine from apartment complex, police say', 'November 18': 'Florida man tried to steal vending machine from apartment complex, police say', 'November 19': 'Florida man arrested for having sex with miniature horse on multiple occasions, deputies say', 'November 20': 'Florida man arrested for having sex with miniature horse – WSVN 7News | Miami News, Weather, Sports | Fort Lauderdale', 'November 21': 'Florida man arrested for having sex with miniature horse on multiple occasions, deputies\xa0say', 'November 22': 'NOVEMBER 22 — FIND YOUR BIRTHDAY — FLORIDA MAN BIRTHDAY CHALLENGE', 'November 23': 'My Florida Man Story - November 23 - Florida man with large neck in viral mugshot arrested again', 'November 24': 'Florida man tried to break into car filled with cops, officials say | Fox News', 'November 25': 'Birthday challenge November 25th. Florida man steals footlong Subway sub, shoves it down his pants, takes off on bike. : FloridaMan', 'November 26': 'My Florida Man Story - November 26 - Florida man charged with stabbing a woman with a fork over underdone potato', 'November 27': 'Florida Man Accused Of Stabbing Woman Over Underdone Potato – CBS Miami', 'November 28': 'Florida man accused of stabbing woman over underdone potato | WCTI', 'November 29': "November 29 Florida man arrested after punching ATM for 'giving him too much money' — FLORIDA MAN BIRTHDAY CHALLENGE", 'November 30': 'Florida man loses his shorts while breaking into a car dealership - NBC2 News', 'December 1': 'Florida Man on my birthday (Dec 1st): Florida man offered to pay officer with hamburger for oral sex, police say : FloridaMan', 'December 2': 'Florida man loses pants during burglary', 'December 3': 'December 3: florida man attacked by alligator in retirement community : FloridaMan', 'December 4': 'Florida man abandons son on highway because he thinks boy is gay, police say', 'December 5': 'The Top ‘Florida Man’ Stories of 2019 – NBC 6 South Florida', 'December 6': '    \n            Florida man charged with attempted murder after failed marriage proposal - CBS News\n    ', 'December 7': '\n                    Police: Florida man tried to pay for McDonald’s with bag of weed — Nation — Bangor Daily News — BDN Maine\n            ', 'December 8': 'December 8 Florida Man Arrested After Driving 110 MPH While Naked with 3 Women in a Cadillac — FLORIDA MAN BIRTHDAY CHALLENGE', 'December 9': 'Florida Man Steals Elderly Woman’s Purse, Runs Her Over in McDonald’s Parking Lot – NBC 6 South Florida', 'December 10': 'Florida Man Accused Of Ditching Boy Outside Police Station Because He Thought He Was Gay – CBS Miami', 'December 11': 'Florida Man Arrested for DUI While Lemur and Wallaby Escape From Truck During Traffic Stop - The Drive', 'December 12': 'DECEMBER 12 — FIND YOUR BIRTHDAY — FLORIDA MAN BIRTHDAY CHALLENGE', 'December 13': 'No result found!', 'December 14': 'Florida man arrested for biting boys out of frustration', 'December 15': 'DECEMBER 15 — FIND YOUR BIRTHDAY — FLORIDA MAN BIRTHDAY CHALLENGE', 'December 16': "Florida Man Arrested After He Attempted to Pay for His McDonald's Order With Weed | Complex", 'December 17': "My Florida Man Story - December 17 - Florida man arrested for trying to buy McDonald's with marijuana", 'December 18': 'Florida Man Tries To Pay For Fast Food With Bag Of Weed – CBS Miami', 'December 19': 'My Florida Man Story - December 19 - Naked Florida man with crossbow who claimed aliens were after him shot by deputy', 'December 20': 'DECEMBER 20 — FIND YOUR BIRTHDAY — FLORIDA MAN BIRTHDAY CHALLENGE', 'December 21': "My Florida Man Story - December 21 - Florida Man Steals Butt Plug, 'Too Embarrassed' to Pay", 'December 22': 'DECEMBER 22 — FIND YOUR BIRTHDAY — FLORIDA MAN BIRTHDAY CHALLENGE', 'December 23': 'Florida man fighting for his life after chasing monkey', 'December 24': "Florida man busted for handing out pot 'because it was Christmas'", 'December 25': 'DECEMBER 25 — FIND YOUR BIRTHDAY — FLORIDA MAN BIRTHDAY CHALLENGE', 'December 26': 'Police: Florida man worried about vampires intentionally burns down his home', 'December 27': 'Florida man pretends to be homeless, gives $100 to those who tried to help | FOX 13 Tampa Bay', 'December 28': 'DECEMBER 28 — FIND YOUR BIRTHDAY — FLORIDA MAN BIRTHDAY CHALLENGE', 'December 29': '    \n            Police: Florida man rigged door in attempt to electrocute pregnant wife - CBS News\n    ', 'December 30': 'Florida Man Screaming About Vampires Allegedly Sets Fire In His Own House', 'December 31': 'Florida man blows hand off after lighting firework in truck'}

json = json.dumps(floridamanDict)
with open("floridamanDict.json","w") as file:
	file.write(json)

