import re
import sublime
import sublime_plugin

DEBUG_ENABLED = False
PRINT_CONTEXT = False

# Toggle between single-line or multi-line formatted css statement
#
# Add the following line to Preferences > Key Bindings - User
# { "keys": ["ctrl+shift+j"], "command": "toggle_single_line_css" }
#
# Credit: http://www.sublimetext.com/forum/viewtopic.php?f=6&t=2237


class ToggleSingleLineCssCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        debug('Invoked "toggle_single_line_css" with %d region(s)' % len(self.view.sel()))
        for region in reversed(self.view.sel()):
            text = self.view.substr(region)

            # check if the css statement needs to be expanded or collapsed
            if re.match(r"^.*\{.*}\s*$", text):
                # expand the css statement
                debug("The css statement needs to be expanded", text)
                m = re.search(r"^(?P<key>.*)\{(?P<params>.*);\s*}$", text)
                if not m:
                    continue
                multiline = "%s{\n\t%s;\n}" % (m.group("key"), m.group("params").strip().replace("; ", ";\n\t"))
                self.view.replace(edit, region, multiline)
            else:
                debug("The css statement needs to be collapsed", text)
                # collapse the css statement
                singleline = " ".join([x.strip() for x in text.split("\n")])
                self.view.replace(edit, region, singleline)


def debug(text, context=""):
    if DEBUG_ENABLED:
        print('[toggle_single_line_css]: ' + text)
    if PRINT_CONTEXT and context != "":
        print(">>> " + context)
