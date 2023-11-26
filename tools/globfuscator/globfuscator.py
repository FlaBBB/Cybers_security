import os
import re
import string
import platform
import argparse
import itertools

class globfuscator:
    REGEX_SPECIAL_CHAR = {
        '.': '\.',
        '^': '\^',
        '$': '\$',
        '*': '\*',
        '+': '\+',
        '?': '\?',
        '{': '\{',
        '}': '\}',
        '[': '\[',
        ']': '\]',
        '(': '\(',
        ')': '\)',
        '|': '\|',
        '\\': '\\\\',
        '/': '\/'
    }

    def __init__(self, not_allowed_string: list = []) -> None:
        self.__ENV = os.environ.items()
        self.__ENV_NAME_DICT = [name.lower() for name, _ in self.__ENV]
        self.__platform = platform.system()

        if self.__platform.lower() == "windows":
            self.__re_dictionary = {
                '?': '[^<>:"/\\|?*]',
                '*': '[^<>:"/\\|?*]*'
            }
            self.__dir_trans = '\\'
        elif self.__platform.lower() == "linux":
            self.__re_dictionary = {
                '?': "[^/\0]",
                '*': "[^/\0]+"
            }
            self.__dir_trans = '/'
        else:
            raise "PLATFORM_NOT_SUPPORTED"

        self.not_allowed_string = not_allowed_string
        return None

    def __replace_with_env(self, path: str) -> tuple:
        env = ("", "")
        for name, value in self.__ENV:
            if value.lower() == path[:len(value.lower())].lower() and env[1].lower() < value.lower():
                env = name, value
        if env != ("", ""):
            return (env[0],  re.compile(re.escape(env[1]), re.IGNORECASE).sub("", path))
        else:
            return (path)

    def get_score(self, in_string: str, ori_string: str) -> int:
        max_score = len(ori_string) * 2
        score = max_score
        for s in in_string:
            if s in (string.ascii_letters + string.digits):
                score -= 2
            elif s in ['?', '*']:
                score -= 1
        return score, round((score / max_score) * 100, 2)

    def __re_check(self, in_string: str, globuscated_str: str, dirs: list) -> bool:
        re_pattern = "^"
        for g in globuscated_str:
            if g in self.__re_dictionary:
                re_pattern += self.__re_dictionary[g]
            elif g in self.REGEX_SPECIAL_CHAR:
                re_pattern += self.REGEX_SPECIAL_CHAR[g]
            else:
                re_pattern += g
        re_pattern += "$"

        if not bool(re.search(re_pattern.lower(), in_string.lower())):
            return False

        for d in dirs:
            if bool(re.search(re_pattern.lower(), d.lower())):
                if d.lower() != in_string.lower():
                    return False

        return True

    def __get_dir(self, path: tuple) -> list:
        path_s = ""
        for p in path:
            path_s += p

        self.path = path_s
        path_s = path_s.split(self.__dir_trans)
        if len(path) > 1 and type(path) == tuple:
            path_s[0] = os.path.expandvars("%" + path_s[0] + "%")
        self.path_s = path_s
        path_a = ""

        res = []
        for i in range(len(path_s) - 1):
            if path_a == "" and self.__platform.lower() == 'windows':
                path_a += path_s[i]
                if ":" in path_a:
                    path_a += self.__dir_trans
            else:
                if path_a[-1] != self.__dir_trans:
                    path_a += self.__dir_trans
                path_a += path_s[i] + self.__dir_trans
            res.append(os.listdir(path_a))

        return res
    
    def get_max_asterisk_conv(self, in_string: str) -> int:
        return len(in_string) * (len(in_string) + 1) // 2

    def get_max_question_conv(self, in_string: str, is_max_seed = False) -> int:
        max_conversable = 0
        for t in in_string:
            if t not in ["*", "?"]:
                max_conversable += 1

        return 2 ** max_conversable - 1 if is_max_seed else max_conversable

    def asterisk_conv(self, in_string: str, seed: int) -> str:
        if seed < 1 or seed > self.get_max_asterisk_conv(in_string):
            return in_string

        x = 1
        for i in list(range(1, len(in_string) + 1))[::-1]:
            if seed > i:
                seed -= i
                x += 1
            else:
                break
        return in_string[:seed - 1] + "*" + in_string[seed - 1 + x:]
    
    def question_conv(self, in_string: str, pattern_list:tuple) -> str:
        max_conversable = self.get_max_question_conv(in_string)

        pattern = ""
        for i in range(max_conversable):
            if i in pattern_list:
                pattern += "0"
            else:
                pattern += "1"

        res = ''
        for z in in_string:
            if z in ["*", "?"]:
                res += z
            else:
                if pattern[0] == "0":
                    res += z
                elif pattern[0] == "1":
                    res += "?"
                pattern = pattern[1:]

        return res

    def __globfuscating(self, name_path: str, dirs:list, is_env:bool = False) -> str:
        globfuscated_path = name_path
        max_asterisk_conv = self.get_max_asterisk_conv(name_path)
        for a in range(max_asterisk_conv if not is_env else -1, -1, -1):
            asterisk_path = self.asterisk_conv(name_path, a)
            if (is_env and "*" in asterisk_path) or (not self.__re_check(name_path, asterisk_path, dirs)):
                continue
            
            max_question_conv = self.get_max_question_conv(asterisk_path)

            for b in range(1, max_question_conv):
                for c in itertools.combinations(range(max_question_conv), b):
                    globfuscated_path = self.question_conv(asterisk_path, c)

                    is_nas = False
                    for nas in self.not_allowed_string:
                        if nas in globfuscated_path:
                            is_nas = True
                            break
                    if is_nas:
                        continue

                    if not self.__re_check(name_path, globfuscated_path, dirs):
                        continue
                    
                    return globfuscated_path

        return globfuscated_path


    def main(self, main_path: str) -> str:
        while self.__dir_trans * 2 in main_path:
            main_path = main_path.replace(
                self.__dir_trans * 2, self.__dir_trans)
        self.path = main_path

        if self.__platform.lower() == "windows":
            path = self.__replace_with_env(self.path)
        elif self.__platform.lower() == "linux":
            path = self.path
        self.dirs = self.__get_dir(path)

        if len(path) > 1 and type(path) == tuple:
            res = "$env:" + \
                self.__globfuscating(path[0], self.__ENV_NAME_DICT, True)
        else:
            res = self.path_s[0]

        for i in range(1, len(self.path_s)):
            res += self.__dir_trans + \
                self.__globfuscating(self.path_s[i], self.dirs[i - 1])

        return res, self.get_score(res, self.path)
    
    @staticmethod
    def parser(path: str) -> argparse.Namespace:
        parser = argparse.ArgumentParser(
            description='Obfuscate path string using wildcard.')

        parser.add_argument('-p', '--path', type=str, help='Specify the path.')
        parser.add_argument('-d', '--banned_string', type=str,
                            help='Specify the banned string. eg:"home,*,k" for multiple')
        parser.add_argument('-V', '--version', action='version',
                            version='%(prog)s version 1.0')

        args = parser.parse_args()
        if args.path == None:
            parser.print_help()
            parser.exit()

        banned_strings = args.banned_string
        if banned_strings == None:
            banned_strings = []
        else:
            if ',' in banned_strings:
                banned_strings = banned_strings.split(',')
            else:
                banned_strings = [banned_strings]
        
        args.banned_string = banned_strings

        return args
    
    @staticmethod
    def globfuscator(path: str = None, not_allowed_string: list = []) -> str:
        if path == None:
            parser = globfuscator.parser(path)
            path = parser.path
            not_allowed_string = parser.banned_string
        glob = globfuscator(not_allowed_string)
        return glob.main(path)


if __name__ == "__main__":
    path = r"C:\Program Files (x86)\Realtek\Realtek Bluetooth\rtl8723b_mp_chip_bt40_fw_asic_rom_patch_new.dat"
    result, score = globfuscator.globfuscator(path)
    print(f"result = {result} ({score[0]} - {score[1]}%)")