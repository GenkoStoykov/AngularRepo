from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time


class Retweeter():
    def __init__(self, keyword, driver, count=20, maximum_timeout=30):
        self.driver = driver
        # self.driver.implicitly_wait(10)
        # self.username = username
        # self.password = password
        self.keyword = keyword
        self.count = count
        self.maximum_timeout = maximum_timeout

    def retweets(self, text, id):
        retval = -1
        try:
            WebDriverWait(self.driver, self.maximum_timeout).until(
                EC.presence_of_element_located((By.XPATH, '//div[@id="container"]/div/section')))
        except:
            print 'occured exception in loading page'
            # print self.driver.page_source.encode('utf-8')
            return retval

        section_count = len(self.driver.find_elements_by_xpath('//div[@id="container"]/div/section'))
        self.close_all_tabs(section_count)

        script_code = '''
                    var add_column = null;
                    var content_div = document.evaluate('/html/body/div[3]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                    if (content_div.getAttribute('class').includes('is-condensed')) {
                         add_column = document.evaluate('//nav[@id="column-navigator"]/div/a/div[1]/i', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                    }
                    else {
                        add_column = document.evaluate('//nav[@id="column-navigator"]/div/a/div[2]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                        } 
                    add_column.click();
                    '''
        self.driver.execute_script(script_code);

        try:
            xpath = '//div[@id="open-modal"]/div/div/div/ul/li[2]/a'
            WebDriverWait(self.driver, self.maximum_timeout).until(
                EC.presence_of_element_located((By.XPATH, xpath)))
        except:
            print 'occured exception in loading add column modal'
            return retval

        script_code = '''
                    var user_column = document.evaluate('//div[@id="open-modal"]/div/div/div/ul/li[2]/a', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                    user_column.click();
                    '''
        self.driver.execute_script(script_code);

        try:
            xpath = '//div[@id="open-modal"]/div/div/div/div[1]/div[1]/form/div/input'
            WebDriverWait(self.driver, self.maximum_timeout).until(
                EC.presence_of_element_located((By.XPATH, xpath)))
        except:
            print 'occured exception in loading add user column modal'
            return retval

        script_code = '''
                    var user_search_input = document.evaluate('//div[@id="open-modal"]/div/div/div/div[1]/div[1]/form/div/input', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                    user_search_input.value = '%s';
                    var user_search_find_btn = document.evaluate('//div[@id="open-modal"]/div/div/div/div[1]/div[1]/form/div/a[1]/i', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                    user_search_find_btn.click();
                ''' % (self.keyword)
        self.driver.execute_script(script_code);

        try:
            xpath = '//div[@id="open-modal"]/div/div/div/div[1]/div[2]/div[1]/ul/li[1]/a/div'
            WebDriverWait(self.driver, self.maximum_timeout).until(
                EC.presence_of_element_located((By.XPATH, xpath)))
        except:
            print 'occured exception in loading add user search result'
            return retval

        script_code = '''
                var search_result_div = document.evaluate('//div[@id="open-modal"]/div/div/div/div[1]/div[2]/div[1]/ul/li[1]/a/div', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                    search_result_div.click();
                    var add_user_column_btn = document.evaluate('//div[@id="open-modal"]/div/div/footer/span/button', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                    add_user_column_btn.click();
                    var close_user_column_btn = document.evaluate('//div[@id="open-modal"]/div/header/a/i', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                    close_user_column_btn.click();
                '''

        self.driver.execute_script(script_code);

        try:
            section_count = len(self.driver.find_elements_by_xpath('//div[@id="container"]/div/section')) - 1
            xpath = '//div[@id="container"]/div/section[%s]/div/div[1]/div[1]/div[3]/div/article[1]' % section_count
            WebDriverWait(self.driver, self.maximum_timeout).until(
                EC.presence_of_element_located((By.XPATH, xpath)))
        except:
            print 'occured exception in loading user section'
            self.close_search(section_count)
            return retval

        script_code = '''
                    var section_div = '//div[@id="container"]/div/section[%s]';
                    var settings_element = document.evaluate(section_div + '/div/div[1]/header/a/i', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                    settings_element.click();
                    var content_element = document.evaluate(section_div + '/div/div[1]/div[1]/div[1]/div[1]/form/fieldset[1]/div/div[1]/div[1]/i[1]',document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                    content_element.click();                         
                ''' % (section_count)
        self.driver.execute_script(script_code);

        try:
            xpath = '//div[@id="container"]/div/section[%s]/div/div[1]/div[1]/div[1]/div[1]/form/fieldset[1]/div/div[1]/div[2]/div/div[2]/div/input' % section_count
            WebDriverWait(self.driver, self.maximum_timeout).until(
                EC.visibility_of_element_located((By.XPATH, xpath)))
        except:
            print 'occured exception in loading matching_input'
            self.close_search(section_count)
            return retval

        try:
            matching_input = self.driver.find_element_by_xpath(xpath)
            matching_input.click();
            matching_input.clear();
            matching_input.send_keys(text)
            # time.sleep(5)
            matching_input.send_keys(Keys.RETURN)
        except:
            print 'occured exception in loading search send key '
            self.close_search(section_count)
            return retval

        try:
            xpath = '//div[@id="container"]/div/section[%s]/div/div[1]/div[1]/div[3]/div/article' % section_count
            WebDriverWait(self.driver, self.maximum_timeout).until(
                EC.presence_of_all_elements_located((By.XPATH, xpath)))
        except:
            print 'occured exception in loading add user search result'
            retval = 0
            self.close_search(section_count)
            return retval

        article_count = len(self.driver.find_elements_by_xpath(
            '//div[@id="container"]/div/section[%s]/div/div[1]/div[1]/div[3]/div/article' % section_count)) + 1
        # finded = False
        for i in range(1, article_count):
            try:
                tweet_id = self.driver.find_element_by_xpath(
                    '//div[@id="container"]/div/section[%s]/div/div[1]/div[1]/div[3]/div/article[%s]' % (
                        section_count, i)).get_attribute('data-key')
            except:
                print 'occured exception in loading add user search result 2'
                retval = 0
                self.close_search(section_count)
                break
            # if (tweet_id == id):
            #     finded = True
            retweet_element = self.driver.find_element_by_xpath(
                '//div[@id="container"]/div/section[%s]/div/div[1]/div[1]/div[3]/div/article[%s]/div/div/footer/ul/li[2]/a/i' % (
                    section_count, i))
            if ('icon-retweet-filled' in retweet_element.get_attribute('class')):
                script_code = '''                         
                    var action_menu = document.evaluate('//div[@id="container"]/div/section[%s]/div/div[1]/div[1]/div[3]/div/article[%s]/div/div/footer/ul/li[4]/a/i', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                    action_menu.click();
                    ''' % (section_count, i)
                self.driver.execute_script(script_code)

                try:
                    WebDriverWait(self.driver, self.maximum_timeout).until(
                        EC.presence_of_element_located((By.XPATH,
                                                        '//div[@id="container"]/div/section[%s]/div/div[1]/div[1]/div[3]/div/article[%s]/div/div/footer/ul/li[4]/div/div[2]' % (
                                                            section_count, i))))
                    undo_retweet_element = self.driver.find_element_by_xpath(
                        '//div[@id="container"]/div/section[%s]/div/div[1]/div[1]/div[3]/div/article[%s]/div/div/footer/ul/li[4]/div/div[2]/ul/li[last()]/a' % (
                            section_count, i))
                    if(undo_retweet_element.text == 'Undo Retweet'):
                        undo_retweet_element.click()
                    time.sleep(5)
                    # script_code = '''
                    #      var undo_retweet_element_div = document.evaluate('//div[@id="container"]/div/section[%s]/div/div[1]/div[1]/div[3]/div/article[%s]/div/div/footer/ul/li[4]/div/div[2]/ul/li[last()]/a', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                    #      undo_retweet_element_div.click();
                    #     ''' % (section_count, i)
                    # self.driver.execute_script(script_code)
                except:
                    retval = -1
                    print 'occured exception in loading undo retweet button'
                    break

                # try:
                #     WebDriverWait(self.driver, self.maximum_timeout).until(
                #         EC.presence_of_element_located((By.XPATH,
                #                                         '//div[@id="container"]/div/section[%s]/div/div[2]/div/div/div/div[2]/article/div/div[1]/footer/ul/li[2]/a/i' % (
                #                                             section_count))))
                #     script_code = '''
                #          var undo_retweet_element_li = document.evaluate('//div[@id="container"]/div/section[%s]/div/div[2]/div/div/div/div[2]/article/div/div[1]/footer/ul/li[4]/a/i', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                #          undo_retweet_element_li.click();
                #          setTimeout(function(){
                #             var undo_retweet_element = document.evaluate('//div[@id="container"]/div/section[%s]/div/div[2]/div/div/div/div[2]/article/div/div[1]/footer/ul/li[4]/div/div[2]/ul/li[last()]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                #             undo_retweet_element.click();
                #             setTimeout(function(){
                #                 var back_to_user_element = document.evaluate('//*[@id="container"]/div/section[%s]/div/div[2]/header/a/div/span', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                #                 back_to_user_element.click();
                #             }, 500);
                #          }, 500);
                #         ''' % (section_count, section_count, section_count)
                #     self.driver.execute_script(script_code)
                # except:
                #     retval = -1
                #     print 'occured exception in loading undo retweet div'
                #     break
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH,
                                                    '//div[@id="container"]/div/section[%s]/div/div[1]/div[1]/div[3]/div/article[%s]/div/div/footer/ul/li[2]/a/i' % (
                                                        section_count, i))))
                # ActionChains(self.driver).move_to_element(retweet_element).click(retweet_element).perform()
                script_code = '''
                     var retweet_element = document.evaluate('//div[@id="container"]/div/section[%s]/div/div[1]/div[1]/div[3]/div/article[%s]/div/div/footer/ul/li[2]/a/i', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                     retweet_element.click();
                     ''' % (section_count, i)
                self.driver.execute_script(script_code)
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//div[@id="actions-modal"]/div/div[1]/div/div/button[2]')))
                retweet_button = self.driver.find_element_by_xpath(
                    '//div[@id="actions-modal"]/div/div[1]/div/div/button[2]')
            except:
                retval = -1
                print 'occured exception in loading retweet button'
                break
            #
            # time_element = self.driver.find_element_by_xpath(
            #     '//div[@id="actions-modal"]/div/div[2]/div/header/time')
            # tweet_time = time_element.get_attribute('datetime')
            # id_element = time_element.find_element_by_tag_name('a')
            # tweet_id = id_element.get_attribute('href').split('/')[-1]
            # retweet_button = self.driver.find_element_by_xpath(
            #     '//div[@id="actions-modal"]/div/div[1]/div/div/button[2]')
            # retweet_button.click()
            try:
                script_code = '''
                     var accounts = document.getElementsByClassName('acc-twitter js-account-item js-show-tip');
                     for(var i=1;i<accounts.length;i++) {
                        accounts[i].click();
                     }
                    setTimeout(function(){
                        if(accounts[accounts.length-1].getAttribute('class').includes("acc-selected")) {
                            retweet_button = document.evaluate('//div[@id="actions-modal"]/div/div[1]/div/div/button[2]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                            retweet_button.click();
                        }
                    }, 500);
                    '''
                self.driver.execute_script(script_code)
                # time.sleep(2)

                WebDriverWait(self.driver, 5).until(EC.staleness_of(retweet_button))
            except:
                script_code = '''
                    var err_msg_div = document.getElementsByClassName('js-status-message status-message');
                    if(err_msg_div.length > 0){
                        close_err_btn = document.evaluate('/html/body/div[3]/div[1]/div/a', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                        close_err_btn.click()
                    }
                    setTimeout(function() {
                        retweet_button = document.evaluate('//div[@id="actions-modal"]/div/div[1]/div/div/button[2]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                        retweet_button.click();
                    }, 100);
                    '''
                self.driver.execute_script(script_code)

            script_code = '''
                        var retweet_divs = document.getElementsByClassName('mdl is-inverted-dark cmp s-inreply l-no-txtarea s-fluid-height');
                        if(retweet_divs.length >  0){
                            close_btn = document.evaluate('//div[@id="actions-modal"]/div/header/a/i', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                            close_btn.click();
                        }
                        '''
            self.driver.execute_script(script_code)
            retval = 1

        # if (finded == False):
        #     print ('No Found tweet')
        #     retval = 0

        self.close_search(section_count)
        return retval

    def close_search(self, section_index):
        try:
            script_code = ''' 
            var section_div = '//div[@id="container"]/div/section[%s]';
             var close_element = document.evaluate(section_div + '/div/div[1]/div[1]/div[1]/div[1]/form/fieldset[2]/button[2]/i', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
             if(close_element){
                close_element.click();
             }
            ''' % (section_index)
            self.driver.execute_script(script_code)
        except:
            pass


    def open_setting(self, section_index):
        try:
            script_code = ''' 
             var setting_element = document.evaluate('//div[@id="container"]/div/section[%s]/div/div[1]/header/a/i', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
             setting_element.click();
            ''' % (section_index)
            self.driver.execute_script(script_code)
        except:
            pass


    def close_all_tabs(self, section_count):
        try:
            i = section_count
            while (i > 1):
                script_code = '''
                var settings_elements = document.getElementsByClassName('js-action-header-button column-header-link column-settings-link');
                settings_elements[settings_elements.length-1].click();
                document.getElementsByClassName('btn btn-alt btn-neutral btn-options-tray padding-hn padding-rs')[0].click();
                '''
                self.driver.execute_script(script_code)
                i = i - 1
        except:
            pass
