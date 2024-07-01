from PyQt5.Qsci import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from LatexRenderer import LatexRenderer
from TexCustomLexer import TexCustomLexer

class Editor(QsciScintilla):
    def __init__(self, parent = None):
        super().__init__(parent)

        self.initEditorSettings()
        self.initAutoCompletion()
        self.initCaret()
        self.initEolSettings()
        self.initLexer()
        self.initMargin()

        self.renderer = LatexRenderer(self)

    def initMargin(self):
        self.setMarginType(0, QsciScintilla.NumberMargin)
        self.setMarginWidth(0, "0000")
        self.setMarginsForegroundColor(QColor("#fd77d7"))
        self.setMarginsBackgroundColor(QColor("#141221"))
        self.setMarginsFont(self.windowFont)

    def initLexer(self):
        self.texLexer = TexCustomLexer(self)
        self.texLexer.setDefaultFont(self.windowFont)

        self.api = QsciAPIs(self.texLexer)

        tex_commands = ['above', 'abovedisplayshortskip', 'abovedisplayskip', 'abovewithdelims', 'accent', 'adjdemerits', 'advance', '', 'afterassignment', 'aftergroup', 'atop', 'atopwithdelims', '', 'badness', 'baselineskip', 'batchmode', 'begingroup', '', 'belowdisplayshortskip', 'belowdisplayskip', 'binoppenalty', '', 'botmark', 'box', 'boxmaxdepth', 'brokenpenalty', 'catcode', 'char', '', 'chardef', 'cleaders', 'closein', 'closeout', 'clubpenalty', 'copy', '', 'count', 'countdef', 'cr', 'crcr', 'csname', 'day', 'deadcycles', 'def', '', 'defaulthyphenchar', 'defaultskewchar', 'delcode', 'delimiter', '', 'delimiterfactor', 'delimeters', 'delimitershortfall', '', 'delimeters', 'dimen', 'dimendef', 'discretionary', '', 'displayindent', 'displaylimits', 'displaystyle', '', 'displaywidowpenalty', 'displaywidth', 'divide', '', 'doublehyphendemerits', 'dp', 'dump', 'edef', 'else', '', 'emergencystretch', 'end', 'endcsname', 'endgroup', 'endinput', '', 'endlinechar', 'eqno', 'errhelp', 'errmessage', '', 'errorcontextlines', 'errorstopmode', 'escapechar', 'everycr', '', 'everydisplay', 'everyhbox', 'everyjob', 'everymath', 'everypar', '', 'everyvbox', 'exhyphenpenalty', 'expandafter', 'fam', 'fi', '', 'finalhyphendemerits', 'firstmark', 'floatingpenalty', 'font', '', 'fontdimen', 'fontname', 'futurelet', 'gdef', 'global', 'group', '', 'globaldefs', 'halign', 'hangafter', 'hangindent', 'hbadness', '', 'hbox', 'hfil', 'horizontal', 'hfill', 'horizontal', 'hfilneg', 'hfuzz', '', 'hoffset', 'holdinginserts', 'hrule', 'hsize', 'hskip', 'hss', '', 'horizontal', 'ht', 'hyphenation', 'hyphenchar', 'hyphenpenalty', '', 'hyphen', 'if', 'ifcase', 'ifcat', 'ifdim', 'ifeof', 'iffalse', 'ifhbox', '', 'ifhmode', 'ifinner', 'ifmmode', 'ifnum', 'ifodd', 'iftrue', 'ifvbox', '', 'ifvmode', 'ifvoid', 'ifx', 'ignorespaces', 'immediate', 'indent', '', 'input', 'inputlineno', 'input', 'insert', 'insertpenalties', '', 'interlinepenalty', 'jobname', 'kern', 'language', 'lastbox', '', 'lastkern', 'lastpenalty', 'lastskip', 'lccode', 'leaders', 'left', '', 'lefthyphenmin', 'leftskip', 'leqno', 'let', 'limits', 'linepenalty', '', 'line', 'lineskip', 'lineskiplimit', 'long', 'looseness', 'lower', '', 'lowercase', 'mag', 'mark', 'mathaccent', 'mathbin', 'mathchar', '', 'mathchardef', 'mathchoice', 'mathclose', 'mathcode', 'mathinner', '', 'mathop', 'mathopen', 'mathord', 'mathpunct', 'mathrel', '', 'mathsurround', 'maxdeadcycles', 'maxdepth', 'meaning', '', 'medmuskip', 'message', 'mkern', 'month', 'moveleft', 'moveright', '', 'mskip', 'multiply', 'muskip', 'muskipdef', 'newlinechar', 'noalign', '', 'noboundary', 'noexpand', 'noindent', 'nolimits', 'nonscript', '', 'scriptscript', 'nonstopmode', 'nulldelimiterspace', '', 'nullfont', 'number', 'omit', 'openin', 'openout', 'or', 'outer', 'output', '', 'outputpenalty', 'over', 'overfullrule', 'overline', '', 'overwithdelims', 'pagedepth', 'pagefilllstretch', '', 'pagefillstretch', 'pagefilstretch', 'pagegoal', 'pageshrink', '', 'pagestretch', 'pagetotal', 'par', 'parfillskip', 'parindent', '', 'parshape', 'parskip', 'patterns', 'pausing', 'penalty', '', 'postdisplaypenalty', 'predisplaypenalty', 'predisplaysize', '', 'pretolerance', 'prevdepth', 'prevgraf', 'radical', 'raise', 'read', '', 'relax', 'relpenalty', 'right', 'righthyphenmin', 'rightskip', '', 'romannumeral', 'scriptfont', 'scriptscriptfont', '', 'scriptscriptstyle', 'scriptspace', 'scriptstyle', '', 'scrollmode', 'setbox', 'setlanguage', 'sfcode', 'shipout', 'show', '', 'showbox', 'showboxbreadth', 'showboxdepth', 'showlists', '', 'showthe', 'skewchar', 'skip', 'skipdef', 'spacefactor', 'spaceskip', '', 'span', 'special', 'splitbotmark', 'splitfirstmark', '', 'splitmaxdepth', 'splittopskip', 'string', 'tabskip', 'textfont', '', 'textstyle', 'the', 'thickmuskip', 'thinmuskip', 'time', 'toks', '', 'toksdef', 'tolerance', 'topmark', 'topskip', 'tracingcommands', '', 'tracinglostchars', 'tracingmacros', 'tracingonline', '', 'tracingoutput', 'tracingpages', 'tracingparagraphs', '', 'tracingrestores', 'tracingstats', 'uccode', 'uchyph', '', 'underline', 'unhbox', 'unhcopy', 'unkern', 'unpenalty', 'unskip', '', 'unvbox', 'unvcopy', 'uppercase', 'vadjust', 'valign', 'vbadness', '', 'vbox', 'vcenter', 'vfil', 'vfill', 'vfilneg', 'vfuzz', 'voffset', 'vrule', '', 'vsize', 'vskip', 'vsplit', 'vss', 'vtop', 'wd', 'widowpenalty', 'write', '', 'xdef', 'xleaders', 'xspaceskip', 'year', '', 'TeX', 'bgroup', 'egroup', 'endgraf', 'space', 'empty', 'null', 'newcount', '', 'newdimen', 'newskip', 'newmuskip', 'newbox', 'newtoks', 'newhelp', '', 'newread', 'newwrite', 'newfam', 'newlanguage', 'newinsert', 'newif', '', 'maxdimen', 'magstephalf', 'magstep', 'frenchspacing', '', 'nonfrenchspacing', 'normalbaselines', 'obeylines', '', 'obeyspaces', 'raggedr', 'ight', 'ttraggedright', 'thinspace', '', 'negthinspace', 'enspace', 'enskip', 'quad', 'qquad', 'smallskip', '', 'medskip', 'bigskip', 'removelastskip', 'topglue', 'vglue', 'hglue', '', 'break', 'nobreak', 'allowbreak', 'filbreak', 'goodbreak', '', 'smallbreak', 'medbreak', 'bigbreak', 'line', 'leftline', '', 'rightline', 'centerline', 'rlap', 'llap', 'underbar', 'strutbox', '', 'strut', 'cases', 'matrix', 'pmatrix', 'bordermatrix', 'eqalign', '', 'displaylines', 'eqalignno', 'leqalignno', 'pageno', 'folio', '', 'tracingall', 'showhyphens', 'fmtname', 'fmtversion', 'hphantom', '', 'vphantom', 'phantom', 'smash']
        for command in tex_commands:
            self.api.add(command)

        self.api.prepare()
        self.setLexer(self.texLexer)

    def initAutoCompletion(self):
        self.setAutoCompletionSource(QsciScintilla.AcsAll)
        self.setAutoCompletionThreshold(1)
        self.setAutoCompletionCaseSensitivity(False)
        self.setAutoCompletionUseSingle(QsciScintilla.AcusNever)

    def initCaret(self):
        self.setCaretForegroundColor(QColor("#4fcdb9"))
        self.setCaretLineVisible(True)
        self.setCaretWidth(2)
        self.setCaretLineBackgroundColor(QColor("#2c313c"))

    def initEolSettings(self):
        self.setEolMode(QsciScintilla.EolWindows)
        self.setEolVisibility(False)

    def initEditorSettings(self):
        self.setUtf8(True)
        self.windowFont = QFont("Arial", 16)
        self.setFont(self.windowFont)
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)
        self.setIndentationGuides(True)
        self.setTabWidth(4)
        self.setIndentationsUseTabs(True)
        self.setAutoIndent(True)

    def toggleComment(self, text: str):
        lines = text.split('\n')
        toggledLines = []
        for line in lines:
            if line.startswith('%'):
                toggledLines.append(line[1:].lstrip())
            else:
                toggledLines.append('%' + line)
        
        return '\n'.join(toggledLines)
    
    def keyPressEvent(self, e: QKeyEvent) -> None:
        if e.modifiers() == Qt.ControlModifier and e.key == Qt.Key_Space:
            self.autoCompleteFromAPIs()
            return

        if e.modifiers() == Qt.ControlModifier and e.text() == "/":
            self.toggleCommentOnSelection()
            return

        return super().keyPressEvent(e) 

    def toggleCommentOnSelection(self):
        if self.hasSelectedText():
            start, startRow, end, endRow = self.getSelection()
            self.setSelection(start, 0, end, self.lineLength(end) - 1)
            self.replaceSelectedText(self.toggleComment(self.selectedText()))
            self.setSelection(start, startRow, end, endRow)
        else:
            line, _ = self.getCursorPosition()
            self.setSelection(line, 0, line, self.lineLength(line) - 1)
            self.replaceSelectedText(self.toggleComment(self.selectedText()))
            self.setSelection(-1, -1, -1, -1) 

    def renderPDFfile(self):
        self.renderer.renderDocument()
        