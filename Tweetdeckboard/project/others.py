# from flask_oauthlib.client import OAuth


import datetime
import re
import smtplib
from email.header import Header
from email.mime.text import MIMEText

from apscheduler.triggers.interval import IntervalTrigger
from flask import session
from project import app, db, drivermap, scheduler
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from twitter import Twitter, OAuth, TwitterHTTPError

from models import Deck, Profile, Log, Link, Adminmail, User
from tweetdeck import Retweeter


def send_email(receiver, message, subject):
    try:
        admin_mail = Adminmail.query.first()
        if (admin_mail != None):
            msg = MIMEText(message, 'plain', 'utf-8')
            me = "TweetBoard" + "<" + admin_mail.email_address + ">"
            msg['From'] = Header(me)
            msg['Subject'] = Header(subject, 'utf-8')
            smtp = smtplib.SMTP_SSL(admin_mail.smtpserver)
            smtp.login(admin_mail.username, admin_mail.password)
            smtp.sendmail(admin_mail.email_address, receiver, msg.as_string())
            smtp.quit()
            return True
        else:
            return False;
    except smtplib.SMTPException as e:
        return False


def setup_scheduler():
    decks = Deck.query.all()
    for deck in decks:
        try:
            driver = create_driver()
            login_code = login_tweetdeck(driver, deck.name, deck.password)['code']
            if (login_code >= 0):
                adddriver(deck.name, driver)
            else:
                driver.quit()
            Deck.query.filter_by(id=deck.id).update({"login_code": login_code})
            db.session.commit();
        except:
            db.session.close()
            driver.quit()

    profiles = Profile.query.filter_by().all()
    for profile in profiles:
        link = Link.query.filter_by(id=profile.linkid).join(Deck).first()
        driver = getdriver(link.deck.name)
        if ((driver == None) or (link.deck.login_code < 1)):
            Profile.query.filter_by(id=profile.id).update({"run_status": 0})
            continue
        scheduler.add_job(
            func=auto_rt,
            kwargs={'profile_id': profile.id, 'driver': driver},
            trigger=IntervalTrigger(minutes=profile.minutes),
            # trigger=IntervalTrigger(minutes=1),
            id='retweet_%s' % (profile.id),
            replace_existing=False,
            misfire_grace_time=app.config['MISFIRE_GRACE_TIME'])
        Profile.query.filter_by(id=profile.id).update({"run_status": 1})
    db.session.commit();


def close_opened_browser():
    for key in drivermap.keys():
        drivermap[key].quit()


def create_driver():
    chrome_options = Options()
    chrome_options.binary_location = app.config['CHROME_BIN_PATH']
    driver = webdriver.Chrome(chrome_options=chrome_options)
    return driver


def is_running(jobid):
    job = scheduler.get_job(job_id=jobid)
    if (job):
        return True
    else:
        return False


def isNotDeckOnline(driver):
    pageSource = driver.find_elements_by_tag_name('body')[0].text
    if('Log in with your Twitter account' in pageSource):
        return True
    else:
        return False


def auto_rt(profile_id, driver):
    # if (type(profile_id) is int):
    #     driver = driver
    #     profile_id = profile_id
    # else:
    #     temp = profile_id
    #     profile_id = driver
    #     driver = temp

    profile = (db.session.query(
        Profile.id, Deck.name,Profile.linkid, Profile.keyword,Profile.tweetid_list,Profile.last_tweetid,Profile.failed_tweetid_list,
        User.username)
               .filter_by(id=profile_id).join(Link).join(Deck).join(User)).first()
    # last_time = profile.last_retweeted
    # if (last_time == None):
    #     last_time = 0
    # else:
    #     last_time = time.mktime(last_time.timetuple())
    keyword = profile.keyword
    if ('@' not in profile.keyword):
        keyword = '@%s' % profile.keyword

    if(isNotDeckOnline(driver)):
        deck = (db.session.query(
            Profile.linkid,Link.deckid,Deck.id, Deck.name, Deck.login_code)
               .filter_by(id=profile_id).join(Link).join(Deck)).first()
        Deck.query.filter_by(id=deck.id).update({'login_code': -1})
        linkid = profile.linkid
        profiles = Profile.query.filter_by(linkid=linkid).all()
        for prof in profiles:
            if (prof.run_status == 1):
                jobid = 'retweet_%s' % (prof.id)
                if (is_running(jobid)):
                    scheduler.remove_job(jobid)
        Profile.query.filter_by(linkid=linkid).update({'run_status': 0})
        db.session.commit()
        removedriver(deck.name)
        db.session.close()
        return

    bot = Retweeter(keyword, driver)
    if(profile.tweetid_list == ''):
        tweetlist = getTweetList(user=keyword, since_id=profile.last_tweetid, count=50)
        if(tweetlist['status'] == 1):
            lists = reversed(tweetlist['list'])
        else:
            Profile.query.filter_by(id=profile_id).update({'run_status': 0})
            db.session.commit()
            jobid = 'retweet_%s' % (profile_id)
            if (is_running(jobid)):
                scheduler.remove_job(jobid)
            return

        tweetid_list = ''
        tweettext_list = ''
        last_tweetid = profile.last_tweetid
        for list in lists:
            id = list['id_str']
            last_tweetid = id
            tweetid_list = tweetid_list + ',' + id
            text = list['text']
            text = re.sub(r'[^\x00-\x7F]+', ' ', text)
            text = re.sub(r'[\n\r\t]+', ' ', text)
            if (text[:2] == 'RT'):
                index = text.index(':') + 1
                text = text[index:]
            if ('&lt;' in text):
                index = text.index('&lt;')
                text = text[:index]
            if ('&gt;' in text):
                index = text.index('&gt;')
                text = text[:index]
            if ('&quot;' in text):
                index = text.index('&quot;')
                text = text[:index]
            if ('&apos;' in text):
                index = text.index('&apos;')
                text = text[:index]
            if (len(text) > 20):
                text = text[:20]
            if(text == ''):
                print ('blank')
            tweettext_list = tweettext_list + ' eof|,|eof ' + text
        tweetid_list = tweetid_list[1:]
        tweettext_list = tweettext_list[12:]
        Profile.query.filter_by(id=profile_id).update({'tweetid_list':tweetid_list, 'tweettext_list':tweettext_list, 'last_tweetid':last_tweetid})
        db.session.commit()
    tweettext_list = Profile.query.filter_by(id=profile_id).first().tweettext_list
    text = tweettext_list.split(' eof|,|eof ')[0]
    tweetid_list = Profile.query.filter_by(id=profile_id).first().tweetid_list
    if(tweetid_list == ''):
        print 'There are no new tweets'
        return
    id = tweetid_list.split(',')[0]
    failed_tweetid_list = Profile.query.filter_by(id=profile_id).first().failed_tweetid_list
    retweeted = bot.retweets(text, id)
    if(retweeted == 1):
        log = Log(
            username=profile.username,
            deckname=profile.name,
            keyword=profile.keyword,
            retweetid=id
        )
        db.session.add(log)
        tweettext_list = tweettext_list.replace(text,'')
        if(tweettext_list != ''):
            tweettext_list = tweettext_list[11:]
        tweetid_list = tweetid_list.replace(id, '')
        if (tweetid_list != ''):
            tweetid_list = tweetid_list[1:]
        Profile.query.filter_by(id=profile_id).update(
            {'tweetid_list': tweetid_list, 'tweettext_list': tweettext_list})
    elif (retweeted == 0):
        tweetid_list = tweetid_list.replace(id, '')
        if (tweetid_list != ''):
            tweetid_list = tweetid_list[1:]
        tweettext_list = tweettext_list.replace(text, '')
        if (tweettext_list != ''):
            tweettext_list = tweettext_list[11:]
        failed_tweetid_list = failed_tweetid_list + ',' + id
        Profile.query.filter_by(id=profile_id).update({'tweetid_list': tweetid_list,'tweettext_list': tweettext_list, "failed_tweetid_list": failed_tweetid_list})
    Profile.query.filter_by(id=profile_id).update({"last_retweeted": (datetime.datetime.utcnow())})
    db.session.commit()
    db.session.close()


def login_tweetdeck(driver, username, password):
    result = {}

    driver.get(
        'https://twitter.com/login?hide_message=true&redirect_after_login=https%3A%2F%2Ftweetdeck.twitter.com%2F%3Fvia_twitter_login%3Dtrue&lang=en')

    # password_element = self.driver.find_element_by_xpath(
    #     '//div[@id="page-container"]/div/div[1]/form/fieldset/div[2]/input')
    # password_element.click()
    # password_element.clear()
    # password_element.send_keys(self.password)
    # time.sleep(5)
    # password_element.send_keys(Keys.RETURN)

    # var login = document.getElementsByClassName('submit EdgeButton EdgeButton--primary EdgeButtom--medium')[0];
    # login.click();
    #
    script_code = ''' 
            var name_element = document.getElementsByName("session[username_or_email]")[1];
            name_element.value = '%s';
            var pass_element = document.getElementsByName("session[password]")[1];
            pass_element.value = '%s';
            ''' % (username, password)

    driver.execute_script(script_code)
    login_element = driver.find_element_by_xpath('//div[@id="page-container"]/div/div[1]/form/div[2]/button')
    login_element.submit()
    wait = WebDriverWait(driver, app.config['PAGE_LOAD_MAXIMUM_TIMEOUT'])
    try:
        if (driver.title == 'Verify your identity'):
            result['code'] = 0
            result['status'] = False
        elif (driver.title == 'TweetDeck'):
            wait.until(EC.visibility_of_all_elements_located((By.XPATH, '/html/body/div[3]/header')))
            result['code'] = 1
            result['status'] = True
        else:
            wait.until(EC.title_is('TweetDeck'))
            result['code'] = 1
            result['status'] = True
    except TimeoutException:
        print
        'occured exception in login tweetdeck'
        driver.get_screenshot_as_file("err_login.jpg")
        result['code'] = -1
        result['status'] = False
        driver.quit()
    return result


def verify_tweetdeck(id, driver, code):
    result = {}
    wait = WebDriverWait(driver, app.config['PAGE_LOAD_MAXIMUM_TIMEOUT'])

    script_code = '''
                    var code_element = document.getElementById("challenge_response");
                    code_element.value = '%s';
                    ''' % (code)
    try:
        driver.execute_script(script_code)
        login_element = driver.find_element_by_xpath('//input[@id="email_challenge_submit"]')
        login_element.submit()
        wait.until(EC.title_is('TweetDeck'))
        result['code'] = 1
        result['status'] = True
    except:
        if (driver.title == 'Login on Twitter'):
            deck = Deck.query.filter_by(id=id).first()
            Deck.query.filter_by(id=deck.id).update({'login_code': -1})
            db.session.commit()
            removedriver(deck.name)
            result['code'] = 0
            result['status'] = False
        else:
            driver.get_screenshot_as_file("err_verify.jpg")
            result['code'] = -1
            result['status'] = False
    db.session.close()
    return result


def getTweetList(user, since_id, count):
    retvalue = {}
    twitter = Twitter(
        auth=OAuth(app.config['OAUTH_TOKEN'], app.config['OAUTH_SECRET'], app.config['CONSUMER_KEY'], app.config['CONSUMER_SECRET']))
    k = count
    i = 0
    while (k < 500 and i < count):
        try:
            result = twitter.statuses.user_timeline(screen_name=user, count=k, include_rts=False)
            i = len(result)
            k = k + count
        except TwitterHTTPError as api_error:
            retvalue['status'] = -1
            retvalue['list'] = None
            return retvalue
    result = result[:count]
    retvalue['status'] = 1
    retvalue['list'] = result
    return retvalue


def adddriver(name, driver):
    drivermap[name] = driver


def removedriver(name):
    if drivermap.get(name):
        drivermap[name].quit()
        del drivermap[name]


def getdriver(name):
    if drivermap.get(name):
        driver = drivermap[name]
    else:
        driver = None
    return driver


def is_admin():
    if session.get('logged_in') and session.get('user'):
        if session['logged_in'] and session['user']:
            user = session['user']
            if (user['admin']):
                return True
            else:
                return False
        else:
            return False
    else:
        return False

def is_deck():
    if session.get('logged_in') and session.get('user'):
        if session['logged_in'] and session['user']:
            user = session['user']
            if (user['deck']):
                return True
            else:
                return False
        else:
            return False
    else:
        return False

        # oauth = OAuth(app)

        #
        # @twitter.tokengetter
        # def get_twitter_token():
        #     if 'twitter_oauth' in session:
        #         resp = session['twitter_oauth']
        #         return resp['oauth_token'], resp['oauth_token_secret']


        # twitter = oauth.remote_app(
        #     'twitter',
        #     base_url='https://api.twitter.com/1.1/',
        #     request_token_url='https://api.twitter.com/oauth/request_token',
        #     access_token_url='https://api.twitter.com/oauth/access_token',
        #     authorize_url='https://api.twitter.com/oauth/authorize',
        #     consumer_key=app.config['CONSUMER_KEY'],
        #     consumer_secret=app.config['CONSUMER_SECRET']
        #     # consumer_key='xBeXxg9lyElUgwZT6AZ0A',
        #     # consumer_secret='aawnSpNTOVuDCjx7HMh6uSXetjNN8zWLpZwCEU4LBrk'
        # )
        #
        # @app.route('/api/addAccount', methods=['POST'])
        # def add_account():
        #     name = request.form['name']
        #     userid = request.form['userid']
        #     params = {'screen_name':name}
        #     callback_url = url_for('oauthorized',userid=userid ,next=request.args.get('next'))
        #     return twitter.authorize(callback=callback_url or request.referrer or None, **params)
        #
        #
        # @app.route('/api/oauthorized')
        # def oauthorized():
        #     userid = request.args['userid']
        #     resp = twitter.authorized_response()
        #     if resp is None:
        #         flash('You denied the request to sign in.')
        #     else:
        #         session['twitter_oauth'] = resp
        #         oauth_token = resp['oauth_token']
        #         oauth_token_secret = resp['oauth_token_secret']
        #         screen_name = resp['screen_name']
        #     return redirect(url_for('index'))
        #
