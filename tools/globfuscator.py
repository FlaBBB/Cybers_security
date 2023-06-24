import os
import re
import string
import platform
import argparse


class globfuscator:
    def __init__(self, not_allowed_string: list = []) -> None:
        self.__ENV = os.environ.items()
        self.__ENV_NAME_DICT = [name.lower() for name, value in self.__ENV]
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
        score = len(ori_string) * 2
        for s in in_string:
            if s in (string.ascii_letters + string.digits):
                score -= 2
            elif s in ['?', '*']:
                score -= 1
        return score

    def __re_check(self, in_string: str, globuscated_str: str, dirs: list) -> bool:
        re_pattern = "^"
        for g in globuscated_str:
            if g in self.__re_dictionary:
                re_pattern += self.__re_dictionary[g]
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

    def asterisk_conv(self, in_string: str, seed: int) -> str:
        if seed < 1:
            return in_string

        x = 1
        for i in list(range(1, len(in_string) + 1))[::-1]:
            if seed > i:
                seed -= i
                x += 1
            else:
                break
        return in_string[:seed - 1] + "*" + in_string[seed - 1 + x:]

    def question_conv(self, in_string: str, seed: int) -> str:
        if seed < 1:
            return in_string

        tot_raw = 0
        for t in in_string:
            if t not in ["*", "?"]:
                tot_raw += 1

        i_o = bin(seed)[2:].zfill(tot_raw)

        res = ''
        for z in in_string:
            if z in ["*", "?"]:
                res += z
            else:
                if i_o[0] == "0":
                    res += z
                elif i_o[0] == "1":
                    res += "?"
                i_o = i_o[1:]

        return res

    def __globfuscating(self, in_string: str, dirs: list, is_env: bool = False) -> str:
        score = 0
        path_t = in_string
        for a in range(sum(range(1, len(in_string) + 1)) + 1):
            temp_a = self.asterisk_conv(in_string, a)

            if is_env and "*" in temp_a:
                break

            tot_raw_temp = 0
            for t in temp_a:
                if t not in ["*", "?"]:
                    tot_raw_temp += 1

            for b in range((2 ** (tot_raw_temp))):
                temp_b = self.question_conv(temp_a, b)
                t_score = self.get_score(temp_b, in_string)

                is_nas = False
                for nas in self.not_allowed_string:
                    if nas in temp_b:
                        is_nas = True
                        break
                if is_nas:
                    continue

                if t_score < score:
                    continue

                if not self.__re_check(in_string, temp_b, dirs):
                    continue

                score = t_score
                path_t = temp_b

        return path_t

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

        return res


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Obfuscate path string using wildcard. *note: only work on local')

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

    glob = globfuscator(not_allowed_string=banned_strings)
    print("result =", glob.main(args.path))