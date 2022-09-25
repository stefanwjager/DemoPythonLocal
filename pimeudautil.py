from dateutil.relativedelta import relativedelta
from pandas.tseries.offsets import *
from pathlib import Path
from img_rest import *
import win32com.client
import datetime as dt
import configparser
import pandas as pd
import subprocess
import webbrowser
import tabulate  # frozen
import pwinput
import getpass
import shutil
import time
import sys
import os
import re


class Parameters(object):
    def __init__(self):
        self.USER = getpass.getuser()
        self.VERSION = '1.3'

        # ------------------------------ [ Dates ] ------------------------------------- #
        # as date object
        self.NOW = dt.datetime.now()
        self.TD = self.NOW.date()
        self.BD1 = self.NOW - BusinessDay(1)
        self.BD2 = self.NOW - BusinessDay(2)
        self.BEOM = (dt.date(self.NOW.year, self.NOW.month, 1) + relativedelta(months=1) - BusinessDay()).date()
        self.EOM = dt.date(self.NOW.year, self.NOW.month, 1) + relativedelta(months=1) - relativedelta(days=1)
        self.EOLM = dt.date(self.NOW.year, self.NOW.month, 1) - relativedelta(days=1)
        self.BEOLM = dt.date(self.NOW.year, self.NOW.month, 1) - BusinessDay()
        self.EOY = dt.date((self.NOW + relativedelta(days=1)).year, 12, 31)

        # string formatted
        self.TD_FORMAT = self.TD.strftime('%Y%m%d')
        self.BD1_FORMAT = self.BD1.strftime('%Y%m%d')
        self.BD2_FORMAT = self.BD2.strftime('%Y%m%d')
        self.BEOLM_FORMAT = self.BEOLM.strftime('%Y%m%d')

        # ------------------------------ [ Standard Folders ] ------------------------------------- #
        self.FOLDER_SP_SCRIPT = Path(sys.argv[0]).resolve().parents[0]
        self.FOLDER_SP_TOOL = self.FOLDER_SP_SCRIPT.parents[0]
        self.FOLDER_SP_SUB = self.FOLDER_SP_SCRIPT.parents[1]
        self.FOLDER_SP_TEAM = self.FOLDER_SP_SCRIPT.parents[2]
        self.FOLDER_SP_ENV = self.FOLDER_SP_SCRIPT.parents[3]

        self.FOLDER_SP_APP_DOC = self.FOLDER_SP_SCRIPT.joinpath('appdoc')
        self.FOLDER_SP_LOG = self.FOLDER_SP_TOOL.joinpath('logs')
        self.FOLDER_SP_IN = self.FOLDER_SP_TOOL.joinpath('in')
        self.FOLDER_SP_OUT = self.FOLDER_SP_TOOL.joinpath('out')
        self.FOLDER_SP_ARC = self.FOLDER_SP_TOOL.joinpath('archive')
        self.FOLDER_SP_DB = self.FOLDER_SP_TEAM.joinpath('Database')
        self.FOLDER_SP_SCH = self.FOLDER_SP_TEAM.joinpath('Scheduling', 'scripts')

        # ------------------------------ [ Standard File Paths ] ------------------------------------- #
        self.PATH_LOG = self.FOLDER_SP_LOG.joinpath(f'{self.TD_FORMAT}_LOG.txt')
        self.PATH_APP_DOCS = self.FOLDER_SP_APP_DOC.joinpath('AppDoc.html')
        self.PATH_SCH_DB = self.FOLDER_SP_DB.joinpath('schedule_db.db')
        self.PATH_APP_DB = self.FOLDER_SP_DB.joinpath('app_db.db')
        self.PATH_IMG_RUN_APP = r"C:\Temp\Batch_Imagine\runApp_run.bat"
        self.PATH_IMG_RUN_APP_TABLE = r"C:\Temp\Batch_Imagine\runApp_run_table.bat"

        # export files
        self.PATH_EXPORT = self.FOLDER_SP_OUT.joinpath(f'{self.TD_FORMAT}_TEST.csv')

        # processed files
        self.PATH_PROCESSED = self.FOLDER_SP_IN.joinpath('Processed')
        self.PATH_NEW = self.FOLDER_SP_IN.joinpath('New')

        # ------------------------------ [ Config.ini ] ------------------------------------- #
        self.CFG_PARSER = configparser.ConfigParser()
        self.CFG_PARSER.read('../in/config.ini')

        # limits
        self.CFG_LIMIT_EXAMPLE = float(self.CFG_PARSER['Limits']['LIMIT_EXAMPLE'])

        # folders
        self.CFG_FOLDER_WORK_TRADES = Path(self.CFG_PARSER['Folders']['FOLDER_WORK_TRADES'])
        self.CFG_FOLDER_WORK_TRADES_PROCESSED = Path(self.CFG_PARSER['Folders']['FOLDER_WORK_TRADES_PROCESSED'])

        # mailing
        self.CFG_MAIL_TO_EXC = (self.CFG_PARSER['Mailing']['MAIL_TO_EXC']).replace("\n", "")
        self.CFG_MAIL_CC_EXC = (self.CFG_PARSER['Mailing']['MAIL_CC_EXC']).replace("\n", "")
        self.CFG_MAIL_TO_EOP = (self.CFG_PARSER['Mailing']['MAIL_TO_EOP']).replace("\n", "")
        self.CFG_MAIL_CC_EOP = (self.CFG_PARSER['Mailing']['MAIL_CC_EOP']).replace("\n", "")

        # switches
        self.CFG_TEST_MODE = int(self.CFG_PARSER['Switches']['TEST_MODE'])
        self.CFG_MASK_PASSWORD = int(self.CFG_PARSER['Switches']['MASK_PASSWORD'])

        # ------------------------------ [ Imagine Scripts] ------------------------------------- #
        self.IMG_GROUP = 'PythonOptimizer'
        self.IMG_NAME = 'PythonOptimizer'

        # downloads
        self.IMG_DL_PLD = r'Excel/exportPLD-LIABPortfolio/main'
        self.IMG_DL_PF = r'Excel/exportPortfolio/main'
        self.IMG_DL_LIAB = r'Excel/downloadLiabilities/main'
        self.IMG_UL_WORKTRADE = r'operations/dataUpdate/optimizerGeneric/main'

        # errors
        self.ERRORS = False
        self.ERROR_MESSAGE = ''

        # ------------------------------ [ Mailing ] ------------------------------------- #
        self.MAIL_TO_EXC = self.CFG_MAIL_TO_EXC
        self.MAIL_CC_EXC = self.CFG_MAIL_CC_EXC
        self.MAIL_SUBJECT_EXC = f'{self.TD_FORMAT} Process Failed'
        self.MAIL_BODY_EXC = 'Dear Colleague, <br>' \
                             '<br>' \
                             f'Process failed with Business Rule Exceptions:<br><br>' \
                             f' [ BUSINESS_RULES ] ' \
                             '<br>' \
                             f'Please check logfile in the attachment or app documentation.<br>' \
                             '<br>' \
                             f'<a href="">Output folder</a> <br>' \
                             f'<br>' \
                             f'<img src="" width="100%", height="100%"> <br>' \
                             '<br>' \
                             'Kind Regards, <br>' \
                             'PIM'

        self.MAIL_TO_EOP = self.CFG_MAIL_TO_EOP
        self.MAIL_CC_EOP = self.CFG_MAIL_CC_EOP
        self.MAIL_SUBJECT_EOP = f'{self.TD_FORMAT} Process Finished Successfully'
        self.MAIL_BODY_EOP = 'Dear Colleague, <br>' \
                             '<br>' \
                             f'Process finished with Business Rule Exceptions:<br><br>' \
                             f' [ BUSINESS_RULES ] ' \
                             '<br>' \
                             f'Please check logfile in the attachment or app documentation.<br>' \
                             '<br>' \
                             f'<a href="">Output folder</a> <br>' \
                             f'<br>' \
                             f'<img src="" width="100%", height="100%"> <br>' \
                             '<br>' \
                             'Kind Regards, <br>' \
                             'PIM'


class LogDecorator(Parameters):
    def __init__(self):
        super().__init__()

    def __call__(self, func):
        """
        Decorator function to log functions. Do not use for functions that have nested try/except in itself.
        :param func:
        :return:
        """

        def wrapper(*args, **kwargs):
            try:
                # log start of process in log of current application script
                time_before = time.time()
                with open(f'{self.PATH_LOG}', 'a') as f:
                    if func.__name__ == 'main':
                        with open('../in/config.ini', 'r') as cfg:
                            contents = cfg.read()
                        message = f'\n{"-" * 100}\n' \
                                  f'[{dt.datetime.now()}][{self.USER}] Process Started.\n\n' \
                                  f'Used config settings:\n\n{contents}\n'
                    else:
                        message = f'\n[{dt.datetime.now()}][{self.USER}] Started function: {func.__name__}.\n'
                    f.write(message)
                    print(message)

                # run actual code
                var = func(*args, **kwargs)

                # log end of process in log of current application script
                duration = time.time() - time_before
                with open(f'{self.PATH_LOG}', 'a') as f:
                    if func.__name__ == 'main':
                        message = f'\n[{dt.datetime.now()}][{self.USER}] Process Ended in ' \
                                  f'{round((duration / 60), 2)} minutes ({round(duration, 2)} seconds).\n' \
                                  f'{"-" * 100}\n\n'
                    else:
                        message = f'[{dt.datetime.now()}][{self.USER}] ' \
                                  f'Ended function: {func.__name__} in {round(duration, 6)} seconds.\n'
                    f.write(message)
                    print(message)

                return var

            except (ValueError, FileNotFoundError, KeyError, TypeError, AttributeError, ModuleNotFoundError,
                    PermissionError, IndexError, NameError, SyntaxError) as msg:

                # log failed process in log of current application script
                with open(f'{self.PATH_LOG}', 'a') as f:
                    message = f'\n[{dt.datetime.now()}][{self.USER}] Error in function: {func.__name__} {msg}.\n' \
                              f'{"-" * 100}\n'
                    f.write(message)
                    print(message)

                sys.exit()

        return wrapper


class ScheduleDecorator(Parameters):
    def __init__(self):
        super().__init__()

        # add the schedule folder to the sys path in order to import the script
        sys.path.append(str(self.FOLDER_SP_SCH))
        import schedule_db

        # connect to scheduler database
        self.database = schedule_db.Database(self.PATH_SCH_DB)

    def __call__(self, func):
        """
        Decorator function to connect to database. Has package requirements: datetime, sys, os.
        Can be deleted if not used.
        :param func:
        :return:
        """

        # add the folder to python-path, in order to find the database class as a package.

        def wrapper(*args, **kwargs):
            # connect to schedule database

            # parse receiving arguments from batch
            script_name = sys.argv[0]
            if len(sys.argv) > 1:
                schedule_id = int(sys.argv[1])
            else:
                # on manual runs, ask the id.
                for i in self.database.fetch_logs()[1]:
                    print(f"{i[2]}: {i[3]}")
                schedule_id = int(input("What is the schedule id of this job?: "))

            try:
                # run actual code
                var = func(*args, **kwargs)

                # write success to the scheduling database
                self.database.update_last_run(last_run=dt.datetime.now(), last_status=1, schedule_id=schedule_id)
                self.database.write_log(dt.datetime.now(), f'SUCCESS: {script_name}')

                # if the actual function has to return something, it should be returned here as well
                return var

            except (ValueError, FileNotFoundError, KeyError, TypeError, AttributeError,
                    PermissionError, IndexError, NameError, SyntaxError) as msg:

                # write fail to the scheduling database
                self.database.update_last_run(last_run=dt.datetime.now(), last_status=3, schedule_id=schedule_id)
                self.database.write_log(dt.datetime.now(), f'FAILED: {script_name} {msg}')

        return wrapper


class Menu(Parameters):
    def __init__(self):
        super().__init__()

    def __call__(self, menu_options):
        """
        Add menu options.
        :param menu_options: dict, with run code, and function name in lower case and display text in a list.
        :return: str, to be evaluated in main.
        """
        while True:
            add_options = ""
            for key in menu_options:
                if key.lower() in ("r", "e", "s", "h"):
                    raise KeyError('The run-keys ("r", "e", "s", "h") are already in use.')
                else:
                    add_options += f"[{key}] {menu_options[key][1]}\n"

            print("----------------------------------------------------\n"
                  " Process:  \n"
                  " Owner:    \n"
                  "----------------------------------------------------\n\n"
                  "[MENU]\n\n"
                  "[r] Run\n"
                  f"{add_options}"
                  "[e] Exit\n"
                  "[s] Settings\n"
                  "[h] Help\n\n")

            run_type = input(f'Choose run type: ')

            if run_type.isspace() or len(run_type) == 0:
                continue
            elif run_type.lower() not in ("r", "e", "s", "h"):
                try:
                    return f"{menu_options[run_type.lower()][0]}()\n" \
                           f"input('Press Enter to go back to Menu.')"
                except (KeyError, NameError):
                    print('There is no function for that key.\n')
            elif run_type.lower() == "r":
                return "main()\n" \
                       "APP.eop_cleanup()\n" \
                       "input('Press Enter to go back to Menu.')"
            elif run_type.lower() == 's':
                self.settings()
            elif run_type.lower() == 'h':
                self.help_info()
            elif run_type.lower() == 'e':
                sys.exit()

            input("Press Enter to go back to Menu.")

    def help_info(self):
        print("""
        [HELP]

        Opening App Docs.
        See Web browser. 
        If the CSS does not render, visit: https://robecobv.sharepoint.com/sites/TMPIMEUDA
        Then refresh the AppDoc.html.

        """)
        webbrowser.open(str(self.PATH_APP_DOCS))

    def settings(self):
        print(f"""
        [SETTINGS]
        
        Restart the app after every change in the config.ini!
        
        Short description of tool.
        
        Used limits / variables or statuses in database.
        ----------------------------
        CFG_LIMIT_EXAMPLE = {self.CFG_LIMIT_EXAMPLE}

    """)


class AppTemplate(Parameters):
    def __init__(self):
        super().__init__()

    # ============================== [ General Functions ] ======================================= #
    def write_log(self, txt):
        """
        Function to create a log file and write to at any point in the script in addition to the logger decorator.
        :param txt: string text to be logged.
        :return: prints text to terminal and creates/appends to .txt
        """
        with open(f'{self.PATH_LOG}', 'a') as f:
            message = f'[{dt.datetime.now()}][{self.USER}] {txt}\n'
            f.write(message)
            print(message)

    @staticmethod
    def check_path_tree():
        """
        Helper function to check the relative paths.
        :return:
        """
        p = Path(sys.argv[0]).resolve()
        print(f"\nIn  [X]: p = Path(sys.argv[0]).resolve()\nOut [X]: {p}\n")
        print(f"In  [Y]: p = Path(sys.argv[0]).resolve().home()\nOut [Y]: {p.home()}\n")

        for path in enumerate(p.parents):
            result = str(path[1])
            code = f"p = Path(sys.argv[0]).resolve().parents[{path[0]}]"
            print(f"In  [{path[0]}]: {code}\nOut [{path[0]}]: {result}\n")

    @staticmethod
    def get_files_in_folder(*args, folder, include_mask=True):
        """
        Find files on a folder based on search criteria.
        :param args: list of file masks
        :param folder: full path of folder
        :param include_mask: do we need to include the mask in the file or exclude to mask from the file
        :return: filtered list of files on the folder
        """
        if isinstance(folder, list):
            list_folder = folder
        elif os.path.isdir(folder):
            list_folder = os.listdir(folder)
        else:
            print('type error folder variable not Path like object or list')
            return None

        list_folder = [f for f in list_folder if "~" not in f]

        args = args[0]

        if include_mask:
            for x in range(len(args)):
                list_folder = [f for f in list_folder if str(args[x]).lower() in f.lower()]

        else:
            for x in range(len(args)):
                list_folder = [f for f in list_folder if str(args[x]).lower() not in f.lower()]

        return list_folder

    @staticmethod
    def archiving(folder):
        # Create an archive folder in the Folder to cleanup
        folder_archive = os.path.join(folder, 'archive')
        if not os.path.isdir(folder_archive):
            os.mkdir(folder_archive)

        # find unique filenames that have a yyyy prefix in the cleanup folder
        unique_dates = set([x[:8] for x in os.listdir(folder)
                            if not os.path.isdir(os.path.join(folder, x))
                            and x[:2] == '20'])

        # for each date bundle all files
        for date in unique_dates:
            list_of_files = [file for file in os.listdir(folder)
                             if not os.path.isdir(os.path.join(folder, file))
                             and date in file]

            for f in list_of_files:
                source = os.path.join(folder, f)

                # create date folder if not exists
                target_folder = os.path.join(folder_archive, date)
                if not os.path.isdir(target_folder):
                    os.mkdir(target_folder)

                # actual move
                target = os.path.join(target_folder, f)
                shutil.move(source, target)

    def replace_string_date(self, text, period):
        """
        Replaces string date in text (yyyymmdd) to variable date of choice.
        :param text: AnyString that contains the yyyymmmdd.
        :param period: [TD] Today. [BD1] Today minus one Business day. [BEOLM] Last Business day of last month.
        :return: String with replaced date.
        """

        # find the date in the provided string
        regex = re.compile(r'20\d{2}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])')

        # set the new date it should be replaced with
        if period.upper() == "TD":
            date_setting = self.TD_FORMAT
        elif period.upper() == "BD1":
            date_setting = self.BD1_FORMAT
        elif period.upper() == "BEOLM":
            date_setting = self.BEOLM_FORMAT
        else:
            raise TypeError(f"Got an unexpected keyword argument '{period}'")

        try:
            # Get the matching string from the regex. If nothing is found it will trigger the Attribute Error
            date_string = re.search(regex, text).group()

            # index slice the year, month and day from the matching string
            year = int(date_string[:4])
            month = int(date_string[4:6])
            day = int(date_string[6:8])

            # actual check that will trigger a value error if not a valid date.
            dt.date(year, month, day)

            # substitute the matching string with the new replacement string
            return re.sub(regex, date_setting, text)

        except AttributeError:
            raise AttributeError("No valid date found.")

        except ValueError as msg:
            raise ValueError(f"Not a valid date: {msg}")

    def switch_user(self, job_path):
        """
        Refactor the username from config in order to connect to the SharePoint directory. E.g. ROB0000 to GEN0000.
        :param job_path: str/Path obj
        :return: Path obj
        """
        path_current_user = Path("C:/Users").joinpath(self.USER)
        path_suffix = Path(job_path).parts[3:]
        new_path = path_current_user.joinpath(*path_suffix)

        return new_path

    # @LogDecorator()
    def send_mail(self, mail_to, mail_cc, subject, body):
        """
        Contains the outlook mailing setup and sends out the mail with attachment, which are the new guidelines.
        :param mail_to:
        :param mail_cc:
        :param subject:
        :param body:
        :return:
        """

        # Create mail
        outlook = win32com.client.Dispatch('outlook.application')
        mail = outlook.CreateItem(0)
        mail.To = mail_to
        mail.Cc = mail_cc
        mail.Subject = subject
        mail.HTMLBody = body
        mail.Attachments.Add(str(self.PATH_LOG))

        mail.Display()

    def eop_cleanup(self):
        """
        Runs after main completed in order to send mail with completed process log.
        Query database for business rules if necessary and substitute mail body.
        :return:
        """
        if self.ERRORS:
            print(self.ERROR_MESSAGE)
        else:
            print(f'\n \n---- SUCCESS ---- \n'
                  f'Work trade upload process ended successfully! \n'
                  f'---- SUCCESS ----')

    @LogDecorator()
    def imagine_api(self, javascript, input_dict, login):
        """
        Helper function for imagine downloads. Make sure excel is not logged in into Imagine.
        :param javascript:
        :param input_dict:
        :param login:
        :return:
        """
        self.write_log(f"Using JavaScript: {javascript} with parameters: {input_dict}")

        con = None
        try:  # If wrong password is used - error handling will quit program directly
            stop = ForceStop(login['id'], login['pw'], login['group'])
            stop.close()
            con = RESTConnect(login['id'], login['pw'], login['group'], login['name'])
        except Exception as msg:  # if error in opening a new node -> send a get request, take/delete the session ID
            self.write_log(f'Imagine API error: {msg}')
            stop = ForceStop(login['id'], login['pw'], login['group'])
            stop.close()

        try:
            result = con.execute(javascript, body=input_dict)
            if isinstance(result, list):
                df_result = pd.DataFrame(result[1:], columns=result[0])

            elif isinstance(result, dict):
                df_result = pd.DataFrame.from_dict(result.items())
                df_result.columns = ['Identifier', 'Result']

            elif list(result.keys())[0] == 'errors':
                self.write_log(f"Imagine API error: {result['errors'][0]['message']}")
                df_result = None

            elif result['data'][0][0] == 'ERROR':
                self.write_log(f"Imagine API error {result['data'][0][4]}")
                df_result = None

            elif 'its_create' in javascript:
                success = result['data'][0][0]
                holding_id = result['data'][0][1]
                order_id = result['data'][0][2]
                sm_id = result['data'][0][3]
                self.write_log('Status: {}, Holding ID: {}, Order ID: {}, SM ID: {}'
                               .format(success, holding_id, order_id, sm_id))

                df_result = json.loads(result['data'][0][4].split("results: ")[1])

            else:
                df_result = pd.DataFrame(result[1:], columns=result[0])

            con.close()
            return df_result

        except Exception as msg:
            self.write_log(f"Imagine API error: {msg}")
            con.close()

    @LogDecorator()
    def batch_ios(self, input_file, output_file, input_table=None):
        """
        Triggers batch through IOS.
        :param input_file: str, filepath for trigger file with javascript and setting parameters
        :param output_file: str, filepath for exports
        :param input_table: str, filepath to csv table file
        :return: writes log from imagine
        """
        self.write_log(f"Processing {input_file}.")

        # call the run app batch file (see filepath run_app) through the application IOS.
        service = "runApp"

        if input_table is None:
            subprocess.call([self.PATH_IMG_RUN_APP, input_file, output_file, service])
        else:
            subprocess.call([self.PATH_IMG_RUN_APP_TABLE, input_file, output_file, service, input_table])

        # read log on abnormal errors
        input_file_log = input_file.replace('.csv', '_Log.txt')

        with open(input_file_log, 'r') as file:
            contents = file.read()
            contents = contents.lower()
            y = contents.find('session terminated abnormally')
            uat_ops = contents.find('uat_ops')
            ops_uat = contents.find('ops_uat')

        if y > 0:
            self.write_log(f"BUSINESS RULE EXCEPTION: Batch IOS Session terminated abnormally. "
                           f"Please check batch log:\n{input_file_log}")
            sys.exit()

        if uat_ops > 0 or ops_uat > 0:
            self.write_log(f"BUSINESS RULE EXCEPTION: "
                           f"User uploaded in UAT for Batch IOS Session. Please check batch log:\n{input_file_log}")


class Login(AppTemplate):
    def __init__(self):
        # ------------------------------ [ Imagine REST ] -------------------------------------
        super().__init__()
        self.user_name = ""
        self.pass_word = ""
        self.choice()
        self.check_img_env()

    def choice(self):
        from_bat = input(f'Get Imagine login credentials from {self.PATH_IMG_RUN_APP}? (Y/N): ')
        # open bat file and read credentials
        if from_bat.lower() == 'y' and os.path.isfile(self.PATH_IMG_RUN_APP):
            with open(self.PATH_IMG_RUN_APP) as f:
                contents = f.readlines()
                for i in contents:
                    if "username" in i:
                        self.user_name = i.split('=')[1].strip()

                    if "password" in i:
                        self.pass_word = i.split('=')[1].strip()

                    if self.user_name != "" and self.pass_word != "":
                        break
        else:
            # let user input credentials
            self.user_name = input("Please type your Imagine userid: ").strip()
            if self.CFG_MASK_PASSWORD == 1:
                self.pass_word = pwinput.pwinput(prompt="Please type your Imagine Password: ", mask="*")
            else:
                self.pass_word = input("Please type your Imagine Password: ")

    def check_img_env(self):
        """
        Show the user in which Imagine they logged into.
        :return:
        """
        if "uat" in self.user_name.lower():
            environment = "UAT Acceptance"
        elif "dev" in self.user_name.lower():
            environment = "DEV Development"
        elif 'santoex' in self.user_name.lower():  # temp accounts
            environment = "PRD Production"
        elif "ops" not in self.user_name.lower():
            environment = "Invalid user id."
        else:
            environment = "PRD Production"

        continue_uat = input(f'Continue in {environment}? (Y/N): ')
        if continue_uat.lower() == 'n':
            sys.exit()

        self.write_log(f"Login: {self.user_name} in {environment}")

    def get_login(self):
        login_details = {
            "id": self.user_name,
            "pw": self.pass_word,
            "group": self.IMG_GROUP,
            "name": self.IMG_NAME
        }
        return login_details
