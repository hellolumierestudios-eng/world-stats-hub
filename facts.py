import requests, os
from datetime import datetime, timezone

T = os.getenv("BOT_TOKEN")
C = os.getenv("CHANNEL_ID")

FACTS = [
    ("🌍", "Did You Know? The Earth Is Mostly Water", "About 71% Of The Earth's Surface Is Covered By Water. Only 2.5% Of It Is Fresh Water We Can Drink."),
    ("⚽", "Did You Know? 3.5 Billion People Watched The Last World Cup Final", "That's Almost Half The Planet Watching One Game. More Than Super Bowl And Olympics Opening Combined."),
    ("🌍", "Did You Know? Your Body Is Mostly Water Too", "About 60% Of Your Body Is Water. Your Brain Is About 75% Water. Drink Water To Think Better."),
    ("⚽", "Did You Know? The Fastest Goal Ever Was In 2 Seconds", "It Was Scored In 2009. The Player Kicked Off And Shot Straight Away. The Keeper Didn't Move."),
    ("🌍", "Did You Know? There Are More Stars Than Sand", "There Are More Stars In The Universe Than Grains Of Sand On All Beaches On Earth."),
    ("⚽", "Did You Know? Football Is Over 3,000 Years Old", "People In China Played Cuju With A Leather Ball More Than 2,000 Years Ago. That's Football's Grandfather."),
    ("🌍", "Did You Know? Bananas Are Berries", "But Strawberries Are NOT Berries. Scientists Say Bananas Count As Berries."),
    ("⚽", "Did You Know? The World Cup Trophy Is Worth Millions", "It Is Made Of 18-Carat Gold And Weighs About 6kg. Winners Only Get A Copy To Take Home."),
    ("🌍", "Did You Know? You Share DNA With Bananas", "Humans Share About 60% Of Their DNA With Bananas. We Are More Alike Than You Think!"),
    ("⚽", "Did You Know? The Ball Is Only In Play For 60 Minutes", "A Match Is 90 Minutes, But The Rest Is Fouls, Throw-Ins And Celebrations."),
    ("🌍", "Did You Know? The Earth Is Not Perfectly Round", "It Is Slightly Squashed At The Poles. Scientists Call It An Oblate Spheroid."),
    ("⚽", "Did You Know? Nigeria Has Won The U17 World Cup 5 Times", "More Than Any Other Country In The World. Nigeria Is A Factory Of Talent."),
    ("🌍", "Did You Know? The Sun Is 99.8% Of Our Solar System's Mass", "Everything Else - All Planets, Moons And Asteroids - Is Just 0.2%."),
    ("⚽", "Did You Know? The Longest Football Match Lasted 3 Days", "It Was Played In England In 2015 For Charity. The Final Score Was 1,821 - 1,820."),
    ("🌍", "Did You Know? Honey Never Expires", "Archaeologists Found 3,000-Year-Old Honey In Egypt And It Was Still Good To Eat."),
    ("⚽", "Did You Know? The First Football Was Made From Animal Skin", "Early Balls Were Made From Pig Bladders Covered In Leather. That's Why It's Called Pigskin."),
    ("🌍", "Did You Know? Your Heart Beats 100,000 Times A Day", "That's About 35 Million Times A Year. It Never Gets Tired."),
    ("⚽", "Did You Know? Pele Scored Over 1,200 Goals", "No Player In History Has Scored More Official Goals Than Pele."),
    ("🌍", "Did You Know? The Moon Is Moving Away From Us", "It Moves About 3.8cm Away Every Year. In Millions Of Years It Will Look Smaller."),
    ("⚽", "Did You Know? The Fastest Shot Ever Was 210 km/h", "It Was Hit By A Brazilian Player. That's Faster Than Most Cars On The Highway."),
    ("🌍", "Did You Know? There Are More Ways To Shuffle Cards Than Atoms On Earth", "A Deck Of 52 Cards Has 8 x 10^67 Combinations. Every Shuffle Is Probably The First Ever."),
    ("⚽", "Did You Know? The First World Cup Was In 1930", "It Was In Uruguay. Only 13 Teams Played. Uruguay Won It."),
    ("🌍", "Did You Know? Octopuses Have 3 Hearts", "Two Pump Blood To The Gills, One Pumps To The Body. They Also Have Blue Blood."),
    ("⚽", "Did You Know? Cristiano Ronaldo Has Scored 900+ Goals", "He Is The Only Player In History To Score 900 Official Career Goals."),
    ("🌍", "Did You Know? The Great Wall Is Visible From Space Is A Myth", "You Cannot See It With The Naked Eye From Space. It Is Too Thin."),
    ("⚽", "Did You Know? A Referee Runs About 12km Per Match", "That's More Than Most Players. Referees Are Athletes Too."),
    ("🌍", "Did You Know? Sharks Are Older Than Trees", "Sharks Have Been Around For 450 Million Years. Trees Came 50 Million Years Later."),
    ("⚽", "Did You Know? Messi Has Won 8 Ballon d'Or Awards", "More Than Any Player In History. The Next Closest Is 5."),
    ("🌍", "Did You Know? Your Bones Are Stronger Than Concrete", "A Matchbox-Sized Piece Of Bone Can Hold 9 Tonnes. That's 4 Times Stronger Than Concrete."),
    ("⚽", "Did You Know? The Biggest Football Stadium Holds 132,000 People", "It's The Rungrado May Day Stadium In North Korea. Bigger Than Camp Nou."),
    ("🌍", "Did You Know? Lightning Is 5 Times Hotter Than The Sun's Surface", "Lightning Can Reach 30,000 Degrees. The Sun's Surface Is Only 5,500 Degrees."),
    ("⚽", "Did You Know? Football Is Played In 200+ Countries", "It Is The Only Sport Played In Every Single Country In The World."),
    ("🌍", "Did You Know? Antarctica Is The Largest Desert", "It Gets Almost No Rain. A Desert Is Defined By Dryness, Not Heat."),
    ("⚽", "Did You Know? The Shortest Footballer Ever Was 1.48m", "His Name Was Josenildo. He Played Professionally In Brazil."),
    ("🌍", "Did You Know? You Can't Taste Food Without Saliva", "Dry Food Has No Taste. Saliva Dissolves It So Your Tongue Can Taste It."),
    ("⚽", "Did You Know? The Champions League Anthem Has Real Lyrics", "It Is Sung In English, French And German. It Means 'They Are The Best, They Are The Champions'."),
    ("🌍", "Did You Know? The Eiffel Tower Grows In Summer", "Metal Expands In Heat. The Tower Grows About 15cm Taller In Summer."),
    ("⚽", "Did You Know? Nigeria's Super Eagles Reached The World Cup 6 Times", "First In 1994. Nigeria Has Never Missed Two World Cups In A Row Since Then."),
    ("🌍", "Did You Know? A Day On Venus Is Longer Than A Year", "Venus Takes 243 Earth Days To Spin Once, But Only 225 Days To Orbit The Sun."),
    ("⚽", "Did You Know? The Most Goals In One Match Was 149-0", "It Was In Madagascar In 2002. The Losing Team Scored Own Goals On Purpose In Protest."),
    ("🌍", "Did You Know? Humans And Giraffes Have The Same Number Of Neck Bones", "Both Have 7 Neck Vertebrae. Giraffe's Are Just Much Longer."),
    ("⚽", "Did You Know? Goalkeepers Used To Wear No Gloves", "Gloves Only Became Popular In The 1970s. Before That, Keepers Used Bare Hands."),
    ("🌍", "Did You Know? The Pacific Ocean Is Bigger Than All Land Combined", "It Covers 30% Of Earth's Surface. You Could Fit All Continents Inside It."),
    ("⚽", "Did You Know? The Premier League Is Watched In 190 Countries", "No Other League Reaches That Many Countries. That's Why It's Called The Biggest League."),
    ("🌍", "Did You Know? Your Nose Can Remember 50,000 Smells", "Your Nose Is More Powerful Than Your Eyes At Remembering."),
    ("⚽", "Did You Know? A Footballer Runs 10km Per Game On Average", "Midfielders Run The Most - Sometimes Up To 13km In One Match."),
    ("🌍", "Did You Know? There Is Water On The Moon", "Scientists Found Ice In Craters At The Moon's Poles. Future Astronauts Could Drink It."),
    ("⚽", "Did You Know? The First Red Card Was In 1970", "Before That, Referees Just Shouted At Players. Cards Made It Clear For Everyone."),
    ("🌍", "Did You Know? Cows Have Best Friends", "Cows Get Stressed When Separated From Their Best Friend. They Are Social Animals."),
    ("⚽", "Did You Know? The Youngest World Cup Player Was 17", "Norman Whiteside Played For Northern Ireland At 17 Years And 41 Days Old."),
    ("🌍", "Did You Know? The Amazon Produces 6% Of Earth's Oxygen", "Not 20% Like Many People Think. Most Oxygen Comes From Ocean Plants."),
    ("⚽", "Did You Know? Barcelona And Real Madrid's Rivalry Is 120 Years Old", "El Clasico Started In 1902. It Is Still The Biggest Club Game In The World."),
    ("🌍", "Did You Know? Hot Water Freezes Faster Than Cold Water", "Scientists Call It The Mpemba Effect. Nobody Fully Understands Why It Happens."),
    ("⚽", "Did You Know? The World Cup Ball Has A Name Every Time", "In 2022 It Was Called Al Rihla - That Means 'The Journey' In Arabic."),
    ("🌍", "Did You Know? Your Brain Uses 20% Of Your Energy", "Even Though It Is Only 2% Of Your Body Weight. Thinking Is Hard Work."),
    ("⚽", "Did You Know? The Tallest Footballer Is 2.10m", "Kristof Van Hout From Belgium. He Is Taller Than Most Basketball Players."),
    ("🌍", "Did You Know? Africa Is The Only Continent With All Climates", "From Desert To Rainforest To Snow. Africa Has Everything."),
    ("⚽", "Did You Know? Arsenal Once Went A Whole Season Unbeaten", "In 2003-04 They Went 38 Games Without Losing. They Are Called The Invincibles."),
    ("🌍", "Did You Know? The First Computer Weighed 27 Tonnes", "It Was Called ENIAC In 1945. Your Phone Is Millions Of Times More Powerful."),
    ("⚽", "Did You Know? The World Cup Trophy Weighs 6.1kg", "But Players Lift It With One Hand. Adrenaline Makes It Feel Light."),
    ("🌍", "Did You Know? Dolphins Have Names For Each Other", "They Use Unique Whistles Like Names. They Call Each Other By Name."),
    ("⚽", "Did You Know? The Oldest Football Club Is Sheffield FC", "Founded In 1857 In England. It Is Still Playing Today."),
    ("🌍", "Did You Know? The Human Body Glows In The Dark", "We Emit Very Faint Light. It Is 1,000 Times Too Faint For Our Eyes To See."),
    ("⚽", "Did You Know? The Fastest Hat-Trick Took 70 Seconds", "It Was Scored In England In 2013. Three Goals In Just Over A Minute."),
    ("🌍", "Did You Know? Nigeria Has Over 500 Languages", "More Than Any Country In Africa. English Is The Official One, But There Are 500+ Local Languages."),
    ("⚽", "Did You Know? A Penalty Is 11 Metres From Goal", "That's Why It's Called The 12-Yard Box. The Keeper Has Only 0.3 Seconds To React."),
    ("🌍", "Did You Know? The Earth Spins At 1,670 km/h", "You Don't Feel It Because Everything Around You Moves At The Same Speed."),
    ("⚽", "Did You Know? The Most Expensive Transfer Ever Is 222 Million Euros", "Neymar To PSG In 2017. Nobody Has Beaten That Price Yet."),
    ("🌍", "Did You Know? You Spend 6 Years Of Your Life Dreaming", "We Dream Every Night, Even If We Don't Remember It."),
    ("⚽", "Did You Know? The World Cup Final 2022 Had 1.5 Billion Viewers", "The Most Watched TV Event In History At That Time."),
    ("🌍", "Did You Know? Wombat Poop Is Cube-Shaped", "It Is The Only Animal That Makes Cube-Shaped Poop. So It Doesn't Roll Away."),
    ("⚽", "Did You Know? Football Was Banned In England In 1314", "The King Said It Was Too Violent. People Played Anyway."),
    ("🌍", "Did You Know? The Sun Will Die In 5 Billion Years", "It Will Grow Huge And Swallow Earth. But Don't Worry, That's Very Far Away."),
    ("⚽", "Did You Know? Only 8 Countries Have Won The World Cup", "Brazil, Germany, Italy, Argentina, France, Uruguay, England And Spain. That's It."),
    ("🌍", "Did You Know? Your Fingerprints Are Unique Even For Twins", "Even Identical Twins Have Different Fingerprints."),
    ("⚽", "Did You Know? The Longest Unbeaten Run Is 37 Games", "Italy Went 37 Games Without Losing From 2018 To 2021. A World Record."),
    ("🌍", "Did You Know? The Deepest Place On Earth Is 10.9km Deep", "The Mariana Trench. If Everest Was Inside It, There Would Still Be 2km Of Water On Top."),
    ("⚽", "Did You Know? The First Women's World Cup Was In 1991", "It Was In China. The USA Won It."),
    ("🌍", "Did You Know? A Single Cloud Can Weigh 500 Tonnes", "That's Like 100 Elephants Floating In The Sky. It Floats Because The Air Holds It Up."),
    ("⚽", "Did You Know? Erling Haaland Scored 36 Goals In One Premier League Season", "That Broke A 29-Year-Old Record In His First Season In England."),
    ("🌍", "Did You Know? The Largest Animal Ever Is The Blue Whale", "Its Heart Is The Size Of A Small Car. Its Heartbeat Can Be Heard 3km Away."),
    ("⚽", "Did You Know? The Offside Rule Was Invented To Stop Cheating", "In 1863, Players Used To Stand Next To The Goal All Game. Offside Stopped That."),
    ("🌍", "Did You Know? The Earth Has A Second Mini Moon", "A Small Asteroid Orbits Earth Sometimes. It Is Called A Quasi-Moon."),
    ("⚽", "Did You Know? Nigeria Beat Spain At The 1998 World Cup", "Nigeria Won 3-2. It Is Still One Of The Greatest World Cup Upsets Ever."),
    ("🌍", "Did You Know? Humans Can Hear A Pin Drop 10 Metres Away In Silence", "Our Ears Are Very Sensitive. In A Quiet Room, You Can Hear A Lot."),
    ("⚽", "Did You Know? The Most Goals In A Calendar Year Is 91", "Messi Scored 91 Goals In 2012. Nobody Has Come Close Since."),
    ("🌍", "Did You Know? The Moon Has Earthquakes Too", "They Are Called Moonquakes. They Can Last For 10 Minutes."),
    ("⚽", "Did You Know? A Football Team Has 11 Players", "But In Total, Including Subs And Staff, A Squad Can Have Over 40 People."),
    ("🌍", "Did You Know? Your Stomach Gets A New Lining Every 3 Days", "Otherwise Your Stomach Acid Would Eat Your Own Stomach."),
    ("⚽", "Did You Know? The African Cup Of Nations Started In 1957", "Only 3 Teams Played The First One. Egypt Won It."),
]

now = datetime.now(timezone.utc)
if now.hour < 8:
    slot = 0
elif now.hour < 14:
    slot = 1
else:
    slot = 2

index = (now.timetuple().tm_yday * 3 + slot) % len(FACTS)
emoji, title, body = FACTS[index]
msg = f"{emoji} {title}\n\n{body}\n\n#WorldStatsHub"
u = f"https://api.telegram.org/bot{T}/sendMessage"
r = requests.get(u, params={"chat_id": C, "text": msg})
print("TELEGRAM:", r.status_code, r.text[:500])
