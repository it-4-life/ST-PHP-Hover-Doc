import sublime
import sublime_plugin
import webbrowser
import subprocess
import html
import re

class ShowScopeNameCommand(sublime_plugin.EventListener):
    def on_hover(self, view, point, hover_zone):
        fileName = view.file_name()

        regexFileExts = r"\.php$"
        if (fileName):
            isMatchedFile = re.search(regexFileExts, fileName, re.IGNORECASE)
        else:
            isMatchedFile = view.settings().get('syntax') == 'Packages/PHP/PHP.sublime-syntax'

        if (hover_zone == sublime.HOVER_TEXT and isMatchedFile):
            word = view.substr(view.word(point))
            line = view.substr(view.line(point))
            line = line[line.find(word):]

            regexMatchFunctionName = r"(?:^|\s|[^a-z0-9_])+([a-z0-9_]+?)\s*\("
            matchFunctionName = re.search(regexMatchFunctionName, line, re.IGNORECASE)

            if (matchFunctionName):
                functionName = matchFunctionName.group(1)
                if (line.startswith(functionName)):
                    doc = subprocess.check_output(['pman', functionName]).decode()
                    htmlContent = '<a href="https://secure.php.net/en/%s">View on php.net/%s</a><br>%s' % (
                        functionName,
                        functionName,
                        html.escape(doc, quote = False).replace('\n', '<br>\n').replace('  ', '&nbsp;')
                    )

                    view.show_popup(
                        htmlContent,
                        max_width = 800,
                        location = point,
                        flags = sublime.HIDE_ON_MOUSE_MOVE_AWAY,
                        on_navigate = webbrowser.open_new_tab
                    )

        return
