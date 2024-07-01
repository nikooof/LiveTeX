import re
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.Qsci import QsciLexerCustom, QsciScintilla

class TexCustomLexer(QsciLexerCustom):

    def __init__(self, parent):
        super().__init__(parent)
        self.initColors()
        self.initStyles()
        self.initFonts()
        self.KEYWORD_LIST = ['begin', 'pagestyle', 'fancyhf', 'fancyfoot', 'renewcommand', 'usepackage', 'documentclass', 'above', 'abovedisplayshortskip', 'abovedisplayskip', 'abovewithdelims', 'accent', 'adjdemerits', 'advance', '', 'afterassignment', 'aftergroup', 'atop', 'atopwithdelims', '', 'badness', 'baselineskip', 'batchmode', 'begingroup', '', 'belowdisplayshortskip', 'belowdisplayskip', 'binoppenalty', '', 'botmark', 'box', 'boxmaxdepth', 'brokenpenalty', 'catcode', 'char', '', 'chardef', 'cleaders', 'closein', 'closeout', 'clubpenalty', 'copy', '', 'count', 'countdef', 'cr', 'crcr', 'csname', 'day', 'deadcycles', 'def', '', 'defaulthyphenchar', 'defaultskewchar', 'delcode', 'delimiter', '', 'delimiterfactor', 'delimeters', 'delimitershortfall', '', 'delimeters', 'dimen', 'dimendef', 'discretionary', '', 'displayindent', 'displaylimits', 'displaystyle', '', 'displaywidowpenalty', 'displaywidth', 'divide', '', 'doublehyphendemerits', 'dp', 'dump', 'edef', 'else', '', 'emergencystretch', 'end', 'endcsname', 'endgroup', 'endinput', '', 'endlinechar', 'eqno', 'errhelp', 'errmessage', '', 'errorcontextlines', 'errorstopmode', 'escapechar', 'everycr', '', 'everydisplay', 'everyhbox', 'everyjob', 'everymath', 'everypar', '', 'everyvbox', 'exhyphenpenalty', 'expandafter', 'fam', 'fi', '', 'finalhyphendemerits', 'firstmark', 'floatingpenalty', 'font', '', 'fontdimen', 'fontname', 'futurelet', 'gdef', 'global', 'group', '', 'globaldefs', 'halign', 'hangafter', 'hangindent', 'hbadness', '', 'hbox', 'hfil', 'horizontal', 'hfill', 'horizontal', 'hfilneg', 'hfuzz', '', 'hoffset', 'holdinginserts', 'hrule', 'hsize', 'hskip', 'hss', '', 'horizontal', 'ht', 'hyphenation', 'hyphenchar', 'hyphenpenalty', '', 'hyphen', 'if', 'ifcase', 'ifcat', 'ifdim', 'ifeof', 'iffalse', 'ifhbox', '', 'ifhmode', 'ifinner', 'ifmmode', 'ifnum', 'ifodd', 'iftrue', 'ifvbox', '', 'ifvmode', 'ifvoid', 'ifx', 'ignorespaces', 'immediate', 'indent', '', 'input', 'inputlineno', 'input', 'insert', 'insertpenalties', '', 'interlinepenalty', 'jobname', 'kern', 'language', 'lastbox', '', 'lastkern', 'lastpenalty', 'lastskip', 'lccode', 'leaders', 'left', '', 'lefthyphenmin', 'leftskip', 'leqno', 'let', 'limits', 'linepenalty', '', 'line', 'lineskip', 'lineskiplimit', 'long', 'looseness', 'lower', '', 'lowercase', 'mag', 'mark', 'mathaccent', 'mathbin', 'mathchar', '', 'mathchardef', 'mathchoice', 'mathclose', 'mathcode', 'mathinner', '', 'mathop', 'mathopen', 'mathord', 'mathpunct', 'mathrel', '', 'mathsurround', 'maxdeadcycles', 'maxdepth', 'meaning', '', 'medmuskip', 'message', 'mkern', 'month', 'moveleft', 'moveright', '', 'mskip', 'multiply', 'muskip', 'muskipdef', 'newlinechar', 'noalign', '', 'noboundary', 'noexpand', 'noindent', 'nolimits', 'nonscript', '', 'scriptscript', 'nonstopmode', 'nulldelimiterspace', '', 'nullfont', 'number', 'omit', 'openin', 'openout', 'or', 'outer', 'output', '', 'outputpenalty', 'over', 'overfullrule', 'overline', '', 'overwithdelims', 'pagedepth', 'pagefilllstretch', '', 'pagefillstretch', 'pagefilstretch', 'pagegoal', 'pageshrink', '', 'pagestretch', 'pagetotal', 'par', 'parfillskip', 'parindent', '', 'parshape', 'parskip', 'patterns', 'pausing', 'penalty', '', 'postdisplaypenalty', 'predisplaypenalty', 'predisplaysize', '', 'pretolerance', 'prevdepth', 'prevgraf', 'radical', 'raise', 'read', '', 'relax', 'relpenalty', 'right', 'righthyphenmin', 'rightskip', '', 'romannumeral', 'scriptfont', 'scriptscriptfont', '', 'scriptscriptstyle', 'scriptspace', 'scriptstyle', '', 'scrollmode', 'setbox', 'setlanguage', 'sfcode', 'shipout', 'show', '', 'showbox', 'showboxbreadth', 'showboxdepth', 'showlists', '', 'showthe', 'skewchar', 'skip', 'skipdef', 'spacefactor', 'spaceskip', '', 'span', 'special', 'splitbotmark', 'splitfirstmark', '', 'splitmaxdepth', 'splittopskip', 'string', 'tabskip', 'textfont', '', 'textstyle', 'the', 'thickmuskip', 'thinmuskip', 'time', 'toks', '', 'toksdef', 'tolerance', 'topmark', 'topskip', 'tracingcommands', '', 'tracinglostchars', 'tracingmacros', 'tracingonline', '', 'tracingoutput', 'tracingpages', 'tracingparagraphs', '', 'tracingrestores', 'tracingstats', 'uccode', 'uchyph', '', 'underline', 'unhbox', 'unhcopy', 'unkern', 'unpenalty', 'unskip', '', 'unvbox', 'unvcopy', 'uppercase', 'vadjust', 'valign', 'vbadness', '', 'vbox', 'vcenter', 'vfil', 'vfill', 'vfilneg', 'vfuzz', 'voffset', 'vrule', '', 'vsize', 'vskip', 'vsplit', 'vss', 'vtop', 'wd', 'widowpenalty', 'write', '', 'xdef', 'xleaders', 'xspaceskip', 'year', '', 'TeX', 'bgroup', 'egroup', 'endgraf', 'space', 'empty', 'null', 'newcount', '', 'newdimen', 'newskip', 'newmuskip', 'newbox', 'newtoks', 'newhelp', '', 'newread', 'newwrite', 'newfam', 'newlanguage', 'newinsert', 'newif', '', 'maxdimen', 'magstephalf', 'magstep', 'frenchspacing', '', 'nonfrenchspacing', 'normalbaselines', 'obeylines', '', 'obeyspaces', 'raggedr', 'ight', 'ttraggedright', 'thinspace', '', 'negthinspace', 'enspace', 'enskip', 'quad', 'qquad', 'smallskip', '', 'medskip', 'bigskip', 'removelastskip', 'topglue', 'vglue', 'hglue', '', 'break', 'nobreak', 'allowbreak', 'filbreak', 'goodbreak', '', 'smallbreak', 'medbreak', 'bigbreak', 'line', 'leftline', '', 'rightline', 'centerline', 'rlap', 'llap', 'underbar', 'strutbox', '', 'strut', 'cases', 'matrix', 'pmatrix', 'bordermatrix', 'eqalign', '', 'displaylines', 'eqalignno', 'leqalignno', 'pageno', 'folio', '', 'tracingall', 'showhyphens', 'fmtname', 'fmtversion', 'hphantom', '', 'vphantom', 'phantom', 'smash']

    def initColors(self):
        self.color1 = "#e6e6e6"
        self.color2 = "#141221"
        self.setDefaultColor(QColor(self.color1))
        self.setDefaultPaper(QColor(self.color2))

    def initStyles(self):
        self.DEFAULT = 0
        self.KEYWORD = 1
        self.KEYARGS = 4
        self.BRACKETS = 5
        self.COMMENTS = 6

        self.setColor(QColor(self.color1), self.DEFAULT)
        self.setColor(QColor("#9CDCFE"), self.KEYWORD)
        self.setColor(QColor("#c678dd"), self.KEYARGS)
        self.setColor(QColor("#fcf403"), self.BRACKETS)
        self.setColor(QColor("#4EC9B0"), self.COMMENTS)

        self.setPaper(QColor(self.color2), self.DEFAULT)
        self.setPaper(QColor(self.color2), self.KEYWORD)
        self.setPaper(QColor(self.color2), self.KEYARGS)
        self.setPaper(QColor(self.color2), self.BRACKETS)
        self.setPaper(QColor(self.color2), self.COMMENTS)

    def initFonts(self):
        font = QFont("Arial", 14, weight=QFont.Bold)
        self.setDefaultFont(font)
        self.setFont(font, self.DEFAULT)
        self.setFont(font, self.KEYWORD)

    def language(self):
        return "TexCustomLexer"

    def description(self, style):
        descriptions = {
            self.DEFAULT: "DEFAULT",
            self.KEYWORD: "KEYWORD",
            self.KEYARGS: "KEYARGS",
            self.BRACKETS: "BRACKETS",
            self.COMMENTS: "COMMENTS"
        }
        return descriptions.get(style, "")

    def getTokens(self, text):
        pattern = re.compile(r"[*]\/|\/[*]|\s+|\w+|\W")
        return [(token, len(token.encode("utf-8"))) for token in pattern.findall(text)]

    def styleText(self, start, end):
        self.startStyling(start)
        editor: QsciScintilla = self.parent()
        text = editor.text()[start:end]
        token_list = self.getTokens(text)
        string_flag = False

        if start > 0:
            previous_style_nr = editor.SendScintilla(editor.SCI_GETSTYLEAT, start - 1)
            if previous_style_nr == self.DEFAULT:
                string_flag = False

        self.applyStyles(token_list, string_flag)

    def applyStyles(self, token_list, string_flag):
        def next_tok(skip: int = None):
            if token_list:
                if skip:
                    for _ in range(skip - 1):
                        if token_list:
                            token_list.pop(0)
                return token_list.pop(0)
            return None

        def peekTOK(n=0):
            try:
                return token_list[n]
            except IndexError:
                return ['']

        def skipSpacePeek(skip=None):
            i = skip if skip else 0
            tok = ' '
            while tok.isspace():
                tok = peekTOK(i)[0]
                i += 1
            return tok, i

        while True:
            curr_token = next_tok()
            if not curr_token:
                break
            tok, tok_len = curr_token

            if string_flag:
                self.setStyling(tok_len, self.KEYARGS)
                if tok in ('"', "'"):
                    string_flag = False
                continue

            if tok in self.KEYWORD_LIST:
                self.setStyling(tok_len, self.KEYWORD)
            elif tok in "({[]})":
                self.setStyling(tok_len, self.BRACKETS)
            elif tok in "+-*/\\%=<>":
                self.setStyling(tok_len, self.KEYARGS)
            elif tok == "%":
                self.setStyling(tok_len, self.COMMENTS)
            else:
                self.setStyling(tok_len, self.DEFAULT)
